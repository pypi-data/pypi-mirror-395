import os

from dotenv import load_dotenv
from pathlib import Path

#########################################################################################
#########################################################################################

def load_teradata_credentials(system_configs:dict,system_selection:str)->dict:

    teradata_params = {
        "host"   : system_configs[system_selection]["HOST"],
        "user"      : system_configs[system_selection]["USER"],
        "password"  : os.getenv(system_configs[system_selection]["PASSWORD_NAME"]),
        "dbs_port"  : '1025'
    }

    return teradata_params