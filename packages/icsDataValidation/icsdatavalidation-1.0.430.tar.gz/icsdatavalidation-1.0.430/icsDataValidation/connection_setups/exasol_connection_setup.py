import os

from dotenv import load_dotenv
from pathlib import Path

#########################################################################################
#########################################################################################

def load_exasol_credentials(system_configs:dict,system_selection:str)->dict:

    exasol_params = {
        "dsn"       : system_configs[system_selection]["DSN"],
        "user"      : system_configs[system_selection]["USER"],
        "password"  : os.getenv(system_configs[system_selection]["PASSWORD_NAME"])
    }

    return exasol_params