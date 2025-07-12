from common.base.selenium_base import SeleniumBase
from utils.locator_utility import Locators


class BusBooking(SeleniumBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.loc = Locators(__class__)

    def select_from_city(self, src_city: str) -> bool:
        self.log.info(f"Selecting source city: {src_city}")

        try:
            
            # Locate and enter source city
            input_type, input_locator = self.loc.page_locators("from_city_input_field", src_city=src_city)
            if not self.send_keys(src_city, input_locator, locator_type=input_type):
                self.log.error(f"Failed to send source city '{src_city}' to input field.")
                return False

            # Locate and click the matching city from dropdown
            city_type, city_locator = self.loc.page_locators("src_city", src_city=src_city)
            if not self.element_click(city_locator, locator_type=city_type):
                self.log.error(f"Failed to click city dropdown option for '{src_city}'.")
                return False

            self.log.info(f"Successfully selected city: {src_city}")
            return True

        except Exception as e:
            self.log.exception(f"Exception during city selection: {e}")
            return False

    def select_dest_city(self, dest_city: str) -> bool:
        self.log.info(f"Selecting destination city: {dest_city}")
        try:
            input_type, input_locator = self.loc.page_locators("dest_city_input_field", dest_city=dest_city)
            if not self.send_keys(dest_city, input_locator, locator_type=input_type):
                self.log.error(f"Failed to type destination city: {dest_city}")
                return False

            city_type, city_locator = self.loc.page_locators("dest_city", dest_city=dest_city)
            if not self.element_click(city_locator, locator_type=city_type):
                self.log.error(f"Failed to click dropdown option for destination city: {dest_city}")
                return False

            self.log.info(f"Successfully selected destination city: {dest_city}")
            return True

        except Exception as e:
            self.log.exception(f"Exception in select_dest_city: {e}")
            return False

    def select_depart_date(self, depart_date: str) -> bool:
        self.log.info(f"Selecting departure date: {depart_date}")
        try:
            date_type, date_locator = self.loc.page_locators("booking_date_loc")
            if not self.element_click(date_locator, locator_type=date_type):
                self.log.error("Failed to click on booking date input")
                return False

            depart_type, depart_locator = self.loc.page_locators("depart_date", depart_date=depart_date)
            if not self.element_click(depart_locator, locator_type=depart_type):
                self.log.error(f"Failed to click on depart date: {depart_date}")
                return False

            self.log.info(f"Successfully selected departure date: {depart_date}")
            return True

        except Exception as e:
            self.log.exception(f"Exception in select_depart_date: {e}")
            return False

    def click_search_button(self) -> bool:
        self.log.info("Clicking search button")
        try:
            search_type, search_locator = self.loc.page_locators("search_btn")
            if not self.element_click(search_locator, locator_type=search_type):
                self.log.error("Search button click failed.")
                return False

            self.log.info("Search button clicked successfully")
            return True

        except Exception as e:
            self.log.exception(f"Exception in click_search_button: {e}")
            return False