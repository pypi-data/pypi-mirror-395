import pyodbc
import pandas.io.sql
import pandas as pd
import logging

from typing import Union, List, Dict

from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.core.database_objects import DatabaseObject

#########################################################################################
#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger('Azure_Service')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

class AzureService:
    def __init__(self, connection_params: dict):
        self.connection_params =connection_params
        self.azure_connection = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.azure_connection is not None:
            self.azure_connection.close()

    def __del__(self):
        if self.azure_connection is not None:
            self.azure_connection.close()

    def _connect_to_azure(self):
        azure_connection_string = (
            f"DRIVER={self.connection_params['Driver']};"
            f"SERVER={self.connection_params['Server']};"
            f"PORT={self.connection_params['Port']};"
            f"DATABASE={self.connection_params['Database']};"
            f"UID={self.connection_params['User']};"
            f"PWD={self.connection_params['Password']}"
        )
        self.azure_connection = pyodbc.connect(azure_connection_string)
        return self.azure_connection

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
        return f"Azure ERROR: {message}\nFailed statement:\n{statement}"


    def get_database_objects(self, database: str, schema: str=None, object_type_restriction: str='include_all') -> dict:
        if self.azure_connection is None:
            self._connect_to_azure()

        all_database_tables=[]
        all_database_views=[]

        if object_type_restriction=='include_all' or object_type_restriction=='include_only_tables':
            if schema:
                query_db_tables=f"select schema_name(t.schema_id) as schema_name, t.name as table_name from sys.tables t where schema_name(t.schema_id) = '{schema}' order by schema_name;"
            else:
                query_db_tables=f"select schema_name(t.schema_id) as schema_name, t.name as table_name from sys.tables t order by schema_name;"

            all_database_tables = self.execute_queries(query_db_tables)

        elif object_type_restriction=='include_all' or object_type_restriction=='include_only_views':
            if schema:
                query_db_views=f"select schema_name(t.schema_id) as schema_name, t.name as table_name from sys.views t where schema_name(t.schema_id) = '{schema}' order by schema_name;"
            else:
                query_db_views=f"select schema_name(t.schema_id) as schema_name, t.name as table_name from sys.views t order by schema_name;"

            all_database_views = self.execute_queries(query_db_views)

        database_objects=[]
        for row in all_database_tables:
            database_table=f'{database}.{row[0].upper()}.{row[1].upper()}'
            database_objects.append({"object_identifier": database_table, "object_type": "table"})
        for row in all_database_views:
            database_view=f'{database}.{row[0].upper()}.{row[1].upper()}'
            database_objects.append({"object_identifier": database_view, "object_type": "view"})
        return database_objects


    def get_columns_from_object(self, object : DatabaseObject) -> list:
        if self.azure_connection is None:
            self._connect_to_azure()

        queries_get_columns = [f"select col.name from sys.tables as tab inner join sys.columns as col on (tab.object_id = col.object_id and upper(tab.name) = '{object.name.upper()}') inner join (select object_id, schema_id from sys.objects) as obj on (tab.object_id = obj.object_id and schema_name(obj.schema_id) = '{object.schema.upper()}');"]

        # select col.name from sys.tables as tab inner join sys.columns as col on tab.object_id = col.object_id where tab.name = 'TBL_CUSTOMER_DATA'

        all_columns = self.execute_queries(queries_get_columns)[0]

        columns=[]

        for row in all_columns:
            columns.append(row[0])

        return columns

    def get_row_count_from_object(self, object : DatabaseObject) -> int:
        if self.azure_connection is None:
            self._connect_to_azure()

        query_get_row_count = f"select count(*) as ROW_COUNT from {object.schema}.{object.name};"

        row_count = self.execute_queries(query_get_row_count).fetchall()[0][0]

        return row_count

    def get_data_types_from_object(self, object : DatabaseObject, column_intersections: list) -> dict:
        results = []

        if self.azure_connection is None:
            self._connect_to_azure()

        column_intersections = str(column_intersections)[1:-1]
        query_get_data_types_from_object=f"select col.name, t.name as data_type from sys.tables as tab inner join sys.columns as col on tab.object_id = col.object_id left join sys.types as t on col.user_type_id = t.user_type_id where tab.name = '{object.name}' and schema_name(tab.schema_id) = '{object.schema}'"
        dict_colummns_datatype=self.execute_queries(query_get_data_types_from_object).fetchall()

        results = [{"COLUMN_NAME":row[0],"DATA_TYPE":row[1]} for row in dict_colummns_datatype]

        return results

    def get_count_distincts_from_object(self, object : DatabaseObject, column_intersections: list,
            enclose_column_by_double_quotes: bool = False) -> dict:
        if self.azure_connection is None:
            self._connect_to_azure()

        unions=""
        for column in column_intersections:
            unions +=f"UNION SELECT '{column}' AS COLUMN_NAME, COUNT(DISTINCT {column}) AS COUNT_DISTINCT FROM {object.schema}.{object.name}"

        query_get_count_distincts_from_object=f"{unions[5:]} ORDER BY COUNT_DISTINCT;"
        dict_count_distincts=self.execute_queries(query_get_count_distincts_from_object).fetchall()

        return dict_count_distincts

    def get_table_size(self, object : DatabaseObject) -> int:
        query_get_table_size = f"select cast(sum(spc.used_pages * 8)/1024.00 *1000000 as integer) as BYTES from sys.tables tab inner join sys.indexes ind on tab.object_id = ind.object_id inner join sys.partitions part on ind.object_id = part.object_id and ind.index_id = part.index_id inner join sys.allocation_units spc on part.partition_id = spc.container_id where schema_name(tab.schema_id) = '{object.schema}' and tab.name = '{object.name}' group by schema_name(tab.schema_id) + '.' + tab.name order by sum(spc.used_pages) desc;"

        size = self.execute_queries(query_get_table_size).fetchall()[0][0]

        return size

    def create_checksums(
            self,
            object : DatabaseObject,
            column_intersections: list,
            enclose_column_by_double_quotes: bool = False
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

        if self.azure_connection is None:
            self._connect_to_azure()

        # column_intersections= [f"{x.upper()}" for x in column_intersections]

        dict_colummns_datatype=self.get_data_types_from_object(object, column_intersections)

        # dict_colummns_datatype_dict = dict(zip(dict_colummns_datatype[::2], dict_colummns_datatype[1::2]))

        aggregates = ""
        count_nulls = ""

        for column in column_intersections:
            column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
            column_datatype = column_datatype.split('(')[0]

            count_nulls += f", sum(case when {column} is null then 1 else 0 end) as countnulls_{column}"

            if column_datatype.lower() == 'tinyint' or column_datatype.lower() == 'smallint' or column_datatype.lower() == 'int' or column_datatype.lower() == 'bigint' or column_datatype.lower() == 'decimal' or column_datatype.lower() == 'numeric' or column_datatype.lower() == 'smallmoney' or column_datatype.lower() == 'money' or column_datatype.lower() == 'float' or column_datatype.lower() == 'real':

                aggregates += f", sum({column}) as sum_{column}"

            elif column_datatype.lower() == 'char' or column_datatype.lower() == 'varchar' or column_datatype.lower() == 'varchar' or column_datatype.lower() == 'text' or column_datatype.lower() == 'nchar' or column_datatype.lower() == 'nvarchar' or column_datatype.lower() == 'nvarchar' or column_datatype.lower() == 'ntext' or column_datatype.lower() == 'binary' or column_datatype.lower() == 'varbinary' or column_datatype.lower() == 'varbinary' or column_datatype.lower() == 'datetime' or column_datatype.lower() == 'datetime2' or column_datatype.lower() == 'smalldatetime' or column_datatype.lower() == 'date' or column_datatype.lower() == 'time' or column_datatype.lower() == 'datetimeoffset' or column_datatype.lower() == 'timestamp':

                aggregates += f", count(distinct lower({column})) as countdistinct_{column}"

            elif column_datatype.lower() == 'bit':

                aggregates += f", (SELECT CONCAT ((select count(*) as val FROM {object.schema}.{object.name} WHERE {column} = 1),'_',(select count(*) as val from {object.schema}.{object.name} WHERE {column} = 0))) AS aggregateboolean_{column}"

            #else: Additional Data Types: image , sql_variant, uniqueidentifier, xml, cursor, table, column_datatype.lower() == 'bit' or

        query_checksums = f"select {aggregates[1:]} from {object.schema}.{object.name};"

        query_countnulls = f"select {count_nulls[1:]} from {object.schema}.{object.name};"

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

    def create_pandas_df_from_group_by(self, object : DatabaseObject, column_intersections: list, group_by_column: str,
        enclose_column_by_double_quotes: bool = False) -> List[Dict]:

        if self.teradata_connection is None:
            self._connect_to_teradata()

        aggregation_columns= [f"{column.upper()}" for column in column_intersections if column != group_by_column]

        dict_colummns_datatype=self.get_data_types_from_object(object, aggregation_columns)

        aggregates = ""

        for column in column_intersections:
            column_datatype=next(x for x in dict_colummns_datatype if x["COLUMN_NAME"] == column)["DATA_TYPE"]
            column_datatype = column_datatype.split('(')[0]

            if column_datatype.lower() == 'tinyint' or column_datatype.lower() == 'smallint' or column_datatype.lower() == 'int' or column_datatype.lower() == 'bigint' or column_datatype.lower() == 'decimal' or column_datatype.lower() == 'numeric' or column_datatype.lower() == 'smallmoney' or column_datatype.lower() == 'money' or column_datatype.lower() == 'float' or column_datatype.lower() == 'real':

                aggregates += f", sum({column}) as sum_{column}"

            elif column_datatype.lower() == 'char' or column_datatype.lower() == 'varchar' or column_datatype.lower() == 'varchar' or column_datatype.lower() == 'text' or column_datatype.lower() == 'nchar' or column_datatype.lower() == 'nvarchar' or column_datatype.lower() == 'nvarchar' or column_datatype.lower() == 'ntext' or column_datatype.lower() == 'binary' or column_datatype.lower() == 'varbinary' or column_datatype.lower() == 'varbinary' or column_datatype.lower() == 'datetime' or column_datatype.lower() == 'datetime2' or column_datatype.lower() == 'smalldatetime' or column_datatype.lower() == 'date' or column_datatype.lower() == 'time' or column_datatype.lower() == 'datetimeoffset' or column_datatype.lower() == 'timestamp':

                aggregates += f", count(distinct lower({column})) as countdistinct_{column}"

            elif column_datatype.lower() == 'bit':

                aggregates += f", (SELECT CONCAT ((select count(*) as val FROM {object.schema}.{object.name} WHERE {column} = 1),'_',(select count(*) as val from {object.schema}.{object.name} WHERE {column} = 0))) AS aggregateboolean_{column}"

            #else: Additional Data Types: image , sql_variant, uniqueidentifier, xml, cursor, table, column_datatype.lower() == 'bit' or

        query_group_by_aggregation = f"select {group_by_column}, count(*) as COUNT_OF_GROUP_BY_VALUE, {aggregates[1:]} from {object.schema}.{object.name} group by {group_by_column};"

        group_by_aggregation_pdf = self.execute_queries(query_group_by_aggregation,True)

        return group_by_aggregation_pdf

    def create_pandas_df(
        self,
        object : DatabaseObject,
        intersection_columns_trgt_src: list,
        where_clause:str="",
        exclude_columns:list=[],
        enclose_column_by_double_quotes: bool = False
        ) -> pd.DataFrame:

        if self.azure_connection is None:
            self._connect_to_azure()

        intersection_columns_trgt_src_ = ', '.join(list(set(intersection_columns_trgt_src) - set(exclude_columns)))

        df_query = f"select {intersection_columns_trgt_src_} from {object.schema}.{object.name} {where_clause};"

        pdf = self.execute_queries(df_query,True)

        return pdf


    def execute_queries(self, query: Union[str, List[str]],return_as_pdf:bool=False)  -> Union[List[Dict], List[List[Dict]]]:
        if self.azure_connection is None:
            self._connect_to_azure()

        query_list: List[str] = query if isinstance(query, list) else [query]

        results = []

        try:
            for single_query in query_list:
                query_result=self.azure_connection.execute(single_query)

                if return_as_pdf:
                    query_result = pd.DataFrame(query_result)

                results.append(query_result)

        except Exception as err:
            raise Exception() from err

        return results[0] if not isinstance(query, list) else results


    def execute_statement(self, statement: Union[str, List[str]]) -> None:
        """
            Executes simple statement against azure
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        if self.azure_connection is None:
            self._connect_to_azure()

        statement_list: List[str] = (
            statement if isinstance(statement, list) else [statement]
        )

        try:
            for single_statement in statement_list:
                stripped_statement = (
                    single_statement.strip()
                )
                _ = self.azure_connection.execute(stripped_statement)

        except Exception as err:
            raise Exception(self._get_error_message(err, single_statement)) from err
