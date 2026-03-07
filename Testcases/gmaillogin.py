from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep as sl

service = Service("D:\TestFrameWork\WebDrivers\chromedriver.exe")

driver = webdriver.Chrome(service=service)
driver.get("https://mail.google.com/")
driver.maximize_window()
driver.find_element(By.ID, "identifierId").send_keys("pavan.katta789")
driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()