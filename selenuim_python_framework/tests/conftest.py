import os
import shutil
from datetime import datetime

import pytest

from common.constants import *
from utils.helper import ConfigUtility
from utils.driver_utility import WebDriver


# @pytest.fixture(scope="session")
# def configs():
#     """
#     Load the configuration file once per test session.
#     """
#     config = ConfigUtility('goibibo')
#     return config.load_config_file()
#
#
# @pytest.fixture(scope="session", autouse=True)
# def set_env_variables(configs):
#     """
#     Sets environment variables for the test session.
#     Cleans up after the session ends.
#     """
#     os.environ["TEST_FOLDER"] = configs.get('PROD', 'folder')
#     yield
#     os.environ.pop("TEST_FOLDER", None)


def pytest_addoption(parser):
    """
    Adds custom CLI options to pytest.
    """
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to use for tests"
    )


@pytest.fixture(scope="session")
def browser(request):
    """
    Get the browser name from CLI options.
    """
    return request.config.getoption("--browser")


@pytest.fixture(scope="class")
def get_driver(request, browser, configs):
    """
    Instantiate WebDriver and assign it to test class.
    """
    wdf = WebDriver(browser, configs)
    driver = wdf.get_web_driver_instance()
    request.node.driver = driver
    yield driver
    driver.quit()


def _capture_screenshot(name: str, driver):
    """
    Saves a screenshot of the current browser state.
    """
    path = os.path.join(SCREENSHOT_DIRECTORY, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.get_screenshot_as_file(path)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Set a default HTML report path if not explicitly passed via CLI.
    """
    report_path = os.path.join(PROJECT_ROOT, REPORT_FILENAME)
    if not config.option.htmlpath:
        config.option.htmlpath = report_path

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Clean temp and screenshot directories at the start of the test session.
    """
    temp_dir = os.path.join(PROJECT_ROOT, TEMP_DIR)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(SCREENSHOT_DIRECTORY, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Capture and embed screenshot in HTML report for failed or xfailed tests.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when in ("setup", "call"):
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            driver = item.funcargs.get("get_driver", None)
            if driver:
                file_name = report.nodeid.replace("::", "_") + ".png"
                _capture_screenshot(file_name, driver)

                rel_path = os.path.join("screenshots", file_name)
                html = (
                    f'<div><img src="{rel_path}" alt="screenshot" '
                    f'style="width:600px;height:228px;" '
                    f'onclick="window.open(this.src)" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))

    report.extra = extra


def pytest_unconfigure(config):
    """
    Post-processing once all tests and reports are finished.
    """
    report_path = os.path.abspath(REPORT_FILENAME)
    if os.path.exists(report_path):
        print(f"\n HTML report generated: {report_path}")
        post_process_report(report_path)
    else:
        print("Report not found.")


def post_process_report(path: str):
    """
    Zip up the reports for archiving.
    """
    print(f"Reports will be zipped from location {path}")
    current_time = datetime.strftime(datetime.now(), '%d_%m_%Y-%H_%M_%S')
    zip_location = os.path.join(PROJECT_ROOT, TEMP_DIR)
    report_base = os.path.join(PROJECT_ROOT, REPORT_CONFIG) + current_time
    shutil.make_archive(base_name=report_base, format='zip', root_dir=zip_location)
