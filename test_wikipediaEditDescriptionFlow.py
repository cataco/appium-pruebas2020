import json
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
        "avd": os.environ.get('adv'),
        "app": os.environ.get('apk')
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
        cls.driver = webdriver.Remote('http://{}:{}/wd/hub'.format(os.environ.get('environment_id'), os.environ.get('SELENIUM_PORT')), cls.dc)

    def test_login(self):
        self.driver.find_element_by_id('org.wikipedia:id/fragment_onboarding_skip_button').click()
        time.sleep(1)
        self.driver.find_element_by_id('org.wikipedia:id/menu_icon').click()
        time.sleep(1)
        self.driver.find_element_by_id('org.wikipedia:id/main_drawer_login_button').click()
        time.sleep(1)
        self.driver.find_element_by_id('org.wikipedia:id/create_account_login_button').click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@text='Username']").send_keys("testAppium2020")
        self.driver.find_element_by_xpath("//*[@text='Password']").send_keys("testAppium123")
        self.driver.find_element_by_id('org.wikipedia:id/login_button').click()
        time.sleep(3)
        self.driver.find_element_by_id('android:id/button2').click()
        self.driver.find_element_by_id('org.wikipedia:id/menu_icon').click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='TestAppium2020']").is_displayed())
        self.driver.back()
        time.sleep(1)

    def test_option_to_edit(self):
        self.driver.find_element_by_accessibility_id('Edits').click()
        time.sleep(2)
        self.driver.find_element_by_id('org.wikipedia:id/addButton').click()
        time.sleep(2)
        self.driver.find_element_by_id('android:id/button2').click()
        self.assertTrue(
            self.driver.find_element_by_id("org.wikipedia:id/addContributionButton").is_displayed())

    def test_several_description_with_random_values(self):
        # read file
        with open('wikipediaTestData.json', 'r') as myfile:
            data = myfile.read()
        # parse file
        test_values = json.loads(data)
        for test_value in test_values:
            description = test_value["description"]
            self.driver.find_element_by_id("org.wikipedia:id/addContributionButton").click()
            time.sleep(1)
            self.driver.find_element_by_id("org.wikipedia:id/view_description_edit_text").send_keys(description)
            time.sleep(1)
            self.driver.find_element_by_id("org.wikipedia:id/view_description_edit_save_button").click()
            time.sleep(2)
            article_subtitle = self.driver.find_element_by_id("org.wikipedia:id/articleSubtitle").get_attribute("text")
            self.assertEquals(description, 'article_subtitle', "Error with description: " + description)
            self.driver.back()
            self.driver.back()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    if __name__ == '__main__':
        unittest.main()
