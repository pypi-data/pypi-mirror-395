import teradatasql
import pandas as pd
import logging

from typing import Union, List, Dict

from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.core.database_objects import DatabaseObject
#########################################################################################
#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger('Teradata_Service')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)


class TeradataService(object):
    def __init__(self, connection_params: dict):
        self.connection_params =connection_params
        self.teradata_connection = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.teradata_connection is not None:
            self.teradata_connection.close()

    # def __del__(self):
    #     if self.teradata_connection is not None:
    #         self.teradata_connection.close()

    def _connect_to_teradata(self):
        self.teradata_connection = teradatasql.connect(host=self.connection_params['host'], user=self.connection_params['user'], password=self.connection_params['password'], dbs_port=self.connection_params['dbs_port'])
        return self.teradata_connection

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
        return f"Teradata ERROR: {message}\nFailed statement:\n{statement}"

    def get_database_objects(self, database: str, schema: str=None, object_type_restriction: str='include_all') -> dict:
        if self.teradata_connection is None:
            self._connect_to_teradata()

        all_database_tables=[]
        all_database_views=[]
        if object_type_restriction=='include_all' or object_type_restriction=='include_only_tables':
            if schema:
                query_db_tables=f"SELECT DataBaseName as schema_name, TableName as table_name FROM dbc.TablesV WHERE TableKind in ('O', 'T') and DatabaseName = '{object.schema}';"
            else:
                query_db_tables=f"SELECT DataBaseName as schema_name, TableName as table_name FROM dbc.TablesV WHERE TableKind in ('O', 'T');"

            all_database_tables = self.execute_queries(query_db_tables)

        elif object_type_restriction=='include_all' or object_type_restriction=='include_only_views':
            if schema:
                query_db_views=f"SELECT DataBaseName as schema_name, TableName as table_name FROM dbc.TablesV WHERE TableKind in ('V') and DatabaseName = '{object.schema}';"
            else:
                query_db_views=f"SELECT DataBaseName as schema_name, TableName as table_name FROM dbc.TablesV WHERE TableKind in ('V');"

            all_database_views = self.execute_queries(query_db_views)

        database_objects=[]
        for row in all_database_tables:
            table_identifier=f'{database}.{row[0].upper()}.{row[1].upper()}'
            database_objects.append({"object_identifier": table_identifier, "object_type": "table"})
        for row in all_database_views:
            view_identifier=f'{database}.{row[0].upper()}.{row[1].upper()}'
            database_objects.append({"object_identifier": view_identifier, "object_type": "view"})
        return database_objects

    def get_columns_from_object(self, object : DatabaseObject) -> list:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        queries_get_columns = [f"SELECT ColumnName FROM dbc.COLUMNSV WHERE DatabaseName = '{object.schema}' AND TableName = '{object.name}';"]

        all_columns = self.execute_queries(queries_get_columns)[0]

        columns=[]

        for row in all_columns:
            columns.append(row[0].strip())

        return columns

    def get_row_count_from_object(self, object : DatabaseObject, where_clause: str="") -> int:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        query_get_row_count = f"SELECT COUNT(*) AS ROW_COUNT FROM {object.schema}.{object.name} {where_clause};"
        row_count = -1
        error_list = []

        try:

            row_count = self.execute_queries(query_get_row_count).fetchall()[0][0]

        except Exception as err:
            error_list.append(str(err))
            error_list.append(query_get_row_count)

        return row_count, error_list

    def get_data_types_from_object(self, object : DatabaseObject, column_intersections: list) -> dict:

        results = []

        if self.teradata_connection is None:
            self._connect_to_teradata()


        column_intersections = str(column_intersections)[1:-1]
        if object.type=='table':
            if column_intersections == '':
                column_intersections = "''"
            query_get_data_types_from_table=f"SELECT COLUMNNAME, COLUMNTYPE  FROM DBC.COLUMNSV WHERE DATABASENAME = '{object.schema}' AND TableName = '{object.name}' AND ColumnName IN ({column_intersections});"
            dict_colummns_datatype=self.execute_queries(query_get_data_types_from_table).fetchall()

        elif object.type=='view':
            query_get_data_types_from_table=f"HELP COLUMN {object.schema}.{object.name}.*"   # TODO: hier fehlt der filter auf die column_intersections und das resultat muss auf column_name und type eingeschränkt werden
            dict_colummns_datatype=self.execute_queries(query_get_data_types_from_table).fetchall()

        for row in dict_colummns_datatype:
            # logger.info(type(row))
            row_to_list = [elem.strip() for elem in row]
            results.append({"COLUMN_NAME":row_to_list[0],"DATA_TYPE":row_to_list[1]})

        return results

    def get_count_distincts_from_object(self, object : DatabaseObject, column_intersections: list, where_clause: str="", exclude_columns:list=[],
        enclose_column_by_double_quotes: bool = False) -> dict:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        unions=""
        for column in column_intersections:
            if column not in exclude_columns:
                unions +=f"UNION SELECT CAST('{column}' AS VARCHAR(500)) AS COLUMN_NAME, COUNT(DISTINCT {column}) AS COUNT_DISTINCT FROM {object.schema}.{object.name} {where_clause}"

        query_get_count_distincts_from_object=f"{unions[5:]} ORDER BY 2;"
        error_list = []
        dict_count_distincts = []

        try:
            count_distincts=self.execute_queries(query_get_count_distincts_from_object).fetchall()
            for result in count_distincts:

                single_dict = {
                    'COLUMN_NAME': result[0]
                    , 'COUNT_DISTINCT': result[1]
                }

                dict_count_distincts.append(single_dict)

        except Exception as err:
            #raise err
            error_list.append(["ERROR", str(err).split('|||')[0], str(err).split('|||')[1]])
        return dict_count_distincts, error_list


    def get_table_size(self, object: DatabaseObject) -> int:

        query_get_table_size = f"select SUM(CURRENTPERM) FROM DBC.TABLESIZE WHERE DatabaseName = '{object.schema}' AND tablename = '{object.name}';"

        size = self.execute_queries(query_get_table_size).fetchall()[0][0]

        return size

    def create_checksums(self, object: DatabaseObject, column_intersections: list, where_clause:str="", exclude_columns:list=[],
            enclose_column_by_double_quotes: bool = False) -> List[Dict]:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        # column_intersections= [f"{x.upper()}" for x in column_intersections]

        dict_colummns_datatype=self.get_data_types_from_object(object, column_intersections)

        # dict_colummns_datatype_dict = dict(zip(dict_colummns_datatype[::2], dict_colummns_datatype[1::2]))

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            if column not in exclude_columns:
                column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
                column_datatype = column_datatype.split('(')[0]

                count_nulls += f", sum(case when {column} is null then 1 else 0 end) as countnulls_{column}"

                if column_datatype.lower() == 'i8' or column_datatype.lower() == 'i1' or column_datatype.lower() == 'i' or column_datatype.lower() == 'i2':
                    aggregates += f", sum(cast ({column} as decimal(30,0))) as SUM_{column}"
                elif  column_datatype.lower() == 'bf' or column_datatype.lower() == 'bv' or column_datatype.lower() == 'd' or column_datatype.lower() == 'f' or column_datatype.lower() == 'dy' or column_datatype.lower() == 'dh' or column_datatype.lower() == 'dm' or column_datatype.lower() == 'ds' or column_datatype.lower() == 'hr' or column_datatype.lower() == 'hs' or column_datatype.lower() == 'mi' or column_datatype.lower() == 'ms' or column_datatype.lower() == 'mo' or column_datatype.lower() == 'sc' or column_datatype.lower() == 'yr' or column_datatype.lower() == 'ym' or column_datatype.lower() == 'n' or column_datatype.lower() == 'd' :
                    aggregates += f", sum({column}) as SUM_{column}"
                elif column_datatype.lower() == 'cv' or column_datatype.lower() == 'cf' or column_datatype.lower() == 'co' or column_datatype.lower() == 'da' or column_datatype.lower() == 'pd' or column_datatype.lower() == 'pt' or column_datatype.lower() == 'pz' or column_datatype.lower() == 'pm' or column_datatype.lower() == 'at' or column_datatype.lower() == 'ts' or column_datatype.lower() == 'tz' or column_datatype.lower() == 'sz':
                    aggregates += f", count(distinct {column}) as countdistinct_{column}"
                elif column_datatype.lower() == 'i1' and 1 == 0:
                    aggregates += f", (SELECT CONCAT ((select trim(count(*)) as val FROM {object.schema}.{object.name} WHERE {column} = 1),'_',(select trim(count(*)) as val from {object.schema}.{object.name} WHERE {column} = 0))) AS aggregateboolean_{column}"
                #else: Additional Data Types: ++ TD_ANYTYPE, a1 ARRAY, AN ARRAY , bo BINARY LARGE OBJECT, us USER‑DEFINED TYPE (all types),xm XML

        query_checksums = f"select {aggregates[1:]} from {object.schema}.{object.name} {where_clause};"

        query_countnulls = f"select {count_nulls[1:]} from {object.schema}.{object.name} {where_clause};"

        error_list = []
        test_list=[]
        aggregation_columns = []

        try:

            aggregation_cursor = self.execute_queries(query_checksums)

            aggregation_columns = [column[0].upper() for column in aggregation_cursor.description]

            aggregation_results = aggregation_cursor.fetchall()[0]

            countnulls_cursor = self.execute_queries(query_countnulls)

            countnulls_results = countnulls_cursor.fetchall()[0]

            for i in range(0,len(aggregation_results)):

                if aggregation_results[i] is None:
                    agg_result = 0
                else:
                    agg_result = aggregation_results[i]

                if countnulls_results[i] is None:
                    cnt_result = 0
                else:
                    cnt_result = countnulls_results[i]

                test_list.append([[item.split("_", 1)[0] for item in aggregation_columns][i],agg_result,cnt_result])



        except Exception as err:
            error_list.append(["ERROR", str(err).split('|||')[0], str(err).split('|||')[1]])
        checksums = dict(zip([item.split("_", 1)[1] for item in aggregation_columns] , test_list))
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
            numeric_scale: int=None,
            enclose_column_by_double_quotes: bool = False
        ) -> List[Dict]:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        if group_by_aggregation_columns == ["all"]:
            aggregation_columns= [f"{column.upper()}" for column in column_intersections if (column not in group_by_columns and column not in exclude_columns)]
        else:
            aggregation_columns= [f"{column.upper()}" for column in column_intersections if (column in group_by_aggregation_columns and column not in exclude_columns)]

        dict_colummns_datatype_grouping=self.get_data_types_from_object(object, group_by_columns)

        group_by_query_columns_string = " "
        grouping_columns_final = []
        error_dict = {}
        try:
            for column in group_by_columns:
                column_datatype_grouping=next(x for x in dict_colummns_datatype_grouping if x["COLUMN_NAME"] == column)["DATA_TYPE"]
                column_datatype_grouping = column_datatype_grouping.split('(')[0]
                if column in column_intersections and column not in exclude_columns:

                    if column_datatype_grouping.lower() == 'cv' or column_datatype_grouping.lower() == 'cf' or column_datatype_grouping.lower() == 'co':
                        group_by_query_columns_string += f"TRIM({column}) AS {column} ,"
                    else:
                        group_by_query_columns_string += f"{column} ,"
                    grouping_columns_final.append(column)

            group_by_query_columns_string = group_by_query_columns_string[:-1]

            dict_colummns_datatype=self.get_data_types_from_object(object, aggregation_columns)

            aggregates = ""
            aggregates_min = ""

            for column in aggregation_columns:
                column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
                column_datatype = column_datatype.split('(')[0]

                if column_datatype.lower() == 'i8' or column_datatype.lower() == 'i1' or column_datatype.lower() == 'i' or column_datatype.lower() == 'i2':

                    if not numeric_scale:
                        aggregates += f", sum(cast ({column} as decimal(30,0))) as sum_{column}"
                    else:
                        aggregates += f", CASE WHEN TRIM(TO_CHAR(CAST(ROUND(sum(cast ({column} as decimal(30,0))), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND(sum(cast ({column} as decimal(30,0))), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) ELSE TRIM(TO_CHAR(CAST(ROUND(sum(cast ({column} as decimal(30,0))), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) END as SUM_{column}"
                        aggregates_min += f", CASE WHEN TRIM(TO_CHAR(CAST(ROUND(min({column}), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND(min({column}), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) ELSE TRIM(TO_CHAR(CAST(ROUND(min({column}), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) END as MIN_{column}, CASE WHEN TRIM(TO_CHAR(CAST(ROUND(max({column}), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND(max({column}), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) ELSE TRIM(TO_CHAR(CAST(ROUND(max({column}), {numeric_scale}) as decimal(38,{numeric_scale})), '999999999999999999.{'0'*numeric_scale}')) END as MAX_{column}"

                elif  column_datatype.lower() == 'bf' or column_datatype.lower() == 'bv' or column_datatype.lower() == 'd' or column_datatype.lower() == 'f' or column_datatype.lower() == 'dy' or column_datatype.lower() == 'dh' or column_datatype.lower() == 'dm' or column_datatype.lower() == 'ds' or column_datatype.lower() == 'hr' or column_datatype.lower() == 'hs' or column_datatype.lower() == 'mi' or column_datatype.lower() == 'ms' or column_datatype.lower() == 'mo' or column_datatype.lower() == 'sc' or column_datatype.lower() == 'yr' or column_datatype.lower() == 'ym' or column_datatype.lower() == 'n' or column_datatype.lower() == 'd' :
                    if not numeric_scale:
                        aggregates += f", sum(({column} )) as sum_{column}"

                    if not numeric_scale:
                        aggregates += f", CASE WHEN TRIM(TO_CHAR(CAST(ROUND(sum({column}), 4) as decimal(38,4)), '999999999999999999.0000')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND(sum({column}), 4) as decimal(38,4)), '999999999999999999.0000')) ELSE TRIM(TO_CHAR(CAST(ROUND(sum({column}), 4) as decimal(38,4)), '999999999999999999.0000')) END as SUM_{column}"
                        aggregates_min += f", CASE WHEN TRIM(TO_CHAR(CAST(ROUND(min({column}), 4) as decimal(38,4)), '999999999999999999.0000')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND(min({column}), 4) as decimal(38,4)), '999999999999999999.0000')) ELSE TRIM(TO_CHAR(CAST(ROUND(min({column}), 4) as decimal(38,4)), '999999999999999999.0000')) END as MIN_{column}, CASE WHEN TRIM(TO_CHAR(CAST(ROUND(max({column}), 4) as decimal(38,4)), '999999999999999999.0000')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND(max({column}), 4) as decimal(38,4)), '999999999999999999.0000')) ELSE TRIM(TO_CHAR(CAST(ROUND(max({column}), 4) as decimal(38,4)), '999999999999999999.0000')) END as MAX_{column}"


                elif not only_numeric and ( column_datatype.lower() == 'da' or column_datatype.lower() == 'pd' or column_datatype.lower() == 'pt' or column_datatype.lower() == 'pz' or column_datatype.lower() == 'pm' or column_datatype.lower() == 'at' or column_datatype.lower() == 'ts' or column_datatype.lower() == 'tz' or column_datatype.lower() == 'sz'):

                    aggregates += f", count(distinct {column}) as COUNTDISTINCT_{column}"
                    aggregates_min += f", min({column}) as MIN_{column}, max({column}) as MAX_{column}"

                elif not only_numeric and (column_datatype.lower() == 'cv' or column_datatype.lower() == 'cf' or column_datatype.lower() == 'co'):

                    aggregates += f", count(distinct {column}) as COUNTDISTINCT_{column}"
                    aggregates_min += f", min(TRIM({column})) as MIN_{column}, max(TRIM({column})) as MAX_{column}"

                elif not only_numeric  and column_datatype.lower() == 'i1' and 1 == 0:

                    aggregates += f", (SELECT CONCAT ((select trim(count(*)) as val FROM {object.schema}.{object.name} WHERE {column} = 1),'_',(select trim(count(*)) as val from {object.schema}.{object.name} WHERE {column} = 0))) AS AGGREGATEBOOLEAN_{column}"

                #else: Additional Data Types: ++ TD_ANYTYPE, a1 ARRAY, AN ARRAY , bo BINARY LARGE OBJECT, us USER‑DEFINED TYPE (all types),xm XML

            # CASE 1: min_max
            if group_by_aggregation_type == "only_min_max":
                group_by_query_aggregation_string = aggregates_min

            # CASE 2; sum, count_distinct, aggregate_boolean
            elif group_by_aggregation_type == "various":
                group_by_query_aggregation_string = aggregates

            # CASE 3: sum, count_distinct, aggregate_boolean, min_max
            elif group_by_aggregation_type == "various_and_min_max":
                group_by_query_aggregation_string = f"{aggregates_min[1:]}{aggregates}"

            query_group_by_aggregation = f"select {group_by_query_columns_string}, count(*) as COUNT_OF_GROUP_BY_VALUE {group_by_query_aggregation_string} from {object.schema}.{object.name} {filter} GROUP BY {group_by_query_columns_string} order by {group_by_query_columns_string};"

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

        return group_by_aggregation_pdf, group_by_query_aggregation_string, group_by_query_columns_string, grouping_columns_final, error_dict


    def create_pandas_df(self, object : DatabaseObject, intersection_columns_trgt_src: list, where_clause:str="", exclude_columns:list=[],
        enclose_column_by_double_quotes: bool = False) -> pd.DataFrame:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        intersection_columns_trgt_src_ = ', '.join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"select {intersection_columns_trgt_src_} from {object.schema}.{object.name} {where_clause};"

        src_pdf = self.execute_queries(df_query,True)

        return src_pdf

    def create_pandas_df_from_sample(self, object: DatabaseObject, column_intersections: list,  key_columns: list, where_clause: str="", exclude_columns:list=[], key_filters: dict={}, dedicated_columns: list=[], sample_count :int=10,
        numeric_scale: int = None,
        enclose_column_by_double_quotes: bool = False) -> List[Dict]:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        sample_count = str(sample_count)
        key_intersection = list((set(column_intersections) & set(key_columns)) - set(exclude_columns))
        filter_intersection = list((set(column_intersections) & set(key_filters.keys())) - set(exclude_columns))
        dedicated_intersection = list((set(column_intersections) & set(dedicated_columns)) - set(exclude_columns))

        key_intersection.sort()
        filter_intersection.sort()
        dedicated_intersection.sort()

        if dedicated_intersection != []:
            is_dedicated = True
            dict_colummns_datatype=self.get_data_types_from_object(object, dedicated_intersection)
            # datatype_query = f"""select column_name, data_type, ordinal_position
            #                         from {object.database}.information_schema.columns
            #                         where table_schema = '{object.schema}'
            #                         and table_name = '{object.name}'
            #                         and data_type not like 'TIMESTAMP%'
            #                         and data_type != 'DATE'
            #                         order by ordinal_position
            #                         ;"""
        else:
            is_dedicated = False
            dict_colummns_datatype=self.get_data_types_from_object(object, column_intersections)

        if key_intersection != [] and is_dedicated:
            column_intersecions_new = []
            used_columns = []
            numeric_columns = []
            for column in dedicated_intersection:
                column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
                column_datatype = column_datatype.split('(')[0]

                if column_datatype.lower() == 'i8' or column_datatype.lower() == 'i1' or column_datatype.lower() == 'i' or column_datatype.lower() == 'i2':
                    column_intersecions_new.append(f"CASE WHEN TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00'))  ELSE TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) END  as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)

                elif  column_datatype.lower() == 'bf' or column_datatype.lower() == 'bv' or column_datatype.lower() == 'd' or column_datatype.lower() == 'f' or column_datatype.lower() == 'dy' or column_datatype.lower() == 'dh' or column_datatype.lower() == 'dm' or column_datatype.lower() == 'ds' or column_datatype.lower() == 'hr' or column_datatype.lower() == 'hs' or column_datatype.lower() == 'mi' or column_datatype.lower() == 'ms' or column_datatype.lower() == 'mo' or column_datatype.lower() == 'sc' or column_datatype.lower() == 'yr' or column_datatype.lower() == 'ym' or column_datatype.lower() == 'n' or column_datatype.lower() == 'd' :
                    column_intersecions_new.append(f"CASE WHEN TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) ELSE TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) END  as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)

                elif column_datatype.lower() == 'cv' or column_datatype.lower() == 'cf' or column_datatype.lower() == 'cf':
                    column_intersecions_new.append(f'TRIM({column}) AS {column}')
                    used_columns.append(column)
                else:
                    column_intersecions_new.append(column)
                    used_columns.append(column)

            column_intersections = column_intersecions_new.copy()
            columns = ""
            for column in column_intersections:
                #columns = str(column_intersections)[1:-1].replace("'", "")
                columns += f"{column}, "
            columns = columns[:-2]
            keys = str(key_intersection)[1:-1].replace("'", "")


            ##
            ## Filter from Sample Logic
            if key_filters == {}:
                sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"
            else:
                if filter_intersection != []:
                    values = list(key_filters.values())
                    if values[0] == []:
                        sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"
                    else:
                        where_clause = f'{where_clause} AND (('
                        print(key_filters)
                        for j in range(len(values[0])):
                            for key in key_filters.keys():
                                if key == 'TECH_ID' or key in numeric_columns:
                                    where_clause += f" CAST(ROUND({key}, 2) as decimal(38,2)) = {str(key_filters[key][j])} AND"
                                else:
                                    where_clause += f" {key} = '{str(key_filters[key][j])}' AND"
                            where_clause = f" {where_clause[:-3]}) OR ("
                        where_clause = f"{where_clause[:-4]})"

                        sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"
                else:
                    sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"

        elif key_intersection != [] and not is_dedicated:
            column_intersecions_new = []
            used_columns = []
            numeric_columns = []
            column_intersections = list(set(column_intersections)  - set(exclude_columns))
            column_intersections.sort()
            for column in column_intersections:
                column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
                column_datatype = column_datatype.split('(')[0]

                if column_datatype.lower() == 'i8' or column_datatype.lower() == 'i1' or column_datatype.lower() == 'i' or column_datatype.lower() == 'i2':
                    #TODO FFR - negativer Fall
                    column_intersecions_new.append(f"CASE WHEN TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) ELSE TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) END  as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)

                elif  column_datatype.lower() == 'bf' or column_datatype.lower() == 'bv' or column_datatype.lower() == 'd' or column_datatype.lower() == 'f' or column_datatype.lower() == 'dy' or column_datatype.lower() == 'dh' or column_datatype.lower() == 'dm' or column_datatype.lower() == 'ds' or column_datatype.lower() == 'hr' or column_datatype.lower() == 'hs' or column_datatype.lower() == 'mi' or column_datatype.lower() == 'ms' or column_datatype.lower() == 'mo' or column_datatype.lower() == 'sc' or column_datatype.lower() == 'yr' or column_datatype.lower() == 'ym' or column_datatype.lower() == 'n' or column_datatype.lower() == 'd' :
                    column_intersecions_new.append(f"CASE WHEN TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) ELSE TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) END as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)

                elif column_datatype.lower() == 'cv' or column_datatype.lower() == 'cf' or column_datatype.lower() == 'cf':
                    column_intersecions_new.append(f'TRIM({column}) AS {column}')
                    used_columns.append(column)
                else:
                    column_intersecions_new.append(column)
                    used_columns.append(column)

            column_intersections = column_intersecions_new.copy()
            columns = ""
            for column in column_intersections:
                #columns = str(column_intersections)[1:-1].replace("'", "")
                columns += f"{column}, "
            columns = columns[:-2]
            keys = str(key_intersection)[1:-1].replace("'", "")


            if key_filters == {}:
                sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"
            else:
                if filter_intersection != []:
                    values = list(key_filters.values())

                    # in_clause = "(('"
                    # for j in range(len(values[0])):
                    #     for value in values:
                    #         in_clause += str(value[j]) + "','"
                    #     in_clause = in_clause[:-2] + "),('"
                    # in_clause = in_clause[:-3] + ')'

                    # where_clause = "WHERE ("
                    # for key in key_filters.keys():
                    #     where_clause += key.replace("'", "") + ","
                    # where_clause = where_clause[:-1] + ")"
                    # where_clause += " in " + in_clause
                    if values[0] == []:
                        sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"
                    else:
                        where_clause = f'{where_clause} AND (('
                        print(key_filters)
                        for j in range(len(values[0])):
                            for key in key_filters.keys():
                                if key_filters.keys() in numeric_columns:
                                    where_clause += f" {key} = {str(key_filters[key][j])} AND"
                                else:
                                    where_clause += f" {key} = '{str(key_filters[key][j])}' AND"
                            where_clause += f" {where_clause[:-3]}) OR ("
                        where_clause = f"{where_clause[:-4]})"

                        sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"
                else:
                    sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count} {where_clause} ORDER BY {keys};"

        else:
            column_intersecions_new = []
            used_columns = []
            numeric_columns = []
            column_intersections = list(set(column_intersections)  - set(exclude_columns))
            column_intersections.sort()
            for column in column_intersections:
                print("COLUMN: " + column)
                print(dict_colummns_datatype)
                column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
                column_datatype = column_datatype.split('(')[0]

                if column_datatype.lower() == 'i8' or column_datatype.lower() == 'i1' or column_datatype.lower() == 'i' or column_datatype.lower() == 'i2':
                    column_intersecions_new.append(f"CASE WHEN TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) ELSE TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) END  as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)

                elif  column_datatype.lower() == 'bf' or column_datatype.lower() == 'bv' or column_datatype.lower() == 'd' or column_datatype.lower() == 'f' or column_datatype.lower() == 'dy' or column_datatype.lower() == 'dh' or column_datatype.lower() == 'dm' or column_datatype.lower() == 'ds' or column_datatype.lower() == 'hr' or column_datatype.lower() == 'hs' or column_datatype.lower() == 'mi' or column_datatype.lower() == 'ms' or column_datatype.lower() == 'mo' or column_datatype.lower() == 'sc' or column_datatype.lower() == 'yr' or column_datatype.lower() == 'ym' or column_datatype.lower() == 'n' or column_datatype.lower() == 'd' :
                    column_intersecions_new.append(f"CASE WHEN TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) like '.%' THEN '0' || TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) ELSE TRIM(TO_CHAR(CAST(ROUND({column}, 2) as decimal(38,2)), '999999999999999999999999.00')) END  as {column}")
                    used_columns.append(column)
                    numeric_columns.append(column)

                elif column_datatype.lower() == 'cv' or column_datatype.lower() == 'cf' or column_datatype.lower() == 'cf':
                    column_intersecions_new.append(f'TRIM({column}) as decimal(38,2)) AS {column}')
                    used_columns.append(column)
                else:
                    column_intersecions_new.append(column)
                    used_columns.append(column)
            column_intersections = column_intersecions_new.copy()
            columns = ""
            for column in column_intersections:
                #columns = str(column_intersections)[1:-1].replace("'", "")
                columns += f"{column}, "
            columns = columns[:-2]
            sample_query = f"SELECT {columns} FROM {object.schema}.{object.name} SAMPLE {sample_count};"

        # ##
        # ## Only Filter for last 5 days for LAGERBESTAND_MAERKTE_TAG
        # if object == 'LAGERBESTAND_MAERKTE_TAG':
        #     sample_query = sample_query.upper()
        #     if 'WHERE ' in sample_query:
        #         sample_query = sample_query.replace("WHERE ", " AND (").replace("ORDER BY ", ") ORDER BY ")
        #     sample_query = sample_query.replace(f"FROM {object.database}.{object.schema}.{object.name}", f"FROM {object.database}.{object.schema}.{object.name} WHERE dat_jjjjmmtt > to_char(current_date()-6, 'YYYYMMDD')")

        error_dict = {}
        key_dict = {}
        try:
            sample_pdf = self.execute_queries(sample_query,True)
            for key in key_intersection:
                key_dict[key] = list(sample_pdf[key])
            test = ''

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


        return return_list , key_dict, used_columns, sample_query.replace("SAMPLE 10", "")

    def execute_queries(self, query: Union[str, List[str]],return_as_pdf:bool=False)  -> Union[List[Dict], List[List[Dict]]]:
        if self.teradata_connection is None:
            self._connect_to_teradata()

        query_list: List[str] = query if isinstance(query, list) else [query]

        results = []

        for single_query in query_list:
            try:
                cursor=self.teradata_connection.cursor()
                query_result=cursor.execute(single_query)

                if return_as_pdf:
                    query_result = pd.DataFrame(query_result)

                results.append(query_result)

            except Exception as err:
                #results.append("ERROR: " + err)
                #raise Exception() from err
                raise Exception(single_query + "|||" + str(err))


        return results[0] if not isinstance(query, list) else results


    def execute_statement(self, statement: Union[str, List[str]]) -> None:
        """
            Executes simple statement against teradata
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        if self.teradata_connection is None:
            self._connect_to_teradata()

        statement_list: List[str] = (
            statement if isinstance(statement, list) else [statement]
        )

        try:
            for single_statement in statement_list:
                stripped_statement = (
                    single_statement.strip()
                )
                _ = self.teradata_connection.execute(stripped_statement)

        except Exception as err:
            raise Exception(self._get_error_message(err, single_statement)) from err
