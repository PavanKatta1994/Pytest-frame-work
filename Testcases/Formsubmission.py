from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.chrome.service import Service

class Automation:

    def chrome_browser(self):
        service = Service("D:\TestFrameWork\WebDrivers\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://testautomationpractice.blogspot.com/")
        return self.driver

    def test_01(self):
        driver = self.chrome_browser()
