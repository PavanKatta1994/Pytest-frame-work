import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Base.BaseDriver import BaseDriver
from Pages.SearchFlights import SearchFlights
from Utilities.Utilities import Utils

class Login(BaseDriver):
    def __init__(self, driver):
        self.driver = driver
        super().__init__(driver)
        self.exclude_login_button_xpath = "//span[@class='style_cross__q1ZoV']//img[@alt='cross']"
        self.log = Utils.custom_logger()
        # data for login test (https://practicetestautomation.com/practice-test-login/)
        self.username_textbox_id = "username"
        self.password_textbox_id = "password"
        self.login_button_id =  "submit"
        self.logout_button_link_text = "Log out"
        

    #this is for Yatra.com
    def exclude_login(self):
        self.log.info("Excluding login button")
        self.driver.find_element(By.XPATH, self.exclude_login_button_xpath).click()
        self.log.info("logging button excluded")
        title = "Flight, Cheap Air Tickets , Hotels, Holiday, Trains Package Booking - Yatra.com"
        self.wait_until_page_loaded(title)
        search_for_flights = SearchFlights(self.driver)
        return search_for_flights

    def set_username(self, username):
        try:
            self.driver.find_element(By.ID, self.username_textbox_id).send_keys(username)
        except NoSuchElementException:
            self.log.error("username field not found")
        else:
            username_field = self.driver.find_element(By.ID, self.username_textbox_id)
            username_set = username_field.get_attribute("value")
            if username_set != username:
                self.log.error("username field does not match")
                self.log.error("username input ({}) != username set ({})".format(username, username_set))
            else:
                self.log.info("username set successfully as " + username)

    def set_password(self, password):
        try:
            self.driver.find_element(By.ID, self.password_textbox_id).send_keys(password)
        except NoSuchElementException:
            self.log.error("password field not found")
        else:
            password_field = self.driver.find_element(By.ID, self.password_textbox_id)
            password_set = password_field.get_attribute("value")
            if password_set != password:
                self.log.error("password field does not match")
                self.log.error("password input ({}) != password set ({})".format(password, password_set))
            else:
                self.log.info("username set successfully as " + password)

    def click_submit(self):
        try:
            self.driver.find_element(By.ID, self.login_button_id).click()
        except NoSuchElementException:
            self.log.error("login button not found")
        else:
            self.log.info("login button is clicked successfully")

    def click_logout(self):
        try:
            self.driver.find_element(By.LINK_TEXT, self.logout_button_link_text).click()
        except NoSuchElementException:
            self.log.error("logout button not found")
        else:
            self.log.info("logout button is clicked successfully")
            self.wait_until_page_loaded("Test Login | Practice Test Automation")

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.click_submit()
        time.sleep(2)
        if self.driver.current_url == "https://practicetestautomation.com/practice-test-login/":
            user_message = self.driver.find_element(By.ID, "error").text
            login_success= "False"
            return  user_message,login_success
        else:
            user_message = self.driver.find_element(By.XPATH, "//p[@class='has-text-align-center']/strong").text
            login_success = "True"
            self.click_logout()
            return user_message,login_success




