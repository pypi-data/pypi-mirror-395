import os

from cloe_util_snowflake_connector.connection_parameters import ConnectionParameters, EnvVariablesInitializer

#########################################################################################
#########################################################################################


def load_snowflake_credentials(system_configs: dict, system_selection: str) -> ConnectionParameters:
    snowflake_params = EnvVariablesInitializer(
        user=system_configs[system_selection]["USER"],
        account=system_configs[system_selection]["ACCOUNT"],
        warehouse=system_configs[system_selection]["WAREHOUSE"],
        database=system_configs[system_selection]["DATABASE"],
        role=system_configs[system_selection]["ROLE"],
        password=os.getenv(system_configs[system_selection]["PASSWORD_NAME"])
        if "PASSWORD_NAME" in system_configs[system_selection]
        else None,
        private_key=os.getenv(system_configs[system_selection]["PRIVATE_KEY_NAME"])
        if "PRIVATE_KEY_NAME" in system_configs[system_selection]
        else None,
        private_key_passphrase=os.getenv(system_configs[system_selection]["PRIVATE_KEY_PASSPHRASE_NAME"])
        if "PRIVATE_KEY_PASSPHRASE_NAME" in system_configs[system_selection]
        else None,
        private_key_file=os.getenv(system_configs[system_selection]["PRIVATE_KEY_FILE_PATH"])
        if "PRIVATE_KEY_FILE_PATH" in system_configs[system_selection]
        else None,
        private_key_file_pwd=os.getenv(system_configs[system_selection]["PRIVATE_KEY_FILE_PASSWORD"])
        if "PRIVATE_KEY_FILE_PASSWORD" in system_configs[system_selection]
        else None,
    )

    connection_params = ConnectionParameters(**snowflake_params.model_dump())

    return connection_params
