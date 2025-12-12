import os
from typing import Dict, List, Union

import utils.file_util as file_util

class icsDataValidationConfig(object):
    """
    Holds icsDataValidation config.
    """

    def __init__(self):
        """ """
        self.module_root_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.config_path = os.environ.get("ICSDATAVALIDATION_CONFIG_PATH")

        self.config_dict = file_util.load_json(self.config_path)