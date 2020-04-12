from automator.def_function import test_function, value_function

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@test_function
def goto_url(
        driver,
        url
):
    driver.get(url=url)


@test_function
def enter_input(
        current_focus,
        input_xpath='//html',
        value=Keys.RETURN
):
    element = current_focus.find_element_by_xpath(input_xpath)
    element.clear()
    element.send_keys(value)


@test_function
def click(
        current_focus,
        target_xpath='//html'
):
    node = current_focus.find_element_by_xpath(target_xpath)
    node.send_keys(Keys.RETURN)


@test_function
def click_at_index(
        current_focus,
        target_index=0
):
    elements = current_focus.find_elements_by_xpath('*')
    elements[target_index].click()


@test_function
def wait_for(
        driver,
        target_xpath='//html',
        timeout=120
):
    WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((By.XPATH, target_xpath))
    )


@test_function
def drag_and_drop(
        driver,
        source_element,
        target_element
):
    ActionChains(driver).drag_and_drop(
        source=source_element,
        target=target_element
    ).perform()


@test_function
def scroll_to(
        driver,
        target_element
):
    ActionChains(driver).move_to_element(target_element).perform()


@test_function
def drag_and_drop_by_xpath(
        current_focus,
        source_xpath='//html',
        target_xpath='//html'
):
    source_element = current_focus.find_element_by_xpath(source_xpath)
    target_element = current_focus.find_element_by_xpath(target_xpath)

    drag_and_drop(
        source_element=source_element,
        target_element=target_element
    )


@test_function
def drag_and_drop_by_index(
        current_focus,
        source_index=1,
        target_index=2
):
    elements = current_focus.find_elements_by_xpath('*')

    drag_and_drop(
        source_element=elements[source_index],
        target_element=elements[target_index]
    )


@test_function
def focus(
        current_focus,
        target_xpath='//html'
):
    element = current_focus.find_element_by_xpath(target_xpath)

    return element


@test_function
def focus_by_index(
        current_focus,
        target_index=0
):
    elements = current_focus.find_elements_by_xpath('*')

    if target_index >= len(elements):
        return False

    return elements[target_index]


@value_function
def get_text_of_node(
        current_focus,
        target_xpath='//html'
):
    element = current_focus.find_element_by_xpath(target_xpath)
    return get_text(current_focus=element)


@value_function
def get_texts_of_nodes(
        current_focus,
        target_xpath='//html'
):
    elements = current_focus.find_elements_by_xpath(target_xpath)
    return [get_text(current_focus=element) for element in elements]


@value_function
def get_text(
        current_focus
):
    return current_focus.text

