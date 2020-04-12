import os
import sys


import json

from driver import DRIVER_DIR
from automator.category import Browser
import automator.action as action

from selenium import webdriver


def get_driver(browser_name=None):
    if "darwin" in sys.platform:
        extention = ""
    elif "win" in sys.platform:
        extention = ".exe"
    else:
        extention = ""

    if browser_name == Browser.Chrome:
        driver_path = os.path.join(DRIVER_DIR, "Chrome/chromedriver{}".format(extention))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--kiosk")
        driver = webdriver.Chrome(driver_path, options=chrome_options)
    elif browser_name == Browser.Firefox:
        driver = None
    else:
        driver = None

    return driver


class Tester:
    def __init__(
            self,
            browser=Browser.Chrome,
            driver=None,
            timeout=120
    ):
        if driver is None:
            driver = get_driver(browser_name=browser)

        self.driver = driver
        self.timeout = timeout
        self.current_focus = self.driver
        self.cached = []
        self.test_cases = None

    def reset_state(self):
        self.current_focus = self.driver
        self.cached = []

    def previous_focus(self, need_remove=True):
        if len(self.cached) > 0:
            self.current_focus = self.cached[-1]

        if need_remove:
            del self.cached[-1]

    def caching(self):
        self.cached.append(self.current_focus)

    def execute(self, func, **kwargs):
        output = func(
            driver=self.driver,
            current_focus=self.current_focus,
            timeout=self.timeout,
            **kwargs
        )
        # print("Executing: {}".format(func.__name__))

        if output:
            self.current_focus = output

            return True

        return False

    def get(self, func, **kwargs):
        output = func(
            driver=self.driver,
            current_focus=self.current_focus,
            timeout=self.timeout,
            **kwargs
        )

        return output

    def read_testcase(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            json_string = f.read()
            test_cases = json.loads(json_string)
            test_cases = test_cases['steps']
            test_cases.sort(key=lambda x: (x['index']))

            self.test_cases = test_cases

        return

    def execute_testcase(self):
        if not self.test_cases:
            raise Exception("YOU NEED TO PROVIDE TEST CASE")

        for i in range(len(self.test_cases)):
            self.execute_step(step=self.test_cases[i])

        return

    def execute_step(self, step):
        print("Processing: {} - {}".format(step['index'], step['name']))
        case_type = step['type']
        case_content = step['content']

        if case_type == 'url':
            action.goto_url(
                driver=self.driver,
                url=case_content['url']
            )
        elif case_type == 'input':
            action.enter_input(
                parent=self.current_focus,
                input_xpath=Tester.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                ),
                value=case_content['value']
            )
        elif case_type == 'wait':
            action.wait_for(
                driver=self.driver,
                target_xpath=Tester.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                )
            )
        elif case_type == 'click':
            action.click(
                parent=self.current_focus,
                target_xpath=Tester.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                )
            )
        elif case_type == 'focus':
            action.focus(
                parent=self.current_focus,
                target_xpath=Tester.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                )
            )
        elif case_type == 'drag_drop_by_index':
            action.drag_and_drop_by_index(
                parent=self.current_focus,
                source_index=case_content['source_index'],
                target_index=case_content['target_index']
            )
        elif case_type == 'click_by_index':
            action.click_at_index(
                parent=self.current_focus,
                target_index=case_content['target_index']
            )

    @classmethod
    def get_xpath(cls, tag_name='html', att_dict=None, is_parent=True):
        if att_dict is None:
            att_dict = {}

        xpath = "//{}".format(tag_name)

        for att, value in att_dict.items():
            xpath = xpath + "[@{}='{}']".format(att, value)

        if is_parent:
            xpath = ".{}".format(xpath)

        return xpath
