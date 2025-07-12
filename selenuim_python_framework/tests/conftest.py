import os
import shutil
from datetime import datetime
import pytest
from common.constants import *
from utils.helper import ConfigUtility
from utils.driver_utility import WebDriver


@pytest.fixture(scope="session", autouse=True)
def set_env_variables(configs):
    """
    Sets environment variables for the entire test session.
    """
    os.environ["TEST_FOLDER"] = configs.get('PROD', 'folder')
    # Clean up environment variables after the session
    yield
    del os.environ["TEST_FOLDER"]


@pytest.fixture(scope='session')
def configs():
    configs = ConfigUtility('goibibo')
    return configs.load_config_file()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="class")
def get_driver(request, browser,configs):
    wdf = WebDriver(browser,configs)
    driver = wdf.get_web_driver_instance()
    request.node.driver = driver  # attach driver to the test node
    yield driver
    driver.quit()

def _capture_screenshot(name, driver):
    path = os.path.join(SCREENSHOT_DIRECTORY, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.get_screenshot_as_file(path)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Set HTML report file path from config if not provided via CLI."""
    report_path = os.path.join(PROJECT_ROOT, REPORT_FILENAME)
    if not config.option.htmlpath:
        config.option.htmlpath = report_path


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Clean temp directory and ensure screenshot directory exists before test session starts."""
    temp_dir = os.path.join(PROJECT_ROOT, TEMP_DIR)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(SCREENSHOT_DIRECTORY, exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Embed screenshot in HTML report for failed or xfailed tests."""
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
    """Runs after the HTML report is fully written."""
    # report_base = "temp/report.html"
    report_path = os.path.abspath(REPORT_FILENAME)
    if os.path.exists(report_path):
        print(f"\n HTML report generated: {report_path}")
        post_process_report(report_path)
    else:
        print("Report not found.")

def post_process_report(path):
    print(f"Reports will be zipped on location {path}")
    current_time = datetime.strftime(datetime.now(), '%d_%m_%Y-%H_%M_%S')
    zip_location = os.path.join(PROJECT_ROOT, TEMP_DIR)
    report_path = os.path.join(PROJECT_ROOT, REPORT_CONFIG)
    zip_destination = report_path + current_time
    shutil.make_archive(root_dir=zip_location, format='zip', base_name=zip_destination)

