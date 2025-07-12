import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import utils.logger_utility as log_utils

class WebDriver:

    log = log_utils.custom_logger(logging.INFO)
    def __init__(self, browser,config):
        self.browser = browser
        self.config = config

    def get_web_driver_instance(self):
        driver = None
        if self.browser == "firefox":
            firefox_options = FirefoxOptions()
            if self.config.get("PROD","headless_mode") == "true":
                firefox_options.add_argument("--headless")
                driver = webdriver.Firefox(options=firefox_options)
            else:
                driver = webdriver.Firefox(options=firefox_options)
        elif self.browser == "chrome":
            chrome_options = ChromeOptions()
            if self.config.get("PROD","headless_mode") == "true":
                chrome_options.add_argument("--headless=new")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option("useAutomationExtension", False)
                chrome_options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
                driver = webdriver.Chrome(options=chrome_options)
            else:
                driver = webdriver.Chrome()
        elif self.browser == "dockerfirefox":
            driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=FirefoxOptions()
            )
        elif self.browser == "dockerchrome":
            driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=ChromeOptions()
            )
        driver.implicitly_wait(3)
        driver.maximize_window()
        base_url = self.config.get('PROD', 'baseURL')
        driver.get(base_url)
        return driver
