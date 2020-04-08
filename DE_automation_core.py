import os
import sys
import platform
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.action_chains import ActionChains


def catch_exception(func):
    def get_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return False

    return get_func


def get_driver(file_name):
    driver_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--kiosk")

    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)

    return driver


class Template:

    def __init__(self, driver, timeout=120):
        self.driver = driver
        self.timeout = timeout
        self.current_focus = None
        self.current_sub_focus = None

    @catch_exception
    def goto_url(self, url):
        self.driver.get(url=url)

        return True

    @catch_exception
    def enter_input(self,
                    input_xpath='//html',
                    value=Keys.RETURN):
        element = self.driver.find_element_by_xpath(input_xpath)
        element.clear()
        element.send_keys(value)

        return True

    @catch_exception
    def press_button(self,
                     btn_xpath='//html'):
        btn_login = self.driver.find_element_by_xpath(btn_xpath)
        btn_login.send_keys(Keys.RETURN)

        return True

    @catch_exception
    def press_button_by_index(self, target_index=0):
        elements = self.current_focus.find_elements_by_xpath('*')
        print('# elements: {}'.format(len(elements)))

        elements[target_index].click()
        return True

    @catch_exception
    def wait_util(self, target_xpath='//html', need_to_close=False):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                ec.presence_of_element_located((By.XPATH, target_xpath))
            )
        except:
            print('CANT LOCATE {}...Close the browser'.format(target_xpath))
            if need_to_close:
                self.driver.close()
            return False

        return True

    @catch_exception
    def drag_and_drop(self, source_element, target_element):
        ActionChains(self.driver).drag_and_drop(source=source_element,
                                                target=target_element).perform()
        return True

    @catch_exception
    def scroll_to(self, target_element):
        ActionChains(self.driver).move_to_element(target_element).perform()
        return True

    @catch_exception
    def drag_and_drop_by_xpath(self, source_xpath='//html', target_xpath='//html'):
        source_element = self.driver.find_element_by_xpath(source_xpath)
        target_element = self.driver.find_element_by_xpath(target_xpath)

        self.drag_and_drop(source_element=source_element,
                           target_element=target_element)
        return True

    @catch_exception
    def drag_and_drop_by_index(self, source_index=1, target_index=2):
        elements = self.current_focus.find_elements_by_xpath('*')

        self.drag_and_drop(source_element=elements[source_index],
                           target_element=elements[target_index])

        return True

    @catch_exception
    def focus(self, target_xpath='//html'):
        element = self.driver.find_element_by_xpath(target_xpath)
        self.current_focus = element

        return True

    @catch_exception
    def focus_to_child(self, target_xpath='//html'):
        element = self.current_focus.find_element_by_xpath(target_xpath)
        self.current_focus = element

    @catch_exception
    def subfocus_to_child(self, target_xpath='//html'):
        element = self.current_sub_focus.find_element_by_xpath(target_xpath)
        self.current_sub_focus = element

    @catch_exception
    def focus_by_index(self, target_index=0, need_log=False):
        elements = self.current_focus.find_elements_by_xpath('*')
        if need_log:
            print('# target_index/elements: {}/{}'.format(target_index, len(elements)))

        if target_index >= len(elements):
            return False

        self.current_sub_focus = elements[target_index]
        return True

    @catch_exception
    def get_text_from_current_sub_focus(self, target_xpath='//html'):
        element = self.current_sub_focus.find_element_by_xpath(target_xpath)
        return element.text

    @catch_exception
    def get_texts_from_current_sub_focus(self, target_xpath='//html'):
        elements = self.current_sub_focus.find_elements_by_xpath(target_xpath)
        return [element.text for element in elements]

    @catch_exception
    def get_text_from_current_focus(self, target_xpath='//html'):
        element = self.current_focus.find_element_by_xpath(target_xpath)
        return element.text

    @classmethod
    def get_xpath(cls, tag_name='html', att_dict={}):
        xpath = "//{}".format(tag_name)
        for att, value in att_dict.items():
            xpath = xpath + "[@{}='{}']".format(att, value)

        return xpath

    @classmethod
    def get_xpath_sub(cls, tag_name='html', att_dict={}):
        xpath = ".//{}".format(tag_name)
        for att, value in att_dict.items():
            xpath = xpath + "[@{}='{}']".format(att, value)

        return xpath


class Utility:
    def __init__(self):
        return

    @classmethod
    def read_config(cls, file_name=''):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name

        with open(file_path, 'r', encoding='utf-8') as f:
            json_string = f.read()
            test_cases = json.loads(json_string)
            test_cases = test_cases['steps']
            test_cases.sort(key=lambda x: (x['index']))

            return test_cases

    @classmethod
    def read_testcase(cls, test_case={}, template=None):
        print("Processing: {} - {}".format(test_case['index'], test_case['name']))
        case_type = test_case['type']
        case_content = test_case['content']
        if case_type == 'url':
            template.goto_url(
                url=case_content['url']
            )
        elif case_type == 'input':
            template.enter_input(
                input_xpath=Template.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']),
                value=case_content['value']
            )
        elif case_type == 'wait':
            template.wait_util(
                target_xpath=Template.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                )
            )
        elif case_type == 'click':
            template.press_button(
                btn_xpath=Template.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                )
            )
        elif case_type == 'focus':
            template.focus(
                target_xpath=Template.get_xpath(
                    tag_name=case_content['tag_name'],
                    att_dict=case_content['att_dict']
                )
            )
        elif case_type == 'drag_drop_by_index':
            template.drag_and_drop_by_index(
                source_index=case_content['source_index'],
                target_index=case_content['target_index']
            )
        elif case_type == 'click_by_index':
            template.press_button_by_index(
                target_index=case_content['target_index']
            )




