import pyodbc
import pandas.io.sql
import logging
import pandas as pd

from pathlib import PurePath

from icsDataValidation.core.database_objects import DatabaseObject
from icsDataValidation.utils.logger_util import configure_dev_ops_logger

#########################################################################################
#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger("SQLServer_Service")
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

class SQLServerService:
    def __init__(self, connection_params: dict):
        self.connection_params = connection_params
        self.sqlserver_connection = None
        self.sqlserver_datatype_mapping = {
            "string": ["varchar", "nvarchar", "text", "ntext", "char","nchar"],
            "numeric": ["tinyint","smallint","int","bigint","decimal","numeric","smallmoney","money","float","real"],
            "date_and_time": ["date", "time", "datetime", "datetime2", "smalldatetime", "datetimeoffset", "timestamp"],
            "binary": ["varbinary", "binary"],
            "boolean": ["bit"],
        }

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.sqlserver_connection is not None:
            self.sqlserver_connection.close()

    def __del__(self):
        if self.sqlserver_connection is not None:
            self.sqlserver_connection.close()

    def _connect_to_sqlserver(self):
        sqlserver_connection_string = (
            f"DRIVER={self.connection_params['Driver']};"
            f"SERVER={self.connection_params['Server']};"
            f"PORT={self.connection_params['Port']};"
            f"DATABASE={self.connection_params['Database']};"
            f"UID={self.connection_params['User']};"
            f"PWD={self.connection_params['Password']}"
        )
        self.sqlserver_connection = pyodbc.connect(sqlserver_connection_string)
        return self.sqlserver_connection

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
        return f"SQLServer ERROR: {message}\nFailed statement:\n{statement}"

    @staticmethod
    def _get_in_clause(key_filters: list, numeric_columns: list, numeric_scale: int,
        enclose_column_by_double_quotes: bool = False) -> str:
        """generates in_clause from list ready to expand the where clause, numeric values are rounded

        Args:
            key_filters (list): list of given expected values
            numeric_columns (list): list of all numeric columns
            numeric_scale (int): number of decimal places after rounding

        Returns:
            str: in clause as string
        """
        values = list(key_filters.values())
        in_clause_values = "'"
        for j in range(len(values[0])):
            for value in values:
                in_clause_values += str(value[j]) + "','"
            in_clause_values = in_clause_values[:-2] + ",'"
        in_clause_values = in_clause_values[:-3] + "'"

        in_clause_cols = " AND (("
        for key in key_filters.keys():
            if key in numeric_columns:
                in_clause_cols += f"""cast(ROUND({key.replace("'", "")}, {numeric_scale}) as numeric(38, {numeric_scale}))""" + ","
            else:
                in_clause_cols += key.replace("'", "") + ","
        in_clause_cols = in_clause_cols[:-1] + ")"
        in_clause = in_clause_cols + " in (" + in_clause_values + "))"
        return in_clause

    def _get_column_clause(self, column_list: list, columns_datatype: list, numeric_scale, key_columns,
        enclose_column_by_double_quotes: bool = False) -> dict:
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

            if column in key_columns or column_datatype.lower() not in self.sqlserver_datatype_mapping["date_and_time"]:
                if column_datatype.lower() in self.sqlserver_datatype_mapping["numeric"]:
                    if numeric_scale:
                        column_intersecions_new.append(
                            f"CAST(ROUND({column}, {numeric_scale}) as decimal(38,{numeric_scale})) as {column}"
                        )
                    else:
                        column_intersecions_new.append(f"{column} as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)
                elif column_datatype.lower() in self.sqlserver_datatype_mapping["string"]:
                    column_intersecions_new.append(f"{column} AS {column}")
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
        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        all_database_tables = []
        all_database_views = []

        if object_type_restriction == "include_all" or object_type_restriction == "include_only_tables":
            if schema:
                query_db_tables = f"SELECT SCHEMA_NAME(T.SCHEMA_ID) AS SCHEMA_NAME, T.NAME AS TABLE_NAME FROM SYS.TABLES T WHERE SCHEMA_NAME(T.SCHEMA_ID) = '{schema}' ORDER BY SCHEMA_NAME;"
            else:
                query_db_tables = f"SELECT SCHEMA_NAME(T.SCHEMA_ID) AS SCHEMA_NAME, T.NAME AS TABLE_NAME FROM SYS.TABLES T ORDER BY SCHEMA_NAME;"

            all_database_tables = self.execute_queries(query_db_tables)

        if object_type_restriction == "include_all" or object_type_restriction == "include_only_views":
            if schema:
                query_db_views = f"SELECT SCHEMA_NAME(T.SCHEMA_ID) AS SCHEMA_NAME, T.NAME AS TABLE_NAME FROM SYS.VIEWS T WHERE SCHEMA_NAME(T.SCHEMA_ID) = '{schema}' ORDER BY SCHEMA_NAME;"
            else:
                query_db_views = F"SELECT SCHEMA_NAME(T.SCHEMA_ID) AS SCHEMA_NAME, T.NAME AS TABLE_NAME FROM SYS.VIEWS T ORDER BY SCHEMA_NAME;"

            all_database_views = self.execute_queries(query_db_views)

        database_objects=[]
        for row in all_database_tables:
            database_table=f"{database}.{row['SCHEMA_NAME'].upper()}.{row['TABLE_NAME'].upper()}"
            database_objects.append({"object_identifier": database_table, "object_type": "table"})
        for row in all_database_views:
            database_view=f"{database}.{row['SCHEMA_NAME'].upper()}.{row['TABLE_NAME'].upper()}"
            database_objects.append({"object_identifier": database_view, "object_type": "view"})
        return database_objects

    def get_last_altered_timestamp_from_object(self, object: DatabaseObject) -> str:
        """
        queries last_altered timestamp for given object

        Args:
            object (str): object for comparison

        Returns:
            str: last_altered timestamp
        """
        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        query_get_last_altered = f"SELECT MODIFY_DATE AS LAST_ALTERED FROM SYS.OBJECTS WHERE NAME = '{object.name}' AND SCHEMA_ID = SCHEMA_ID('{object.schema}');"

        last_altered = self.execute_queries(query_get_last_altered)[0]

        return last_altered

    def get_columns_from_object(self, object: DatabaseObject) -> list:
        """
        returns all columns from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            list: list of all columns
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        if object.type == "table":
            query_get_columns = f"""
                                    SELECT
                                        COL.NAME
                                    FROM SYS.TABLES AS TAB
                                        INNER JOIN SYS.COLUMNS AS COL ON (
                                            TAB.OBJECT_ID = COL.OBJECT_ID
                                            AND UPPER(TAB.NAME) = '{object.name.upper()}'
                                            )
                                        INNER JOIN (
                                            SELECT
                                                OBJECT_ID,
                                                SCHEMA_ID
                                            FROM
                                                SYS.OBJECTS
                                            ) AS OBJ ON (
                                                TAB.OBJECT_ID = OBJ.OBJECT_ID
                                                AND SCHEMA_NAME(OBJ.SCHEMA_ID) = '{object.schema.upper()}'
                                            )
                                    ;
                                    """

        if object.type == "view":
            query_get_columns = f"""
                                    SELECT
                                        COL.NAME
                                    FROM SYS.VIEWS AS VW
                                        INNER JOIN SYS.COLUMNS AS COL ON (
                                            VW.OBJECT_ID = COL.OBJECT_ID
                                            AND UPPER(VW.NAME) = '{object.name.upper()}'
                                            )
                                        INNER JOIN (
                                            SELECT
                                                OBJECT_ID,
                                                SCHEMA_ID
                                            FROM
                                                SYS.OBJECTS
                                            ) AS OBJ ON (
                                                VW.OBJECT_ID = OBJ.OBJECT_ID
                                                AND SCHEMA_NAME(OBJ.SCHEMA_ID) = '{object.schema.upper()}'
                                            )
                                    ;
                                    """

        columns_result = self.execute_queries(query_get_columns)

        columns = [row['NAME'] for row in columns_result]

        return columns

    def get_row_count_from_object(self, object: DatabaseObject, where_clause: str = "") -> int:
        """
        gets row count from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: number of rows in object
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        # TODO is it more efficient to select the information_schema.table view to get the rows?
        query_get_row_count = (
            f"SELECT COUNT(*) AS ROW_COUNT FROM {object.schema}.{object.name} {where_clause};"
        )
        row_count = -1
        error_list = []

        try:
            row_count = self.execute_queries(query_get_row_count)[0]['ROW_COUNT']

        except Exception as err:
            error_list.append(str(err))
            error_list.append(query_get_row_count)

        return row_count, error_list

    def get_data_types_from_object(self, object: DatabaseObject, column_intersections: list) -> dict:
        """
        returns datatypes for all intersection columns in a database object

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns for which the data type is queried

        Returns:
            dict: columns and their datatype
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        column_intersections = str(column_intersections)[1:-1]
        if column_intersections == "":
            column_intersections = "''"

        if object.type == 'table':
            query_get_data_types_from_object = f"""
                                                SELECT
                                                    COL.NAME,
                                                    T.NAME AS DATA_TYPE
                                                FROM
                                                    SYS.TABLES AS TAB
                                                    INNER JOIN SYS.COLUMNS AS COL ON TAB.OBJECT_ID = COL.OBJECT_ID
                                                    LEFT JOIN SYS.TYPES AS T ON COL.USER_TYPE_ID = T.USER_TYPE_ID
                                                WHERE
                                                    TAB.NAME = '{object.name}'
                                                    AND SCHEMA_NAME (TAB.SCHEMA_ID) = '{object.schema}'
                                                AND COL.NAME IN ({column_intersections})
                                                ;
                                                """
        elif object.type == 'view':
            query_get_data_types_from_object = f"""
                                    SELECT
                                        COL.NAME,
                                        T.NAME AS DATA_TYPE
                                    FROM
                                        SYS.VIEWS AS VW
                                        INNER JOIN SYS.COLUMNS AS COL ON VW.OBJECT_ID = COL.OBJECT_ID
                                        LEFT JOIN SYS.TYPES AS T ON COL.USER_TYPE_ID = T.USER_TYPE_ID
                                    WHERE
                                        VW.NAME = '{object.name}'
                                        AND SCHEMA_NAME (VW.SCHEMA_ID) = '{object.schema}'
                                    AND COL.NAME IN ({column_intersections})
                                    ;
                                    """

        data_types_result = self.execute_queries(query_get_data_types_from_object)

        datatypes = [{"COLUMN_NAME":row['NAME'],"DATA_TYPE":row['DATA_TYPE']} for row in data_types_result]

        return datatypes

    def get_count_distincts_from_object(
        self,
        object: DatabaseObject,
        column_intersections: list,
        where_clause: str = "",
        exclude_columns: list = [],
        enclose_column_by_double_quotes: bool = False
    ) -> dict:
        """
        get distinct count for every column in a database object that is in column intersections list

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns that are used for distinct count
            where_clause (str, optional): optional further filter. Defaults to "".
            exclude_columns (list, optional): columns to exclude from distinct count. Defaults to [].

        Returns:
            dict: distinct counts for columns
            error_list: list of failed executions for distinct counts
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        unions = ""

        for column in column_intersections:
            if column not in exclude_columns:
                unions += f"""
                            UNION
                                SELECT
                                    '{column}' AS COLUMN_NAME,
                                      COUNT(DISTINCT {column}) AS COUNT_DISTINCT
                                FROM {object.schema}.{object.name}
                                {where_clause}
                        """

        query_get_count_distincts_from_object = f"{unions[6:]} ORDER BY COUNT_DISTINCT;"
        error_list = []

        try:
            dict_count_distincts = self.execute_queries(query_get_count_distincts_from_object)
        except Exception as err:
            dict_count_distincts = []
            error_list.append(["ERROR", str(err).split("|||")[0], str(err).split("|||")[1]])

        return dict_count_distincts, error_list

    def get_table_size(self, object: DatabaseObject) -> int:
        """
        returns size of given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: size of object
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        query_get_table_size = f"""
                                SELECT
                                    CAST(
                                        SUM(SPC.USED_PAGES * 8) / 1024.00 * 1000000 AS INTEGER
                                    ) AS BYTES
                                FROM
                                    SYS.TABLES TAB
                                    INNER JOIN SYS.INDEXES IND ON TAB.OBJECT_ID = IND.OBJECT_ID
                                    INNER JOIN SYS.PARTITIONS PART ON IND.OBJECT_ID = PART.OBJECT_ID
                                    AND IND.INDEX_ID = PART.INDEX_ID
                                    INNER JOIN SYS.ALLOCATION_UNITS SPC ON PART.PARTITION_ID = SPC.CONTAINER_ID
                                WHERE
                                    SCHEMA_NAME (TAB.SCHEMA_ID) = '{object.schema}'
                                    AND TAB.NAME = '{object.name}'
                                GROUP BY
                                    SCHEMA_NAME (TAB.SCHEMA_ID) + '.' + TAB.NAME
                                ORDER BY
                                    SUM(SPC.USED_PAGES) DESC;
                                """
        size = self.execute_queries(query_get_table_size)[0]['BYTES']

        return size

    def create_checksums(
        self,
        object: DatabaseObject,
        column_intersections: list,
        where_clause: str = "",
        exclude_columns: list = [],
        numeric_scale: int = None,
        enclose_column_by_double_quotes: bool = False,
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

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        column_intersections = [f"{x.upper()}" for x in column_intersections if x not in exclude_columns]

        dict_colummns_datatype = self.get_data_types_from_object(object, column_intersections)

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            column_datatype = next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

            count_nulls += f", SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END) AS COUNTNULLS_{column}"

            if column_datatype.lower() in self.sqlserver_datatype_mapping["numeric"]:
                if numeric_scale:
                    aggregates += (
                        f", CAST(ROUND(SUM({column}), {numeric_scale}) AS DECIMAL(38, {numeric_scale})) AS SUM_{column}"
                    )
                else:
                    aggregates += f", CAST(SUM({column}) AS DECIMAL(38)) AS SUM_{column}"

            elif (
                column_datatype.lower() in self.sqlserver_datatype_mapping["string"]
                or column_datatype.lower() in self.sqlserver_datatype_mapping["date_and_time"]
            ):
                aggregates += f", COUNT(DISTINCT LOWER({column})) AS COUNTDISTINCT_{column}"

            elif column_datatype.lower() in self.sqlserver_datatype_mapping["binary"]:
                aggregates += f", COUNT(DISTINCT LOWER(TRY_CONVERT(VARCHAR,{column}))) AS COUNTDISTINCT_{column}"

            elif column_datatype.lower() in self.sqlserver_datatype_mapping["boolean"]:
                aggregates += f", CONCAT(CONCAT(CONVERT(VARCHAR,COUNT(CASE WHEN {column} = 1 THEN 1 ELSE NULL END)) , '_'),  CONVERT(VARCHAR, COUNT(CASE WHEN {column} = 0 THEN 1 ELSE NULL END))) AS AGGREGATEBOOLEAN_{column}"

            #else: Additional Data Types: image , sql_variant, uniqueidentifier, xml, cursor, table, column_datatype.lower() == 'bit' or

        query_checksums = (
            f"SELECT {aggregates[1:]} FROM {object.schema}.{object.name} {where_clause};"
        )

        query_countnulls = (
            f"SELECT {count_nulls[1:]} FROM {object.schema}.{object.name} {where_clause};"
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
        enclose_column_by_double_quotes: bool = False,
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

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

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
                if column in column_intersections and column not in exclude_columns:
                    group_by_query_columns_string += f"{column} ,"
                    grouping_columns_final.append(column)

            group_by_query_columns_string = group_by_query_columns_string[:-1]

            dict_colummns_datatype = self.get_data_types_from_object(object, aggregation_columns)

            aggregates = ""
            aggregates_min = ""

            for column in aggregation_columns:
                column_datatype = next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

                if column_datatype.lower() in self.sqlserver_datatype_mapping["numeric"]:
                    if numeric_scale:
                        aggregates_min += f", CAST(ROUND(MIN({column}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS MIN_{column}, CAST(ROUND(MAX({column}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS MAX_{column}"
                        aggregates += f", CAST(ROUND(SUM({column}), {numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS SUM_{column}"
                    else:
                        aggregates_min += f", MIN({column}) AS MIN_{column}, MAX({column}) AS MAX_{column}"
                        aggregates += f", SUM({column}) AS SUM_{column}"

                elif not only_numeric and (
                    column_datatype.lower() in self.sqlserver_datatype_mapping["string"]
                    or column_datatype.lower() in self.sqlserver_datatype_mapping["date_and_time"]
                ):
                    aggregates += f", COUNT(DISTINCT LOWER({column})) AS COUNTDISTINCT_{column}"

                elif not only_numeric and column_datatype.lower() in self.sqlserver_datatype_mapping["binary"]:
                    aggregates += f", COUNT(DISTINCT LOWER(TRY_CONVERT(VARCHAR,{column}))) AS COUNTDISTINCT_{column}"

                elif not only_numeric and column_datatype.lower() in self.sqlserver_datatype_mapping["boolean"]:
                    aggregates += f", CONCAT(CONCAT(CONVERT(VARCHAR,COUNT(CASE WHEN {column} = 1 THEN 1 ELSE NULL END)) , '_'),  CONVERT(VARCHAR, COUNT(CASE WHEN {column} = 0 THEN 1 ELSE NULL END))) AS AGGREGATEBOOLEAN_{column}"

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
        enclose_column_by_double_quotes: bool = False,
    ) -> pd.DataFrame:
        """creates pandas dataframes with all data from given object in given columns

        Args:
            object (DatabaseObject): table or view
            intersection_columns_trgt_src (list): columns existing in source and target

        Returns:
            pd.DataFrame: direct result of sql query
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        intersection_columns_trgt_src_ = ", ".join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"SELECT {intersection_columns_trgt_src_} FROM {object.schema}.{object.name} {where_clause};"

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
        enclose_column_by_double_quotes: bool = False,
    ) -> list[dict]:
        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

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
            sample_query = f"""
                            SELECT TOP ({sample_count}) {column_clause}
                                FROM {object.schema}.{object.name}
                                {where_clause}{in_clause}
                                ORDER BY {keys};
                            """
        elif key_intersection != [] and not is_dedicated:
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
            sample_query = f"""
                            SELECT TOP ({sample_count}) {column_clause}
                                FROM {object.schema}.{object.name}
                                {where_clause}{in_clause}
                                ORDER BY {keys};
                            """
        else:
            column_intersections = list(set(column_intersections) - set(exclude_columns))
            column_intersections.sort()
            column_clause, numeric_columns, used_columns = self._get_column_clause(
                column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes
            )
            sample_query = f"""
                            SELECT TOP ({sample_count}) {column_clause}
                            FROM {object.schema}.{object.name}
                            {where_clause}
                            ORDER BY NEWID();
                            """

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

        Raises:
            Exception: Raises exception if single query cannot be executed.

        Returns:
            Union[List[Dict], List[List[Dict]]]: returns results
        """

        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        if query:
            query_list: list[str] = query if isinstance(query, list) else [query]
        else:
            logger.error("Query defined as null - please check input for execute_queries function.")

        results = []

        cursor = self.sqlserver_connection.cursor()

        for single_query in query_list:
            try:
                query_result=cursor.execute(single_query).fetchall()
                columns = [column[0] for column in cursor.description]
                query_result = [dict(zip(columns, row)) for row in query_result]

                if return_as_pdf:
                    query_result = pd.DataFrame(query_result)

                results.append(query_result)
            except Exception as err:
                raise Exception(single_query + "|||" + str(err))

        return results[0] if not isinstance(query, list) else results

    def execute_statement(self, statement: str | list[str]) -> None:
        """
            Executes simple statement against sqlserver
            Schema and Database settings must be set beforehand
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        if self.sqlserver_connection is None:
            self._connect_to_sqlserver()

        statement_list: list[str] = statement if isinstance(statement, list) else [statement]

        try:
            for single_statement in statement_list:
                stripped_statement = single_statement.strip()
                _ = self.sqlserver_connection.execute(stripped_statement)

        except Exception as err:
            raise Exception(self._get_error_message(err, single_statement)) from err
