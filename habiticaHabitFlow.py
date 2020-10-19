import os
import unittest
import time

import pytest
from appium import webdriver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HabiticaHabitFlow(unittest.TestCase):
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
        cls.dc['appPackage'] = 'com.habitrpg.android.habitica'
        cls.dc['appActivity'] = '.ui.activities.MainActivity'
        cls.dc['platformName'] = 'android'
        cls.driver = webdriver.Remote('http://{}:{}/wd/hub'.format(os.environ.get('environment_id'), os.environ.get('SELENIUM_PORT')), cls.dc)

    def test_create_habit(self):
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/skipButton').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/show_login_button').click()
        time.sleep(2)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/username").send_keys('myname123fff')
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/password").send_keys('myname123fff')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/login_btn').click()
        time.sleep(2)
        user = self.driver.find_element_by_id('com.habitrpg.android.habitica:id/toolbar_title').get_attribute("text")
        self.assertEqual(user, 'myname123fff')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/add_button').click()
        time.sleep(2)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").send_keys('apippium habit')
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/notes_edit_text").send_keys('test habit')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='apippium habit']").is_displayed())

    def test_created_habit_validation(self):
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/main_task_wrapper").click()
        time.sleep(2)
        name = self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").get_attribute(
            "text")
        note = self.driver.find_element_by_id("com.habitrpg.android.habitica:id/notes_edit_text").get_attribute("text")
        self.assertEqual(name, 'apippium habit')
        self.assertEqual(note, 'test habit')

    def test_edit_habit(self):
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").send_keys('apippium habit-EDIT')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='apippium habit-EDIT']").is_displayed())

    def test_remove_habit(self):
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/main_task_wrapper").click()
        time.sleep(1)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/action_delete").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='Delete Task']").click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element_by_id("com.habitrpg.android.habitica:id/emptyViewTitle").is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    if __name__ == '__main__':
        unittest.main()
