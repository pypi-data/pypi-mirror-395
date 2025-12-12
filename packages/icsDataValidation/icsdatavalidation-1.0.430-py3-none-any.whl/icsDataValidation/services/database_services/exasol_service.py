import pyexasol as px
from typing import Union, List, Dict
import pandas as pd

from icsDataValidation.core.database_objects import DatabaseObject

#########################################################################################
#########################################################################################

class ExasolService(object):
    def __init__(self, connection_params: dict):
        self.connection_params =connection_params
        self.exasol_connection = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.exasol_connection is not None:
            self.exasol_connection.close()

    def __del__(self):
        if self.exasol_connection is not None:
            self.exasol_connection.close()

    def _connect_to_exasol(self):
        self.exasol_connection = px.connect(**self.connection_params,fetch_dict=True)
        return self.exasol_connection

    #@staticmethod
    #def _get_error_message(excepction: Exception, statement: str) -> None:
    #    """
    #    Compose error message if the execution of a statement or query fails.
    #    """
    #    return

    def get_database_objects(self, database: str, schema: str=None, object_type_restriction: str='include_all') -> dict:
        if self.exasol_connection is None:
            self._connect_to_exasol()

        all_database_tables=[]
        all_database_views=[]

        if object_type_restriction=='include_all' or object_type_restriction=='include_only_tables':
            if schema:
                query_db_tables=f"select * from EXA_ALL_OBJECTS where root_name='{object.schema}' and object_type='TABLE';"
            else:
                query_db_tables=f"select * from EXA_ALL_OBJECTS where object_type='TABLE';"

            all_database_tables = self.execute_queries(query_db_tables)


        elif object_type_restriction=='include_all' or object_type_restriction=='include_only_views':
            if schema:
                query_db_views=f"select * from EXA_ALL_OBJECTS where root_name='{object.schema}' and object_type='VIEW';"
            else:
                query_db_views=f"select * from EXA_ALL_OBJECTS where object_type='VIEW';"

            all_database_views = self.execute_queries(query_db_views)

        database_objects=[]
        for row in all_database_tables:
            table_identifier=f'{database.upper()}.{row["ROOT_NAME"]}.{row["OBJECT_NAME"]}'
            database_objects.append({"object_identifier": table_identifier, "object_type": "table"})
        for row in all_database_views:
            view_identifier=f'{database.upper()}.{row["ROOT_NAME"]}.{row["OBJECT_NAME"]}'
            database_objects.append({"object_identifier": view_identifier, "object_type": "view"})
        return database_objects


    def get_columns_from_object(self, object: DatabaseObject) -> list:

        if self.exasol_connection is None:
            self._connect_to_exasol()

        # select system table and filter on current table to get column names
        queries_get_columns = [f" SELECT COLUMN_NAME FROM EXA_ALL_COLUMNS WHERE COLUMN_TABLE = '{object.name}';"]


        all_columns = self.execute_queries(queries_get_columns)[0]

        columns=[]

        for row in all_columns:
            columns.append(row["COLUMN_NAME"])

        return columns

    def get_row_count_from_table(self, object:DatabaseObject, where_clause: str="") -> int:

        if self.exasol_connection is None:
            self._connect_to_exasol()

        query_get_row_count = f"select count(*) as ROW_COUNT from {object.schema}.{object.name} {where_clause};"

        row_count = self.execute_queries(query_get_row_count).fetchall()[0]["ROW_COUNT"]

        return row_count

    def get_data_types_from_object(self, object: DatabaseObject, column_intersections: list) -> dict:

        if self.exasol_connection is None:
            self._connect_to_exasol()

        column_intersections = str(column_intersections)[1:-1]
        query_get_data_types_from_table=f"select COLUMN_NAME , column_type  from EXA_ALL_COLUMNS where column_table='{object.name}' AND column_schema = '{object.schema}' and COLUMN_NAME in ({column_intersections});"
        dict_colummns_datatype=self.execute_queries(query_get_data_types_from_table).fetchall()
        return dict_colummns_datatype

    def get_count_distincts_from_object(self, object: DatabaseObject, column_intersections: list, where_clause: str="",
        enclose_column_by_double_quotes: bool = False) -> dict:

        if self.exasol_connection is None:
            self._connect_to_exasol()

        unions=""
        for column in column_intersections:
            unions +=f"UNION SELECT '{column}' AS COLUMN_NAME, COUNT(DISTINCT {column}) AS COUNT_DISTINCT FROM {object.schema}.{object.name} {where_clause}"

        query_get_count_distincts_from_object=f"{unions[5:]} ORDER BY COUNT_DISTINCT;"
        dict_count_distincts=self.execute_queries(query_get_count_distincts_from_object).fetchall()
        return dict_count_distincts

    def create_checksums(self, object : DatabaseObject, column_intersections: list, where_clause: str="",
            enclose_column_by_double_quotes: bool = False) -> List[Dict]:

        if self.exasol_connection is None:
            self._connect_to_exasol()

        column_intersections= [f"{x.upper()}" for x in column_intersections]

        dict_colummns_datatype=self.get_data_types_from_object(object, column_intersections)

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["COLUMN_TYPE"]
            column_datatype = column_datatype.split('(')[0]

            count_nulls += f", sum(case when {column} is null then 1 else 0 end) countnulls_{column}"

            if column_datatype.lower() == 'decimal' or column_datatype.lower() == 'double':

                aggregates += f", sum({column}) as sum_{column}"

            elif column_datatype.lower() == 'char' or column_datatype.lower() == 'varchar' or column_datatype.lower() == 'date' or column_datatype.lower() == 'timestamp':

                aggregates += f", count(distinct lower({column})) as countdistinct_{column}"

            elif column_datatype.lower() == 'boolean':

                aggregates += f", max(select count(*) FROM {object.schema}.{object.name} WHERE {column} = true)::varchar || '_' || max(select count(*) FROM {object.schema}.{object.name} WHERE {column} = false) :: varchar as aggregateboolean_{column}"

            #else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

        query_checksums = f"select {aggregates[1:]} from {object.schema}.{object.name} {where_clause};"

        query_countnulls = f"select {count_nulls[1:]} from {object.schema}.{object.name} {where_clause};"

        aggregation_cursor = self.execute_queries(query_checksums)

        aggregation_columns = [column[0].upper() for column in aggregation_cursor.description]

        aggregation_results = aggregation_cursor.fetchall()[0]


        countnulls_cursor = self.execute_queries(query_countnulls)

        countnulls_results = countnulls_cursor.fetchall()[0]

        test_list=[]

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

        checksums = dict(zip([item.split("_", 1)[1] for item in aggregation_columns] , test_list))

        return checksums


    def create_pandas_df_from_group_by(self, object : DatabaseObject, object_type: str, column_intersections: list, group_by_column: str, where_clause: str="",
        enclose_column_by_double_quotes: bool = False) -> List[Dict]:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        aggregation_columns= [f"{column.upper()}" for column in column_intersections if column != group_by_column]

        dict_colummns_datatype=self.get_data_types_from_object(object, aggregation_columns)

        aggregates = ""

        for column in column_intersections:
            column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["COLUMN_TYPE"]
            column_datatype = column_datatype.split('(')[0]

            if column_datatype.lower() == 'decimal' or column_datatype.lower() == 'double':

                aggregates += f", sum({column}) as sum_{column}"

            elif column_datatype.lower() == 'char' or column_datatype.lower() == 'varchar' or column_datatype.lower() == 'date' or column_datatype.lower() == 'timestamp':

                aggregates += f", count(distinct lower({column})) as countdistinct_{column}"

            elif column_datatype.lower() == 'boolean':

                aggregates += f", max(select count(*) FROM {object.schema}.{object} WHERE {column} = true)::varchar || '_' || max(select count(*) FROM {object.schema}.{object} WHERE {column} = false) :: varchar as aggregateboolean_{column}"

            #else: Additional Data Types: VARIANT OBJECT ARRAY GEOGRAPHY

        query_group_by_aggregation = f"select {group_by_column}, count(*) as COUNT_OF_GROUP_BY_VALUE, {aggregates[1:]} from {object.schema}.{object}  {where_clause} group by {group_by_column};"

        group_by_aggregation_pdf = self.execute_queries(query_group_by_aggregation,True)

        return group_by_aggregation_pdf


    def create_pandas_df(self, object:DatabaseObject, intersection_columns_trgt_src: list, where_clause:str="", exclude_columns:list=[],
        enclose_column_by_double_quotes: bool = False) -> pd.DataFrame:
        if self.exasol_connection is None:
            self._connect_to_exasol()

        intersection_columns_trgt_src_ = ', '.join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"select {intersection_columns_trgt_src_} from {object.schema}.{object.name} {where_clause};"

        pdf = self.execute_queries(df_query,True)

        return pdf


    def execute_queries(self, query: Union[str, List[str]],return_as_pdf:bool=False)  -> Union[List[Dict], List[List[Dict]]]:
        if self.exasol_connection is None:
            self._connect_to_exasol()

        query_list: List[str] = query if isinstance(query, list) else [query]

        results = []

        try:
            for single_query in query_list:
                if return_as_pdf:
                    query_result=self.exasol_connection.export_to_pandas(single_query)
                else:
                    query_result=self.exasol_connection.execute(single_query)

                results.append(query_result)

        except Exception as err:
            raise Exception() from err

        return results[0] if not isinstance(query, list) else results
