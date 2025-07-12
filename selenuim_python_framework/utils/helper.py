import inspect
import json
import logging
import os
import os.path
from configparser import ConfigParser
import utils.logger_utility as log_utils
from common.constants import *

log = log_utils.custom_logger(logging.INFO)

def parse_json(filepath):
    """
    Parse a JSON file and return its contents as a Python object.
    :param filepath: Path to the JSON file.
    :return: Parsed JSON data or None if error occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception as e:
        log.error(f"Failed to parse the JSON file at {filepath}. Exception: {e}")
        return None

def get_test_data(test_cls):
    """
    Retrieve test data for a given test class from a JSON file in the data directory.
    :param test_cls: The test class object.
    :return: Parsed JSON data or None if error occurs.
    """
    try:
        current_file = inspect.getfile(test_cls)
        data_file_path = os.path.dirname(os.path.dirname(current_file) + "/data/")
        return  parse_json(os.path.join(data_file_path, test_cls.__name__))
    except Exception as e:
        log.error(f"Failed to get test data for {test_cls.__name__}. Exception: {e}")
        return None

class ConfigUtility:
    """
    This class includes basic reusable config_helpers.
    """
    log = log_utils.custom_logger(logging.INFO)
    def __init__(self, config_name):
        config_dir = os.path.join(PROJECT_ROOT, "config")
        self.config_path = os.path.join(config_dir, f'{config_name}.ini')

    def load_config_file(self):
        """
        This method loads the config/ini file
        :return: this method returns config reader instance.
        """
        config = None
        try:
            config = ConfigParser()
            config.read(self.config_path)
        except Exception as ex:
            self.log.error("Failed to load ini/properties file.", ex)
        return config
