import snowflake.connector
import logging
import pandas as pd

from pathlib import PurePath

from cloe_util_snowflake_connector import connection_parameters

from icsDataValidation.core.database_objects import DatabaseObject
from icsDataValidation.utils.logger_util import configure_dev_ops_logger

#########################################################################################
#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger("Snowflake_Service")
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)


class SnowflakeService:
    def __init__(self, connection_params: connection_parameters.ConnectionParameters):
        self.connection_params = connection_params
        self.snowflake_connection = None
        self.snowflake_datatype_mapping = {
            "string": ["text"],
            "numeric": ["number", "float"],
            "date_and_time": ["date", "time", "timestamp_ntz", "timestamp_tz", "timestamp_ltz"],
            "binary": ["binary"],
            "boolean": ["boolean"],
        }

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.snowflake_connection is not None:
            self.snowflake_connection.close()

    def __del__(self):
        if self.snowflake_connection is not None:
            self.snowflake_connection.close()

    def _connect_to_snowflake(self):
        self.snowflake_connection = snowflake.connector.connect(**self.connection_params.model_dump(exclude_none=True))
        return self.snowflake_connection

    @staticmethod
    def _get_error_message(excepction: Exception, statement: str) -> None:
        """
        Compose error message if the execution of a statement or query fails.
        """
        if hasattr(excepction, "raw_msg"):
            message = excepction.raw_msg.replace("\n", " ")
        else:
            message = str(
                excepction
            )  # this makes sure that all kinds of errors can have a message, even if they do not have raw_msg attribute
        if hasattr(excepction, "sfqid"):
            message = message + f"\nQuery ID: {excepction.sfqid}"
        return f"Snowflake ERROR: {message}\nFailed statement:\n{statement}"

    @staticmethod
    def _get_in_clause(key_filters: list, numeric_columns: list, numeric_scale: int, enclose_column_by_double_quotes: bool = False) -> str:
        """generates in_clause from list ready to expand the where clause, numeric values are rounded

        Args:
            key_filters (list): list of given expected values
            numeric_columns (list): list of all numeric columns
            numeric_scale (int): number of decimal places after rounding

        Returns:
            str: in clause as string
        """
        values = list(key_filters.values())
        in_clause_values = "('"
        for j in range(len(values[0])):
            for value in values:
                in_clause_values += str(value[j]) + "','"
            in_clause_values = in_clause_values[:-2] + "),('"
        in_clause_values = in_clause_values[:-3] + ")"

        in_clause_cols = " AND (("
        for key in key_filters.keys():
            column_identifier = key.replace("'", "")
            if enclose_column_by_double_quotes:
                column_identifier = f'"{column_identifier}"'
            if key in numeric_columns:
                in_clause_cols += f"""ROUND({column_identifier}, {numeric_scale}),"""
            else:
                in_clause_cols += f"{column_identifier},"
        in_clause_cols = in_clause_cols[:-1] + ")"
        in_clause = in_clause_cols + " in (" + in_clause_values + ")"
        return in_clause

    def _get_column_clause(self, column_list: list, columns_datatype: list, numeric_scale, key_columns, enclose_column_by_double_quotes: bool = False) -> dict:
        """
        Turns list of desired columns into a sql compatible string.
        Columns with a date or time data type are omitted.

        Args:
            column_list (list): list of all columns
            columns_datatype (list): datatypes of given columns
            numeric_scale (_type_): number of decimal places for numeric columns
            key_columns (_type_):list of columns of interest

        Returns:
            dict: _description_
        """
        column_intersecions_new = []
        used_columns = []
        numeric_columns = []
        for column in column_list:

            column_datatype = next(x for x in columns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

            if enclose_column_by_double_quotes:
                column_identifier = f'"{column}"'
            else:
                column_identifier = column

            if column in key_columns or column_datatype.lower() not in self.snowflake_datatype_mapping["date_and_time"]:
                if column_datatype.lower() in self.snowflake_datatype_mapping["numeric"]:
                    if numeric_scale:
                        column_intersecions_new.append(
                            f'CAST(ROUND({column_identifier}, {numeric_scale}) as decimal(38,{numeric_scale})) as {column_identifier}'
                        )
                    else:
                        column_intersecions_new.append(f"{column_identifier} as {column_identifier}")
                    used_columns.append(column)
                    numeric_columns.append(column)
                elif column_datatype.lower() in self.snowflake_datatype_mapping["string"]:
                    column_intersecions_new.append(f"{column_identifier} AS {column_identifier}")
                    used_columns.append(column)
                else:
                    column_intersecions_new.append(column)
                    used_columns.append(column)

        column_intersections = column_intersecions_new.copy()
        column_clause = str(column_intersections)[1:-1].replace("'", "")
        return column_clause, numeric_columns, used_columns

    def get_database_objects(
        self, database: str, schema: str = None, object_type_restriction: str = "include_all"
    ) -> dict:
        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        all_database_tables = []
        all_database_views = []

        if object_type_restriction == "include_all" or object_type_restriction == "include_only_tables":
            if schema:
                query_db_tables = f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema.upper()}' AND TABLE_SCHEMA != 'INFORMATION_SCHEMA' AND TABLE_TYPE ='BASE TABLE'; "
            else:
                query_db_tables = f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA != 'INFORMATION_SCHEMA' AND TABLE_TYPE ='BASE TABLE';"

            all_database_tables = self.execute_queries(query_db_tables)

        if object_type_restriction == "include_all" or object_type_restriction == "include_only_views":
            if schema:
                query_db_views = f"SELECT * FROM {database}.INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA = '{schema.upper()}' AND TABLE_SCHEMA != 'INFORMATION_SCHEMA';"
            else:
                query_db_views = (
                    f"SELECT * FROM {database}.INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA != 'INFORMATION_SCHEMA';"
                )

            all_database_views = self.execute_queries(query_db_views)

        database_objects = []
        for row in all_database_tables:
            table_identifier = f"{row['TABLE_CATALOG']}.{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
            database_objects.append({"object_identifier": table_identifier, "object_type": "table"})
        for row in all_database_views:
            view_identifier = f"{row['TABLE_CATALOG']}.{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
            database_objects.append({"object_identifier": view_identifier, "object_type": "view"})
        return database_objects

    def get_last_altered_timestamp_from_object(self, object: DatabaseObject) -> str:
        """queries last_altered timestamp for given object

        Args:
            object (str): object for comparison

        Returns:
            str: last_altered timestamp
        """
        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        self.execute_statement("ALTER SESSION SET TIMEZONE = 'Europe/London';")

        query_get_last_altered = f"SELECT LAST_ALTERED FROM {object.database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{object.name}' AND TABLE_SCHEMA = '{object.schema}';"

        last_altered = self.execute_queries(query_get_last_altered)[0]

        return last_altered

    def get_columns_from_object(self, object: DatabaseObject) -> list:
        """returns all columns from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            list: list of all columns
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        if object.type == "table":
            query_show_columns = f"SHOW COLUMNS IN TABLE {object.database}.{object.schema}.{object.name};"

            show_columns_result, query_id, test = self.execute_queries(
                query_show_columns, return_as_pdf=False, return_query_ids=True
            )

            query_get_columns = f"SELECT $3 AS COLUMN_NAME FROM TABLE(result_scan('{query_id}'));"

        if object.type == "view":
            query_show_columns = f"SHOW COLUMNS IN VIEW {object.database}.{object.schema}.{object.name};"

            show_columns_result, query_id, test = self.execute_queries(
                query_show_columns, return_as_pdf=False, return_query_ids=True
            )

            query_get_columns = f"SELECT $3 AS COLUMN_NAME FROM TABLE(result_scan('{query_id}'));"

        all_columns = self.execute_queries(query_get_columns)
        columns = []

        for row in all_columns:
            columns.append(row["COLUMN_NAME"])

        return columns

    def get_row_count_from_object(self, object: DatabaseObject, where_clause: str = "") -> int:
        """gets row count from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: number of rows in object
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        # TODO is it more efficient to select the information_schema.table view to get the rows?
        query_get_row_count = (
            f"SELECT COUNT(*) AS ROW_COUNT FROM {object.database}.{object.schema}.{object.name} {where_clause};"
        )
        row_count = -1
        error_list = []

        try:
            row_count = self.execute_queries(query_get_row_count)[0]["ROW_COUNT"]

        except Exception as err:
            error_list.append(str(err))
            error_list.append(query_get_row_count)

        return row_count, error_list

    def get_data_types_from_object(self, object: DatabaseObject, column_intersections: list) -> dict:
        """returns datatypes for all intersection columns in a database object

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns for which the data type is queried

        Returns:
            dict: columns and their datatype
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        column_intersections = str(column_intersections)[1:-1]
        if column_intersections == "":
            column_intersections = "''"

        query_get_data_types_from_object = f"SELECT COLUMN_NAME , DATA_TYPE   \
                                            FROM {object.database.upper()}.INFORMATION_SCHEMA.COLUMNS  \
                                            WHERE TABLE_NAME='{object.name.upper()}'  \
                                            AND TABLE_SCHEMA = '{object.schema.upper()}'  \
                                            AND COLUMN_NAME IN ({column_intersections})  \
                                            ;"

        dict_colummns_datatype = self.execute_queries(query_get_data_types_from_object)
        return dict_colummns_datatype

    def get_count_distincts_from_object(
        self,
        object: DatabaseObject,
        column_intersections: list,
        where_clause: str = "",
        exclude_columns: list = [],
        enclose_column_by_double_quotes: bool = False
    ) -> dict:
        """get distinct count for every column in a database object that is in column intersections list

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns that are used for distinct count
            where_clause (str, optional): optional further filter. Defaults to "".
            exclude_columns (list, optional): columns to exclude from distinct count. Defaults to [].

        Returns:
            dict: distinct counts for columns
            error_list: list of failed executions for distinct counts
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        unions = ""

        for column in column_intersections:
            if enclose_column_by_double_quotes:
                column_identifier = f'"{column}"'
            else:
                column_identifier = column
            if column not in exclude_columns:
                unions += f" UNION SELECT '{column}' AS COLUMN_NAME, COUNT(DISTINCT {column_identifier}) AS COUNT_DISTINCT FROM {object.database}.{object.schema}.{object.name} {where_clause}"

        query_get_count_distincts_from_object = f"{unions[6:]} ORDER BY COUNT_DISTINCT;"
        error_list = []
        try:
            dict_count_distincts = self.execute_queries(query_get_count_distincts_from_object)

        except Exception as err:
            # raise err
            dict_count_distincts = []
            error_list.append(["ERROR", str(err).split("|||")[0], str(err).split("|||")[1]])

        return dict_count_distincts, error_list

    def get_table_size(self, object: DatabaseObject) -> int:
        """returns size of given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: size of object
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        query_get_table_size = f"SELECT BYTES FROM {object.database.upper()}.INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = '{object.database.upper()}' AND TABLE_SCHEMA = '{object.schema.upper()}' AND TABLE_NAME = '{object.name.upper()}' AND BYTES IS NOT NULL;"

        size = self.execute_queries(query_get_table_size)[0]["BYTES"]

        return size

    def create_checksums(
        self,
        object: DatabaseObject,
        column_intersections: list,
        where_clause: str = "",
        exclude_columns: list = [],
        numeric_scale: int = None,
        enclose_column_by_double_quotes: bool = False
    ) -> list[dict]:
        """creates checksums for given object in compliance with given conditions

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns that are used for checksums
            where_clause (str, optional): Optional filter criteria given as sql-usable string. Defaults to "".
            exclude_columns (list, optional): columns to exlude from calculation. Defaults to [].
            numeric_scale (int, optional): number of decimal places for aggregations. Defaults to None.

        Returns:
            List[Dict]: checksums for columns of object
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        column_intersections = [f"{x.upper()}" for x in column_intersections if x not in exclude_columns]

        logger.debug(f"Column Intersections: {column_intersections}")

        dict_colummns_datatype = self.get_data_types_from_object(object, column_intersections)

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            if enclose_column_by_double_quotes:
                column_identifier = f'"{column}"'
            else:
                column_identifier = column
            column_datatype = next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

            count_nulls += f', SUM(CASE WHEN {column_identifier} IS NULL THEN 1 ELSE 0 END) AS "COUNTNULLS_{column}"'

            if column_datatype.lower() in self.snowflake_datatype_mapping["numeric"]:
                if numeric_scale:
                    aggregates += (
                        f', CAST(ROUND(SUM({column_identifier}), {numeric_scale}) AS DECIMAL(38, {numeric_scale})) AS "SUM_{column}"'
                    )
                else:
                    aggregates += f', CAST(SUM({column_identifier}) AS DECIMAL(38)) AS "SUM_{column}"'

            elif (
                column_datatype.lower() in self.snowflake_datatype_mapping["string"]
                or column_datatype.lower() in self.snowflake_datatype_mapping["date_and_time"]
            ):
                aggregates += f', COUNT(DISTINCT LOWER({column_identifier})) AS "COUNTDISTINCT_{column}"'

            elif column_datatype.lower() in self.snowflake_datatype_mapping["binary"]:
                aggregates += f', COUNT(DISTINCT LOWER(TRY_TO_NUMBER({column_identifier}::VARCHAR))) AS "COUNTDISTINCT_{column}"'

            elif column_datatype.lower() in self.snowflake_datatype_mapping["boolean"]:
                aggregates += f", MAX(SELECT COUNT(*) FROM {object.database}.{object.schema}.{object.name} WHERE {column_identifier} = true)::VARCHAR || '_' || MAX(SELECT COUNT(*) FROM {object.database}.{object.schema}.{object.name} WHERE {column_identifier} = false) :: VARCHAR AS \"AGGREGATEBOOLEAN_{column}\""


            # else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

        query_checksums = (
            f"SELECT {aggregates[1:]} FROM {object.database}.{object.schema}.{object.name} {where_clause};"
        )

        query_countnulls = (
            f"SELECT {count_nulls[1:]} FROM {object.database}.{object.schema}.{object.name} {where_clause};"
        )

        error_list = []
        test_list = []
        aggregation_results = {}

        try:
            checksums_results = self.execute_queries([query_checksums, query_countnulls])

            aggregation_results = checksums_results[0][0]

            countnulls_results = checksums_results[1][0]

            for i in range(0, len(aggregation_results)):
                if list(aggregation_results.values())[i] is None:
                    agg_result = 0
                else:
                    agg_result = list(aggregation_results.values())[i]

                if list(countnulls_results.values())[i] is None:
                    cnt_result = 0
                else:
                    cnt_result = list(countnulls_results.values())[i]

                test_list.append(
                    [[item.split("_", 1)[0] for item in list(aggregation_results.keys())][i], agg_result, cnt_result]
                )

        except Exception as err:
            error_list.append(["ERROR", str(err).split("|||")[0], str(err).split("|||")[1]])

        checksums = dict(zip([item.split("_", 1)[1] for item in aggregation_results.keys()], test_list))
        checksums["TESTATM_ERRORS"] = error_list

        return checksums

    def create_pandas_df_from_group_by(
        self,
        object: DatabaseObject,
        column_intersections: list,
        group_by_columns: list,
        group_by_aggregation_columns: list,
        group_by_aggregation_type: str,
        only_numeric: bool,
        where_clause: str,
        exclude_columns: list,
        numeric_scale: int = None,
        enclose_column_by_double_quotes: bool = False
    ) -> list[dict]:
        """execution of multiple aggregations at once

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns existing in src and trgt
            group_by_columns (list): columns for grouping the aggregations
            group_by_aggregation_columns (list): list of columns that are supposed to be aggregated
            group_by_aggregation_type (str): choice between:  only_min_max, various, various_and_min_max
            only_numeric (bool): whether to also include distinct counts or only do numeric aggregations
            where_clause (str): optional filter for aggregations, given as sql compatible where-string
            exclude_columns (list): columns to exclude from comparisons
            numeric_scale (int, optional): number of decimal places for aggregations. Defaults to None.

        Returns:
            List[Dict]: list of pandas dataframes with results from aggregations, used sql queries
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        if group_by_aggregation_columns == ["all"]:
            aggregation_columns = [
                f"{column.upper()}"
                for column in column_intersections
                if (column not in group_by_columns and column not in exclude_columns)
            ]
        else:
            aggregation_columns = [
                f"{column.upper()}"
                for column in column_intersections
                if (column in group_by_aggregation_columns and column not in exclude_columns)
            ]

        group_by_query_columns_string = " "
        grouping_columns_final = []
        error_dict = {}

        try:
            for column in group_by_columns:
                if enclose_column_by_double_quotes:
                    column_identifier = f'"{column}"'
                else:
                    column_identifier = column
                if column in column_intersections and column not in exclude_columns:
                    group_by_query_columns_string += f"{column_identifier} ,"
                    grouping_columns_final.append(column)

            group_by_query_columns_string = group_by_query_columns_string[:-1]

            dict_colummns_datatype = self.get_data_types_from_object(object, aggregation_columns)

            aggregates = ""
            aggregates_min = ""

            for column in aggregation_columns:
                if enclose_column_by_double_quotes:
                    column_identifier = f'"{column}"'
                else:
                    column_identifier = column
                column_datatype = next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

                if column_datatype.lower() in self.snowflake_datatype_mapping["numeric"]:
                    if numeric_scale:
                        aggregates_min += f', CAST(ROUND(MIN({column_identifier}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS "MIN_{column}", CAST(ROUND(max({column_identifier}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS "MAX_{column}"'
                        aggregates += f', CAST(ROUND(SUM({column_identifier}), {numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS "SUM_{column}"'
                    else:
                        aggregates_min += f', MIN({column_identifier}) AS "MIN_{column}", MAX({column_identifier}) AS "MAX_{column}"'
                        aggregates += f', SUM({column_identifier}) AS "SUM_{column}"'

                elif not only_numeric and (
                    column_datatype.lower() in self.snowflake_datatype_mapping["string"]
                    or column_datatype.lower() in self.snowflake_datatype_mapping["date_and_time"]
                ):
                    aggregates += f', COUNT(DISTINCT LOWER({column_identifier})) AS "COUNTDISTINCT_{column}"'

                elif not only_numeric and column_datatype.lower() in self.snowflake_datatype_mapping["binary"]:
                    aggregates += f', COUNT(DISTINCT LOWER(TRY_TO_NUMBER({column_identifier}::VARCHAR))) AS "COUNTDISTINCT_{column}"'

                elif not only_numeric and column_datatype.lower() in self.snowflake_datatype_mapping["boolean"]:
                    aggregates += f", COUNT(CASE WHEN {column_identifier} = true THEN 1 ELSE NULL END)::VARCHAR || '_' || COUNT(CASE WHEN {column_identifier} = false THEN 1 ELSE NULL END)::VARCHAR AS \"AGGREGATEBOOLEAN_{column}\""

                # else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

            # CASE 1: min_max
            if group_by_aggregation_type == "only_min_max":
                group_by_query_aggregation_string = aggregates_min[1:]

            # CASE 2: sum, count_distinct, aggregate_boolean
            elif group_by_aggregation_type == "various":
                group_by_query_aggregation_string = aggregates[1:]

            # CASE 3: sum, count_distinct, aggregate_boolean, min_max
            elif group_by_aggregation_type == "various_and_min_max":
                group_by_query_aggregation_string = f"{aggregates_min[1:]}{aggregates}"

            query_group_by_aggregation = f"SELECT {group_by_query_columns_string}, COUNT(*) AS COUNT_OF_GROUP_BY_VALUE, {group_by_query_aggregation_string} FROM {object.database}.{object.schema}.{object.name} {where_clause} GROUP BY {group_by_query_columns_string} ORDER BY {group_by_query_columns_string};"

            group_by_aggregation_pdf = self.execute_queries(query_group_by_aggregation, True)
        except Exception as err:
            group_by_aggregation_pdf = pd.DataFrame()
            group_by_aggregation_pdf["TESTATM_ERROR"] = [1]
            if not grouping_columns_final:
                error_dict = {
                    "QUERY": "NO Group-BY Columns found in the Columns Intersection. Please check if the configurated Group-By Columns exist in the Table",
                    "ERROR": "NO Group-BY Columns found in the Columns Intersection. Please check if the configurated Group-By Columns exist in the Table",
                }
                group_by_query_aggregation_string = ""
            elif "|||" in str(err):
                error_dict = {"QUERY": str(err).split("|||")[0], "ERROR": str(err).split("|||")[1]}
            else:
                error_dict = {
                    "QUERY": "NO Query generated. Please check if the configurated Grouping Columns exist in the Table",
                    "ERROR": str(err),
                }
                group_by_query_aggregation_string = ""

        return (
            group_by_aggregation_pdf,
            group_by_query_aggregation_string,
            group_by_query_columns_string,
            grouping_columns_final,
            error_dict,
        )

    def create_pandas_df(
        self,
        object: DatabaseObject,
        intersection_columns_trgt_src: list,
        where_clause: str = "",
        exclude_columns: list = [],
        enclose_column_by_double_quotes: bool = False
    ) -> pd.DataFrame:
        """creates pandas dataframes with all data from given object in given columns

        Args:
            object (DatabaseObject): table or view
            intersection_columns_trgt_src (list): columns existing in source and target

        Returns:
            pd.DataFrame: direct result of sql query
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()
        if enclose_column_by_double_quotes:
            intersection_columns_trgt_src_ = '", "'.join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))
            intersection_columns_trgt_src_ = f'"{intersection_columns_trgt_src_}"'
        else:
            intersection_columns_trgt_src_ = ", ".join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"SELECT {intersection_columns_trgt_src_} FROM {object.database}.{object.schema}.{object.name} {where_clause};"

        pdf = self.execute_queries(df_query, True)

        return pdf

    def create_pandas_df_from_sample(
        self,
        object: DatabaseObject,
        column_intersections: list,
        key_columns: list,
        where_clause: str = "",
        exclude_columns: list = [],
        key_filters: dict = {},
        dedicated_columns: list = [],
        sample_count: int = 10,
        numeric_scale: int = None,
        enclose_column_by_double_quotes: bool = False
    ) -> list[dict]:
        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        sample_count = str(sample_count)
        key_intersection = list((set(column_intersections) & set(key_columns)) - set(exclude_columns))
        filter_intersection = list((set(column_intersections) & set(key_filters.keys())) - set(exclude_columns))
        dedicated_intersection = list((set(column_intersections) & set(dedicated_columns)) - set(exclude_columns))

        key_intersection.sort()
        filter_intersection.sort()
        dedicated_intersection.sort()

        if not where_clause:
            where_clause = "WHERE 1=1 "

        if dedicated_intersection != []:
            is_dedicated = True

            dict_colummns_datatype = self.get_data_types_from_object(object, dedicated_intersection)

        else:
            is_dedicated = False

            dict_colummns_datatype = self.get_data_types_from_object(object, column_intersections)

        if key_intersection != [] and is_dedicated:
            if enclose_column_by_double_quotes:
                keys = str(key_intersection)[1:-1].replace("'", "\"")
            else:
                keys = str(key_intersection)[1:-1].replace("'", "")

            column_clause, numeric_columns, used_columns = self._get_column_clause(
                dedicated_intersection, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes
            )
            if (key_filters != {}) & (filter_intersection != []):
                values = list(key_filters.values())
                if values[0] != []:
                    in_clause = self._get_in_clause(key_filters, numeric_columns, numeric_scale, enclose_column_by_double_quotes)
                else:
                    in_clause = ""
            else:
                in_clause = ""
            sample_query = f"SELECT {column_clause} FROM {object.database}.{object.schema}.{object.name} SAMPLE ({sample_count} ROWS) {where_clause}{in_clause} ORDER BY {keys};"
        elif key_intersection != [] and not is_dedicated:
            if enclose_column_by_double_quotes:
                keys = str(key_intersection)[1:-1].replace("'", "\"")
            else:
                keys = str(key_intersection)[1:-1].replace("'", "")
            column_clause, numeric_columns, used_columns = self._get_column_clause(
                column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes
            )
            if (key_filters != {}) & (filter_intersection != []):
                values = list(key_filters.values())
                if values[0] != []:
                    in_clause = self._get_in_clause(key_filters, numeric_columns, numeric_scale, enclose_column_by_double_quotes)
                else:
                    in_clause = ""
            else:
                in_clause = ""
            sample_query = f"SELECT {column_clause} FROM {object.database}.{object.schema}.{object.name} SAMPLE ({sample_count} ROWS) {where_clause}{in_clause} ORDER BY {keys};"
        else:
            column_intersections = list(set(column_intersections) - set(exclude_columns))
            column_intersections.sort()
            column_clause, numeric_columns, used_columns = self._get_column_clause(
                column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes
            )
            sample_query = f"SELECT {column_clause} FROM {object.database}.{object.schema}.{object.name} SAMPLE ({sample_count} ROWS) {where_clause};"

        error_dict = {}
        key_dict = {}
        try:
            sample_pdf = self.execute_queries(sample_query, return_as_pdf=True)
            for key in key_intersection:
                if pd.api.types.is_datetime64_any_dtype(sample_pdf[key]):
                    key_dict[key] = list(sample_pdf[key].astype(str))
                else:
                    key_dict[key] = list(sample_pdf[key])

        except Exception as err:
            sample_pdf = pd.DataFrame()
            sample_pdf["TESTATM_ERROR"] = [1]
            if "|||" in str(err):
                error_dict = {"QUERY": str(err).split("|||")[0], "ERROR": str(err).split("|||")[1]}
            else:
                error_dict = {"QUERY": "No SQL Error", "ERROR": str(err)}

        return_list = []
        return_list.append(sample_pdf)
        return_list.append(error_dict)

        return return_list, key_dict, used_columns, sample_query

    def execute_queries(
        self, query: str | list[str], return_as_pdf: bool = False, return_query_ids: bool = False
    ) -> list[dict] | list[list[dict]]:
        """actual execution of defined queries

        Args:
            query (Union[str, List[str]]): queries to be executed
            return_as_pdf (bool, optional): If true, queries returned as pandas data frames. Defaults to False.
            return_query_ids (bool, optional): If true, results and queri ids are returned, otherwise only results. Defaults to False.

        Raises:
            Exception: Raises exception if single query cannot be executed.

        Returns:
            Union[List[Dict], List[List[Dict]]]: returns results or results with query-ids
        """

        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        if query:
            query_list: list[str] = query if isinstance(query, list) else [query]
        else:
            logger.error("Query defined as null - please check input for execute_queries function.")

        cursor = self.snowflake_connection.cursor(snowflake.connector.DictCursor)

        results = []
        query_ids = []

        for single_query in query_list:
            try:
                query_result = cursor.execute(single_query).fetchall()
                if return_as_pdf:
                    query_result = pd.DataFrame(query_result)

                results.append(query_result)
                query_ids.append(cursor.sfqid)

            except Exception as err:
                raise Exception(single_query + "|||" + str(err))

        if return_query_ids:
            return results[0], query_ids[0] if not isinstance(query, list) else results, query_ids

        else:
            return results[0] if not isinstance(query, list) else results

    def execute_statement(self, statement: str | list[str]) -> None:
        """
            Executes simple statement against snowflake
            Schema and Database settings must be set beforehand
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        if self.snowflake_connection is None:
            self._connect_to_snowflake()

        statement_list: list[str] = statement if isinstance(statement, list) else [statement]

        try:
            for single_statement in statement_list:
                stripped_statement = single_statement.strip()
                _ = self.snowflake_connection.execute_string(stripped_statement)

        except Exception as err:
            raise Exception(self._get_error_message(err, single_statement)) from err

    def upload_to_stage(self, stage_name: str, folder_path: str, file_name: str, is_temporary: bool):
        file_path = PurePath(folder_path).joinpath(PurePath(file_name))

        if is_temporary:
            create_query = f"CREATE TEMPORARY STAGE IF NOT EXISTS {stage_name};"
        else:
            create_query = f"CREATE STAGE IF NOT EXISTS {stage_name};"

        put_query = rf"PUT 'file://{file_path}' @{stage_name};"

        put_query = put_query.replace("\\", "\\\\")

        self.execute_statement(create_query)

        self.execute_statement(put_query)

    def insert_json_results(
        self,
        run_guid: str,
        pipeline_name: str,
        pipeline_id: str,
        start_time_utc: str,
        result_table: str,
        stage_name: str,
    ) -> None:
        """
        copy into - result table for json results
        """
        result_database = result_table.split(".")[0]
        meta_data_schema = result_table.split(".")[1]

        statement = f"COPY INTO {result_table} (RUN_GUID, PIPELINE_NAME, PIPELINE_ID, START_TIME_UTC, RESULT, CREATION_TIME_UTC) FROM (SELECT '{run_guid}', '{pipeline_name}', '{pipeline_id}', '{start_time_utc}', $1, SYSDATE() from @{stage_name} (file_format => {result_database}.{meta_data_schema}.ff_json ));"

        self.execute_statement(statement)

    def insert_json_results_live(
        self,
        run_guid: str,
        pipeline_name: str,
        pipeline_id: str,
        result_table: str,
        stage_name: str,
        source_system: str,
        target_system: str,
        database: str,
        schema: str,
        object: str,
    ) -> None:
        """
        copy into - result table for json results live
        """
        result_database = result_table.split(".")[0]
        meta_data_schema = result_table.split(".")[1]

        statement = f"COPY INTO {result_table} (RUN_GUID, PIPELINE_NAME, PIPELINE_ID, SOURCE_SYSTEM, TARGET_SYSTEM, DATABASE_NAME, SCHEMA_NAME, OBJECT_NAME  ,RESULT, CREATION_TS) FROM (SELECT '{run_guid}', '{pipeline_name}', '{pipeline_id}', '{source_system}', '{target_system}', '{database}', '{schema}', '{object}', $1, SYSDATE() from @{stage_name} (file_format => {result_database}.{meta_data_schema}.ff_json ));"

        self.execute_statement(statement)

    def insert_highlevel_results(
        self, results: dict, run_guid: str, pipeline_name: str, pipeline_id: str, result_table_highlevel: str
    ) -> None:
        """
        insert into - highlevel results per "pipeline run" / "ics data validation execution"
        """
        TESTSET_ = ", ".join(results["TESTSET"])

        OBJECTS_TO_COMPARE_SRC_ = ", ".join(results["OBJECTS_TO_COMPARE_SRC"])

        OBJECTS_TO_COMPARE_TRGT_ = ", ".join(results["OBJECTS_TO_COMPARE_TRGT"])

        SRC_MINUS_TRGT_ = ", ".join(results["SRC_MINUS_TRGT"])

        TRGT_MINUS_SRC_ = ", ".join(results["TRGT_MINUS_SRC"])

        insert_statement = f"INSERT INTO {result_table_highlevel} ( \
                                                                        RUN_GUID, \
                                                                        PIPELINE_NAME,  \
                                                                        PIPELINE_ID,  \
                                                                        START_TIME_UTC,  \
                                                                        SOURCE_SYSTEM,  \
                                                                        TARGET_SYSTEM,  \
                                                                        DATABASE_NAME,  \
                                                                        TESTSET,  \
                                                                        ALL_OBJECTS_MATCHING,  \
                                                                        ALL_COLUMNS_EQUAL,  \
                                                                        ALL_DATATYPES_EQUAL,  \
                                                                        ALL_ROWCOUNTS_EQUAL,  \
                                                                        ALL_CHECKSUMS_EQUAL,  \
                                                                        ALL_SAMPLES_EQUAL,  \
                                                                        ALL_OBJECTS_EQUAL,  \
                                                                        OBJECTS_TO_COMPARE_SRC,  \
                                                                        OBJECTS_TO_COMPARE_TRGT,  \
                                                                        NUMBER_OF_OBJECTS_TO_COMPARE,  \
                                                                        SRC_MINUS_TRGT,  \
                                                                        TRGT_MINUS_SRC, \
                                                                        CREATION_TS) \
                                                                        VALUES  \
                                                                        ('{run_guid}', \
                                                                        '{pipeline_name}', \
                                                                        '{pipeline_id}', \
                                                                        '{results['START_TIME_UTC']}',  \
                                                                        '{results['SOURCE_SYSTEM']}',  \
                                                                        '{results['TARGET_SYSTEM']}', \
                                                                        '{results['DATABASE_NAME']}',  \
                                                                        '{TESTSET_}',  \
                                                                        '{results['ALL_OBJECTS_MATCHING']}',  \
                                                                        '{results['ALL_COLUMNS_EQUAL']}',  \
                                                                        '{results['ALL_DATATYPES_EQUAL']}',  \
                                                                        '{results['ALL_ROWCOUNTS_EQUAL']}',  \
                                                                        '{results['ALL_CHECKSUMS_EQUAL']}',  \
                                                                        NULLIF('{results['ALL_SAMPLES_EQUAL']}', 'None'),  \
                                                                        NULLIF('{results['ALL_OBJECTS_EQUAL']}', 'None'),  \
                                                                        '{OBJECTS_TO_COMPARE_SRC_}',  \
                                                                        '{OBJECTS_TO_COMPARE_TRGT_}',  \
                                                                        '{results['NUMBER_OF_OBJECTS_TO_COMPARE']}',  \
                                                                        '{SRC_MINUS_TRGT_}',  \
                                                                        '{TRGT_MINUS_SRC_}', \
                                                                        SYSDATE())"

        self.execute_statement(insert_statement)

    def insert_objectlevel_results(self, result_table: dict, result_table_objectlevel: str, run_guid: str) -> None:
        """
        insert into - detailed results per object
        """
        insert_statement = f"INSERT INTO {result_table_objectlevel} ( \
                                                                        RUN_GUID, \
                                                                        PIPELINE_ID, \
                                                                        START_TIME_UTC,\
                                                                        SRC_DATABASE_NAME, \
                                                                        SRC_SCHEMA_NAME, \
                                                                        SRC_OBJECT_NAME, \
                                                                        SRC_OBJECT_TYPE, \
                                                                        TRGT_DATABASE_NAME, \
                                                                        TRGT_SCHEMA_NAME, \
                                                                        TRGT_OBJECT_NAME, \
                                                                        TRGT_OBJECT_TYPE, \
                                                                        SRC_FILTER, \
                                                                        TRGT_FILTER, \
                                                                        EXCLUDED_COLUMNS, \
                                                                        COLUMNS_EQUAL, \
                                                                        COLUMN_INTERSECTION, \
                                                                        SRC_COLUMNS_MINUS_TRGT_COLUMNS, \
                                                                        TRGT_COLUMNS_MINUS_SRC_COLUMNS, \
                                                                        DATATYPES_EQUAL, \
                                                                        ROW_COUNTS_EQUAL, \
                                                                        SRC_ROW_COUNT, \
                                                                        TRGT_ROW_COUNT, \
                                                                        ALL_COUNT_NULLS_EQUAL, \
                                                                        AGGREGATIONS_EQUAL, \
                                                                        AGGREGATIONS_EQUAL_TOLERATED,\
                                                                        SRC_ERROR_QUERY, \
                                                                        TRGT_ERROR_QUERY, \
                                                                        SRC_ERROR_MSG, \
                                                                        TRGT_ERROR_MSG, \
                                                                        GROUP_BY_COLUMNS, \
                                                                        GROUP_BY_EQUAL, \
                                                                        GROUP_BY_VALUES_WITH_MISMATCHES, \
                                                                        COLUMNS_WITH_MISMATCH, \
                                                                        GROUP_BY_DIFF_DICT, \
                                                                        SRC_GROUP_BY_QUERY, \
                                                                        TRGT_GROUP_BY_QUERY, \
                                                                        SRC_GROUP_BY_ERROR, \
                                                                        TRGT_GROUP_BY_ERROR, \
                                                                        SAMPLES_COMPARED, \
                                                                        SAMPLES_EQUAL, \
                                                                        SAMPLE_KEYS, \
                                                                        SRC_SAMPLE, \
                                                                        TRGT_SAMPLE, \
                                                                        SRC_SAMPLE_QUERY, \
                                                                        TRGT_SAMPLE_QUERY, \
                                                                        SRC_SAMPLE_ERROR_MSG, \
                                                                        TRGT_SAMPLE_ERROR_MSG, \
                                                                        PANDAS_DATAFRAME_COMPARED, \
                                                                        PANDAS_DATAFRAME_EQUAL, \
                                                                        SRC_NOT_ALTERED_DURING_COMPARISON, \
                                                                        TRGT_NOT_ALTERED_DURING_COMPARISON, \
                                                                        SRC_LAST_ALTERED, \
                                                                        TRGT_LAST_ALTERED, \
                                                                        CREATION_TS) \
                                            SELECT\
                                                RESULTS.RUN_GUID AS RUN_GUID, \
                                                RESULTS.PIPELINE_ID AS PIPELINE_ID, \
                                                RESULTS.START_TIME_UTC::VARCHAR AS START_TIME_UTC, \
                                                F1.VALUE:SRC_DATABASE_NAME::VARCHAR AS SRC_DATABASE_NAME, \
                                                F1.VALUE:SRC_SCHEMA_NAME::VARCHAR AS SRC_SCHEMA_NAME, \
                                                F1.VALUE:SRC_OBJECT_NAME::VARCHAR AS SRC_OBJECT_NAME, \
                                                F1.VALUE:SRC_OBJECT_TYPE::VARCHAR AS SRC_OBJECT_TYPE, \
                                                F1.VALUE:TRGT_DATABASE_NAME::VARCHAR AS TRGT_DATABASE_NAME, \
                                                F1.VALUE:TRGT_SCHEMA_NAME::VARCHAR AS TRGT_SCHEMA_NAME, \
                                                F1.VALUE:TRGT_OBJECT_NAME::VARCHAR AS TRGT_OBJECT_NAME, \
                                                F1.VALUE:TRGT_OBJECT_TYPE::VARCHAR AS TRGT_OBJECT_TYPE, \
                                                F1.VALUE:SRC_FILTER::VARCHAR AS SRC_FILTER, \
                                                F1.VALUE:TRGT_FILTER::VARCHAR AS TRGT_FILTER, \
                                                F1.VALUE:EXCLUDED_COLUMNS AS EXCLUDED_COLUMNS, \
                                                F1.VALUE:COLUMNS_EQUAL::BOOLEAN AS COLUMNS_EQUAL, \
                                                F1.VALUE:COLUMN_INTERSECTION AS COLUMN_INTERSECTION, \
                                                F1.VALUE:SRC_COLUMNS_MINUS_TRGT_COLUMNS AS SRC_COLUMNS_MINUS_TRGT_COLUMNS, \
                                                F1.VALUE:TRGT_COLUMNS_MINUS_SRC_COLUMNS AS TRGT_COLUMNS_MINUS_SRC_COLUMNS, \
                                                F1.VALUE:DATATYPES_EQUAL::BOOLEAN AS DATATYPES_EQUAL, \
                                                F1.VALUE:ROW_COUNTS_EQUAL::BOOLEAN AS ROW_COUNTS_EQUAL, \
                                                F1.VALUE:SRC_ROW_COUNT::INT AS SRC_ROW_COUNT, \
                                                F1.VALUE:TRGT_ROW_COUNT::INT AS TRGT_ROW_COUNT, \
                                                F1.VALUE:ALL_COUNT_NULLS_EQUAL::BOOLEAN AS ALL_COUNT_NULLS_EQUAL, \
                                                F1.VALUE:AGGREGATIONS_EQUAL::BOOLEAN AS AGGREGATIONS_EQUAL, \
                                                F1.VALUE:AGGREGATIONS_EQUAL_TOLERATED::BOOLEAN AS AGGREGATIONS_EQUAL_TOLERATED,\
                                                F1.VALUE:SRC_ERROR:QUERY::VARCHAR AS SRC_ERROR_QUERY, \
                                                F1.VALUE:TRGT_ERROR:QUERY::VARCHAR AS TRGT_ERROR_QUERY, \
                                                F1.VALUE:SRC_ERROR:ERROR::VARCHAR AS SRC_ERROR_MSG, \
                                                F1.VALUE:TRGT_ERROR:ERROR::VARCHAR AS TRGT_ERROR_MSG, \
                                                F1.VALUE:GROUP_BY_COLUMNS AS GROUP_BY_COLUMNS, \
                                                F1.VALUE:GROUP_BY_EQUAL::BOOLEAN AS GROUP_BY_EQUAL, \
                                                F1.VALUE:GROUP_BY_VALUES_WITH_MISMATCHES AS GROUP_BY_VALUES_WITH_MISMATCHES, \
                                                F1.VALUE:COLUMNS_WITH_MISMATCH AS COLUMNS_WITH_MISMATCH, \
                                                F1.VALUE:GROUP_BY_DIFF_DICT AS GROUP_BY_DIFF_DICT, \
                                                CASE WHEN F1.VALUE:SRC_GROUP_BY_ERROR::VARCHAR = '{{}}'  \
                                                            THEN NULLIF(F1.VALUE:SRC_GROUP_BY_QUERY::VARCHAR, '')  \
                                                    WHEN F1.VALUE:SRC_GROUP_BY_ERROR::VARCHAR != '{{}}' \
                                                        THEN NULLIF(F1.VALUE:SRC_GROUP_BY_ERROR:QUERY::VARCHAR, '') \
                                                    END		AS SRC_GROUP_BY_QUERY, \
                                                CASE WHEN F1.VALUE:TRGT_GROUP_BY_ERROR::VARCHAR = '{{}}'  \
                                                            THEN NULLIF(F1.VALUE:TRGT_GROUP_BY_QUERY::VARCHAR, '')  \
                                                    WHEN F1.VALUE:TRGT_GROUP_BY_ERROR::VARCHAR != '{{}}' \
                                                        THEN NULLIF(F1.VALUE:TRGT_GROUP_BY_ERROR:QUERY::VARCHAR, '') \
                                                    END		AS TRGT_GROUP_BY_QUERY, \
                                                CASE WHEN F1.VALUE:SRC_GROUP_BY_ERROR::VARCHAR = '{{}}' \
                                                    THEN NULL  \
                                                    ELSE F1.VALUE:SRC_GROUP_BY_ERROR::VARCHAR \
                                                    END AS SRC_GROUP_BY_ERROR, \
                                                CASE WHEN F1.VALUE:TRGT_GROUP_BY_ERROR::VARCHAR = '{{}}' \
                                                    THEN NULL  \
                                                    ELSE F1.VALUE:TRGT_GROUP_BY_ERROR::VARCHAR \
                                                    END AS TRGT_GROUP_BY_ERROR, \
                                                F1.VALUE:SAMPLES_COMPARED::BOOLEAN AS SAMPLES_COMPARED, \
                                                F1.VALUE:SAMPLES_EQUAL::BOOLEAN AS SAMPLES_EQUAL, \
                                                F1.VALUE:SAMPLE_KEYS AS SAMPLE_KEYS, \
                                                F1.VALUE:SRC_SAMPLE AS SRC_SAMPLE, \
                                                F1.VALUE:TRGT_SAMPLE AS TRGT_SAMPLE, \
                                                F1.VALUE:SRC_SAMPLE_QUERY AS SRC_SAMPLE_QUERY, \
                                                F1.VALUE:TRGT_SAMPLE_QUERY AS TRGT_SAMPLE_QUERY, \
                                                F1.VALUE:SRC_SAMPLE_ERROR_DICT:ERROR::VARCHAR AS SRC_SAMPLE_ERROR_MSG, \
                                                F1.VALUE:TRGT_SAMPLE_ERROR_DICT:ERROR::VARCHAR AS TRGT_SAMPLE_ERROR_MSG, \
                                                F1.VALUE:PANDAS_DATAFRAME_COMPARED::BOOLEAN AS PANDAS_DATAFRAME_COMPARED, \
                                                F1.VALUE:PANDAS_DATAFRAME_EQUAL::BOOLEAN AS PANDAS_DATAFRAME_EQUAL, \
                                                F1.VALUE:SRC_NOT_ALTERED_DURING_COMPARISON::BOOLEAN AS SRC_NOT_ALTERED_DURING_COMPARISON, \
                                                F1.VALUE:TRGT_NOT_ALTERED_DURING_COMPARISON::BOOLEAN AS TRGT_NOT_ALTERED_DURING_COMPARISON, \
                                                F1.VALUE:SRC_LAST_ALTERE::VARCHAR AS SRC_LAST_ALTERED, \
                                                F1.VALUE:TRGT_LAST_ALTERED::VARCHAR AS TRGT_LAST_ALTERED, \
                                                SYSDATE() \
                                            FROM {result_table} RESULTS \
                                            CROSS JOIN LATERAL FLATTEN(INPUT => RESULT:OBJECTS) F1\
                                            WHERE RUN_GUID = '{run_guid}'\
                                ;"

        self.execute_statement(insert_statement)

    def insert_columnlevel_results(self, result_table: str, result_table_columnlevel: str, run_guid: str) -> None:
        """
        insert into - detailed results per column
        """
        insert_statement = f"INSERT INTO {result_table_columnlevel} ( \
                                                                RUN_GUID,\
                                                                PIPELINE_ID,\
                                                                START_TIME_UTC,\
                                                                SRC_DATABASE_NAME, \
                                                                SRC_SCHEMA_NAME, \
                                                                SRC_OBJECT_NAME, \
                                                                SRC_OBJECT_TYPE, \
                                                                TRGT_DATABASE_NAME, \
                                                                TRGT_SCHEMA_NAME, \
                                                                TRGT_OBJECT_NAME, \
                                                                TRGT_OBJECT_TYPE, \
                                                                COLUMN_NAME,\
                                                                IN_SRC,\
                                                                IN_TRGT,\
                                                                IN_SYNC,\
                                                                IN_EXCLUDED,\
                                                                SRC_DATATYPE,\
                                                                TRGT_DATATYPE,\
                                                                DATATYPE_EQUAL,\
                                                                AGGREGATION_TYPE,\
                                                                AGGREGATION_EQUAL,\
                                                                AGGREGATION_RESULT_SRC,\
                                                                AGGREGATION_RESULT_TRGT,\
                                                                AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC,\
                                                                AGGREGATION_EQUAL_TOLERATED,\
                                                                COUNT_NULLS_EQUAL,\
                                                                COUNT_NULLS_SRC,\
                                                                COUNT_NULLS_TRGT,\
                                                                COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC,\
                                                                ERROR_QUERY_SRC ,\
                                                                ERROR_MSG_SRC ,\
                                                                ERROR_QUERY_TRGT ,\
                                                                ERROR_MSG_TRGT ,\
                                                                ERROR_FLAG,\
                                                                CREATION_TS )\
                                                            SELECT\
                                                            RESULTS.RUN_GUID AS RUN_GUID,\
                                                            RESULTS.PIPELINE_ID AS PIPELINE_ID,\
                                                            RESULTS.START_TIME_UTC::VARCHAR AS START_TIME_UTC,\
                                                            F1.VALUE:SRC_DATABASE_NAME::VARCHAR AS SRC_DATABASE_NAME,\
                                                            F1.VALUE:SRC_SCHEMA_NAME::VARCHAR AS SRC_SCHEMA_NAME,\
                                                            F1.VALUE:SRC_OBJECT_NAME::VARCHAR AS SRC_OBJECT_NAME,\
                                                            F1.VALUE:SRC_OBJECT_TYPE::VARCHAR AS SRC_OBJECT_TYPE,\
                                                            F1.VALUE:TRGT_DATABASE_NAME::VARCHAR AS TRGT_DATABASE_NAME,\
                                                            F1.VALUE:TRGT_SCHEMA_NAME::VARCHAR AS TRGT_SCHEMA_NAME,\
                                                            F1.VALUE:TRGT_OBJECT_NAME::VARCHAR AS TRGT_OBJECT_NAME,\
                                                            F1.VALUE:TRGT_OBJECT_TYPE::VARCHAR AS TRGT_OBJECT_TYPE,\
                                                            F2.VALUE:COLUMN_NAME::VARCHAR AS COLUMN_NAME,\
                                                            F2.VALUE:IN_SRC::BOOLEAN AS IN_SRC,\
                                                            F2.VALUE:IN_TRGT::BOOLEAN AS IN_TRGT,\
                                                            F2.VALUE:IN_SYNC::BOOLEAN AS IN_SYNC,\
                                                            F2.VALUE:IN_EXCLUDED::BOOLEAN AS IN_EXCLUDED,\
                                                            F2.VALUE:SRC_DATATYPE::VARCHAR AS SRC_DATATYPE,\
                                                            F2.VALUE:TRGT_DATATYPE::VARCHAR AS TRGT_DATATYPE,\
                                                            F2.VALUE:DATATYPE_EQUAL::BOOLEAN AS DATATYPE_EQUAL,\
                                                            F2.VALUE:AGGREGATION_TYPE::VARCHAR AS AGGREGATION_TYPE,\
                                                            F2.VALUE:AGGREGATION_EQUAL::BOOLEAN AS AGGREGATION_EQUAL,\
                                                            F2.VALUE:AGGREGATION_RESULT_SRC::VARCHAR AS AGGREGATION_RESULT_SRC,\
                                                            F2.VALUE:AGGREGATION_RESULT_TRGT::VARCHAR AS AGGREGATION_RESULT_TRGT,\
                                                            F2.VALUE:AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC::VARCHAR AS AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC,\
                                                            F2.VALUE:AGGREGATION_EQUAL_TOLERATED::BOOLEAN AS AGGREGATION_EQUAL_TOLERATED,\
                                                            F2.VALUE:COUNT_NULLS_EQUAL::BOOLEAN AS COUNT_NULLS_EQUAL,\
                                                            F2.VALUE:COUNT_NULLS_SRC::VARCHAR AS COUNT_NULLS_SRC,\
                                                            F2.VALUE:COUNT_NULLS_TRGT::VARCHAR AS COUNT_NULLS_TRGT,\
                                                            F2.VALUE:COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC::VARCHAR AS COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC,\
                                                            F1.VALUE:SRC_ERROR:QUERY::VARCHAR AS ERROR_QUERY_SRC,\
                                                            F1.VALUE:SRC_ERROR:ERROR::VARCHAR AS ERROR_MSG_SRC,\
                                                            F1.VALUE:TRGT_ERROR:QUERY::VARCHAR AS ERROR_QUERY_TRGT,\
                                                            F1.VALUE:TRGT_ERROR:ERROR::VARCHAR AS ERROR_MSG_TRGT,\
                                                            CASE WHEN ERROR_MSG_SRC IS NULL AND ERROR_MSG_TRGT IS NULL THEN FALSE ELSE TRUE END AS ERROR_FLAG,\
                                                            SYSDATE()\
                                                            FROM {result_table} RESULTS\
                                                            CROSS JOIN LATERAL FLATTEN(INPUT => RESULT:OBJECTS) F1\
                                                            CROSS JOIN LATERAL FLATTEN(INPUT => F1.VALUE:COLUMNS) F2\
                                                            WHERE RUN_GUID = '{run_guid}';"

        self.execute_statement(insert_statement)
