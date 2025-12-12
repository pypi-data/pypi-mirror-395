import logging
import os

from pathlib import PurePath

from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.input_parameters.testing_tool_params import TestingToolParams

#########################################################################################
# Configure Dev Ops Logger

logger = logging.getLogger('InitializationService')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

#########################################################################################
#########################################################################################

class InitializationService:
    """
    Class to initialize the icsDataValidation Tool with the input parameters.
    Process the TestingToolParams.
    Extend the TestingToolParams with additional parameters.
    """

    def __init__(self, testing_tool_params: TestingToolParams, current_working_dir: str, start_time_utc: str):
        self.testing_tool_params = testing_tool_params
        self.current_working_dir = current_working_dir
        self.start_time_utc = start_time_utc

    def create_list_of_testset_file_names(self):
        """
        Create list of testset file names.
        """
        if self.testing_tool_params.testset_file_names and not self.testing_tool_params.testset_file_names == 'testset_file_names env variable not found' and not self.testing_tool_params.testset_file_names =='null':
            self.testing_tool_params.testset_file_names = [testset_file_name.strip() for testset_file_name in self.testing_tool_params.testset_file_names.split(',') ]
        else:
            self.testing_tool_params.testset_file_names = []
        
    def create_result_table_identifiers(self):
        """
        Create result table identifiers from result database, result schema, and result table names.
        """
        self.testing_tool_params.result_table = f"{self.testing_tool_params.result_database_name}.{self.testing_tool_params.result_meta_data_schema_name}.{self.testing_tool_params.result_table_name}"         
        self.testing_tool_params.result_table_highlevel = f"{self.testing_tool_params.result_database_name}.{self.testing_tool_params.result_schema_name}.{self.testing_tool_params.result_table_highlevel_name}"           
        self.testing_tool_params.result_table_objectlevel  = f"{self.testing_tool_params.result_database_name}.{self.testing_tool_params.result_schema_name}.{self.testing_tool_params.result_table_objectlevel_name}"        
        self.testing_tool_params.result_table_columnlevel   = f"{self.testing_tool_params.result_database_name}.{self.testing_tool_params.result_schema_name}.{self.testing_tool_params.result_table_columnlevel_name}"

    def get_config_file_paths(self):
        """
        Create config file paths independent of operation system and append the currenct working directory to the paths.
        Get migration config file path and database config file path.
        """
        config_folder_path = PurePath(self.current_working_dir).joinpath(PurePath(self.testing_tool_params.config_folder_name))
        config_file_path = config_folder_path.joinpath(PurePath(self.testing_tool_params.configuration_file_name))
        migration_config_file_path = config_folder_path.joinpath(PurePath(self.testing_tool_params.migration_configuration_file_name))
        
        return config_file_path, migration_config_file_path
    
    def get_testset_file_paths(self):
        """
        Get testset file paths independent of operation system and append the currenct working directory to the paths.
        """
        testset_folder_path = PurePath(self.current_working_dir).joinpath(PurePath(self.testing_tool_params.testset_folder_name))
        testset_file_paths = []
        for testset_file_name in self.testing_tool_params.testset_file_names:
            
            testset_file_paths.append(testset_folder_path.joinpath(PurePath(testset_file_name)))

        return testset_file_paths
    
    def create_result_file_paths(self):
        """
        Create result file paths independent of operation system and append the currenct working directory to the paths.
        Create result folder path, result file name, result file path, and stage_name.
        """

        self.testing_tool_params.result_folder_path = PurePath(self.current_working_dir).joinpath(PurePath(self.testing_tool_params.result_folder_name))
        self.testing_tool_params.result_file_name = f"Comparison_Result_{self.testing_tool_params.source_system_selection}_{self.testing_tool_params.target_system_selection}_{self.testing_tool_params.database_name}_{self.start_time_utc}.json"
        self.testing_tool_params.result_file_path = self.testing_tool_params.result_folder_path.joinpath(PurePath(self.testing_tool_params.result_file_name))
        self.testing_tool_params.stage_name = f'{self.testing_tool_params.result_database_name}.{self.testing_tool_params.stage_schema}."{self.testing_tool_params.stage_name_prefix}_{self.testing_tool_params.run_guid}"'

    def create_live_result_file_path(self):
        """
        Create live result file paths independent of operation system and append the currenct working directory to the paths.
        Create live result folder if it does not exist.
        """

        self.testing_tool_params.live_result_folder_path = self.testing_tool_params.result_folder_path.joinpath(PurePath(f"Live_Result_{self.testing_tool_params.source_system_selection}_{self.testing_tool_params.target_system_selection}_{self.testing_tool_params.database_name}_{self.start_time_utc}"))

        if not os.path.exists(self.testing_tool_params.live_result_folder_path):
            os.makedirs(self.testing_tool_params.live_result_folder_path) 

        self.testing_tool_params.result_live_table = f"{self.testing_tool_params.result_database_name}.{self.testing_tool_params.result_meta_data_schema_name}.{self.testing_tool_params.result_live_table_name}"

    def create_remaining_mapping_objects_file_path(self):
        """
        Create live remaining mapping objects file path independent of operation system and append the currenct working directory to the path.
        """

        remaining_mapping_objects_folder_path = PurePath(self.current_working_dir).joinpath(PurePath(self.testing_tool_params.remaining_mapping_objects_folder_name))
        remaining_mapping_objects_file_name = f"Remaining_Mapping_Objects_{self.testing_tool_params.database_name}_{self.start_time_utc}.json"
        self.testing_tool_params.remaining_mapping_objects_file_path = remaining_mapping_objects_folder_path.joinpath(PurePath(remaining_mapping_objects_file_name))