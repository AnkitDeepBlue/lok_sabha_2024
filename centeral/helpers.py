# helpers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class WebScraperHelper:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def select_dropdown_option(self, locator, visible_text):
        element = self.wait_for_element(locator)
        select = Select(element)
        select.select_by_visible_text(visible_text)

    def get_element_text(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))
        return element.text

