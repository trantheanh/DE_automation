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


class Template:

    def __init__(self, driver, timeout=120):
        self.driver = driver
        self.timeout = timeout
        self.current_focus = None

    def goto_url(self, url):
        self.driver.get(url=url)

        return True

    def enter_input(self,
                    input_xpath='//html',
                    value=''):
        element = self.driver.find_element_by_xpath(input_xpath)
        element.clear()
        element.send_keys(value)

        return True

    def press_button(self,
                     btn_xpath='//html'):
        btn_login = self.driver.find_element_by_xpath(btn_xpath)
        btn_login.send_keys(Keys.RETURN)

        return True

    def press_button_by_index(self, target_index=0):
        elements = self.current_focus.find_elements_by_xpath('*')
        print('# elements: {}'.format(len(elements)))

        elements[target_index].click()
        return True

    def wait_util(self, target_xpath='//html'):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                ec.presence_of_element_located((By.XPATH, target_xpath))
            )
        except:
            print('CANT LOCATE {}...Close the browser'.format(target_xpath))
            self.driver.close()
            return False

        return True

    def drag_and_drop(self, source_element, target_element):
        ActionChains(self.driver).drag_and_drop(source=source_element,
                                                target=target_element).perform()
        return True

    def drag_and_drop_by_xpath(self, source_xpath='//html', target_xpath='//html'):
        source_element = self.driver.find_element_by_xpath(source_xpath)
        target_element = self.driver.find_element_by_xpath(target_xpath)

        self.drag_and_drop(source_element=source_element,
                           target_element=target_element)
        return True

    def drag_and_drop_by_index(self, source_index=1, target_index=2):
        elements = self.current_focus.find_elements_by_xpath('*')

        self.drag_and_drop(source_element=elements[source_index],
                           target_element=elements[target_index])

        return True

    # Target to specific element to act later
    def focus(self, target_xpath='//html'):
        element = self.driver.find_element_by_xpath(target_xpath)
        self.current_focus = element

        return True

    @classmethod
    def get_xpath(cls, tag_name='html', att_dict={}):
        xpath = "//{}".format(tag_name)
        for att, value in att_dict.items():
            xpath = xpath + "[@{}='{}']".format(att, value)

        return xpath


class Utility:
    def __init__(self):
        return

    @classmethod
    def read_config(cls, file_name=''):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + file_name

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


