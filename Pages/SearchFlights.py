import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Base.BaseDriver import BaseDriver
from Pages.FlightsResults import FlightResults
from Utilities.Utilities import Utils

class SearchFlights(BaseDriver):
    def __init__(self, driver):
        self.log = Utils.custom_logger()
        self.driver = driver
        super().__init__(driver)
        #Locators for source and destination
        self.Search_Button_Xpath =  "//button[normalize-space()='Search']"
        self.Source_Xpath = " //*[contains(@class, '1az9q6q')]/div[1]/div[1]/div[1]/p[3]"
        self.Destination_Xpath = " //*[contains(@class, '1az9q6q')]/div[1]/div[2]/div[1]/p[3]"
        self.Enter_Location_Name_Xpath = "//*[@id='input-with-icon-adornment']"
        self.Location_Values_List_Xpath = "//*[contains(@class, '134xwrj')]//div"
        # Locators for setting date value
        self.current_date = None
        self.date_components = None
        self.Open_Date_Field_Xpath = '//*[@id="__next"]/div/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div[2]'
        self.Current_Month_Year_Value_Xpath =  "//div[contains(@class, 'dual-calendar')]/div[2]//span[contains(@class, 'current-month')]"
        self.Next_Month_Year_Value_Xpath = "//div[contains(@class, 'dual-calendar')]/div[3]//span[contains(@class, 'current-month')]"
        self.Days_Of_Current_Month_Xpath ="//div[contains(@class, 'dual-calendar')]/div[2]"
        self.Days_Of_Next_Month_Xpath = "//div[contains(@class, 'dual-calendar')]/div[3]"
        self.Next_Month_Button_Xpath =  "//*[@id='__next']/div/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div/button[2]"

    def select_city(self, name):
        time.sleep(2)
        self.wait_until_element_located(By.XPATH, self.Location_Values_List_Xpath)
        values = self.driver.find_elements(By.XPATH, self.Location_Values_List_Xpath)
        for i in range(1, len(values) + 1):
            value = self.driver.find_element(By.XPATH, "{0}[{1}]/li[1]/div[1]/div[1]/div[1]/div[1]".format(self.Location_Values_List_Xpath, i))
            if value.text.lower().strip() == name.lower().strip():
                value.click()
                break

    def set_source(self, source):
        self.log.info("Setting source to '{}'".format(source))
        try:
            self.driver.find_element(By.XPATH, self.Source_Xpath).click()
            self.driver.find_element(By.XPATH, self.Enter_Location_Name_Xpath).send_keys(source)
            SearchFlights.select_city(self, source)
        except NoSuchElementException:
            self.log.error("error in setting source as {}".format(source))
            self.log.warning("Please update the xpath of source city element")
        else:
            self.log.debug("source set to '{}'".format(source))

    def set_destination(self, destination):
        self.log.info("Setting destination to '{}'".format(destination))
        try:
            self.driver.find_element(By.XPATH, self.Destination_Xpath).click()
            self.driver.find_element(By.XPATH, self.Enter_Location_Name_Xpath).send_keys(destination)
            SearchFlights.select_city(self, destination)
        except NoSuchElementException:
            self.log.error("error in setting source as {}".format(destination))
            self.log.warning("Please update the xpath of source city element")
        else:
            self.log.debug("destination set to '{}'".format(destination))

    def set_journey_date(self,journey_date_as_string):  #date to be sent in DD/MM/YYYY format
        self.log.info("Setting journey date as'{}'".format(journey_date_as_string))
        self.date_components = list(Utils.get_day_month_year_from_date(journey_date_as_string))
        # print(self.date_components)
        self.current_date = Utils.get_current_date()
        if self.date_components[3] >= self.current_date:
           self.driver.find_element(By.XPATH, self.Open_Date_Field_Xpath).click()
           month_year = self.date_components[1] + " " + self.date_components[2]
           date_not_set = True
           while date_not_set:
               current_month_year = self.driver.find_element(By.XPATH, self.Current_Month_Year_Value_Xpath).text
               next_month_year = self.driver.find_element(By.XPATH, self.Next_Month_Year_Value_Xpath).text
               if current_month_year == month_year:
                   self.driver.find_element(By.XPATH, "//div[contains(@class, 'dual-calendar')]/div[2]/div[2]/div/div[contains(@class, '0{}')]".format(self.date_components[0])).click()
                   self.log.info(" journey date set to '{}'".format(journey_date_as_string))
                   date_not_set = False
               elif next_month_year == month_year:
                   self.driver.find_element(By.XPATH,  "//div[contains(@class, 'dual-calendar')]/div[3]/div[2]/div/div[contains(@class, '0{}')]".format(self.date_components[0])).click()
                   self.log.info(" journey date set to '{}'".format(journey_date_as_string))
                   date_not_set = False
               else:
                   self.driver.find_element(By.XPATH,self.Next_Month_Button_Xpath).click()
        else:
            self.log.warning("journey date cannot be a past date - {}".format(journey_date_as_string))
            self.log.info("journey date set to - {}".format(self.current_date))


    def search(self):
        self.log.info("Performing search")
        try:
             self.driver.find_element(By.XPATH, self.Search_Button_Xpath).click()
        except NoSuchElementException:
            self.log.error("Error in Performing search")
            self.log.info("Please update the xpath of search button")
        else:
            self.log.info("Successfully performed search")

    def search_for_flights(self, source, destination, journey_date):
        self.set_source(source)
        self.set_destination(destination)
        self.set_journey_date(journey_date)
        self.search()
        self.wait_until_page_loaded("Yatra.com | {} to {} flights".format(source, destination))
        flight_results = FlightResults(self.driver)
        return flight_results