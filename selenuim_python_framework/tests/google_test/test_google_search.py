import time
from datetime import datetime, timedelta

import pytest
from pages.google.google_search_page_class import GoogleSearch
from utils.helper import *


@pytest.mark.usefixtures("get_driver")
class TestGoogleSearch():

    @pytest.fixture(autouse=True)
    def setup(self,get_driver):
        self.driver = get_driver
        self.search = GoogleSearch(self.driver)
        self.page_data = get_test_data(__class__)

    @pytest.mark.smoke
    def test_verify_page_title(self, request):
        self.search.log.info(f"TEST CASE: {request.node.name}")
        assert self.search.get_page_title() == self.page_data['page_title'], f"Page title does not match: {self.page_data['page_title']}"

    def test_search_keyword(self, request):
        self.search.log.info(f"TEST CASE: {request.node.name}")
        assert self.search.search_keyword(self.page_data['search_keyword']), f"Failed to search keyword: {self.page_data['search_keyword']}"

    #Issue with captcha on Google search page, skipping this test for now
    @pytest.mark.skip(reason="Google search page has captcha, skipping this test.")
    def test_verify_selenium_download_search(self, request):
        self.search.log.info(f"TEST CASE: {request.node.name}")
        assert self.search.verify_selenium_download_search(), "Selenium download not found in search results."

