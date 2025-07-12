import logging

from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotSelectableException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumBase:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        self.log = logging.getLogger(__name__)

    @property
    def title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def capture_screenshot(self, name):
        self.driver.get_screenshot_as_file(name)

    @staticmethod
    def get_by_type(locator_type):
        mapping = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME,
            "link": By.LINK_TEXT,
        }
        try:
            return mapping[locator_type.lower()]
        except KeyError as exc:
            raise ValueError(f"Unsupported locator_type: {locator_type}") from exc

    def get_element(self, locator, locator_type="id"):
        try:
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info(f"Element found with locator: {locator} and locator_type: {locator_type}")
            return element
        except Exception as e:
            self.log.error(f"Element not found with locator: {locator} and locator_type: {locator_type}. Exception: {e}")
            return False

    def get_element_list(self, locator, locator_type="id"):
        """
        NEW METHOD
        Get list of elements
        """
        try:
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_elements(by_type, locator)
            self.log.info(f"Element list found with locator: {locator} and locator_type: {locator_type}")
            return element
        except Exception as e:
            self.log.error(f"Element list not found with locator: {locator} and locator_type: {locator_type}. Exception: {e}")
            return False

    def element_click(self, locator="", locator_type="id", element=None):
        """
        Click on an element -> MODIFIED
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info(f"Clicked on element with locator: {locator} locator_type: {locator_type}")
            return True
        except Exception as e:
            self.log.error(f"Cannot click on the element with locator: {locator} locator_type: {locator_type}. Exception: {e}")
            return False

    def send_keys(self, data, locator="", locator_type="id", element=None):
        """
        Send keys to an element -> MODIFIED
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(f"Sent data on element with locator: {locator} locator_type: {locator_type}")
            return True
        except Exception as e:
            self.log.error(f"Cannot send data on the element with locator: {locator} locator_type: {locator_type}. Exception: {e}")
            return False

    def clear_field(self, locator="", locator_type="id", element=None):
        """
        Clear an element's input field.
        Either provide the element directly or pass a locator and type.
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.clear()
            self.log.info(f"Cleared field with locator: {locator} locator_type: {locator_type}")
            return True
        except Exception as e:
            self.log.error(f"Cannot clear field with locator: {locator} locator_type: {locator_type}. Exception: {e}")
            return False

    def get_text(self, locator="", locator_type="id", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator: # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info(f"Getting text on element :: {info}")
                self.log.info(f"The text is :: '{text}'")
                text = text.strip()
            return text
        except Exception as e:
            self.log.error(f"Failed to get text on element {info}. Exception: {e}")
            return False


    def is_element_present(self, locator="", locator_type="id", element=None):
        """
        Check if an element is present -> MODIFIED
        Either provide the element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                self.log.info(f"Element present with locator: {locator} locator_type: {locator_type}")
                return True
            else:
                self.log.error(f"Element not present with locator: {locator} locator_type: {locator_type}")
                return False
        except Exception as e:
            print(f"Element not found. Exception: {e}")
            return False

    def is_element_displayed(self, locator="", locator_type="id", element=None):
        """
        NEW METHOD
        Check if the element is displayed
        Either provide element or a combination of locator and locator_type
        """
        is_displayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed" )
            else:
                self.log.info("Element not displayed")
            return is_displayed
        except Exception as e:
            print(f"Element not found. Exception: {e}")
            return False

    def element_presence_check(self, locator, by_type):
        """
        Check if the element is present
        """
        try:
            element_list = self.driver.find_elements(by_type, locator)
            if len(element_list) > 0:
                self.log.info(f"Element present with locator: {locator} locator_type: {str(by_type)}")
                return True
            else:
                self.log.error(f"Element not present with locator: {locator} locator_type: {str(by_type)}")
                return False
        except Exception as e:
            self.log.info(f"Element not found. Exception: {e}")
            return False

    def wait_for_element(self, locator, locator_type="id", timeout=60, poll_frequency=0.5):
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info(f"Waiting for maximum :: {timeout} :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(ec.element_to_be_clickable((by_type, locator)))
            self.log.info("Element appeared on the web page")
            return element
        except Exception as e:
            self.log.error(f"Element not appeared on the web page. Exception: {e}")
            return False

    def web_scroll(self, direction="up"):
        """
        NEW METHOD
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 700);")

    def verify_page_title(self, title_to_verify):
        """
        Verify the page Title
        Parameters:
            title_to_verify: Title on the page that needs to be verified
        """
        try:
            actual_title = self.title
            if actual_title.lower() in title_to_verify.lower():
                self.log.info("### VERIFICATION CONTAINS !!!")
                return True
            else:
                self.log.info("### VERIFICATION DOES NOT CONTAINS !!!")
                return False
        except Exception as e:
            self.log.error(f"Failed to get page title. Exception: {e}")
            return False

    def element_move_to(self, locator="", locator_type="id", element=None):
        """
        Move on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            action = ActionChains(self.driver)
            action.move_to_element(element).perform()
            self.log.info(f"Moved on element with locator: {locator} locator_type: {locator_type}")
            return True
        except Exception as e:
            self.log.error(f"Cannot move on the element with locator: {locator} locator_type: {locator_type}. Exception: {e}")
            return False

    def element_move_to_click(self, locator="", locator_type="id", element=None):
        """
        Move on an element and click
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            action = ActionChains(self.driver)
            action.move_to_element(element).click().perform()
            self.log.info(f"Moved on element and click with locator: {locator} locator_type: {locator_type}")
            return True
        except Exception as e:
            self.log.error(f"Cannot move and click on the element with locator: {locator} locator_type: {locator_type}. Exception: {e}")
            return False