import logging
import time

from typing import Union, List, Dict
from threading import current_thread
from pathlib import PurePath

from icsDataValidation.services.system_service import SystemService
from icsDataValidation.services.comparison_service import ComparisonService
from icsDataValidation.services.result_service import ResultService
from icsDataValidation.utils.sql_util import parse_filter
from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.utils.file_util import write_json_to_file
from icsDataValidation.core.database_objects import DatabaseObject
from icsDataValidation.input_parameters.testing_tool_params import TestingToolParams

#########################################################################################
# Configure Dev Ops Logger

logger = logging.getLogger('Object_Comparison')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

#########################################################################################
#########################################################################################

def get_additional_configuration(src_object: DatabaseObject, testing_tool_params: TestingToolParams) -> Union[str, List[str]]:
    """
    Get additional configuration from the migration_config.json. Retrieve e.g. the filter and excluded columns.
    """
    src_filter = ""
    trgt_filter = ""
    exclude_columns = []
    if "ADDITIONAL_CONFIGURATION" in testing_tool_params.migration_config.keys():
        additional_configuration = testing_tool_params.migration_config["ADDITIONAL_CONFIGURATION"]
        if f"{src_object.database}.{src_object.schema}.{src_object.name}" in additional_configuration.keys():
            if "FILTER" in additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]:
                src_filter = parse_filter(additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]["FILTER"])
                trgt_filter = parse_filter(additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]["FILTER"])
                logger.info(f"SRC_FILTER: {src_filter} ")
                logger.info(f"TRGT_FILTER: {trgt_filter} ")
            else:
                if "SRC_FILTER" in additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]:
                    src_filter = parse_filter(additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]["SRC_FILTER"])
                    logger.info(f"SRC_FILTER: {src_filter} ")
                if "TRGT_FILTER" in additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]:
                    trgt_filter = parse_filter(additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]["TRGT_FILTER"])
                    logger.info(f"TRGT_FILTER: {trgt_filter} ")

            if "EXCLUDE_COLUMNS" in additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]:
                exclude_columns = additional_configuration[f"{src_object.database}.{src_object.schema}.{src_object.name}"]["EXCLUDE_COLUMNS"]
                exclude_columns = [excluded_column.upper() for excluded_column in exclude_columns]
                logger.info(f"EXCLUDE_COLUMNS: {exclude_columns} ")

    return src_filter, trgt_filter, exclude_columns

def compare_objects(testing_tool_params: TestingToolParams, objects_to_compare: List[Dict]) -> List[Dict]:

    source_system=SystemService(testing_tool_params.source_system_selection,testing_tool_params.systems)
    target_system=SystemService(testing_tool_params.target_system_selection,testing_tool_params.systems)
    result_system=SystemService(testing_tool_params.result_system_selection,testing_tool_params.systems)

    testing_tool_params.connection_params_src=source_system.get_connection_params()
    testing_tool_params.connection_params_trgt=target_system.get_connection_params()
    testing_tool_params.connection_params_result = result_system.get_connection_params()

    database_service_src=source_system.initialize_database_service(testing_tool_params.connection_params_src)
    database_service_trgt=target_system.initialize_database_service(testing_tool_params.connection_params_trgt)
    database_service_result=result_system.initialize_database_service(testing_tool_params.connection_params_result)

    with database_service_src as db_service_src, database_service_trgt as db_service_trgt, database_service_result as db_service_result:

        object_level_comparison_results=[]

        for n_object, object in enumerate(objects_to_compare):
            start_time_object_comparison_ = time.time()
            comp_id = n_object+1
            #####################################################################
            # initialize comparison service

            src_object=DatabaseObject(object["src_object_identifier"],object["src_object_type"])
            trgt_object=DatabaseObject(object["trgt_object_identifier"],object["trgt_object_type"])

            logger.info(f"++++++++++++++++ [{comp_id}] START Comparison of {src_object.database}.{src_object.schema}.{src_object.name} vs. {trgt_object.database}.{trgt_object.schema}.{trgt_object.name}")

            src_filter, trgt_filter, exclude_columns = get_additional_configuration(src_object, testing_tool_params)

            comparison_service=ComparisonService(src_object, trgt_object, db_service_src, db_service_trgt, src_filter, trgt_filter, exclude_columns, comp_id)

            #####################################################################
            # execute comparison

            comparison_service.row_count_comparison()
            comparison_service.column_names_comparison()
            comparison_service.aggregation_comparison()
            if testing_tool_params.execute_group_by_comparison:
                comparison_service.group_by_comparison()
            comparison_service.sample_comparison()
            comparison_service.pandas_dataframe_comparison()

            #####################################################################
            # TODO as function - check if the object was changed during comparison

            ### structure of output needs to be adjusted to enable comparison using > in the if statements
            ### florian said the feature is not too important for now, so it's being skipped for now

            # comparison_service.result_params.last_altered_src = db_service_src.get_last_altered_timestamp_from_object(src_object)
            # last_altered_trgt = db_service_trgt.get_last_altered_timestamp_from_object(trgt_object)

            # if comparison_service.result_params.last_altered_src>start_time_utc:
            #     comparison_service.result_params.not_altered_during_comparison_src = False

            # if last_altered_trgt>start_time_utc:
            #     comparison_service.result_params.not_altered_during_comparison_trgt = False

            #####################################################################
            # prepare column level results

            comparison_service.result_params.all_count_nulls_equal = True
            comparison_service.result_params.datatypes_equal = True
            column_level_comparison_results = []

            for column in comparison_service.result_params.all_columns_trgt_src:

                column_level_comparison_result=ResultService.prepare_column_level_result(column, exclude_columns, comparison_service.result_params)

                if column_level_comparison_result["COUNT_NULLS_EQUAL"] is False:
                    comparison_service.result_params.all_count_nulls_equal = False
                if column_level_comparison_result["DATATYPE_EQUAL"] is False:
                    comparison_service.result_params.datatypes_equal = False


                column_level_comparison_results.append(column_level_comparison_result)

            #####################################################################
            # prepare object level result

            object_level_comparison_result = ResultService.prepare_object_level_result(
                src_object,
                trgt_object,
                src_filter,
                trgt_filter,
                exclude_columns,
                comparison_service.result_params,
                column_level_comparison_results
            )

            object_level_comparison_results.append(object_level_comparison_result)

            #####################################################################
            # prepare and upload live result of the current object

            live_object_level_comparison_result = ResultService.prepare_object_level_live_result(
                    object_level_comparison_result,
                    testing_tool_params,
                )

            # TODO write as function
            if testing_tool_params.upload_result_to_result_database and not (testing_tool_params.upload_result_to_result_database =='upload_result_to_result_database env variable not found' or testing_tool_params.upload_result_to_result_database =='False'):

                stage_name = f'{testing_tool_params.result_database_name}.{testing_tool_params.stage_schema}."STG_LIVE_{src_object.schema}_{src_object.name}_{testing_tool_params.run_guid}"'

                result_file_name = f"{src_object.schema}_{src_object.name}.json"

                result_file_path = testing_tool_params.live_result_folder_path.joinpath(PurePath(result_file_name))

                write_json_to_file(live_object_level_comparison_result, result_file_path)

                # TODO handle result systems other than Snowflake
                if testing_tool_params.systems[testing_tool_params.result_system_selection]["DATABASE_TYPE"] == 'snowflake':

                    db_service_result.upload_to_stage(stage_name, testing_tool_params.live_result_folder_path, result_file_name, False)

                    db_service_result.insert_json_results_live(testing_tool_params.run_guid, testing_tool_params.pipeline_name, testing_tool_params.pipeline_id, testing_tool_params.result_live_table, stage_name, testing_tool_params.source_system_selection, testing_tool_params.target_system_selection, testing_tool_params.database_name, src_object.schema, src_object.name)

            end_time_object_comparison_ = time.time()
            #####################################################################
            # object level result log

            # TODO write as function
            logger.info('****************************************************')
            logger.info(f"++++++++++++++++ [{comp_id}] Comparison Result: {comp_id} of {len(objects_to_compare)} ++++++++++++++++")
            logger.info(f"[{comp_id}] Source object => {object['src_object_identifier']}")
            logger.info(f"[{comp_id}] Target object => {object['trgt_object_identifier']}")
            logger.info(f"[{comp_id}] --- Comparison Time ---> {round(end_time_object_comparison_ - start_time_object_comparison_, 2)} s")
            if  comparison_service.result_params.row_counts_equal:
                logger.info(f"[{comp_id}] --- Row counts --------> EQUAL")
            else:
                logger.info(f"[{comp_id}] --- Row counts --------> NOT equal")
                logger.info(f"[{comp_id}]                          Source row count: {comparison_service.result_params.src_row_count}. Target row count: {comparison_service.result_params.trgt_row_count}")

            if len(comparison_service.result_params.src_columns_upper) != len(set(comparison_service.result_params.src_columns_upper)):
                logger.info(f"[{comp_id}] --- Duplicates in the source column names -> The source system seems to be case sensitive.")

            if len(comparison_service.result_params.trgt_columns_upper) != len(set(comparison_service.result_params.trgt_columns_upper)):
                logger.info(f"[{comp_id}] --- Duplicates in the target column names -> The target system seems to be case sensitive.")

            if comparison_service.result_params.columns_equal:
                logger.info(f"[{comp_id}] --- Column names ------> EQUAL")
            else:
                logger.info(f"[{comp_id}] --- Column names ------> NOT equal")
                logger.info(f"[{comp_id}]                          src_minus_trgt {comparison_service.result_params.src_columns_minus_trgt_columns} and trgt_minus_src {comparison_service.result_params.trgt_columns_minus_src_columns}")

            if comparison_service.result_params.datatypes_equal:
                logger.info(f"[{comp_id}] --- Data Types --------> EQUAL")
            else:
                logger.info(f"[{comp_id}] --- Data Types --------> NOT equal")

            if not comparison_service.result_params.aggregations_compared:
                logger.info(f"[{comp_id}] --- Aggregations ------> NOT compared")
            elif comparison_service.result_params.aggregations_equal:
                logger.info(f"[{comp_id}] --- Aggregations ------> EQUAL")
            else:
                logger.info(f"[{comp_id}] --- Aggregations ------> NOT equal")

            if not comparison_service.result_params.object_group_by_columns:
                logger.info(f"[{comp_id}] --- Group-By ----------> NOT compared")
            elif comparison_service.result_params.group_by_equal:
                logger.info(f"[{comp_id}] --- Group-By ----------> EQUAL")
            else:
                logger.info(f"[{comp_id}] --- Group-By ----------> NOT equal")

            if not comparison_service.result_params.samples_compared:
                logger.info(f"[{comp_id}] --- Samples -----------> NOT compared")
            elif comparison_service.result_params.samples_equal:
                logger.info(f"[{comp_id}] --- Samples -----------> EQUAL")
            else:
                logger.info(f"[{comp_id}] --- Samples -----------> NOT equal")

            if not comparison_service.result_params.pandas_df_compared:
                logger.info(f"[{comp_id}] --- Pandas Dataframes -> NOT compared")
                logger.info(f"[{comp_id}]                       -> src_tbl_size: {comparison_service.result_params.src_tbl_size} trgt_tbl_size:{comparison_service.result_params.trgt_tbl_size} max_object_size {testing_tool_params.max_object_size}")
                logger.info(f"[{comp_id}]                       -> src_row_count: {comparison_service.result_params.src_row_count} trgt_row_count:{comparison_service.result_params.trgt_row_count} max_row_number {testing_tool_params.max_row_number}")
            elif comparison_service.result_params.pandas_df_is_equal:
                logger.info(f"[{comp_id}] --- Pandas Dataframes -> EQUAL")

            else:
                logger.info(f"[{comp_id}] --- Pandas Dataframes -> NOT equal")
            logger.info('****************************************************')

    return object_level_comparison_results
