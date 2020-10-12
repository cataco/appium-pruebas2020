import os
import unittest
import time

import pytest
from appium import webdriver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class WikipediaFlow(unittest.TestCase):
    reportDirectory = 'reports'
    reportFormat = 'xml'
    dc = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "emulator-5556",
        "app": "/Users/ccordob/Downloads/wikipedia-2-7-50332-r-2020-09-28.apk"
    }
    testName = 'Untitled'
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.dc['reportDirectory'] = cls.reportDirectory
        cls.dc['reportFormat'] = cls.reportFormat
        cls.dc['testName'] = cls.testName
        cls.dc['udid'] = 'emulator-5554'
        cls.dc['appPackage'] = 'org.wikipedia'
        cls.dc['appActivity'] = '.main.MainActivity'
        cls.dc['platformName'] = 'android'
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', cls.dc)

    def test_search(self):
        self.driver.find_element_by_id('org.wikipedia:id/fragment_onboarding_skip_button').click()
        time.sleep(1)
        self.driver.find_element_by_id("org.wikipedia:id/search_container").click()
        self.driver.find_element_by_id("org.wikipedia:id/search_src_text").send_keys('colombia')
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='Country in the northwestern part of South America']").click()
        time.sleep(5)
        self.assertTrue(self.driver.find_element_by_id("org.wikipedia:id/view_page_header_image_gradient_top").is_displayed())

    def test_search_change_content_navigation(self):
        self.driver.find_element_by_id('org.wikipedia:id/article_menu_show_toc').click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='History']").click()
        time.sleep(3)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='Pre-Columbian era']").is_displayed())

    def test_search_change_language(self):
        self.driver.find_element_by_id('org.wikipedia:id/article_menu_change_language').click()
        time.sleep(1)
        self.driver.find_element_by_id("org.wikipedia:id/menu_search_language").click()
        time.sleep(1)
        self.driver.find_element_by_id("org.wikipedia:id/search_src_text").send_keys('espa')
        time.sleep(1)
        self.driver.find_element_by_id("org.wikipedia:id/non_localized_language_name").click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath(
            "//*[@text='país en América del Sur']").is_displayed())

    def test_search_new_search(self):
        self.driver.find_element_by_id('org.wikipedia:id/article_menu_search').click()
        time.sleep(1)
        self.driver.find_element_by_id("org.wikipedia:id/search_src_text").send_keys("wikipedia")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@text='Free online encyclopedia that anyone can edit']").click()
        time.sleep(3)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='WP']").is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    if __name__ == '__main__':
        unittest.main()
