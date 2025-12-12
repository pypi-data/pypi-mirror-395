#########################################################################################
#########################################################################################

import logging
import os
import sys
import time
import warnings
from datetime import datetime

##############################
# Append the list of python system paths with the current working directory.
# Is needed for remote runs of the pipeline, such that, python looks for modules to load in the current working directory.
current_working_dir = os.getcwd()
sys.path.append(current_working_dir)
##############################
# Ignore Userwarning
warnings.simplefilter("ignore", UserWarning)
##############################

import icsDataValidation.utils.parallelization_util as parallelization_util

from icsDataValidation.input_parameters.testing_tool_params import TestingToolParams
from icsDataValidation.services.system_service import SystemService
from icsDataValidation.services.testset_service import TestsetService
from icsDataValidation.services.initialization_service import InitializationService
from icsDataValidation.services.result_service import ResultService
from icsDataValidation.core.object_comparison import compare_objects
from icsDataValidation.utils.file_util import load_json
from icsDataValidation.utils.logger_util import configure_dev_ops_logger

#########################################################################################
#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger('Testing_Tool')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

def execute():

    #########################################################################################
    logger.info('****************************************************\n')
    logger.info(f"++++++++++++++++ INITIALIZE icsDataValidation")

    start_time_utc = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")

    initialization_service = InitializationService(TestingToolParams, current_working_dir, start_time_utc)

    config_file_path, migration_config_file_path = initialization_service.get_config_file_paths()

    #########################################################################################
    logger.info(f"++++++++++++++++ LOAD setup_config.json")

    for configs_key, configs_value in load_json(config_file_path).items():
        setattr(TestingToolParams, configs_key, configs_value)

    initialization_service.create_list_of_testset_file_names()

    initialization_service.create_result_table_identifiers()

    testset_file_paths = initialization_service.get_testset_file_paths()

    initialization_service.create_result_file_paths()

    initialization_service.create_live_result_file_path()

    initialization_service.create_remaining_mapping_objects_file_path()

    #########################################################################################
    logger.info(f"++++++++++++++++ LOAD migration_config.json")

    migration_configs=load_json(migration_config_file_path)

    try:
        TestingToolParams.migration_config=migration_configs[f"{TestingToolParams.source_system_selection}_{TestingToolParams.target_system_selection}"]
    except KeyError as error:
        logger.warning("The source and target database of this setup do not match with any information in the migration_config.json")
        logger.info(f"##vso[task.complete result=SucceededWithIssues ;]DONE")
        TestingToolParams.migration_config=None

    #########################################################################################
    logger.info(f"++++++++++++++++ INITIALIZE TestsetService")

    if TestingToolParams.migration_config:
        try:
            testset_service=TestsetService(TestingToolParams.migration_config["MAPPING"],TestingToolParams.migration_config["BLACKLIST"],testset_file_paths)
        except KeyError as error:
            raise ValueError(f"TestsetService could not be initialized. Check wether the migration_config contains the 'MAPPING' key and the 'BLACKLIST' key. {error}")
    else:
        raise ValueError("migration_config not found!")

    #########################################################################################
    logger.info(f"++++++++++++++++ HANDLE database mapping")

    target_database_name = testset_service.handle_database_mapping(TestingToolParams.database_name)

    #########################################################################################
    logger.info(f"++++++++++++++++ HANDLE schema mapping and schema replace mapping")

    if TestingToolParams.schema_name:
        target_schema_name, found_schema_mapping = testset_service.handle_schema_mapping(TestingToolParams.schema_name, TestingToolParams.database_name)
        if not found_schema_mapping:
            target_schema_name = testset_service.handle_schema_replace_mapping(TestingToolParams.schema_name)
    else:
        target_schema_name = TestingToolParams.schema_name

    #########################################################################################
    logger.info('\n****************************************************\n')
    logger.info('++++++++++++++++ Input Parameters ++++++++++++++++')
    logger.info(f"Source System Selection: {TestingToolParams.source_system_selection}")
    logger.info(f"Target System Selection: {TestingToolParams.target_system_selection}")
    logger.info(f"Source Database Name: {TestingToolParams.database_name}")
    logger.info(f"Target Database Name: {target_database_name}")
    logger.info(f"Source Schema Name: {TestingToolParams.schema_name}")
    logger.info(f"Target Schema Name: {target_schema_name}")
    logger.info(f"Source System Config: {TestingToolParams.systems[TestingToolParams.source_system_selection]}")
    logger.info(f"Target System Config: {TestingToolParams.systems[TestingToolParams.target_system_selection]}")
    logger.info('\n****************************************************\n')

    #################################################################################################################
    logger.info(f"++++++++++++++++ INITIALIZE SystemService for source- and target-system")

    source_system=SystemService(TestingToolParams.source_system_selection,TestingToolParams.systems)
    target_system=SystemService(TestingToolParams.target_system_selection,TestingToolParams.systems)

    TestingToolParams.connection_params_src=source_system.get_connection_params()
    TestingToolParams.connection_params_trgt=target_system.get_connection_params()

    database_service_src=source_system.initialize_database_service(TestingToolParams.connection_params_src)
    database_service_trgt=target_system.initialize_database_service(TestingToolParams.connection_params_trgt)

    #########################################################################################
    logger.info(f"++++++++++++++++ GET database_objects")
    with database_service_src as db_service_src, database_service_trgt as db_service_trgt:

        database_objects_src= db_service_src.get_database_objects(TestingToolParams.database_name, TestingToolParams.schema_name, TestingToolParams.object_type_restriction)
        database_objects_trgt= db_service_trgt.get_database_objects(target_database_name, target_schema_name, TestingToolParams.object_type_restriction)

    #########################################################################################
    logger.info(f"++++++++++++++++ HANDLE blacklist")

    if testset_service.testset_blacklist and any(testset_service.testset_blacklist.values()):

        database_objects_src=testset_service.handle_blacklist(database_objects_src, "SRC")
        database_objects_trgt=testset_service.handle_blacklist(database_objects_trgt, "TRGT")

    #########################################################################################
    logger.info(f"++++++++++++++++ HANDLE whitelist")

    if testset_service.testset_whitelist and any(testset_service.testset_whitelist.values()):

        database_objects_src=testset_service.handle_whitelist(database_objects_src, "SRC")
        database_objects_trgt=testset_service.handle_whitelist(database_objects_trgt, "TRGT")

    #########################################################################################
    logger.info(f"++++++++++++++++ HANDLE object mapping")#
    database_objects_src=sorted(database_objects_src, key=lambda d: d["object_identifier"])
    database_objects_trgt=sorted(database_objects_trgt, key=lambda d: d["object_identifier"])

    (
        intersection_objects_mapped_trgt_src,
        object_identifiers_src_minus_trgt,
        object_identifiers_trgt_minus_src,
        remaining_mapping_objects,
        all_objects_matching
    ) = testset_service.map_objects(database_objects_src, database_objects_trgt)

    #########################################################################################
    logger.info(f"++++++++++++++++ GET objects_to_compare")#

    objects_to_compare=testset_service.get_intersection_objects_trgt_src(database_objects_src, database_objects_trgt, intersection_objects_mapped_trgt_src)

    object_identifiers_to_compare_src = [object["src_object_identifier"] for object in objects_to_compare]

    object_identifiers_to_compare_trgt = [object["trgt_object_identifier"] for object in objects_to_compare]

    #########################################################################################
    logger.info('\n****************************************************\n')
    logger.info(f"++++++++++++++++ INITIALIZE comparison for {len(objects_to_compare)} objects")

    start_time_object_comparison = time.time()

    if TestingToolParams.max_number_of_threads<=1:
        object_level_comparison_results=compare_objects(TestingToolParams, objects_to_compare)
    else:
        object_level_comparison_results=parallelization_util.execute_func_in_parallel(compare_objects, objects_to_compare, TestingToolParams.max_number_of_threads, TestingToolParams)

    end_time_object_comparison = time.time()

    logger.info(f"++++++++++++++++ END of object comparison - Execution Time: {round(end_time_object_comparison - start_time_object_comparison, 2)} s")
    logger.info('****************************************************\n')

    #########################################################################################
    logger.info(f"++++++++++++++++ INITIALIZE ResultService")

    result_service=ResultService(
            start_time_utc,
            remaining_mapping_objects,
            object_identifiers_src_minus_trgt,
            object_identifiers_trgt_minus_src,
            object_identifiers_to_compare_src,
            object_identifiers_to_compare_trgt,
            objects_to_compare,
            all_objects_matching,
            object_level_comparison_results
        )

    result_service.determine_highlevel_results()

    result_service.write_results_to_git()

    if TestingToolParams.upload_result_to_blob:
        result_service.upload_json_result_to_blob(start_time_utc)

    if TestingToolParams.upload_result_to_bucket:
        result_service.upload_json_result_to_bucket(start_time_utc)

    if TestingToolParams.upload_result_to_result_database:
        result_service.load_results_to_result_database()

    #########################################################################################


if __name__ == "__main__":
    execute()
