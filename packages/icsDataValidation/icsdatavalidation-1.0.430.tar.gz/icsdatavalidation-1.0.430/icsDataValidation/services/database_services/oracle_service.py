
import oracledb
oracledb.defaults.fetch_decimals = True
import pandas as pd
import logging

from typing import Union, List, Dict

from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.core.database_objects import DatabaseObject

#########################################################################################
#########################################################################################

logger = logging.getLogger('Oracle_Service')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

class OracleService(object):
    def __init__(self, connection_params: dict):
        self.connection_params =connection_params
        self.oracle_connection = None
        self.oracle_datatype_mapping = {
                                            "string": ['text'],
                                            "numeric": [
                                               'number',
                                               'float',
                                               'long',
                                               'binary_float',
                                               'binary_double',
                                               'numeric',
                                               'decimal',
                                               'int',
                                               'integer',
                                               'smallint',
                                               'real'
                                                ],
                                            "binary": ['binary'],
                                            "boolean": ['boolean'],
                                            "date_and_time":['date','time','datetime','timestamp','year']
        }

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.oracle_connection is not None:
            self.oracle_connection.close()

    #def __del__(self):
    #    if self.oracle_connection is not None:
    #        self.oracle_connection.close()

    def _connect_to_oracle(self):
        # self.oracle_connection = oracledb.connect(**self.connection_params, mode=oracledb.SYSDBA)
        self.oracle_connection = oracledb.connect(**self.connection_params)
        return self.oracle_connection

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
        return f"Oracle ERROR: {message}\nFailed statement:\n{statement}"

    @staticmethod
    def _get_in_clause(key_filters:list, numeric_columns:list, numeric_scale:int,
        enclose_column_by_double_quotes: bool = False) -> str:
        """ generates in_clause from list ready to expand the where clause, numeric values are rounded

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
        in_clause_values = in_clause_values[:-3] + ')'

        in_clause_cols = f" AND (("
        for key in key_filters.keys():
            if key in numeric_columns:
                in_clause_cols += f"""ROUND({key.replace("'", "")}, {numeric_scale})""" + ","
            else:
                in_clause_cols += key.replace("'", "") + ","
        in_clause_cols = in_clause_cols[:-1] + ")"
        in_clause = in_clause_cols + " in ("  + in_clause_values + ")"
        return in_clause

    def _get_column_clause(self, column_list: list, columns_datatype: list,  numeric_scale, key_columns,
        enclose_column_by_double_quotes: bool = False) ->dict :
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
            column_datatype=next(x for x in columns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

            if column in  key_columns or not (column_datatype.lower() in self.oracle_datatype_mapping["date_and_time"]):
                if column_datatype.lower() in  self.oracle_datatype_mapping["numeric"]:
                    if numeric_scale:
                        column_intersecions_new.append(f"CAST(ROUND({column}, {numeric_scale}) as decimal(38,{numeric_scale})) as {column}")
                    else:
                        column_intersecions_new.append(f"{column} as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)
                elif column_datatype.lower() in  self.oracle_datatype_mapping["string"]:
                    column_intersecions_new.append(f'{column} AS {column}')
                    used_columns.append(column)
                else:
                    column_intersecions_new.append(column)
                    used_columns.append(column)

        column_intersections = column_intersecions_new.copy()
        column_clause = str(column_intersections)[1:-1].replace("'", "")
        return column_clause, numeric_columns, used_columns

    def get_database_objects(self, database: str, schema: str=None, object_type_restriction: str='include_all') -> dict:
        if self.oracle_connection is None:
            self._connect_to_oracle()

        all_database_tables=[]
        all_database_views=[]

        if object_type_restriction=='include_all' or object_type_restriction=='include_only_tables':
            if schema:
                query_db_tables=f"SELECT * FROM all_tables WHERE OWNER = '{schema.upper()}'"
            else:
                query_db_tables=f"SELECT * FROM all_tables "

            all_database_tables = self.execute_queries(query_db_tables)


        if object_type_restriction=='include_all' or object_type_restriction=='include_only_views':
            if schema:
                query_db_views=f"SELECT * FROM all_views WHERE OWNER = '{schema.upper()}'"
            else:
                query_db_views=f"SELECT * FROM all_views "

            all_database_views = self.execute_queries(query_db_views)


        database_objects=[]
        for row in all_database_tables:
            table_identifier=f'{database.upper()}.{row["OWNER"]}.{row["TABLE_NAME"]}'
            database_objects.append({"object_identifier": table_identifier, "object_type": "table"})
        for row in all_database_views:
            view_identifier=f'{database.upper()}.{row["OWNER"]}.{row["VIEW_NAME"]}'
            database_objects.append({"object_identifier": view_identifier, "object_type": "view"})
        return database_objects

    def get_last_altered_timestamp_from_object(
            self,
            object: DatabaseObject
        ) -> str:
        """queries last_altered timestamp for given object

        Args:
            object (str): object for comparison

        Returns:
            str: last_altered timestamp
        """
        if self.oracle_connection is None:
            self._connect_to_oracle()

        self.execute_statement("ALTER SESSION SET TIMEZONE = 'Europe/London'")

        query_get_last_altered=f"SELECT LAST_ALTERED FROM {object.database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{object.name}' AND TABLE_SCHEMA = '{object.schema}'"

        last_altered = self.execute_queries(query_get_last_altered)[0]

        return last_altered

    def get_columns_from_object(self, object: DatabaseObject) -> list:
        """returns all columns from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            list: list of all columns
        """
        if self.oracle_connection is None:
            self._connect_to_oracle()

        query_get_columns = f"SELECT COLUMN_NAME FROM SYS.ALL_TAB_COLUMNS  WHERE OWNER = '{object.schema}' AND TABLE_NAME = '{object.name}'"

        all_columns = self.execute_queries(query_get_columns)

        columns=[]

        for row in all_columns:
            columns.append(row["COLUMN_NAME"])

        return columns

    def get_row_count_from_object(self, object: DatabaseObject, where_clause: str="") -> int:
        """ gets row count from given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: number of rows in object
        """

        if self.oracle_connection is None:
            self._connect_to_oracle()

        query_get_row_count = f"SELECT COUNT(*) AS ROW_COUNT FROM {object.schema}.{object.name} {where_clause}"
        row_count = -1
        error_list = []

        try:
            row_count = self.execute_queries(query_get_row_count)[0]["ROW_COUNT"]

        except Exception as err:
            error_list.append(str(err))
            error_list.append(query_get_row_count)

        return row_count, error_list

    def get_data_types_from_object(self, object: DatabaseObject, column_intersections: list) -> dict:
        """ returns datatypes for all intersection columns in a database object

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns for which the data type is queried

        Returns:
            dict: columns and their datatype
        """

        if self.oracle_connection is None:
            self._connect_to_oracle()

        column_intersections = str(column_intersections)[1:-1]
        if column_intersections == '':
            column_intersections = "''"

        query_get_data_types_from_object=f"SELECT COLUMN_NAME , DATA_TYPE   \
                                            FROM sys.all_tab_columns   \
                                            WHERE TABLE_NAME='{object.name.upper()}'  \
                                            AND OWNER = '{object.schema.upper()}'  \
                                            AND COLUMN_NAME IN ({column_intersections})  \
                                            "

        dict_colummns_datatype=self.execute_queries(query_get_data_types_from_object)
        return dict_colummns_datatype

    def get_count_distincts_from_object(self, object: DatabaseObject, column_intersections: list, where_clause: str="", exclude_columns: list=[],
        enclose_column_by_double_quotes: bool = False) -> dict:
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

        if self.oracle_connection is None:
            self._connect_to_oracle()

        unions=""

        for column in column_intersections:
            if column not in exclude_columns:
                unions +=f" UNION SELECT '{column}' AS COLUMN_NAME, COUNT(DISTINCT {column}) AS COUNT_DISTINCT FROM {object.schema}.{object.name} {where_clause}"

        query_get_count_distincts_from_object=f"{unions[6:]} ORDER BY COUNT_DISTINCT"
        error_list = []
        try:
            dict_count_distincts=self.execute_queries(query_get_count_distincts_from_object)

        except Exception as err:
            #raise err
            dict_count_distincts = []
            error_list.append(["ERROR", str(err).split('|||')[0], str(err).split('|||')[1]])


        return dict_count_distincts, error_list

    def get_table_size(self, object: DatabaseObject) -> int:
        """ returns size of given object

        Args:
            object (DatabaseObject): table or view

        Returns:
            int: size of object
        """

        if self.oracle_connection is None:
            self._connect_to_oracle()

        query_get_table_size = f"SELECT SEGMENT_NAME,SUM(BYTES) BYTES FROM DBA_SEGMENTS WHERE OWNER = '{object.schema.upper()}' AND SEGMENT_TYPE='TABLE' AND SEGMENT_NAME='{object.name.upper()}' GROUP BY SEGMENT_NAME"

        query_result=self.execute_queries(query_get_table_size)

        if query_result:
            size = query_result[0]["BYTES"]
        else:
            size = 0

        return size

    def create_checksums(self, object: DatabaseObject , column_intersections: list, where_clause: str="", exclude_columns:list=[], numeric_scale: int = None,
            enclose_column_by_double_quotes: bool = False) -> List[Dict]:
        """ creates checksums for given object in compliance with given conditions

        Args:
            object (DatabaseObject): table or view
            column_intersections (list): columns that are used for checksums
            where_clause (str, optional): Optional filter criteria given as sql-usable string. Defaults to "".
            exclude_columns (list, optional): columns to exlude from calculation. Defaults to [].
            numeric_scale (int, optional): number of decimal places for aggregations. Defaults to None.

        Returns:
            List[Dict]: checksums for columns of object
        """

        if self.oracle_connection is None:
            self._connect_to_oracle()

        column_intersections= [f"{x.upper()}" for x in column_intersections if x not in exclude_columns]

        dict_colummns_datatype=self.get_data_types_from_object(object, column_intersections)

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

            count_nulls += f", SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END) AS COUNTNULLS_{column}"

            if column_datatype.lower() in  self.oracle_datatype_mapping["numeric"]:

                if numeric_scale:
                    aggregates += f", CAST(ROUND(SUM({column}), {numeric_scale}) AS DECIMAL(38, {numeric_scale})) AS sum_{column}"
                else:
                    aggregates += f", CAST(SUM({column}) AS DECIMAL(38)) AS sum_{column}"

            elif 'char' in column_datatype.lower() or 'raw' in column_datatype.lower():

                aggregates += f", COUNT(DISTINCT LOWER({column})) AS countdistinct_{column}"

            elif column_datatype.lower() == 'date' or 'timestamp' in  column_datatype.lower() or 'interval' in  column_datatype.lower():

                aggregates += f", COUNT(DISTINCT {column}) AS countdistinct_{column}"
            #else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

        query_checksums = f"SELECT {aggregates[1:]} FROM {object.schema}.{object.name} {where_clause}"

        query_countnulls = f"SELECT {count_nulls[1:]} FROM {object.schema}.{object.name} {where_clause}"

        error_list = []
        test_list=[]
        aggregation_results={}

        try:
            checksums_results = self.execute_queries([query_checksums,query_countnulls])

            aggregation_results=checksums_results[0][0]

            countnulls_results=checksums_results[1][0]

            for i in range(0,len(aggregation_results)):

                if list(aggregation_results.values())[i] is None:
                    agg_result = 0
                else:
                    agg_result = list(aggregation_results.values())[i]

                if list(countnulls_results.values())[i] is None:
                    cnt_result = 0
                else:
                    cnt_result = list(countnulls_results.values())[i]


                test_list.append([[item.split("_", 1)[0] for item in list(aggregation_results.keys())][i],agg_result,cnt_result])

        except Exception as err:
            error_list.append(["ERROR", str(err).split('|||')[0], str(err).split('|||')[1]])

        checksums = dict(zip([item.split("_", 1)[1] for item in aggregation_results.keys()] , test_list))
        checksums['TESTATM_ERRORS'] = error_list

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

        if self.oracle_connection is None:
            self._connect_to_oracle()

        if group_by_aggregation_columns == ["all"]:
            aggregation_columns= [f"{column.upper()}" for column in column_intersections if (column not in group_by_columns and column not in exclude_columns)]
        else:
            aggregation_columns= [f"{column.upper()}" for column in column_intersections if (column in group_by_aggregation_columns and column not in exclude_columns)]

        group_by_query_columns_string = " "
        grouping_columns_final = []
        error_dict = {}

        try:
            for column in group_by_columns:
                if column in column_intersections and column not in exclude_columns:
                    group_by_query_columns_string += f"{column} ,"
                    grouping_columns_final.append(column)

            group_by_query_columns_string = group_by_query_columns_string[:-1]

            dict_colummns_datatype=self.get_data_types_from_object(object, aggregation_columns)

            aggregates = ""
            aggregates_min = ""

            for column in aggregation_columns:

                column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]

                if column_datatype.lower() in  self.oracle_datatype_mapping["numeric"]:
                    if numeric_scale:
                        aggregates_min += f", CAST(ROUND(MIN({column}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS MIN_{column}, CAST(ROUND(max({column}),{numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS MAX_{column}"
                        aggregates += f", CAST(ROUND(SUM({column}), {numeric_scale}) AS DECIMAL(38,{numeric_scale})) AS SUM_{column}"
                    else:
                        aggregates_min += f", MIN({column}) AS MIN_{column}, MAX({column}) AS MAX_{column}"
                        aggregates += f", SUM({column}) AS SUM_{column}"

                elif 'char' in column_datatype.lower() or 'raw' in  column_datatype.lower():

                    aggregates += f", COUNT(DISTINCT LOWER({column})) AS COUNTDISTINCT_{column}"

                elif column_datatype.lower() == 'date' or 'timestamp' in  column_datatype.lower() or 'interval' in  column_datatype.lower():

                    aggregates += f", COUNT(DISTINCT {column}) AS COUNTDISTINCT_{column}"
                #else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

            # CASE 1: min_max
            if group_by_aggregation_type == "only_min_max":
                group_by_query_aggregation_string = aggregates_min[1:]

            # CASE 2: sum, count_distinct, aggregate_boolean
            elif group_by_aggregation_type == "various":
                group_by_query_aggregation_string = aggregates[1:]

            # CASE 3: sum, count_distinct, aggregate_boolean, min_max
            elif group_by_aggregation_type == "various_and_min_max":
                group_by_query_aggregation_string = f"{aggregates_min[1:]}{aggregates}"

            query_group_by_aggregation = f"SELECT {group_by_query_columns_string}, COUNT(*) AS COUNT_OF_GROUP_BY_VALUE, {group_by_query_aggregation_string} FROM {object.schema}.{object.name} {where_clause} GROUP BY {group_by_query_columns_string} ORDER BY {group_by_query_columns_string}"

            group_by_aggregation_pdf = self.execute_queries(query_group_by_aggregation,True)
        except Exception as err:
            group_by_aggregation_pdf = pd.DataFrame()
            group_by_aggregation_pdf["TESTATM_ERROR"] = [1]
            if not grouping_columns_final:
                error_dict = {
                    "QUERY": "NO Group-BY Columns found in the Columns Intersection. Please check if the configurated Group-By Columns exist in the Table",
                    "ERROR":  "NO Group-BY Columns found in the Columns Intersection. Please check if the configurated Group-By Columns exist in the Table"
                }
                group_by_query_aggregation_string = ""
            elif '|||' in str(err):
                error_dict = {
                    "QUERY": str(err).split('|||')[0],
                    "ERROR":  str(err).split('|||')[1]
                }
            else:
                error_dict = {
                    "QUERY": "NO Query generated. Please check if the configurated Grouping Columns exist in the Table",
                    "ERROR":  str(err)
                }
                group_by_query_aggregation_string = ""

        return group_by_aggregation_pdf, group_by_query_aggregation_string, group_by_query_columns_string, grouping_columns_final, error_dict

    def create_pandas_df(self, object: DatabaseObject, intersection_columns_trgt_src: list, where_clause:str="", exclude_columns:list=[],
        enclose_column_by_double_quotes: bool = False) -> pd.DataFrame:
        """ creates pandas dataframes with all data from given object in given columns

        Args:
            object (DatabaseObject): table or view
            intersection_columns_trgt_src (list): columns existing in source and target

        Returns:
            pd.DataFrame: direct result of sql query
        """

        if self.oracle_connection is None:
            self._connect_to_oracle()

        intersection_columns_trgt_src_ = ', '.join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"SELECT {intersection_columns_trgt_src_} FROM {object.schema}.{object.name} {where_clause}"

        src_pdf = self.execute_queries(df_query,True)

        return src_pdf

    def create_pandas_df_from_sample(self, object: DatabaseObject, column_intersections: list, key_columns: list, where_clause:str="", exclude_columns:list=[], key_filters: dict={}, dedicated_columns: list=[], sample_count :int=10, numeric_scale: int = None, enclose_column_by_double_quotes: bool = False) -> List[Dict]:

        if self.oracle_connection is None:
            self._connect_to_oracle()

        sample_count = str(sample_count)
        key_intersection = list((set(column_intersections) & set(key_columns)) - set(exclude_columns))
        filter_intersection = list((set(column_intersections) & set(key_filters.keys())) - set(exclude_columns))
        dedicated_intersection = list((set(column_intersections) & set(dedicated_columns)) - set(exclude_columns))

        key_intersection.sort()
        filter_intersection.sort()
        dedicated_intersection.sort()

        if not where_clause:
            where_clause= 'WHERE 1=1 '

        if dedicated_intersection != []:
            is_dedicated = True

            dict_colummns_datatype=self.get_data_types_from_object(object, dedicated_intersection)

        else:
            is_dedicated = False

            dict_colummns_datatype=self.get_data_types_from_object(object, column_intersections)


        if key_intersection != [] and is_dedicated:
            keys = str(key_intersection)[1:-1].replace("'", "")
            column_clause, numeric_columns, used_columns = self._get_column_clause(dedicated_intersection, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes)
            if (key_filters != {}) & (filter_intersection != []):
                values = list(key_filters.values())
                if values[0] != []:
                    in_clause = self._get_in_clause(key_filters, numeric_columns, numeric_scale, enclose_column_by_double_quotes)
                else:
                    in_clause = ""
            else:
                in_clause = ""
            sample_query = f"SELECT {column_clause} FROM (SELECT * FROM {object.schema}.{object.name} ORDER BY DBMS_RANDOM.VALUE) {where_clause} AND rownum <= {sample_count} {in_clause} ORDER BY {keys}"
        elif key_intersection != [] and not is_dedicated:
            keys = str(key_intersection)[1:-1].replace("'", "")
            column_clause, numeric_columns, used_columns = self._get_column_clause(column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes)
            if (key_filters != {}) & (filter_intersection != []):
                values = list(key_filters.values())
                if values[0] != []:
                    in_clause = self._get_in_clause(key_filters, numeric_columns, numeric_scale, enclose_column_by_double_quotes)
                else:
                    in_clause = ""
            else:
                in_clause = ""
            sample_query = f"SELECT {column_clause} FROM (SELECT * FROM {object.schema}.{object.name} ORDER BY DBMS_RANDOM.VALUE) {where_clause} AND rownum <= {sample_count} {in_clause} ORDER BY {keys}"
        else:
            column_intersections = list(set(column_intersections)  - set(exclude_columns))
            column_intersections.sort()
            column_clause, numeric_columns, used_columns = self._get_column_clause(column_intersections, dict_colummns_datatype, numeric_scale, key_columns,
                enclose_column_by_double_quotes)
            sample_query = f"SELECT {column_clause} FROM (SELECT * FROM {object.schema}.{object.name} ORDER BY DBMS_RANDOM.VALUE) {where_clause} AND rownum <= {sample_count}"

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
            if '|||' in str(err):
                error_dict = {
                    "QUERY": str(err).split('|||')[0],
                    "ERROR":  str(err).split('|||')[1]
                }
            else:
                error_dict = {
                    "QUERY": 'No SQL Error',
                    "ERROR":  str(err)
                }

        return_list = []
        return_list.append(sample_pdf)
        return_list.append(error_dict)


        return return_list , key_dict, used_columns, sample_query

    def execute_queries(self, query: Union[str, List[str]],return_as_pdf:bool=False, return_query_ids:bool=False)  -> Union[List[Dict], List[List[Dict]]]:
        """ actual execution of defined queries

        Args:
            query (Union[str, List[str]]): queries to be executed
            return_as_pdf (bool, optional): If true, queries returned as pandas data frames. Defaults to False.
            return_query_ids (bool, optional): If true, results and queri ids are returned, otherwise only results. Defaults to False.

        Raises:
            Exception: Raises exception if single query cannot be executed.

        Returns:
            Union[List[Dict], List[List[Dict]]]: returns results or results with query-ids
        """

        if self.oracle_connection is None:
            self._connect_to_oracle()

        if query:
            query_list: List[str] = query if isinstance(query, list) else [query]
        else:
            logger.error('Query defined as null - please check input for execute_queries function.')

        cursor = self.oracle_connection.cursor()

        results = []

        for single_query in query_list:
            try:
                if return_as_pdf:

                        query_list=cursor.execute(single_query).fetchall()
                        columns = [col[0] for col in cursor.description]
                        query_result = pd.DataFrame(query_list, columns = columns)
                else:
                    cursor.execute(single_query)
                    columns = [col[0] for col in cursor.description]
                    cursor.rowfactory = lambda *args: dict(zip(columns, args))
                    query_result = cursor.fetchall()

            except Exception as err:
                raise Exception(single_query + "|||" + str(err))

            results.append(query_result)

        return results[0] if not isinstance(query, list) else results

    def execute_statement(self, statement: Union[str, List[str]]) -> None:
        """
            Executes simple statement against oracle
            Schema and Database settings must be set beforehand
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        if self.oracle_connection is None:
            self._connect_to_oracle()

        statement_list: List[str] = (
            statement if isinstance(statement, list) else [statement]
        )

        try:
            for single_statement in statement_list:
                stripped_statement = (
                    single_statement.strip()
                )
                _ = self.oracle_connection.execute_string(stripped_statement)

        except Exception as err:
            raise Exception(self._get_error_message(err, single_statement)) from err
