from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Base.BaseDriver import BaseDriver
from Utilities.Utilities import Utils


class FlightResults(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.log = Utils.custom_logger()
        self.One_Stop_Xpath = "//p[normalize-space()='1']"
        self.Two_Stops_Xpath = "//p[normalize-space()='2']"
        self.Non_Stop_Xpath = "//p[normalize-space()='0']"
        self.Stops_List_Xpath = "//span[contains(@aria-label,'Stop')]"

    def onestop(self):
        print("clicking one stop")
        try:
             self.driver.find_element(By.XPATH, self.One_Stop_Xpath).click()
        except NoSuchElementException as e:
            print("Exception occurred :", e)
            # self.log.error("clicking one stop option failed")
            # self.log.info("update the location")
        else:
            print("clicking one stop successful")

    def twostop(self):
        print("clicking two stops")
        try:
            self.driver.find_element(By.XPATH, self.Two_Stops_Xpath).click()
        except NoSuchElementException as e:
            print("Exception occurred :", e)
            # self.log.error("clicking two stops option failed")
            # self.log.info("update the location")
        else:
            print("clicking two stops successful")

    def nonstop(self):
        print("clicking non stop")
        try:
            self.driver.find_element(By.XPATH, self.Non_Stop_Xpath).click()
        except NoSuchElementException as e:
            print("Exception occurred :", e)
            # self.log.error("clicking non stop option failed")
            # self.log.info("update the location")
        else:
            print("clicking non stop successful")

    def fetch_stop_values_in_results(self):
        print("fetching stop values")
        try:
            stops_value_in_results = self.driver.find_elements(By.XPATH, self.Stops_List_Xpath)
        except NoSuchElementException as e:
            print("Exception occurred :", e)
            # self.log.error("unable to collect stop values from results")
            # self.log.info("please update the stops values xpaths")
        else:
            print("collected stop values from results")
            print("no of stop values collected are :  {}".format(len(stops_value_in_results)))
            return stops_value_in_results


