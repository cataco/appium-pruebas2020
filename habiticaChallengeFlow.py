import os
import unittest
import time


import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HabiticaChallengeFlow(unittest.TestCase):
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
    challenge_name = ''

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

    def test_create_public_challenge_without_gems(self):
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/skipButton').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/show_login_button').click()
        time.sleep(2)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/username").send_keys('myname123fff')
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/password").send_keys('myname123fff')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/login_btn').click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id('Open navigation drawer').click()
        time.sleep(1)
        self.driver.scroll(self.driver.find_element_by_xpath("//*[@text='Tasks']"),
                           self.driver.find_element_by_xpath("//*[@text='Time Travelers']"))
        time.sleep(1)
        self.driver.swipe(100, 1235, 100, 600, 400)
        self.driver.swipe(100, 1235, 100, 600, 400)
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='Challenges']").click()
        time.sleep(1)
        self.driver.find_element_by_accessibility_id('More options').click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='Create Challenge']").click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/create_challenge_title').send_keys(
            'Test Challenge Title Appium')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/create_challenge_tag').send_keys(
            'Short Challenge')
        self.driver.swipe(100, 1235, 100, 600, 400)
        self.driver.find_element_by_xpath("//*[@text='Add Habit']").click()
        time.sleep(1)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").send_keys('challenge habit')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text='Test Challenge Title Appium']").is_displayed())

    def test_join_public_challenge(self):
        self.driver.find_element_by_accessibility_id('Discover').click()
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/challenge_name').click()
        time.sleep(2)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/join_button').click()
        time.sleep(2)
        self.challenge_name = self.driver.find_element_by_id(
            'com.habitrpg.android.habitica:id/challenge_name').get_attribute("text")
        self.driver.back()
        time.sleep(1)
        self.driver.find_element_by_accessibility_id('My Challenges').click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@text=" + self.challenge_name + "]").is_displayed())

    def test_leave_public_challenge(self):
        self.driver.find_element_by_xpath("//*[@text=" + self.challenge_name + "]").click()
        time.sleep(1)
        nunmber_participants = int(self.driver.find_element_by_id(
            'com.habitrpg.android.habitica:id/participant_count').get_attribute("text"))
        self.driver.swipe(100, 1235, 100, 600, 400)
        self.driver.swipe(100, 1235, 100, 600, 400)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/leave_button').click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@text='Leave & Delete Tasks']").click()
        new_number_participants = int(self.driver.find_element_by_id(
            'com.habitrpg.android.habitica:id/participant_count').get_attribute("text"))
        self.assertEquals(new_number_participants, nunmber_participants - 1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    if __name__ == '__main__':
        unittest.main()
