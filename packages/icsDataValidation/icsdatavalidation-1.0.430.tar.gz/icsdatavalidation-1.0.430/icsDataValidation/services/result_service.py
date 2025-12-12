import logging
import boto3
import subprocess
import json

from azure.storage.blob import BlobServiceClient
from decimal import Decimal

from icsDataValidation.services.system_service import SystemService
from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.input_parameters.testing_tool_params import TestingToolParams
from icsDataValidation.output_parameters.result_params import ResultParams
from icsDataValidation.core.database_objects import DatabaseObject
from icsDataValidation.utils.file_util import write_json_to_file, CustomJSONEncoder

#########################################################################################
# Configure Dev Ops Logger

logger = logging.getLogger('ResultService')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

#########################################################################################
#########################################################################################


class ResultService(TestingToolParams):
    """
    Class to process comparison results and save the results in various formats.
    """

    def __init__(
            self, start_time_utc: str,
            remaining_mapping_objects: dict,
            object_identifiers_src_minus_trgt: list,
            object_identifiers_trgt_minus_src: list,
            object_identifiers_to_compare_src: list,
            object_identifiers_to_compare_trgt: list,
            objects_to_compare: list[dict],
            all_objects_matching: bool,
            object_level_comparison_results: list[dict]
        ):
        super().__init__()

        self.results = {
                    "PIPELINE_NAME": TestingToolParams.pipeline_name,
                    "PIPELINE_ID": TestingToolParams.pipeline_id,
                    "START_TIME_UTC": start_time_utc,
                    "SOURCE_SYSTEM": TestingToolParams.source_system_selection,
                    "TARGET_SYSTEM": TestingToolParams.target_system_selection,
                    "DATABASE_NAME": TestingToolParams.database_name,
                    "TESTSET": TestingToolParams.testset_file_names,
                    "SRC_MINUS_TRGT": object_identifiers_src_minus_trgt,
                    "TRGT_MINUS_SRC": object_identifiers_trgt_minus_src,
                    "OBJECTS_TO_COMPARE_SRC": object_identifiers_to_compare_src,
                    "OBJECTS_TO_COMPARE_TRGT": object_identifiers_to_compare_trgt,
                    "NUMBER_OF_OBJECTS_TO_COMPARE": len(objects_to_compare),
                    "ALL_OBJECTS_MATCHING": all_objects_matching,
                    "ALL_COLUMNS_EQUAL": None,
                    "ALL_DATATYPES_EQUAL": None,
                    "ALL_ROWCOUNTS_EQUAL": None,
                    "ALL_CHECKSUMS_EQUAL": None,
                    "ALL_SAMPLES_EQUAL" : None,
                    "ALL_OBJECTS_EQUAL": None,
                    #"ALL_OBJECTS_NOT_ALTERED_DURING_COMPARISON": True,
                    "OBJECTS": object_level_comparison_results
        }

        self.remaining_mapping_objects = remaining_mapping_objects
        self.start_time_utc = start_time_utc

        self.load_results_function_mapping = {
            "SNOWFLAKE": self.load_results_to_snowflake,
            "EXASOL": None,
            "AZURE": None,
            "TERADATA": None,
            "ORACLE": None,
            "DATABRICKS_HIVE_METASTORE": self.load_results_to_databricks,
            "DATABRICKS_UNITY_CATALOG": self.load_results_to_databricks,
        }

    @staticmethod
    def _compare_column_datatypes(
            src_datatype: str,
            trgt_datatype: str
            ):
        """
        Compare the data types of a source- and a target-column.
        Uses data-type-mapping defined in the migration_config.json.
        """
        if not src_datatype or not trgt_datatype:
            datatype_equal = None

        if src_datatype.lower() == trgt_datatype.lower():
            datatype_equal = True
        elif "DATATYPE_MAPPING" in TestingToolParams.migration_config["MAPPING"] and TestingToolParams.migration_config["MAPPING"]["DATATYPE_MAPPING"]:
            datatype_equal = False
            for datatype_mapping in TestingToolParams.migration_config["MAPPING"]["DATATYPE_MAPPING"]:
                if (
                    src_datatype.lower() in [datatype.lower() for datatype in datatype_mapping["src_datatypes"]]
                    and trgt_datatype.lower() in [datatype.lower() for datatype in datatype_mapping["trgt_datatypes"]]
                    ):
                    datatype_equal = True
        else:
            datatype_equal = False

        return datatype_equal


    @staticmethod
    def prepare_column_level_result(
            column: str,
            exclude_columns: list,
            result_params: ResultParams
        ) -> dict:
        """
        Get column level result dictionary from the result parameters.
        """
        in_sync = False
        datatype_equal = None
        aggregation_type_src = None
        aggregation_type_trgt = None
        aggregation_type = None
        aggregation_result_src = None
        aggregation_result_trgt = None
        aggregation_equal = None
        aggregation_tolerated = None
        aggregation_difference_trgt_minus_src = None
        count_nulls_src = None
        count_nulls_trgt = None
        count_nulls_equal = None
        count_nulls_difference_trgt_minus_src = None

        if column in result_params.src_columns_upper:
            in_src = True
            src_datatype = next(item["DATA_TYPE"] for item in result_params.src_column_datatypes if item["COLUMN_NAME"].upper() == column)
        else:
            in_src = False
            src_datatype = None

        if column in result_params.trgt_columns_upper:
            in_trgt = True
            trgt_datatype = next(item["DATA_TYPE"] for item in result_params.trgt_column_datatypes if item["COLUMN_NAME"].upper() == column)
        else:
            in_trgt = False
            trgt_datatype = None

        if column.upper() in exclude_columns:
            in_excluded = True
        else:
            in_excluded = False

        if in_src and in_trgt :
            in_sync=True
            if result_params.src_columns_aggregate != {}:

                if column in result_params.src_columns_aggregate:
                    aggregation_type_src = result_params.src_columns_aggregate[column][0]
                    aggregation_result_src = result_params.src_columns_aggregate[column][1]
                    count_nulls_src = result_params.src_columns_aggregate[column][2]

                if column in result_params.trgt_columns_aggregate:
                    aggregation_type_trgt = result_params.trgt_columns_aggregate[column][0]
                    aggregation_result_trgt = result_params.trgt_columns_aggregate[column][1]
                    count_nulls_trgt = result_params.trgt_columns_aggregate[column][2]

                if column in result_params.aggregation_differences_trgt_minus_src and result_params.aggregation_differences_trgt_minus_src[column] and not result_params.aggregation_differences_trgt_minus_src[column] == '0_0':
                    aggregation_equal = False
                    aggregation_difference_trgt_minus_src = result_params.aggregation_differences_trgt_minus_src[column]

                elif aggregation_result_src is not None and aggregation_result_trgt is not None and aggregation_type_src and aggregation_type_trgt and aggregation_type_src == aggregation_type_trgt:
                    aggregation_equal = True

                    if column in result_params.aggregation_differences_trgt_minus_src and result_params.aggregation_differences_trgt_minus_src[column] == '0_0':
                        aggregation_difference_trgt_minus_src='0_0'

                    else:
                        aggregation_difference_trgt_minus_src='0'

                if aggregation_type_src and aggregation_type_trgt and aggregation_type_src == aggregation_type_trgt:
                    aggregation_type = aggregation_type_src

            '''
            Comparison Based on Decimal Places
            Logic is defined in migration_config.json
            '''
            aggregation_tolerated = aggregation_equal

            if 'DATATYPE_TOLERANCE' in TestingToolParams.migration_config['MAPPING'].keys():
                if (
                    src_datatype in TestingToolParams.migration_config['MAPPING']['DATATYPE_TOLERANCE'].keys()
                    and aggregation_type == 'SUM'
                    and abs(Decimal(aggregation_difference_trgt_minus_src)) <= Decimal(TestingToolParams.migration_config['MAPPING']['DATATYPE_TOLERANCE'][src_datatype])
                    ):
                    aggregation_tolerated = True
            else :
                aggregation_tolerated = None

            if count_nulls_src is not None and count_nulls_trgt is not None and count_nulls_src==count_nulls_trgt:
                count_nulls_equal = True
                count_nulls_difference_trgt_minus_src = '0'
            elif count_nulls_src is not None and count_nulls_trgt is not None:
                    count_nulls_equal = False
                    count_nulls_difference_trgt_minus_src = int(count_nulls_trgt)-int(count_nulls_src)

            datatype_equal = ResultService._compare_column_datatypes(src_datatype, trgt_datatype)

        column_comparison_result = {
            "COLUMN_NAME": column,
            "IN_SRC": in_src,
            "IN_TRGT": in_trgt,
            "IN_SYNC": in_sync,
            "IN_EXCLUDED": in_excluded,
            "SRC_DATATYPE": src_datatype,
            "TRGT_DATATYPE": trgt_datatype,
            "DATATYPE_EQUAL": datatype_equal,
            "AGGREGATION_TYPE": aggregation_type,
            "AGGREGATION_EQUAL": aggregation_equal,
            "AGGREGATION_EQUAL_TOLERATED": aggregation_tolerated,
            "AGGREGATION_RESULT_SRC": aggregation_result_src,
            "AGGREGATION_RESULT_TRGT": aggregation_result_trgt,
            "AGGREGATION_DIFFERENCE_TRGT_MINUS_SRC": aggregation_difference_trgt_minus_src,
            "COUNT_NULLS_EQUAL": count_nulls_equal,
            "COUNT_NULLS_SRC": count_nulls_src,
            "COUNT_NULLS_TRGT": count_nulls_trgt,
            "COUNT_NULLS_DIFFERENCE_TRGT_MINUS_SRC": count_nulls_difference_trgt_minus_src
        }

        return column_comparison_result

    @staticmethod
    def prepare_object_level_result(
            src_object: DatabaseObject,
            trgt_object: DatabaseObject,
            src_filter: str,
            trgt_filter: str,
            exclude_columns: list,
            result_params: ResultParams,
            column_level_comparison_result: dict
        ) -> dict:
        """
        Get object level result dictionary from the result parameters and from the column level result.
        """

        if 'DATATYPE_TOLERANCE' not in TestingToolParams.migration_config['MAPPING']:
            aggregations_equal_tolerated = None
        elif result_params.aggregations_equal:
            aggregations_equal_tolerated = True
        elif all([column['AGGREGATION_EQUAL_TOLERATED'] for column in column_level_comparison_result if column['AGGREGATION_EQUAL_TOLERATED'] is not None]):
            aggregations_equal_tolerated = True
        else:
            aggregations_equal_tolerated = False

        object_level_comparison_result = {
            "SRC_DATABASE_NAME": src_object.database,
            "SRC_SCHEMA_NAME": src_object.schema,
            "SRC_OBJECT_NAME": src_object.name,
            "SRC_OBJECT_TYPE": src_object.type,
            "TRGT_DATABASE_NAME": trgt_object.database,
            "TRGT_SCHEMA_NAME": trgt_object.schema,
            "TRGT_OBJECT_NAME": trgt_object.name,
            "TRGT_OBJECT_TYPE": trgt_object.type,
            "SRC_FILTER": src_filter,
            "TRGT_FILTER": trgt_filter,
            "EXCLUDED_COLUMNS": exclude_columns,
            "COLUMNS_EQUAL": result_params.columns_equal,
            "COLUMN_INTERSECTION": result_params.intersection_columns_trgt_src,
            "SRC_COLUMNS_MINUS_TRGT_COLUMNS": result_params.src_columns_minus_trgt_columns,
            "TRGT_COLUMNS_MINUS_SRC_COLUMNS": result_params.trgt_columns_minus_src_columns,
            "DATATYPES_EQUAL": result_params.datatypes_equal,
            "ROW_COUNTS_EQUAL": result_params.row_counts_equal,
            "SRC_ROW_COUNT": result_params.src_row_count,
            "TRGT_ROW_COUNT": result_params.trgt_row_count,
            "ALL_COUNT_NULLS_EQUAL": result_params.all_count_nulls_equal,
            "AGGREGATIONS_EQUAL": result_params.aggregations_equal,
            "AGGREGATIONS_EQUAL_TOLERATED": aggregations_equal_tolerated,
            "SRC_ERROR": result_params.src_error_dict,
            "TRGT_ERROR":  result_params.trgt_error_dict,
            "GROUP_BY_COLUMNS": result_params.object_group_by_columns,
            "SRC_GROUP_BY_QUERY": result_params.src_group_by_query,
            "TRGT_GROUP_BY_QUERY": result_params.trgt_group_by_query,
            "GROUP_BY_EQUAL": result_params.group_by_equal,
            "GROUP_BY_VALUES_WITH_MISMATCHES": result_params.group_by_values_with_mismatches,
            "COLUMNS_WITH_MISMATCH": result_params.columns_with_mismatch,
            "GROUP_BY_DIFF_DICT": result_params.group_by_diff_dict,
            "SRC_GROUP_BY_ERROR": result_params.src_group_by_error,
            "TRGT_GROUP_BY_ERROR": result_params.trgt_group_by_error,
            "SAMPLES_COMPARED": result_params.samples_compared,
            "SAMPLES_EQUAL": result_params.samples_equal,
            "SAMPLE_KEYS": result_params.trgt_key_filters,
            "SRC_SAMPLE": result_params.src_sample_dict,
            "TRGT_SAMPLE": result_params.trgt_sample_dict,
            "SRC_SAMPLE_QUERY": result_params.src_sample_query,
            "TRGT_SAMPLE_QUERY": result_params.trgt_sample_query,
            "SRC_SAMPLE_ERROR_DICT": result_params.src_sample_error_dict,
            "TRGT_SAMPLE_ERROR_DICT": result_params.trgt_sample_error_dict,
            "PANDAS_DATAFRAME_COMPARED" : result_params.pandas_df_compared,
            "PANDAS_DATAFRAME_EQUAL": result_params.pandas_df_is_equal,
            "SRC_NOT_ALTERED_DURING_COMPARISON": result_params.not_altered_during_comparison_src,
            "TRGT_NOT_ALTERED_DURING_COMPARISON": result_params.not_altered_during_comparison_trgt,
            "SRC_LAST_ALTERED": result_params.last_altered_src,
            "TRGT_LAST_ALTERED": result_params.last_altered_trgt,
            "ALL_COLUMNS": result_params.all_columns_trgt_src,
            "COLUMNS": column_level_comparison_result

            #"PANDAS_DATAFRAME_MISMATCH": str(err_msg)
        }

        return object_level_comparison_result

    @staticmethod
    def prepare_object_level_live_result(
            object_level_comparison_result: dict,
            testing_tool_params: TestingToolParams,
        ) -> dict:
        """
        Get object level live result dictionary from the object level comparison result and from the testing tool parameters.
        """
        live_object_level_comparison_result = {
                "PIPELINE_NAME": testing_tool_params.pipeline_name,
                "PIPELINE_ID": testing_tool_params.pipeline_id,
                "RUN_GUID": testing_tool_params.run_guid,
                "SOURCE_SYSTEM": testing_tool_params.source_system_selection,
                "TARGET_SYSTEM": testing_tool_params.target_system_selection,
                "DATABASE_NAME": testing_tool_params.database_name,
                #"ALL_OBJECTS_NOT_ALTERED_DURING_COMPARISON": True,
                "OBJECTS": object_level_comparison_result
                }

        return  live_object_level_comparison_result

    def determine_highlevel_results(self):
        """
        Determine highlevel results based on all object level results.
        """
        logger.info(f"++++++++++++++++ DETERMINE highlevel results")

        if any(not object_level_comparison_result['COLUMNS_EQUAL'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_COLUMNS_EQUAL"] = False
        else:
            self.results["ALL_COLUMNS_EQUAL"] = True

        if any(not object_level_comparison_result['DATATYPES_EQUAL'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_DATATYPES_EQUAL"] = False
        else:
            self.results["ALL_DATATYPES_EQUAL"] = True

        if any(not object_level_comparison_result['ROW_COUNTS_EQUAL'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_ROWCOUNTS_EQUAL"] = False
        else:
            self.results["ALL_ROWCOUNTS_EQUAL"] = True

        if any(not object_level_comparison_result['AGGREGATIONS_EQUAL'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_CHECKSUMS_EQUAL"] = False
        else:
            self.results["ALL_CHECKSUMS_EQUAL"] = True

        if all(not object_level_comparison_result['SAMPLES_COMPARED'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_SAMPLES_EQUAL"] = None
        elif any(not object_level_comparison_result['SAMPLES_EQUAL'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_SAMPLES_EQUAL"] = False
        else:
            self.results["ALL_SAMPLES_EQUAL"] = True

        if all(not object_level_comparison_result['PANDAS_DATAFRAME_COMPARED'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_OBJECTS_EQUAL"] = None
        elif any(not object_level_comparison_result['PANDAS_DATAFRAME_EQUAL'] for object_level_comparison_result in self.results["OBJECTS"]):
            self.results["ALL_OBJECTS_EQUAL"] = False
        else:
            self.results["ALL_OBJECTS_EQUAL"] = True

        # TODO add ALL_OBJECTS_NOT_ALTERED_DURING_COMPARISON flag
        #if any(object_level_comparison_result['NOT_ALTERED_DURING_COMPARISON_SRC'] == False for object_level_comparison_result in self.results["OBJECTS"]) or any(object_level_comparison_result['NOT_ALTERED_DURING_COMPARISON_TRGT'] == False for object_level_comparison_result in self.results["OBJECTS"]):
        #    self.results["ALL_OBJECTS_NOT_ALTERED_DURING_COMPARISON"] = False
        #else:
        #    self.results["ALL_OBJECTS_NOT_ALTERED_DURING_COMPARISON"] = True

        logger.info("\n****************************************************")
        logger.info(f"++++++++++++++++ Highlevel results  ++++++++++++++++")
        logger.info(f"RUN_GUID: {self.run_guid}")
        logger.info(f"NUMBER_OF_OBJECTS_TO_COMPARE: {self.results['NUMBER_OF_OBJECTS_TO_COMPARE']}")
        logger.info(f"ALL_OBJECTS_MATCHING: {self.results['ALL_OBJECTS_MATCHING']}")
        logger.info(f"ALL_COLUMNS_EQUAL: {self.results['ALL_COLUMNS_EQUAL']}")
        logger.info(f"ALL_DATATYPES_EQUAL: {self.results['ALL_DATATYPES_EQUAL']}")
        logger.info(f"ALL_ROWCOUNTS_EQUAL: {self.results['ALL_ROWCOUNTS_EQUAL']}")
        logger.info(f"ALL_CHECKSUMS_EQUAL: {self.results['ALL_CHECKSUMS_EQUAL']}")
        logger.info(f"ALL_SAMPLES_EQUAL: {self.results['ALL_SAMPLES_EQUAL']}")
        logger.info(f"ALL_OBJECTS_EQUAL: {self.results['ALL_OBJECTS_EQUAL']}")
        logger.info("****************************************************\n")


    def load_results_to_result_database(self):
        """
        Initialize database service for result-system.
        Load results to result database.
        """
        result_system_selection_type=self.systems[self.result_system_selection]["DATABASE_TYPE"]

        result_system = SystemService(self.result_system_selection, self.systems)
        self.connection_params_result = result_system.get_connection_params()
        database_service_result=result_system.initialize_database_service(self.connection_params_result)

        with database_service_result as db_service_result:

            load_results_function = self.load_results_function_mapping[result_system_selection_type.upper()]

            if load_results_function:
                load_results_function(db_service_result, self.results)
            else:
                raise ValueError(f"Result system selection of type '{result_system_selection_type}' not supported!")

    def load_results_to_snowflake(self, db_service_result, results: dict):
        """
        Load results to Snowflake.
        """
        logger.info(f"++++++++++++++++ LOAD comparison results to Snowflake")

        db_service_result.upload_to_stage(self.stage_name, self.result_folder_path, self.result_file_name, is_temporary=True)

        db_service_result.insert_json_results(self.run_guid, self.pipeline_name, self.pipeline_id, self.start_time_utc, self.result_table, self.stage_name)

        db_service_result.insert_highlevel_results(results, self.run_guid, self.pipeline_name, self.pipeline_id, self.result_table_highlevel)

        db_service_result.insert_objectlevel_results(self.result_table, self.result_table_objectlevel, self.run_guid)

        db_service_result.insert_columnlevel_results(self.result_table, self.result_table_columnlevel, self.run_guid)

    def load_results_to_databricks(self, db_service_result, results: dict):
        """
        Load results to Databricks Hive Metastore or Unity Catalog.
        """
        logger.info(f"++++++++++++++++ LOAD comparison results to Databricks")

        db_service_result.create_schemas(
            database_name=self.database_name,
            schemas=[self.result_meta_data_schema_name, self.result_schema_name],
        )

        db_service_result.insert_json_results(
            self.run_guid,
            self.pipeline_name,
            self.pipeline_id,
            self.start_time_utc,
            self.result_table,
            self.results,
        )

        db_service_result.insert_highlevel_results(
            results,
            self.run_guid,
            self.pipeline_name,
            self.pipeline_id,
            self.result_table_highlevel,
        )

        db_service_result.insert_objectlevel_results(
            self.result_table,
            self.result_table_objectlevel,
            self.run_guid,
            self.results,
        )

        db_service_result.insert_columnlevel_results(
            self.result_table, self.result_table_columnlevel, self.run_guid, self.results
        )

    def upload_json_result_to_blob(self, start_time_utc:str) -> str:

        """
        Upload the comparison result (JSON) to a blob storage and return the full blob url. If blob container does not exist create it before uploading the blob.
        """
        logger.info(f"++++++++++++++++ LOAD comparison results to Azure Blob Storage")

        prep_result_json = json.dumps(self.results, indent = 4, cls=CustomJSONEncoder)

        blob_file_prefix = start_time_utc[0:10]
        blob_file_name = f"comparison_results_{start_time_utc}_{self.pipeline_name}_{self.pipeline_id}_{self.run_guid}.json"
        blob_name = f"{blob_file_prefix}/{blob_file_name}"

        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=self.azure_storage_connection_string)
        except Exception as error:
            logger.info(f"FAILED to connect to Azure Blob Storage with error '{str(error)}'")
            raise error

        container_client = blob_service_client.get_container_client(self.container_name)

        if not container_client.exists():

            container_client = blob_service_client.create_container(self.container_name)

        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)

        blob_url = blob_client.url

        try:
            logger.info(f"Upload comparison result (JSON) for run_guid {self.run_guid} and pipeline_id {self.pipeline_id} to Azure Blob Storage under '{blob_url}'")
            blob_client.upload_blob(prep_result_json)
        except Exception as error:
            logger.info(f"FAILED comparison result (JSON) upload to Azure Blob Storage under '{blob_url}' with error '{str(error)}'")
            raise error

    def upload_json_result_to_bucket(self, start_time_utc:str) -> str:

        """
        Upload the comparison result (JSON) to an AWS S3 bucket.
        """
        logger.info(f"++++++++++++++++ LOAD comparison results to AWS Bucket")

        prep_result_json = json.dumps(self.results, indent = 4, cls=CustomJSONEncoder)

        bucket_file_prefix = start_time_utc[0:10]
        bucket_file_info = f"comparison_results_{start_time_utc}_{self.pipeline_name}_{self.pipeline_id}_{self.run_guid}.json"
        bucket_file_name = f"{bucket_file_prefix}_-_{bucket_file_info}"

        try:
            s3_service_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_bucket_access_key,
                aws_secret_access_key=self.aws_bucket_secret_key
            )
        except Exception as error:
            logger.info(f"FAILED to connect to AWS S3 bucket with error '{str(error)}'")
            raise error

        try:
            logger.info(f"Upload comparison result (JSON) for run_guid {self.run_guid} and pipeline_id {self.pipeline_id} to AWS S3 bucket")
            s3_service_client.put_object(
                Body=prep_result_json,
                Bucket=self.bucket_name,
                Key=bucket_file_name
            )
        except Exception as error:
            logger.info(f"FAILED comparison result (JSON) upload to AWS S3 bucket with error '{str(error)}'")
            raise error

    def write_results_to_git(self):
        """
        Write comparison results to GIT repository.
        In case of a remote pipeline run: Pull latest changes from GIT befor writing to the local repository, and push to the remote repository at the end.
        """
        logger.info(f"++++++++++++++++ WRITE comparison results to GIT repository")

        if self.pipeline_id:
            logger.info(f"++++++ Pull latest changes from GIT")
            subprocess.run(["git", "checkout", f"origin/{self.branch_name}"])
            subprocess.run(["git", "pull", "--no-rebase"])

        logger.info(f"++++++++++++++++ WRITE to local GIT repository")

        write_json_to_file(self.results, self.result_file_path)

        if self.remaining_mapping_objects:
            logger.info(f"++++++++++++++++ WRITE remaining mapping objects to local GIT repository")

            write_json_to_file( self.remaining_mapping_objects, self.remaining_mapping_objects_file_path)

        if self.pipeline_id:
            logger.info(f"++++++++++++++++ PUSH latest changes to GIT Source Branch: {self.source_branch}; Branch: {self.branch_name}")

            if self.azure_devops_pipeline:
                subprocess.run(["git", "add", f"{self.remaining_mapping_objects_folder_name}"])
                subprocess.run(["git", "add", f"{self.result_folder_name}"])
                subprocess.run(["git", "commit", "-m", f"Added icsDataValidation Tool comparison results of the {self.pipeline_name} Pipeline run with ID {self.pipeline_id}"])
                subprocess.run(["git", "push", "-u","origin", f"HEAD:{self.source_branch}"])

            if self.gitlab_pipeline:
                branches = subprocess.run(["git", "branch"], stdout=subprocess.PIPE, text=True)
                logger.info('+++ BEGIN BRANCHES')
                logger.info(branches.stdout)
                logger.info('+++ END BRANCHES')
                subprocess.run(["git", "add", f"{self.remaining_mapping_objects_folder_name}"])
                subprocess.run(["git", "add", f"{self.result_folder_name}"])
                subprocess.run(["git", "commit", "-m", f"Added icsDataValidation Tool comparison results of the {self.pipeline_name} Pipeline run with ID {self.pipeline_id}"])
                subprocess.run(["git", "push", "-u","origin", f"HEAD:{self.source_branch}"])
                subprocess.run(["git", "push", f"https://user:{self.testatm_access_token}@{self.gitlab_ci_server_host}/{self.gitlab_ci_project_path}.git/", "-u","origin", f"HEAD:origin/{self.branch_name}", "-o", "ci.skip"])
