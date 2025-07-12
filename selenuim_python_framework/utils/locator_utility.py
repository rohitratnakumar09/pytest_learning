import json
import logging
import os
import utils.logger_utility as log_utils
from common.constants import *

class Locators:
    log = log_utils.custom_logger(logging.INFO)

    def __init__(self,page_cls):
        self.page_cls = page_cls
        locator_dir = os.path.join(PROJECT_ROOT, "locators_repo")
        loc_web_repo_dir = os.path.join(os.getenv("TEST_FOLDER"), self.page_cls.__name__ + ".json")
        self.filename = os.path.join(locator_dir, loc_web_repo_dir)

    def read_json(self):
        """
        Read and parse the locator JSON file for the page class.
        :return: Parsed JSON data or None if error occurs.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as fh:
                return json.load(fh)
        except Exception as e:
            self.log.error(f"Failed to read locator JSON file at {self.filename}. Exception: {e}")
            return None

    def page_locators(self, locator_name, **kwargs):
        """
        Retrieve locator tuple (locate, locator_value) for a given locator name.
        Supports dynamic locators with string formatting if 'is_dynamic' is True.
        :param locator_name: Name of the locator to retrieve.
        :param kwargs: Dynamic values for formatting the locator string.
        :return: Tuple (locate, locator_value) or None if not found.
        """
        locator_json_data = self.read_json()
        if not locator_json_data:
            self.log.error(f"No locator data found for {self.filename}")
            return None
        for locator in locator_json_data:
            if locator.get('name') == locator_name:
                is_dynamic = locator.get("is_dynamic", False)
                try:
                    locator_value = locator['locator'].format(**kwargs) if is_dynamic else locator['locator']
                except Exception as e:
                    self.log.error(f"Failed to format locator '{locator_name}' with args {kwargs}. Exception: {e}")
                    return None
                return locator['locate'], locator_value
        self.log.error(f"Locator '{locator_name}' not found in {self.filename}")
        return None
