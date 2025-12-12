#########################################################################################
#########################################################################################

import os
import uuid

from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path, PurePath


#########################################################################################
#########################################################################################

@dataclass
class TestingToolParams:

    pipeline_id: str                            = os.environ.get('BUILD_BUILDNUMBER')
    pipeline_name: str                          = os.environ.get('BUILD_DEFINITIONNAME','build_definitionname env variable not found')

    #########################################################################################

    # manual execution load input parameters
    if pipeline_id is None:
        from examples.manual_execution_params import manual_execution_params

        pipeline_name = 'manual'

        manual_execution_params()

        env_filepath: str = os.environ.get('ENV_FILEPATH', 'env_filepath env variable not found')

        # load in env variables from local file (e.g. passwords or azure blob storage connection string )
        _ = load_dotenv(dotenv_path=(PurePath(Path.home()).joinpath(PurePath(env_filepath))), override=True)

    #########################################################################################
    config_folder_name:str                      = os.environ.get('CONFIG_FOLDER_NAME', 'CONFIG FOLDER NAME env variable not found')
    configuration_file_name:str                 = os.environ.get('CONFIGURATION_FILE_NAME', 'DATABASE CONFIGURATION FILE NAME env variable not found')
    migration_configuration_file_name: str      = os.environ.get('MIGRATION_CONFIGURATION_FILE_NAME', 'MIGRATION CONFIGURATION FILE NAME env variable not found')

    database_name: str                          = None if os.environ.get('DATABASE_NAME','Database name env variable not found') == 'null' else os.environ.get('DATABASE_NAME','Database name env variable not found')
    schema_name: str                            = None if os.environ.get('SCHEMA_NAME','Target schema name env variable not found') == 'null' else os.environ.get('SCHEMA_NAME','Target schema name env variable not found')
    testset_file_names: str                     = os.environ.get('TESTSET_FILE_NAMES','testset_file_names env variable not found')
    object_type_restriction: str                = os.environ.get('OBJECT_TYPE_RESTRICTION','object_type_restriction env variable not found')
    azure_devops_pipeline: bool                 = True if os.environ.get('AZURE_DEVOPS_PIPELINE','azure_devops_pipeline env variable not found') == 'True' else False
    gitlab_pipeline: bool                       = True if os.environ.get('GITLAB_PIPELINE','gitlab_pipeline env variable not found') == 'True' else False
    upload_result_to_blob: bool                 = True if os.environ.get('UPLOAD_RESULT_TO_BLOB','upload_result_to_blob env variable not found') == 'True' else False
    upload_result_to_bucket: bool               = True if os.environ.get('UPLOAD_RESULT_TO_BUCKET','upload_result_to_bucket env variable not found') == 'True' else False
    upload_result_to_result_database: bool      = True if os.environ.get('UPLOAD_RESULT_TO_RESULT_DATABASE','upload_result_to_result_database env variable not found') == 'True' else False
    max_object_size: int                        = int(os.environ.get('MAX_OBJECT_SIZE','max_object_size env variable not found'))
    max_row_number: int                         = int(os.environ.get('MAX_ROW_NUMBER','max_row_number env variable not found'))
    max_number_of_threads: int                  = int(os.environ.get('MAX_NUMBER_OF_THREADS','max_number_of_threads env variable not found'))
    execute_group_by_comparison: bool           = True if os.environ.get('EXECUTE_GROUP_BY_COMPARISON','execute_group_by_comparison env variable not found') == 'True' else False
    use_group_by_columns: bool                  = True if os.environ.get('USE_GROUP_BY_COLUMNS','use_group_by_columns env variable not found') == 'True' else False
    min_group_by_count_distinct: int            = int(os.environ.get('MIN_GROUP_BY_COUNT_DISTINCT','min_group_by_count_distinct env variable not found'))
    max_group_by_count_distinct: int            = int(os.environ.get('MAX_GROUP_BY_COUNT_DISTINCT','max_group_by_count_distinct env variable not found'))
    max_group_by_size: int                      = int(os.environ.get('MAX_GROUP_BY_SIZE','max_group_by_size env variable not found'))
    numeric_scale: int                          = int(os.environ.get('NUMERIC_SCALE','numeric_scale env variable not found'))
    enclose_column_by_double_quotes: bool       = True if os.environ.get('ENCLOSE_COLUMN_BY_DOUBLE_QUOTES','enclose_column_by_double_quotes env variable not found') == 'True' else False
    branch_name: str                            = os.environ.get('BRANCH_NAME', 'branch_name env variable not found')
    source_branch:str                           = os.environ.get('BUILD_SOURCEBRANCH', 'build_sourcebranch env variable not found')
    azure_storage_connection_string: str        = os.environ.get('AZURE_STORAGE_CONNECTION_STRING','azure_storage_connection_string env variable not found')
    aws_bucket_access_key: str                  = os.environ.get('AWS_BUCKET_ACCESS_KEY', 'aws_bucket_access_key env variable not found')
    aws_bucket_secret_key: str                  = os.environ.get('AWS_BUCKET_SECRET_KEY', 'aws_bucket_secret_key env variable not found')
    run_guid: str                               = str(uuid.uuid4())
    testatm_access_token: str                   = os.environ.get('TESTATM_ACCESS_TOKEN', 'testatm_access_token env variable not found')
    gitlab_ci_server_host: str                  = os.environ.get('GITLAB_CI_SERVER_HOST', 'gitlab_ci_server_host env variable not found')
    gitlab_ci_project_path: str                 = os.environ.get('GITLAB_CI_PROJECT_PATH', 'gitlab_ci_project_path env variable not found')


    #########################################################################################

    if max_object_size != 'max_object_size env variable not found':
        max_object_size=int(max_object_size)
    if max_row_number != 'max_row_number env variable not found':
        max_row_number=int(max_row_number)
    if max_number_of_threads != 'max_number_of_threads env variable not found':
        max_number_of_threads=int(max_number_of_threads)
    if min_group_by_count_distinct != 'min_group_by_count_distinct env variable not found':
        min_group_by_count_distinct=int(min_group_by_count_distinct)
    if max_group_by_count_distinct != 'max_group_by_count_distinct env variable not found':
        max_group_by_count_distinct=int(max_group_by_count_distinct)
