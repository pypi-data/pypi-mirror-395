#########################################################################################
#########################################################################################

from databricks.sdk.core import Config, oauth_service_principal
import os

def load_databricks_credentials(database_configs: dict, system_selection: str) -> dict:

    if "DBX_ACCESS_TOKEN_NAME" in database_configs[system_selection]:
        # personal access token authentication
        access_token = os.getenv(database_configs[system_selection]["DBX_ACCESS_TOKEN_NAME"])
    else:
        # OAuth machine-to-machine (M2M) authentication
        ad_config = {
            "tenant_id": database_configs[system_selection]["TENANT_ID"],
            "client_id": database_configs[system_selection]["CLIENT_ID"],
            "client_secret": os.getenv(database_configs[system_selection]["CLIENT_SECRET"]),
        }

        access_token=oauth_service_principal(Config(ad_config))

    databricks_params = {
        "server_hostname": database_configs[system_selection]["SERVER_HOSTNAME"],
        "http_path": database_configs[system_selection]["CLUSTER_HTTP_PATH"],
        "access_token": access_token
    }

    return databricks_params
