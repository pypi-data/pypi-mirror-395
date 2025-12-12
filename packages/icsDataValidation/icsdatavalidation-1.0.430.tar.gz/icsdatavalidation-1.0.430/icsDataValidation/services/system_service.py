from icsDataValidation.connection_setups.snowflake_connection_setup import load_snowflake_credentials
from icsDataValidation.connection_setups.exasol_connection_setup import load_exasol_credentials
from icsDataValidation.connection_setups.azure_connection_setup import load_azure_credentials
from icsDataValidation.connection_setups.sqlserver_connection_setup import load_sqlserver_credentials
from icsDataValidation.connection_setups.teradata_connection_setup import load_teradata_credentials
from icsDataValidation.connection_setups.oracle_connection_setup import load_oracle_credentials
from icsDataValidation.connection_setups.databricks_connection_setup import load_databricks_credentials
from icsDataValidation.services.database_services.snowflake_service import SnowflakeService
from icsDataValidation.services.database_services.teradata_service import TeradataService
from icsDataValidation.services.database_services.exasol_service import ExasolService
from icsDataValidation.services.database_services.azure_service import AzureService
from icsDataValidation.services.database_services.sqlserver_service import SQLServerService
from icsDataValidation.services.database_services.oracle_service import OracleService
from icsDataValidation.services.database_services.databricks_hive_metastore_service import DatabricksHiveMetastoreService
from icsDataValidation.services.database_services.databricks_unity_catalog_service import DatabricksUnityCatalogService

#########################################################################################
#########################################################################################

class SystemService:
    """
    Class to initialize database services dependent on the system selection.
    """

    def __init__(self, system_selection: str, database_config: dict):
        self.database_config = database_config
        self.system_selection = system_selection
        self.system_type = database_config[system_selection]["DATABASE_TYPE"].upper()

    def get_connection_params(self):
        """
        Get the connection parameters dependent on the system type.
        """
        credentials_function_mapping = {
            "SNOWFLAKE": load_snowflake_credentials,
            "EXASOL": load_exasol_credentials,
            "AZURE": load_azure_credentials,
            "SQLSERVER": load_sqlserver_credentials,
            "TERADATA": load_teradata_credentials,
            "ORACLE": load_oracle_credentials,
            "DATABRICKS_HIVE_METASTORE": load_databricks_credentials,
            "DATABRICKS_UNITY_CATALOG": load_databricks_credentials,
        }

        connection_params = credentials_function_mapping[self.system_type](
            self.database_config, self.system_selection
        )
        return connection_params

    def initialize_database_service(self, connection_params: dict):
        """
        Initialize the database service dependent on the system type.
        """
        database_service_mapping = {
            "SNOWFLAKE": SnowflakeService,
            "EXASOL": ExasolService,
            "AZURE": AzureService,
            "SQLSERVER": SQLServerService,
            "TERADATA": TeradataService,
            "ORACLE": OracleService,
            "DATABRICKS_HIVE_METASTORE": DatabricksHiveMetastoreService,
            "DATABRICKS_UNITY_CATALOG": DatabricksUnityCatalogService,
        }
        database_service = database_service_mapping[self.system_type](connection_params)
        return database_service
