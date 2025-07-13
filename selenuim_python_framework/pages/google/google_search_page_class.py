import time

from common.base.selenium_base import SeleniumBase
from utils.locator_utility import Locators


class GoogleSearch(SeleniumBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.loc = Locators(__class__)

    def get_page_title(self) -> str:
        """
        Get the title of the Google search page.
        """
        try:
            title = self.driver.title
            self.log.info(f"Page title is: {title}")
            return title
        except Exception as e:
            self.log.exception(f"Failed to get page title: {e}")
            return False

    def search_keyword(self, search_keyword: str) -> bool:
        self.log.info(f"Google Search: {search_keyword}")
        try:
            # Locate search bar input field
            input_type, input_locator = self.loc.page_locators("search_box")
            if not self.send_keys(search_keyword, input_locator, locator_type=input_type):
                self.log.error(f"Failed to send google keyword '{search_keyword}' to input field.")
                return False

            # Verify if the search options is populated with the keyword
            search_op_type, search_op_locator = self.loc.page_locators("search_option")
            search_result_op_l = self.get_element_list(search_op_locator, locator_type=search_op_type)
            for search_op in search_result_op_l:
                self.log.info(f"Search option found: {search_op.text}")
                if not search_keyword.lower() in search_op.text.lower():
                    self.log.warning(f"Search option '{search_op.text}' does not match keyword '{search_keyword}'.")
                    self.log.error(f"No search options found for keyword '{search_keyword}'.")
                    return False
            return True
        except Exception as e:
            self.log.exception(f"Exception during google keyword search: {e}")
            return False

    def verify_selenium_download_search(self) -> bool:
        """
        Verify if the Selenium download is shown in the search results after searching for Selenium.
        """
        try:

            #select the download option from the search options and click on it
            select_type, select_locator = self.loc.page_locators("select_search_option")
            if not self.element_click(select_locator, locator_type=select_type):
                self.log.error("Failed to select Selenium download from search options.")
                return False

            button_type, button_locator = self.loc.page_locators("selenium_download")
            if not self.is_element_present(button_locator, locator_type=button_type):
                self.log.error("Failed to find Selenium download after google search.")
                return False
            return True
        except Exception as e:
            self.log.exception(f"Exception in google search verification for selenium download : {e}")
            return False