from databricks import sql as databricks_sqlconnect
import pandas as pd
import logging
import re
from datetime import datetime

from typing import Union, List, Dict
from pathlib import PurePath

from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.core.database_objects import DatabaseObject

#########################################################################################
#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger("Databricks_Hive_Metastore_Service")
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)


class DatabricksHiveMetastoreService(object):
    def __init__(self, connection_params: dict):
        self.connection_params = connection_params
        self.databricks_connection = None
        self.databricks_datatype_mapping = {
            "string": ["string", "array", "map", "struct"],
            "numeric": [
                "int",
                "bigint",
                "double",
                "decimal",
                "float",
                "smallint",
                "tinyint",
            ],
            "date_and_time": [
                "timestamp",
                "date",
                "interval",
                "timestamp_ntz",
                "timestamp_tz",
                "timestamp_ltz",
            ],
            "binary": ["binary"],
            "boolean": ["boolean"],
        }

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.databricks_connection is not None:
            self.databricks_connection.close()

    def __del__(self):
        if self.databricks_connection is not None:
            self.databricks_connection.close()

    def _connect_to_databricks(self):
        self.databricks_connection = databricks_sqlconnect.connect(
            **self.connection_params
        )
        return self.databricks_connection

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
        return f"Databricks ERROR: {message}\nFailed statement:\n{statement}"

    @staticmethod
    def _get_in_clause(
        key_filters: list,
        numeric_columns: list,
        numeric_scale: int,
        where_exists: bool = True,
        enclose_column_by_double_quotes: bool = False,
    ) -> str:
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

        if where_exists:
            in_clause_cols = f" AND (("
        else:
            in_clause_cols = f" WHERE (("
        for key in key_filters.keys():
            if key in numeric_columns:
                in_clause_cols += f"""ROUND({key.replace("'", "")}, {numeric_scale})""" + ","
            else:
                in_clause_cols += key.replace("'", "") + ","
        in_clause_cols = in_clause_cols[:-1] + ")"
        in_clause = in_clause_cols + " in (" + in_clause_values + ")"
        return in_clause

    def _get_column_clause(
        self, column_list: list, columns_datatype: list, numeric_scale, key_columns,
        enclose_column_by_double_quotes: bool = False
    ) -> dict:
        """turns list of desired columns into a sql compatible string

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
            column_datatype = next(
                x for x in columns_datatype if x["COLUMN_NAME"] == column
            )["DATA_TYPE"]

            if column in key_columns or not (
                column_datatype.lower()
                in self.databricks_datatype_mapping["date_and_time"]
            ):
                if (
                    column_datatype.lower()
                    in self.databricks_datatype_mapping["numeric"]
                ):
                    if numeric_scale:
                        column_intersecions_new.append(
                            f"CAST(ROUND({column}, {numeric_scale}) as decimal(38,{numeric_scale})) as {column}"
                        )
                    else:
                        column_intersecions_new.append(f"{column} as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)
                elif (
                    column_datatype.lower()
                    in self.databricks_datatype_mapping["string"]
                ):
                    column_intersecions_new.append(f"{column} AS {column}")
                    used_columns.append(column)
                else:
                    column_intersecions_new.append(column)
                    used_columns.append(column)

        column_intersections = column_intersecions_new.copy()
        column_clause = str(column_intersections)[1:-1].replace("'", "")
        return column_clause, numeric_columns, used_columns

    def get_database_objects(
        self,
        database: str,
        schema: str = None,
        object_type_restriction: str = "include_all",
    ) -> dict:
        if self.databricks_connection is None:
            self._connect_to_databricks()

        all_database_tables = []
        all_database_views = []

        if (
            object_type_restriction == "include_all"
            or object_type_restriction == "include_only_tables"
        ):
            if schema:
                query_db_tables = f"SHOW TABLES IN {database}.{schema}"
            else:
                logger.error(
                    "Query defined as null - please check input for execute_queries function."
                )
                exit()

            all_database_tables = self.execute_queries(query_db_tables)

        if (
            object_type_restriction == "include_all"
            or object_type_restriction == "include_only_views"
        ):
            if schema:
                query_db_views = f"SHOW VIEWS IN {schema}"
            else:
                logger.error(
                    "Query defined as null - please check input for execute_queries function."
                )
                exit()

            all_database_views = self.execute_queries(query_db_views)

        database_objects = []
        for row in all_database_tables:
            database_table = (
                f'hive_metastore.{row["database"]}.{row["tableName"]}'.upper()
            )
            database_objects.append(
                {"object_identifier": database_table, "object_type": "table"}
            )
        for row in all_database_views:
            database_view = f'{row["TABLE_CATALOG"]}.{row["TABLE_SCHEMA"]}.{row["TABLE_NAME"]}'.upper()
            database_objects.append(
                {"object_identifier": database_view, "object_type": "view"}
            )
        return database_objects

    def get_last_altered_timestamp_from_object(self, object: DatabaseObject) -> str:
        """queries last_altered timestamp for given object

        Args:
            object (str): object for comparison

        Returns:
            str: last_altered timestamp
        """
        if self.databricks_connection is None:
            self._connect_to_databricks()

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

        if self.databricks_connection is None:
            self._connect_to_databricks()

        query_show_columns = (
            f"SHOW COLUMNS IN {object.database}.{object.schema}.{object.name};"
        )

        all_columns = self.execute_queries(query_show_columns)
        columns = []

        for row in all_columns:
            columns.append(row["col_name"])

        return columns

    def get_row_count_from_object(self, object: DatabaseObject, where_clause: str="") -> int:
        """gets row count from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: number of rows in object
        """

        if self.databricks_connection is None:
            self._connect_to_databricks()

        # is it more efficient to select the information_schema.table view to get the rows?
        query_get_row_count = f"SELECT COUNT(*) AS ROW_COUNT FROM {object.database}.{object.schema}.{object.name} {where_clause};"
        row_count = -1
        error_list = []

        try:
            row_count = self.execute_queries(query_get_row_count)[0]["ROW_COUNT"]

        except Exception as err:
            error_list.append(str(err))
            error_list.append(query_get_row_count)

        return row_count, error_list

    def get_data_types_from_object(
        self, object: DatabaseObject, column_intersections: list
    ) -> dict:
        """returns datatypes for all intersection columns in a database object

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns for which the data type is queried

        Returns:
            dict: columns and their datatype
        """

        if self.databricks_connection is None:
            self._connect_to_databricks()

        column_intersections = str(column_intersections)[1:-1]
        if column_intersections == "":
            column_intersections = "''"

        query_get_data_types_from_object = (
            f"DESCRIBE TABLE {object.database}.{object.schema}.{object.name};"
        )

        table_description = self.execute_queries(query_get_data_types_from_object)

        dict_colummns_datatype = []

        for row in table_description:
            dict_colummns_datatype.append(
                {"COLUMN_NAME": row["col_name"], "DATA_TYPE": row["data_type"]}
            )
        return dict_colummns_datatype

    def get_count_distincts_from_object(
        self,
        object: DatabaseObject,
        column_intersections: list,
        where_clause: str = "",
        exclude_columns: list = [],
        enclose_column_by_double_quotes: bool = False,
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

        if self.databricks_connection is None:
            self._connect_to_databricks()

        unions = ""

        for column in column_intersections:
            if column not in exclude_columns:
                unions += f" UNION SELECT '{column}' AS COLUMN_NAME, COUNT(DISTINCT {column}) AS COUNT_DISTINCT FROM {object.database}.{object.schema}.{object.name} {where_clause}"

        query_get_count_distincts_from_object = f"{unions[6:]} ORDER BY COUNT_DISTINCT;"
        error_list = []
        try:
            dict_count_distincts = self.execute_queries(
                query_get_count_distincts_from_object
            )

        except Exception as err:
            # raise err
            dict_count_distincts = []
            error_list.append(
                ["ERROR", str(err).split("|||")[0], str(err).split("|||")[1]]
            )

        return dict_count_distincts, error_list

    def get_table_size(self, object: DatabaseObject) -> int:
        """returns size of given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: size of object
        """

        if self.databricks_connection is None:
            self._connect_to_databricks()

        query_analyze_table = f"ANALYZE TABLE {object.database}.{object.schema}.{object.name} COMPUTE STATISTICS NOSCAN"
        self.execute_queries(query_analyze_table)

        query_get_table_size = (
            f"DESC EXTENDED {object.database}.{object.schema}.{object.name}"
        )

        table_description = self.execute_queries(query_get_table_size)
        size_string = [
            row["data_type"]
            for row in table_description
            if row["col_name"] == "Statistics"
        ][0]
        size = int(re.search(r"\d+", size_string).group())

        return size

    def create_checksums(
        self,
        object: DatabaseObject,
        column_intersections: list,
        where_clause: str = "",
        exclude_columns: list = [],
        numeric_scale: int = None,
        enclose_column_by_double_quotes: bool = False,
    ) -> List[Dict]:
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

        if self.databricks_connection is None:
            self._connect_to_databricks()

        column_intersections = [
            f"{x.upper()}" for x in column_intersections if x not in exclude_columns
        ]

        dict_colummns_datatype = self.get_data_types_from_object(
            object, column_intersections
        )

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            column_datatype = next(
                x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column
            )["DATA_TYPE"]

            count_nulls += f", SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END) AS COUNTNULLS_{column}"

            if column_datatype.lower() in self.databricks_datatype_mapping["numeric"]:
                if numeric_scale:
                    aggregates += f", CAST(ROUND(SUM({column}), {numeric_scale}) as decimal(38, {numeric_scale})) AS sum_{column}"
                else:
                    aggregates += (
                        f", CAST(SUM({column}) as decimal(38)) AS sum_{column}"
                    )

            elif (
                column_datatype.lower() in self.databricks_datatype_mapping["string"]
                or column_datatype.lower()
                in self.databricks_datatype_mapping["date_and_time"]
            ):
                aggregates += (
                    f", COUNT(DISTINCT LOWER({column})) AS countdistinct_{column}"
                )

            elif column_datatype.lower() in self.databricks_datatype_mapping["binary"]:
                aggregates += f", COUNT(DISTINCT LOWER(TRY_TO_NUMBER({column}::VARCHAR))) AS countdistinct_{column}"

            elif column_datatype.lower() in self.databricks_datatype_mapping["boolean"]:
                aggregates += f", MAX((SELECT COUNT(*) FROM {object.database}.{object.schema}.{object.name} WHERE {column} = true)) || '_' || MAX((SELECT COUNT(*) FROM {object.database}.{object.schema}.{object.name} WHERE {column} = false)) AS aggregateboolean_{column}"

            # else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

        query_checksums = f"SELECT {aggregates[1:]} FROM {object.database}.{object.schema}.{object.name} {where_clause};"

        query_countnulls = f"SELECT {count_nulls[1:]} FROM {object.database}.{object.schema}.{object.name} {where_clause};"

        error_list = []
        checksums={}

        try:
            checksums_results = self.execute_queries(
                [query_checksums, query_countnulls]
            )

            aggregation_results = checksums_results[0][0]
            countnulls_results = checksums_results[1][0]

            checksums = {}
            for key in aggregation_results.asDict().keys():
                aggregation = key.split("_", 1)[0].upper()
                col_name = key.split("_", 1)[1]
                value = aggregation_results[key]
                cnt_nulls = countnulls_results[f"COUNTNULLS_{col_name}"]
                checksums[col_name] = [aggregation, value, cnt_nulls]

        except Exception as err:
            # TODO: Improve error formatting
            error_list.append(["ERROR",query_checksums, str(err)])

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
        enclose_column_by_double_quotes: bool = False,
    ) -> List[Dict]:
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

        if self.databricks_connection is None:
            self._connect_to_databricks()

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
                if (
                    column in group_by_aggregation_columns
                    and column not in exclude_columns
                )
            ]

        group_by_query_columns_string = " "
        grouping_columns_final = []
        error_dict = {}

        try:
            for column in group_by_columns:
                if column in column_intersections and column not in exclude_columns:
                    group_by_query_columns_string += f"{column} ,"
                    grouping_columns_final.append(column)

            group_by_query_columns_string = group_by_query_columns_string[:-1]

            dict_colummns_datatype = self.get_data_types_from_object(
                object, aggregation_columns
            )

            aggregates = ""
            aggregates_min = ""

            for column in aggregation_columns:
                column_datatype = next(
                    x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column
                )["DATA_TYPE"]

                if (
                    column_datatype.lower()
                    in self.databricks_datatype_mapping["numeric"]
                ):
                    if numeric_scale:
                        aggregates_min += f", CAST(ROUND(MIN({column}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS MIN_{column}, CAST(ROUND(max({column}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS MAX_{column}"
                        aggregates += f", CAST(ROUND(SUM({column}), {numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS SUM_{column}"

                    else:
                        aggregates_min += f", MIN({column}) AS MIN_{column}, MAX({column}) AS MAX_{column}"
                        aggregates += f", SUM({column}) AS SUM_{column}"

                elif not only_numeric and (
                    column_datatype.lower()
                    in self.databricks_datatype_mapping["string"]
                    or column_datatype.lower()
                    in self.databricks_datatype_mapping["date_and_time"]
                ):
                    aggregates += (
                        f", COUNT(DISTINCT LOWER({column})) AS COUNTDISTINCT_{column}"
                    )

                elif (
                    not only_numeric
                    and column_datatype.lower()
                    in self.databricks_datatype_mapping["binary"]
                ):
                    aggregates += f", COUNT(DISTINCT LOWER(TRY_TO_NUMBER({column}::VARCHAR))) AS COUNTDISTINCT_{column}"

                elif (
                    not only_numeric
                    and column_datatype.lower()
                    in self.databricks_datatype_mapping["boolean"]
                ):
                    aggregates += f", MAX((SELECT COUNT(*) FROM {object.database}.{object.schema}.{object.name} WHERE {column} = true)) || '_' || MAX((SELECT COUNT(*) FROM {object.database}.{object.schema}.{object.name} WHERE {column} = false)) AS AGGREGATEBOOLEAN_{column}"

                # else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

            # CASE 1: min_max
            if group_by_aggregation_type == "only_min_max":
                group_by_query_aggregation_string = aggregates_min[1:]

            # CASE 2; sum, count_distinct, aggregate_boolean
            elif group_by_aggregation_type == "various":
                group_by_query_aggregation_string = aggregates[1:]

            # CASE 3: sum, count_distinct, aggregate_boolean, min_max
            elif group_by_aggregation_type == "various_and_min_max":
                group_by_query_aggregation_string = f"{aggregates_min[1:]}{aggregates}"

            query_group_by_aggregation = f"SELECT {group_by_query_columns_string}, COUNT(*) AS COUNT_OF_GROUP_BY_VALUE, {group_by_query_aggregation_string} FROM {object.database}.{object.schema}.{object.name} {where_clause} GROUP BY {group_by_query_columns_string} ORDER BY {group_by_query_columns_string};"

            group_by_aggregation_pdf = self.execute_queries(
                query_group_by_aggregation, True
            )
        except Exception as err:
            group_by_aggregation_pdf = pd.DataFrame()
            group_by_aggregation_pdf["TESTATM_ERROR"] = [1]
            if not grouping_columns_final:
                error_dict = {
                    "QUERY": "NO Group-BY Columns found in the Columns Intersection. Please check if the configurated Group-By Columns exist in the Table",
                    "ERROR":  "NO Group-BY Columns found in the Columns Intersection. Please check if the configurated Group-By Columns exist in the Table"
                }
                group_by_query_aggregation_string = ""
            elif "|||" in str(err):
                error_dict = {
                    "QUERY": str(err).split("|||")[0],
                    "ERROR": str(err).split("|||")[1],
                }
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
            error_dict
        )

    def create_pandas_df(
        self,
        object: DatabaseObject,
        intersection_columns_trgt_src: list,
        where_clause:str="",
        exclude_columns:list=[],
        enclose_column_by_double_quotes: bool = False
    ) -> pd.DataFrame:
        """creates pandas dataframes with all data from given object in given columns

        Args:
            object (DatabaseObject): table or view
            intersection_columns_trgt_src (list): columns existing in source and target

        Returns:
            pd.DataFrame: direct result of sql query
        """
        if self.databricks_connection is None:
            self._connect_to_databricks()

        intersection_columns_trgt_src_ = ', '.join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"SELECT {intersection_columns_trgt_src_} FROM {object.database}.{object.schema}.{object.name} {where_clause};"

        src_pdf = self.execute_queries(df_query, True)

        return src_pdf

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
        enclose_column_by_double_quotes: bool = False,
    ) -> List[Dict]:
        if self.databricks_connection is None:
            self._connect_to_databricks()

        where_exists = True
        if not where_clause:
            where_exists = False

        sample_count = str(sample_count)
        key_intersection = list(
            (set(column_intersections) & set(key_columns)) - set(exclude_columns)
        )
        filter_intersection = list(
            (set(column_intersections) & set(key_filters.keys())) - set(exclude_columns)
        )
        dedicated_intersection = list(
            (set(column_intersections) & set(dedicated_columns)) - set(exclude_columns)
        )

        key_intersection.sort()
        filter_intersection.sort()
        dedicated_intersection.sort()

        if dedicated_intersection != []:
            is_dedicated = True

            dict_colummns_datatype = self.get_data_types_from_object(
                object, dedicated_intersection
            )

        else:
            is_dedicated = False

            dict_colummns_datatype = self.get_data_types_from_object(
                object, column_intersections
            )

        if key_intersection != [] and is_dedicated:
            keys = str(key_intersection)[1:-1].replace("'", "")
            column_clause, numeric_columns, used_columns = self._get_column_clause(
                dedicated_intersection,
                dict_colummns_datatype,
                numeric_scale,
                key_columns,
            )
            if (key_filters != {}) & (filter_intersection != []):
                values = list(key_filters.values())
                if values[0] != []:
                    in_clause = self._get_in_clause(
                        key_filters, numeric_columns, numeric_scale, where_exists, enclose_column_by_double_quotes
                    )
            else:
                in_clause = ""
            sample_query = f"SELECT {column_clause} FROM {object.database}.{object.schema}.{object.name} TABLESAMPLE ({sample_count} ROWS) {where_clause}{in_clause} ORDER BY {keys};"
        elif key_intersection != [] and not is_dedicated:
            keys = str(key_intersection)[1:-1].replace("'", "")
            column_clause, numeric_columns, used_columns = self._get_column_clause(
                column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes
            )
            if (key_filters != {}) & (filter_intersection != []):
                values = list(key_filters.values())
                if values[0] != []:
                    in_clause = self._get_in_clause(
                        key_filters, numeric_columns, numeric_scale, where_exists, enclose_column_by_double_quotes
                    )
            else:
                in_clause = ""
            sample_query = f"SELECT {column_clause} FROM {object.database}.{object.schema}.{object.name} TABLESAMPLE ({sample_count} ROWS) {where_clause}{in_clause} ORDER BY {keys};"
        else:
            column_intersections = list(
                set(column_intersections) - set(exclude_columns)
            )
            column_intersections.sort()
            column_clause, numeric_columns, used_columns = self._get_column_clause(
                column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes
            )
            sample_query = f"SELECT {column_clause} FROM {object.database}.{object.schema}.{object.name} TABLESAMPLE ({sample_count} ROWS) {where_clause};"

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
                error_dict = {
                    "QUERY": str(err).split("|||")[0],
                    "ERROR": str(err).split("|||")[1],
                }
            else:
                error_dict = {"QUERY": "No SQL Error", "ERROR": str(err)}

        return_list = []
        return_list.append(sample_pdf)
        return_list.append(error_dict)

        return return_list, key_dict, used_columns, sample_query

    def execute_queries(
        self,
        query: Union[str, List[str]],
        return_as_pdf: bool = False,
        return_query_ids: bool = False,
    ) -> Union[List[Dict], List[List[Dict]]]:
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
        if self.databricks_connection is None:
            self._connect_to_databricks()

        if query:
            query_list: List[str] = query if isinstance(query, list) else [query]
        else:
            logger.error(
                "Query defined as null - please check input for execute_queries function."
            )

        cursor = self.databricks_connection.cursor()

        results = []
        query_ids = []

        for single_query in query_list:
            try:
                query_result = cursor.execute(single_query).fetchall()
                if return_as_pdf:
                    columns = [col[0] for col in cursor.description]
                    query_result = pd.DataFrame(query_result, columns=columns)

                results.append(query_result)
                query_ids.append(0)  # there is no query id returned by databricks

            except Exception as err:
                raise Exception(single_query + "|||" + str(err))

        if return_query_ids:
            return (
                results[0],
                query_ids[0] if not isinstance(query, list) else results,
                query_ids,
            )

        else:
            return results[0] if not isinstance(query, list) else results

    def execute_statement(self, statement: Union[str, List[str]]) -> None:
        """
            Executes simple statement against snowflake
            Schema and Database settings must be set beforehand
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        if self.databricks_connection is None:
            self._connect_to_databricks()

        statement_list: List[str] = (
            statement if isinstance(statement, list) else [statement]
        )

        cursor = self.databricks_connection.cursor()

        for single_statement in statement_list:
            try:
                stripped_statement = single_statement.strip()
                _ = cursor.execute(stripped_statement)

            except Exception as err:
                raise Exception(self._get_error_message(err, single_statement)) from err

    def create_schemas(self, database_name: str, schemas: List):
        statement_list = []

        for schema in schemas:
            statement_list.append(f"CREATE SCHEMA IF NOT EXISTS {schema}")

        self.execute_statement(statement_list)

    def insert_json_results(
        self,
        run_guid: str,
        pipeline_name: str,
        pipeline_id: str,
        start_time_utc: str,
        result_table: str,
        results: dict,
    ) -> None:
        """
        copy into - result table for json results
        """

        statement = f"CREATE TABLE IF NOT EXISTS {result_table} (RUN_GUID STRING, PIPELINE_NAME STRING, PIPELINE_ID STRING, START_TIME_UTC STRING, RESULT STRING, CREATION_TIME_UTC STRING)"

        self.execute_statement(statement)

        statement = (
            "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(
                result_table,
                run_guid,
                pipeline_name,
                pipeline_id,
                start_time_utc,
                str(results).replace("'", '"'),
                datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S"),
            )
        )

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
        result_database = result_table.split(".", 1)[0]

        statement = f"COPY INTO {result_table} (RUN_GUID, PIPELINE_NAME, PIPELINE_ID, SOURCE_SYSTEM, TARGET_SYSTEM, DATABASE_NAME, SCHEMA_NAME, OBJECT_NAME  ,RESULT, CREATION_TS) FROM (SELECT '{run_guid}', '{pipeline_name}', '{pipeline_id}', '{source_system}', '{target_system}', '{database}', '{schema}', '{object}', $1, SYSDATE() from @{stage_name} (file_format => {result_database}.meta_data.ff_json ));"

        self.execute_statement(statement)

    def insert_highlevel_results(
        self,
        results: dict,
        run_guid: str,
        pipeline_name: str,
        pipeline_id: str,
        result_table_highlevel: str,
    ) -> None:
        """
        insert into - highlevel results per "pipeline run" / "generic testing tool execution"
        """

        statement = f"CREATE TABLE IF NOT EXISTS {result_table_highlevel} (RUN_GUID STRING, PIPELINE_NAME STRING, PIPELINE_ID STRING, START_TIME_UTC STRING, SOURCE_SYSTEM STRING, TARGET_SYSTEM STRING, DATABASE_NAME STRING, TESTSET STRING, ALL_OBJECTS_MATCHING BOOLEAN, ALL_COLUMNS_EQUAL BOOLEAN, ALL_ROWCOUNTS_EQUAL BOOLEAN, ALL_CHECKSUMS_EQUAL BOOLEAN, ALL_SAMPLES_EQUAL BOOLEAN, ALL_OBJECTS_EQUAL BOOLEAN, OBJECTS_TO_COMPARE_SRC STRING, OBJECTS_TO_COMPARE_TRGT STRING, NUMBER_OF_OBJECTS_TO_COMPARE INT, SRC_MINUS_TRGT STRING, TRGT_MINUS_SRC STRING, CREATION_TS_UTC STRING)"

        self.execute_statement(statement)

        TESTSET_ = ", ".join(results["TESTSET"])

        OBJECTS_TO_COMPARE_SRC_ = ", ".join(results["OBJECTS_TO_COMPARE_SRC"])

        OBJECTS_TO_COMPARE_TRGT_ = ", ".join(results["OBJECTS_TO_COMPARE_TRGT"])

        SRC_MINUS_TRGT_ = ", ".join(results["SRC_MINUS_TRGT"])

        TRGT_MINUS_SRC_ = ", ".join(results["TRGT_MINUS_SRC"])

        date_utc = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")

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
                                                                        ALL_DATATYPES_EQUAL, \
                                                                        ALL_ROWCOUNTS_EQUAL,  \
                                                                        ALL_CHECKSUMS_EQUAL,  \
                                                                        ALL_SAMPLES_EQUAL,  \
                                                                        ALL_OBJECTS_EQUAL,  \
                                                                        OBJECTS_TO_COMPARE_SRC,  \
                                                                        OBJECTS_TO_COMPARE_TRGT,  \
                                                                        NUMBER_OF_OBJECTS_TO_COMPARE,  \
                                                                        SRC_MINUS_TRGT,  \
                                                                        TRGT_MINUS_SRC, \
                                                                        CREATION_TS_UTC) \
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
                                                                        '{date_utc}')"

        self.execute_statement(insert_statement)

    def insert_objectlevel_results(
        self,
        result_table: str,
        result_table_objectlevel: str,
        run_guid: str,
        results: dict,
    ) -> None:
        """
        insert into - detailed results per object
        """
        date_utc = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")

        statement = f"CREATE TABLE IF NOT EXISTS {result_table_objectlevel} (RUN_GUID STRING, PIPELINE_ID STRING, START_TIME_UTC STRING, SRC_DATABASE_NAME STRING, SRC_SCHEMA_NAME STRING, SRC_OBJECT_NAME STRING, SRC_OBJECT_TYPE STRING, TRGT_DATABASE_NAME STRING, TRGT_SCHEMA_NAME STRING, TRGT_OBJECT_NAME STRING, TRGT_OBJECT_TYPE STRING, SRC_FILTER STRING, TRGT_FILTER STRING, EXCLUDED_COLUMNS STRING, COLUMNS_EQUAL BOOLEAN, COLUMN_INTERSECTION STRING,SRC_COLUMNS_MINUS_TRGT_COLUMNS STRING, TRGT_COLUMNS_MINUS_SRC_COLUMNS STRING, ROW_COUNTS_EQUAL BOOLEAN, SRC_ROW_COUNT INT, TRGT_ROW_COUNT INT, ALL_COUNT_NULLS_EQUAL BOOLEAN, AGGREGATIONS_EQUAL BOOLEAN, SRC_ERROR_QUERY  STRING, TRGT_ERROR_QUERY STRING, SRC_ERROR_MSG STRING, TRGT_ERROR_MSG STRING, GROUP_BY_COLUMNS STRING,GROUP_BY_EQUAL BOOLEAN, GROUP_BY_VALUES_WITH_MISMATCHES STRING, COLUMNS_WITH_MISMATCH STRING, SRC_GROUP_BY_QUERY STRING, TRGT_GROUP_BY_QUERY STRING, SRC_GROUP_BY_ERROR STRING, TRGT_GROUP_BY_ERROR STRING, SAMPLES_COMPARED BOOLEAN,SAMPLES_EQUAL BOOLEAN, SAMPLE_KEYS STRING, SRC_SAMPLE STRING, TRGT_SAMPLE STRING, SRC_SAMPLE_QUERY STRING, TRGT_SAMPLE_QUERY STRING, SRC_SAMPLE_ERROR_MSG STRING, TRGT_SAMPLE_ERROR_MSG STRING, PANDAS_DATAFRAME_COMPARED BOOLEAN, PANDAS_DATAFRAME_EQUAL BOOLEAN, SRC_NOT_ALTERED_DURING_COMPARISON BOOLEAN, TRGT_NOT_ALTERED_DURING_COMPARISON BOOLEAN, SRC_LAST_ALTERED STRING, TRGT_LAST_ALTERED STRING, CREATION_TS_UTC STRING)"

        self.execute_statement(statement)

        dict_list = self.get_objects_in_result_column(result_table, run_guid)

        """
        Now, we have to extract all the information in the dicts manually to
        insert them in the query. We write one line for each object one by one.
        """

        for element in dict_list:
            elem = element
            help_str, elem = elem.split(",", 1)
            src_database_name = re.sub(
                r"(.*)\"SRC_DATABASE_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_schema_name = re.sub(
                r"(.*)\"SRC_SCHEMA_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_object_name = re.sub(
                r"(.*)\"SRC_OBJECT_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_object_type = re.sub(
                r"(.*)\"SRC_OBJECT_TYPE\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_database_name = re.sub(
                r"(.*)\"TRGT_DATABASE_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_schema_name = re.sub(
                r"(.*)\"TRGT_SCHEMA_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_object_name = re.sub(
                r"(.*)\"TRGT_OBJECT_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_object_type = re.sub(
                r"(.*)\"TRGT_OBJECT_TYPE\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_filter = re.sub(
                r"(.*)\"SRC_FILTER\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_filter = re.sub(
                r"(.*)\"TRGT_FILTER\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("],", 1)
            help_str = help_str + "]"
            excluded_columns = re.sub(
                r"(.*)\"EXCLUDED_COLUMNS\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            columns_equal = re.sub(r"(.*)\"COLUMNS_EQUAL\":\s(.*)", r"\2", help_str)
            help_str, elem = elem.split("],", 1)
            help_str = help_str + "]"
            column_intersection = re.sub(
                r"(.*)\"COLUMN_INTERSECTION\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("],", 1)
            help_str = help_str + "]"
            src_columns_minus_trgt_columns = re.sub(
                r"(.*)\"SRC_COLUMNS_MINUS_TRGT_COLUMNS\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("],", 1)
            help_str = help_str + "]"
            trgt_columns_minus_src_columns = re.sub(
                r"(.*)\"TRGT_COLUMNS_MINUS_SRC_COLUMNS\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            row_counts_equal = re.sub(
                r"(.*)\"ROW_COUNTS_EQUAL\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_row_count = re.sub(
                r"(.*)\"SRC_ROW_COUNT\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_row_count = re.sub(
                r"(.*)\"TRGT_ROW_COUNT\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            all_count_nulls_equal = re.sub(
                r"(.*)\"ALL_COUNT_NULLS_EQUAL\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            aggregations_equal = re.sub(
                r"(.*)\"AGGREGATIONS_EQUAL\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            src_error = re.sub(
                r"(.*)\"SRC_ERROR\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            trgt_error = re.sub(
                r"(.*)\"TRGT_ERROR\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(', "SRC_GROUP_BY_QUERY', 1)
            elem = '"SRC_GROUP_BY_QUERY' + elem
            group_by_columns = re.sub(
                r"(.*)\"GROUP_BY_COLUMNS\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_group_by_query = re.sub(
                r"(.*)\"SRC_GROUP_BY_QUERY\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_group_by_query = re.sub(
                r"(.*)\"TRGT_GROUP_BY_QUERY\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            group_by_equal = re.sub(r"(.*)\"GROUP_BY_EQUAL\":\s(.*)", r"\2", help_str)
            help_str, elem = elem.split(', "COLUMNS_WITH_MISMATCH', 1)
            elem = '"COLUMNS_WITH_MISMATCH' + elem
            group_by_values_with_mismatches = re.sub(
                r"(.*)\"GROUP_BY_VALUES_WITH_MISMATCHES\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(', "SRC_GROUP_BY_ERROR', 1)
            elem = '"SRC_GROUP_BY_ERROR' + elem
            columns_with_mismatch = re.sub(
                r"(.*)\"COLUMNS_WITH_MISMATCH\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(', "TRGT_GROUP_BY_ERROR', 1)
            elem = '"TRGT_GROUP_BY_ERROR' + elem
            src_group_by_error = re.sub(
                r"(.*)\"SRC_GROUP_BY_ERROR\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(', "SAMPLES_COMPARED', 1)
            elem = '"SAMPLES_COMPARED' + elem
            trgt_group_by_error = re.sub(
                r"(.*)\"TRGT_GROUP_BY_ERROR\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            samples_compared = re.sub(
                r"(.*)\"SAMPLES_COMPARED\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            samples_equal = re.sub(
                r"(.*)\"SAMPLES_EQUAL\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            sample_keys = re.sub(
                r"(.*)\"SAMPLE_KEYS\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("}},", 1)
            help_str = help_str + "}}"
            src_sample = re.sub(
                r"(.*)\"SRC_SAMPLE\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("}},", 1)
            help_str = help_str + "}}"
            trgt_sample = re.sub(
                r"(.*)\"TRGT_SAMPLE\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(';",', 1)
            help_str = help_str + ';"'
            src_sample_query = re.sub(
                r"(.*)\"SRC_SAMPLE_QUERY\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(';",', 1)
            help_str = help_str + ';"'
            trgt_sample_query = re.sub(
                r"(.*)\"TRGT_SAMPLE_QUERY\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            src_sample_error_dict = re.sub(
                r"(.*)\"SRC_SAMPLE_ERROR_DICT\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            trgt_sample_error_dict = re.sub(
                r"(.*)\"TRGT_SAMPLE_ERROR_DICT\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            pandas_dataframe_compared = re.sub(
                r"(.*)\"PANDAS_DATAFRAME_COMPARED\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            pandas_dataframe_equal = re.sub(
                r"(.*)\"PANDAS_DATAFRAME_EQUAL\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_not_altered_during_comparison = re.sub(
                r"(.*)\"SRC_NOT_ALTERED_DURING_COMPARISON\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_not_altered_during_comparison = re.sub(
                r"(.*)\"TRGT_NOT_ALTERED_DURING_COMPARISON\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_last_altered = re.sub(
                r"(.*)\"SRC_LAST_ALTERED\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_last_altered = re.sub(r"(.*)\"TRGT_LAST_ALTERED\":\s(.*)", r"\2", help_str)

            # the rest in elem is not used for this table

            insert_statement = f"INSERT INTO {result_table_objectlevel} ( \
                                                                            RUN_GUID, \
                                                                            PIPELINE_ID, \
                                                                            START_TIME_UTC, \
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
                                                                            ROW_COUNTS_EQUAL, \
                                                                            SRC_ROW_COUNT, \
                                                                            TRGT_ROW_COUNT, \
                                                                            ALL_COUNT_NULLS_EQUAL, \
                                                                            AGGREGATIONS_EQUAL, \
                                                                            SRC_ERROR_QUERY , \
                                                                            TRGT_ERROR_QUERY, \
                                                                            SRC_ERROR_MSG, \
                                                                            TRGT_ERROR_MSG, \
                                                                            GROUP_BY_COLUMNS, \
                                                                            GROUP_BY_EQUAL, \
                                                                            GROUP_BY_VALUES_WITH_MISMATCHES, \
                                                                            COLUMNS_WITH_MISMATCH, \
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
                                                                            CREATION_TS_UTC) \
                                                WITH group_error_src AS (SELECT\
                                                    json_tuple('{src_group_by_error}', 'QUERY', 'ERROR') AS (grouping_errors_src_query, grouping_errors_src_error)\
                                                ),\
                                                group_error_trgt AS (SELECT\
                                                    json_tuple('{trgt_group_by_error}', 'QUERY', 'ERROR') AS (grouping_errors_trgt_query, grouping_errors_trgt_error)\
                                                ),\
                                                src_error AS (SELECT\
                                                    json_tuple('{src_error}', 'QUERY', 'ERROR') AS (src_error_query, src_error_error)\
                                                ),\
                                                trgt_error AS (SELECT\
                                                    json_tuple('{trgt_error}', 'QUERY', 'ERROR') AS (trgt_error_query, trgt_error_error)\
                                                ),\
                                                src_sample_error AS (SELECT\
                                                    json_tuple('{src_sample_error_dict}', 'QUERY', 'ERROR') AS (src_sample_error_dict_query, src_sample_error_dict_error)\
                                                ),\
                                                trgt_sample_error AS (SELECT\
                                                    json_tuple('{trgt_sample_error_dict}', 'QUERY', 'ERROR') AS (trgt_sample_error_dict_query, trgt_sample_error_dict_error)\
                                                )\
                                                SELECT\
                                                    RESULTS.RUN_GUID AS RUN_GUID, \
                                                    RESULTS.PIPELINE_ID AS PIPELINE_ID, \
                                                    RESULTS.START_TIME_UTC::STRING AS START_TIME_UTC, \
                                                    '{src_database_name}' AS SRC_DATABASE_NAME, \
                                                    '{src_schema_name}' AS SRC_SCHEMA_NAME, \
                                                    '{src_object_name}' AS SRC_OBJECT_NAME, \
                                                    '{src_object_type}' AS SRC_OBJECT_TYPE, \
                                                    '{trgt_database_name}' AS TRGT_DATABASE_NAME, \
                                                    '{trgt_schema_name}' AS TRGT_SCHEMA_NAME, \
                                                    '{trgt_object_name}' AS TRGT_OBJECT_NAME, \
                                                    '{trgt_object_type}' AS TRGT_OBJECT_TYPE, \
                                                    '{src_filter}' AS SRC_FILTER, \
                                                    '{trgt_filter}' AS TRGT_FILTER, \
                                                    '{excluded_columns}' AS EXCLUDED_COLUMNS, \
                                                    '{columns_equal}'::BOOLEAN AS COLUMNS_EQUAL, \
                                                    '{column_intersection}'::BOOLEAN AS COLUMN_INTERSECTION, \
                                                    '{src_columns_minus_trgt_columns}' AS SRC_COLUMNS_MINUS_TRGT_COLUMNS, \
                                                    '{trgt_columns_minus_src_columns}' AS TRGT_COLUMNS_MINUS_SRC_COLUMNS, \
                                                    '{row_counts_equal}'::BOOLEAN AS ROW_COUNTS_EQUAL, \
                                                    '{src_row_count}'::INT AS SRC_ROW_COUNT, \
                                                    '{trgt_row_count}'::INT AS TRGT_ROW_COUNT, \
                                                    '{all_count_nulls_equal}'::BOOLEAN AS ALL_COUNT_NULLS_EQUAL, \
                                                    '{aggregations_equal}'::BOOLEAN AS AGGREGATIONS_EQUAL, \
                                                    src_error_query::STRING AS SRC_ERROR_QUERY, \
                                                    trgt_error_query::STRING AS TRGT_ERROR_QUERY, \
                                                    src_error_error::STRING AS SRC_ERROR_MSG, \
                                                    trgt_error_error::STRING AS TRGT_ERROR_MSG, \
                                                    '{group_by_columns}' AS GROUP_BY_COLUMNS, \
                                                    '{group_by_equal}'::BOOLEAN AS GROUP_BY_EQUAL, \
                                                    '{group_by_values_with_mismatches}' AS GROUP_BY_VALUES_WITH_MISMATCHES, \
                                                    '{columns_with_mismatch}' AS COLUMNS_WITH_MISMATCH, \
                                                    CASE WHEN '{src_group_by_error}'::STRING = '{{}}'  \
                                                                THEN NULLIF('{src_group_by_query}'::STRING, '')  \
                                                        WHEN'{src_group_by_error}'::STRING != '{{}}' \
                                                            THEN NULLIF(grouping_errors_src_query::STRING, '') \
                                                        END		AS SRC_GROUP_BY_QUERY, \
                                                    CASE WHEN '{trgt_group_by_error}'::STRING = '{{}}'  \
                                                                THEN NULLIF('{trgt_group_by_query}'::STRING, '')  \
                                                        WHEN '{trgt_group_by_error}'::STRING != '{{}}' \
                                                            THEN NULLIF(grouping_errors_trgt_query::STRING, '') \
                                                        END		AS TRGT_GROUP_BY_QUERY, \
                                                    CASE WHEN '{src_group_by_error}'::STRING = '{{}}'  \
                                                                THEN NULL  \
                                                                ELSE '{src_group_by_error}'::STRING \
                                                                END AS SRC_GROUP_BY_ERROR, \
                                                    CASE WHEN '{trgt_group_by_error}'::STRING = '{{}}'  \
                                                                THEN NULL  \
                                                                ELSE '{trgt_group_by_error}'::STRING \
                                                                END AS TRGT_GROUP_BY_ERROR, \
                                                    '{samples_compared}'::BOOLEAN AS SAMPLES_COMPARED, \
                                                    '{samples_equal}'::BOOLEAN AS SAMPLES_EQUAL, \
                                                    '{sample_keys}' AS SAMPLE_KEYS, \
                                                    '{src_sample}' AS SRC_SAMPLE, \
                                                    '{trgt_sample}' AS TRGT_SAMPLE, \
                                                    '{src_sample_query}' AS SRC_SAMPLE_QUERY, \
                                                    '{trgt_sample_query}' AS TRGT_SAMPLE_QUERY, \
                                                    src_sample_error_dict_error::STRING AS SRC_SAMPLE_ERROR_MSG, \
                                                    trgt_sample_error_dict_error::STRING AS TRGT_SAMPLE_ERROR_MSG, \
                                                    '{pandas_dataframe_compared}'::BOOLEAN AS PANDAS_DATAFRAME_COMPARED, \
                                                    '{pandas_dataframe_equal}'::BOOLEAN AS PANDAS_DATAFRAME_EQUAL, \
                                                    '{src_not_altered_during_comparison}'::BOOLEAN AS SRC_NOT_ALTERED_DURING_COMPARISON, \
                                                    '{trgt_not_altered_during_comparison}'::BOOLEAN AS TRGT_NOT_ALTERED_DURING_COMPARISON, \
                                                    '{src_last_altered}'::STRING AS SRC_LAST_ALTERED, \
                                                    '{trgt_last_altered}'::STRING AS TRGT_LAST_ALTERED, \
                                                    '{date_utc}' \
                                                FROM {result_table} RESULTS, group_error_src, group_error_trgt, src_error, trgt_error, src_sample_error, trgt_sample_error \
                                                WHERE RUN_GUID = '{run_guid}'\
                                    ;"

            self.execute_statement(insert_statement)

    def insert_columnlevel_results(
        self,
        result_table: str,
        result_table_columnlevel: str,
        run_guid: str,
    ) -> None:
        """
        insert into - detailed results per column
        """

        date_utc = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")

        statement = f"CREATE TABLE IF NOT EXISTS {result_table_columnlevel} (RUN_GUID STRING, PIPELINE_ID STRING, START_TIME_UTC STRING, SRC_DATABASE_NAME STRING, SRC_SCHEMA_NAME STRING, SRC_OBJECT_NAME STRING, SRC_OBJECT_TYPE STRING, TRGT_DATABASE_NAME STRING, TRGT_SCHEMA_NAME STRING, TRGT_OBJECT_NAME STRING, TRGT_OBJECT_TYPE STRING, COLUMN_NAME STRING, IN_SRC BOOLEAN, IN_TRGT BOOLEAN, IN_SYNC BOOLEAN, IN_EXCLUDED BOOLEAN, SRC_DATATYPE STRING, TRGT_DATATYPE STRING, AGGREGATION_TYPE STRING, AGGREGATION_EQUAL BOOLEAN, AGGREGATION_RESULT_SRC STRING, AGGREGATION_RESULT_TRGT STRING, AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC STRING, COUNT_NULLS_EQUAL BOOLEAN, COUNT_NULLS_SRC STRING, COUNT_NULLS_TRGT STRING, COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC STRING, ERROR_QUERY_SRC STRING, ERROR_MSG_SRC STRING, ERROR_QUERY_TRGT STRING, ERROR_MSG_TRGT STRING, ERROR_FLAG BOOLEAN, CREATION_TS_UTC STRING);"

        self.execute_statement(statement)

        dict_list = self.get_objects_in_result_column(result_table, run_guid)

        # extract the information needed for the table on object level
        for element in dict_list:
            elem = element
            help_str, elem = elem.split(",", 1)
            src_database_name = re.sub(
                r"(.*)\"SRC_DATABASE_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_schema_name = re.sub(
                r"(.*)\"SRC_SCHEMA_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_object_name = re.sub(
                r"(.*)\"SRC_OBJECT_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_object_type = re.sub(
                r"(.*)\"SRC_OBJECT_TYPE\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_database_name = re.sub(
                r"(.*)\"TRGT_DATABASE_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_schema_name = re.sub(
                r"(.*)\"TRGT_SCHEMA_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_object_name = re.sub(
                r"(.*)\"TRGT_OBJECT_NAME\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_object_type = re.sub(
                r"(.*)\"TRGT_OBJECT_TYPE\":\s\"(.*)\"", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            src_filter = re.sub(
                r"(.*)\"SRC_FILTER\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(",", 1)
            trgt_filter = re.sub(
                r"(.*)\"TRGT_FILTER\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("],", 1)
            help_str = help_str + "]" # EXCLUDED_COLUMNS not needed for column level table
            help_str, elem = elem.split(",", 1) # COLUMNS_EQUAL not needed for column level table
            help_str, elem = elem.split("],", 1) # COLUMN_INTERSECTION not needed for column level table
            help_str, elem = elem.split("],", 1) # SRC_COLUMNS_MINUS_TRGT_COLUMNS not needed for column level table
            help_str = help_str + "]" # SRC_COLUMNS_MINUS_TRGT_COLUMNS not needed for column level table
            help_str, elem = elem.split("],", 1) # TRGT_COLUMNS_MINUS_SRC_COLUMNS not needed for column level table
            help_str, elem = elem.split(",", 1) # ROW_COUNTS_EQUAL not needed for column level table
            help_str, elem = elem.split(",", 1) # SRC_ROW_COUNT not needed for column level table
            help_str, elem = elem.split(",", 1) # TRGT_ROW_COUNT not needed for column level table
            help_str, elem = elem.split(",", 1) # ALL_COUNT_NULLS_EQUAL not needed for column level table
            help_str, elem = elem.split(",", 1) # AGGREGATIONS_EQUAL not needed for column level table
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            src_error = re.sub(
                r"(.*)\"SRC_ERROR\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split("},", 1)
            help_str = help_str + "}"
            trgt_error = re.sub(
                r"(.*)\"TRGT_ERROR\":\s(.*)", r"\2", help_str
            )
            help_str, elem = elem.split(', "SRC_GROUP_BY_QUERY', 1) # GROUP_BY_COLUMNS not needed for column level table
            elem = '"SRC_GROUP_BY_QUERY' + elem
            help_str, elem = elem.split(",", 1) # SRC_GROUP_BY_QUERY not needed for column level table
            help_str, elem = elem.split(",", 1) # TRGT_GROUP_BY_QUERY not needed for column level table
            help_str, elem = elem.split(",", 1) # GROUP_BY_EQUAL not needed for column level table
            help_str, elem = elem.split(', "COLUMNS_WITH_MISMATCH', 1) # GROUP_BY_VALUES_WITH_MISMATCHES not needed for column level table
            elem = '"COLUMNS_WITH_MISMATCH' + elem
            help_str, elem = elem.split(', "SRC_GROUP_BY_ERROR', 1) # COLUMNS_WITH_MISMATCH not needed for column level table
            elem = '"SRC_GROUP_BY_ERROR' + elem
            help_str, elem = elem.split(', "TRGT_GROUP_BY_ERROR', 1) # SRC_GROUP_BY_ERROR not needed for column level table
            elem = '"TRGT_GROUP_BY_ERROR' + elem
            help_str, elem = elem.split(', "SAMPLES_COMPARED', 1) # TRGT_GROUP_BY_ERROR not needed for column level table
            elem = '"SAMPLES_COMPARED' + elem
            help_str, elem = elem.split(",", 1) # SAMPLES_COMPARED not needed for column level table
            help_str, elem = elem.split(",", 1) # SAMPLES_EQUAL not needed for column level table
            help_str, elem = elem.split("},", 1) # SAMPLE_KEYS not needed for column level table
            help_str, elem = elem.split("}},", 1) # SRC_SAMPLE not needed for column level table
            help_str, elem = elem.split("}},", 1) # TRGT_SAMPLE not needed for column level table
            help_str, elem = elem.split(';",', 1) # SRC_SAMPLE_QUERY not needed for column level table
            help_str, elem = elem.split(';",', 1) # TRGT_SAMPLE_QUERY not needed for column level table
            help_str, elem = elem.split("},", 1) # SRC_SAMPLE_ERROR_DICT not needed for column level table
            help_str, elem = elem.split("},", 1) # TRGT_SAMPLE_ERROR_DICT not needed for column level table
            help_str, elem = elem.split(",", 1) # PANDAS_DATAFRAME_COMPARED not needed for column level table
            help_str, elem = elem.split(",", 1) # PANDAS_DATAFRAME_EQUAL not needed for column level table
            help_str, elem = elem.split(",", 1) # SRC_NOT_ALTERED_DURING_COMPARISON not needed for column level table
            help_str, elem = elem.split(",", 1) # TRGT_NOT_ALTERED_DURING_COMPARISON not needed for column level table
            help_str, elem = elem.split(",", 1) # SRC_LAST_ALTERED not needed for column level table
            help_str, elem = elem.split(",", 1) # TRGT_LAST_ALTERED not needed for column level table
            help_str, elem = elem.split("],", 1) # ALL_COLUMNS not needed for column level table
            help_str, elem = elem.split("}]}", 1)
            help_str = help_str + "}]"
            columns_liststr = re.search(r'(.*)"COLUMNS":\s\[(.*)\]', help_str).group(2)
            columns_dictlist = columns_liststr.split("}")
            columns_dictlist = [
                dictionary + "}"
                for dictionary in columns_dictlist
                if len(dictionary) > 0
            ]

            # extract the information needed for the table on column level
            for column in columns_dictlist:
                col = re.sub(r"^,", "", column)
                help_str, col = col.split(",", 1)
                column_name = re.sub(r"(.*)\"COLUMN_NAME\":\s\"(.*)\"", r"\2", help_str)
                help_str, col = col.split(",", 1)
                in_src = re.sub(r"(.*)\"IN_SRC\":\s(.*)", r"\2", help_str)
                help_str, col = col.split(",", 1)
                in_trgt = re.sub(r"(.*)\"IN_TRGT\":\s(.*)", r"\2", help_str)
                help_str, col = col.split(",", 1)
                in_sync = re.sub(r"(.*)\"IN_SYNC\":\s(.*)", r"\2", help_str)
                help_str, col = col.split(",", 1)
                in_excluded = re.sub(r"(.*)\"IN_EXCLUDED\":\s(.*)", r"\2", help_str)
                help_str, col = col.split(",", 1)
                if help_str == ' "SRC_DATATYPE": None':
                    src_datatype = "None"
                else:
                    src_datatype = re.sub(
                        r"(.*)\"SRC_DATATYPE\":\s\"(.*)\"", r"\2", help_str
                    )
                help_str, col = col.split(",", 1)
                if help_str == ' "TRGT_DATATYPE": None':
                    trgt_datatype = "None"
                else:
                    trgt_datatype = re.sub(
                        r"(.*)\"TRGT_DATATYPE\":\s\"(.*)\"", r"\2", help_str
                    )
                help_str, col = col.split(",", 1)
                if help_str == ' "AGGREGATION_TYPE": None':
                    aggregation_type = "None"
                else:
                    aggregation_type = re.sub(
                        r"(.*)\"AGGREGATION_TYPE\":\s\"(.*)\"", r"\2", help_str
                    )
                help_str, col = col.split(",", 1)
                aggregation_equal = re.sub(
                    r"(.*)\"AGGREGATION_EQUAL\":\s(.*)", r"\2", help_str
                )
                help_str, col = col.split(",", 1)
                aggregation_result_src = re.sub(
                    r"(.*)\"AGGREGATION_RESULT_SRC\":\s(.*)", r"\2", help_str
                )
                help_str, col = col.split(",", 1)
                aggregation_result_trgt = re.sub(
                    r"(.*)\"AGGREGATION_RESULT_TRGT\":\s(.*)", r"\2", help_str
                )
                help_str, col = col.split(",", 1)
                if help_str == ' "AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC": None':
                    aggregation_difference_trgt_minus_src = "None"
                else:
                    aggregation_difference_trgt_minus_src = re.sub(
                        r"(.*)\"AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC\":\s\"(.*)\"",
                        r"\2",
                        help_str,
                    )
                help_str, col = col.split(",", 1)
                count_nulls_equal = re.sub(
                    r"(.*)\"COUNT_NULLS_EQUAL\":\s(.*)", r"\2", help_str
                )
                help_str, col = col.split(",", 1)
                count_nulls_src = re.sub(
                    r"(.*)\"COUNT_NULLS_SRC\":\s(.*)", r"\2", help_str
                )
                help_str, col = col.split(",", 1)
                count_nulls_trgt = re.sub(
                    r"(.*)\"COUNT_NULLS_TRGT\":\s(.*)", r"\2", help_str
                )
                if col == ' "COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC": None}':
                    count_nulls_difference_trgt_minus_src = "None"
                else:
                    count_nulls_difference_trgt_minus_src = re.sub(
                        r"(.*)\"COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC\":\s\"(.*)\"\}",
                        r"\2",
                        col,
                    )

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
                                                                        IN_EXCLUDED, \
                                                                        SRC_DATATYPE,\
                                                                        TRGT_DATATYPE,\
                                                                        AGGREGATION_TYPE,\
                                                                        AGGREGATION_EQUAL,\
                                                                        AGGREGATION_RESULT_SRC,\
                                                                        AGGREGATION_RESULT_TRGT,\
                                                                        AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC,\
                                                                        COUNT_NULLS_EQUAL,\
                                                                        COUNT_NULLS_SRC,\
                                                                        COUNT_NULLS_TRGT,\
                                                                        COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC,\
                                                                        ERROR_QUERY_SRC ,\
                                                                        ERROR_MSG_SRC ,\
                                                                        ERROR_QUERY_TRGT ,\
                                                                        ERROR_MSG_TRGT ,\
                                                                        ERROR_FLAG,\
                                                                        CREATION_TS_UTC)\
                                                                    WITH errors_src AS (SELECT\
                                                                        json_tuple('{src_error}', 'QUERY', 'ERROR') AS (ERROR_QUERY_SRC, ERROR_MSG_SRC)\
                                                                    ),\
                                                                    errors_trgt AS (SELECT\
                                                                        json_tuple('{trgt_error}', 'QUERY', 'ERROR') AS (ERROR_QUERY_TRGT, ERROR_MSG_TRGT)\
                                                                    )\
                                                                    SELECT\
                                                                        RESULTS.RUN_GUID AS RUN_GUID,\
                                                                        RESULTS.PIPELINE_ID AS PIPELINE_ID,\
                                                                        RESULTS.START_TIME_UTC::STRING AS START_TIME_UTC,\
                                                                        '{src_database_name}' AS SRC_DATABASE_NAME,\
                                                                        '{src_schema_name}' AS SRC_SCHEMA_NAME,\
                                                                        '{src_object_name}' AS SRC_OBJECT_NAME,\
                                                                        '{src_object_type}' AS SRC_OBJECT_TYPE,\
                                                                        '{trgt_database_name}' AS TRGT_DATABASE_NAME,\
                                                                        '{trgt_schema_name}' AS TRGT_SCHEMA_NAME,\
                                                                        '{trgt_object_name}' AS TRGT_OBJECT_NAME,\
                                                                        '{trgt_object_type}' AS TRGT_OBJECT_TYPE,\
                                                                        '{column_name}' AS COLUMN_NAME,\
                                                                        '{in_src}'::BOOLEAN AS IN_SRC,\
                                                                        '{in_trgt}'::BOOLEAN AS IN_TRGT,\
                                                                        '{in_sync}'::BOOLEAN AS IN_SYNC,\
                                                                        '{in_excluded}'::BOOLEAN AS IN_SYNC,\
                                                                        '{src_datatype}' AS SRC_DATATYPE,\
                                                                        '{trgt_datatype}' AS TRGT_DATATYPE,\
                                                                        '{aggregation_type}' AS AGGREGATION_TYPE,\
                                                                        '{aggregation_equal}'::BOOLEAN AS AGGREGATION_EQUAL,\
                                                                        '{aggregation_result_src}' AS AGGREGATION_RESULT_SRC,\
                                                                        '{aggregation_result_trgt}' AS AGGREGATION_RESULT_TRGT,\
                                                                        '{aggregation_difference_trgt_minus_src}' AS AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC,\
                                                                        '{count_nulls_equal}'::BOOLEAN AS COUNT_NULLS_EQUAL,\
                                                                        '{count_nulls_src}'::INT AS COUNT_NULLS_SRC,\
                                                                        '{count_nulls_trgt}'::INT AS COUNT_NULLS_TRGT,\
                                                                        '{count_nulls_difference_trgt_minus_src}' AS COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC,\
                                                                        ERROR_QUERY_SRC,\
                                                                        ERROR_MSG_SRC,\
                                                                        ERROR_QUERY_TRGT,\
                                                                        ERROR_MSG_TRGT,\
                                                                        CASE WHEN ERROR_MSG_SRC IS NULL AND ERROR_MSG_TRGT IS NULL THEN FALSE ELSE TRUE END AS ERROR_FLAG,\
                                                                        '{date_utc}'\
                                                                        FROM {result_table} RESULTS, errors_src, errors_trgt\
                                                                        WHERE RUN_GUID = '{run_guid}';"

                self.execute_statement(insert_statement)

    def get_objects_in_result_column(
        self,
        result_table: str,
        run_guid: str,
    ):
        """
        The results could only be written back as almost dictionary
        (replacing quotes) and a conversion back is not possible since
        they are also used in a different context. Here, we do string
        parsing to extract the list of dictionaries (one for each object
        to compare).
        """

        select_statement = (
            f"SELECT RESULT FROM {result_table} WHERE RUN_GUID = '{run_guid}'"
        )

        results_dict = self.execute_queries(select_statement)[0][0]
        result_string = re.search(
            r'"OBJECTS":(.*)', results_dict, flags=re.DOTALL
        ).group(1)
        result_string = re.sub(
            "}$", "", result_string
        )  # remove } from the outer dictionary, the objects string is in
        result_dictstr = re.sub(r"^\s\[(.*)]$", r"\1", result_string, flags=re.DOTALL)
        dict_list = result_dictstr.split(
            '{"SRC_DATABASE_NAME"'
        )  # cannot split dictionaries at } because there are dicts in the dict
        dict_list = [
            '{"SRC_DATABASE_NAME"' + dictionary
            for dictionary in dict_list
            if len(dictionary) > 0
        ]  # add the string used for splitting
        dict_list = [
            re.sub(r",\s$", "", dictionary) for dictionary in dict_list
        ]  # remove ', ' at the end for those dicts not at the end of the list

        return dict_list
