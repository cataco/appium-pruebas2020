import json
import os
import unittest
import time

from appium import webdriver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class habiticaMultipleTasksFlow(unittest.TestCase):
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

    def test_create_tasks_with_random_data(self):
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/skipButton').click()
        time.sleep(1)
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/show_login_button').click()
        time.sleep(2)
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/username").send_keys('myname123fff')
        self.driver.find_element_by_id("com.habitrpg.android.habitica:id/password").send_keys('myname123fff')
        self.driver.find_element_by_id('com.habitrpg.android.habitica:id/login_btn').click()
        time.sleep(2)
        # Create tasks according to test data json values
        # read file
        with open('habiticaTestData.json', 'r') as myfile:
            data = myfile.read()
        # parse file
        test_values = json.loads(data)
        for test_value in test_values:
            task_type = test_value["task_type"]
            task_title = test_value["title"]
            task_notes = test_value["notes"]
            task_difficulty = test_value["difficulty"]
            # Select task type to create
            self.driver.find_element_by_id('com.habitrpg.android.habitica:id/' + task_type + '_tab').click()
            time.sleep(1)
            self.driver.find_element_by_id('com.habitrpg.android.habitica:id/add_button').click()
            time.sleep(2)
            self.driver.find_element_by_id("com.habitrpg.android.habitica:id/text_edit_text").send_keys(task_title)
            self.driver.find_element_by_id("com.habitrpg.android.habitica:id/notes_edit_text").send_keys(task_notes)
            self.driver.back()
            time.sleep(1)
            if (task_difficulty == 'Easy'):
                diffculty_selector = task_difficulty + ", Selected"
            else:
                diffculty_selector = task_difficulty + ", Not selected"
            self.driver.find_element_by_accessibility_id(diffculty_selector).click()
            self.driver.find_element_by_id('com.habitrpg.android.habitica:id/action_save').click()
            time.sleep(2)
            self.assertTrue(self.driver.find_element_by_xpath("//*[@text='" + task_title + "']").is_displayed(),
                            "Error with task of type: " + task_type + ". and title: " + task_title)
            self.driver.find_element_by_id("com.habitrpg.android.habitica:id/main_task_wrapper").click()
            time.sleep(1)
            self.driver.find_element_by_id("com.habitrpg.android.habitica:id/action_delete").click()
            time.sleep(1)
            self.driver.find_element_by_xpath("//*[@text='Delete Task']").click()
            time.sleep(1)
            self.assertTrue(
                self.driver.find_element_by_id("com.habitrpg.android.habitica:id/emptyViewTitle").is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    if __name__ == '__main__':
        unittest.main()
