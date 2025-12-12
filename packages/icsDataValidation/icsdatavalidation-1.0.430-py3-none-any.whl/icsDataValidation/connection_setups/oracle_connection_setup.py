import os
import oracledb

from dotenv import load_dotenv
from pathlib import Path

#########################################################################################
#########################################################################################

def load_oracle_credentials(system_configs:dict,system_selection:str)->dict:

    oracle_params = {
        "user"   : system_configs[system_selection]["USERNAME"],
        "dsn"      : system_configs[system_selection]["DSN"],
        "port" : system_configs[system_selection]["PORT"],
        "password"  : os.getenv(system_configs[system_selection]["PASSWORD_NAME"])
    }

    if "SERVICE_NAME" in system_configs[system_selection]:
        oracle_params["service_name"] = system_configs[system_selection]["SERVICE_NAME"]

    if "MODE" in system_configs[system_selection]:
        mode = system_configs[system_selection]["MODE"]
        oracle_params["mode"] = getattr(oracledb, mode)

    return oracle_params