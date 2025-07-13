import time
from datetime import datetime, timedelta

import pytest
from pages.goibibo.bus_booking_page_class import BusBooking
from utils.helper import *


@pytest.mark.usefixtures("get_driver")
class TestBusBooking():

    @pytest.fixture(autouse=True)
    def setup(self,get_driver):
        self.driver = get_driver
        self.bus = BusBooking(self.driver)
        self.page_data = get_test_data(__class__)

    @pytest.mark.smoke
    def test_verify_page_title(self, request):
        self.bus.log.info(f"TEST CASE: {request.node.name}")
        assert self.bus.title == self.page_data['page_title'], f"Page title does not match: {self.page_data['page_title']}"

    def test_select_src_city(self, request):
        self.bus.log.info(f"TEST CASE: {request.node.name}")
        assert self.bus.select_from_city(self.page_data['src_city']), f"Failed to select source city: {self.page_data['src_city']}"

    def test_select_dest_city(self, request):
        self.bus.log.info(f"TEST CASE: {request.node.name}")
        assert self.bus.select_dest_city(self.page_data['dest_city']), f"Failed to select destination city: {self.page_data['dest_city']}"

    def test_select_depart_date(self, request):
         self.bus.log.info(f"TEST CASE: {request.node.name}")
         next_2_days_date = (datetime.today() + timedelta(days=2)).day
         assert self.bus.select_depart_date(next_2_days_date), f"Failed to select departure date: {self.page_data['next_2_days_date']}"

    def test_click_to_search_button(self, request):
         self.bus.log.info(f"TEST CASE: {request.node.name}")
         time.sleep(20)
         assert self.bus.click_search_button(), f"Failed to click search button"
