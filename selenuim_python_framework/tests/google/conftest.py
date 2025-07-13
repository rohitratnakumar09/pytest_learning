import os
import pytest
from common.constants import *
from utils.helper import ConfigUtility
from utils.driver_utility import WebDriver


@pytest.fixture(scope="session")
def configs():
    """
    Load the configuration file once per test session.
    """
    config = ConfigUtility('google')
    return config.load_config_file()


@pytest.fixture(scope="session", autouse=True)
def set_env_variables(configs):
    """
    Sets environment variables for the test session.
    Cleans up after the session ends.
    """
    os.environ["TEST_FOLDER"] = configs.get('PROD', 'folder')
    yield
    os.environ.pop("TEST_FOLDER", None)