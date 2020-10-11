import base64
import os
import unittest
import time

import pytest
from appium import webdriver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HabiticaDailyFlow(unittest.TestCase):
    reportDirectory = 'reports'
    reportFormat = 'xml'
    dc = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "emulator-5556",
        "app": "/Users/ccordob/Downloads/habitica-3-0-1-1.apk"
    }
    testName = 'Untitled'
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.dc['reportDirectory'] = cls.reportDirectory
        cls.dc['reportFormat'] = cls.reportFormat
        cls.dc['testName'] = cls.testName
        cls.dc['udid'] = 'emulator-5554'
        cls.dc['appPackage'] = 'com.habitrpg.android.habitica'
        cls.dc['appActivity'] = '.ui.activities.MainActivity'
        cls.dc['platformName'] = 'android'
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', cls.dc)


    def test_create_daily(self):
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/skipButton').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/show_login_button').click()
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/username").send_keys('myname123fff')
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/password").send_keys('myname123fff')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/login_btn').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/dailies_tab').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/add_button').click()
        time.sleep(1)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").send_keys('apippium daily')
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/notes_edit_text").send_keys('test daily')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='apippium daily']").is_displayed())

    @pytest.mark.dependency(depends=["test_create_daily"])
    def test_created_daily_validation(self):
        self.driver.find_element_by_xpath("//*[@text='apippium daily']").click()
        time.sleep(2)
        name = self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").get_attribute("text")
        note = self.driver.find_element_by_id("com.habitrpg.android.habitica:id/notes_edit_text").get_attribute("text")
        self.assertEqual(name, 'apippium daily')
        self.assertEqual(note, 'test daily')

    @pytest.mark.dependency(depends=["test_read_daily"])
    def test_edit_daily(self):
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").send_keys('apippium daily-EDIT')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='apippium daily-EDIT']").is_displayed())

    @pytest.mark.dependency(depends=["test_edit_daily"])
    def test_remove_daily(self):
        self.driver.find_element_by_xpath("//*[@text='apippium daily-EDIT']").click()
        time.sleep(2)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/action_delete").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='Delete Task']").click()
        time.sleep(1)
        self.assertFalse(self.driver.find_element_by_xpath("//*[@text='apippium daily-EDIT']").is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


    if __name__ == '__main__':
        unittest.main()
