import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Utilities.Utilities import Utils


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
        self.log = Utils.custom_logger()

    def  page_scroll_down(self):
        self.log.info("scrolling down through page")
        driver = self.driver
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                self.log.info("final height of the page {}".format(new_height))
                self.log.info("scroll down complete")
                break
            last_height = new_height

    def wait_until_element_clickable(self, locator_type, locator):
        try:
            element = self.wait.until(ec.element_to_be_clickable((locator_type, locator)))
        except StaleElementReferenceException:
            self.log.error("StaleElementReferenceException occurred")
            self.log.info("waiting 2 sec to retry")
            time.sleep(2)
            element = self.wait.until(ec.element_to_be_clickable((locator_type,locator)))
        else:
            self.log.info("element is clickable")

    def wait_until_element_located(self, locator_type, locator):
        try:
            element = self.wait.until(ec.presence_of_element_located((locator_type,locator)))
        except StaleElementReferenceException:
            self.log.error("StaleElementReferenceException occurred")
            self.log.info("waiting 2 sec to retry")
            time.sleep(2)
            element = self.wait.until(ec.presence_of_element_located((locator_type,locator)))
        else:
            self.log.info("element is located")
            return element

    def wait_until_page_loaded(self, page):
        self.wait.until(ec.title_is(page))
        self.log.info("New page Loaded - {}".format(page))
        self.log.info("driver in page - {}".format(page))


