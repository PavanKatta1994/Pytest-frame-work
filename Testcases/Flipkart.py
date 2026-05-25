from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pytest


class Flipkart:
    def __init__(self):
        service = Service("D:\TestFrameWork\WebDrivers\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://www.flipkart.com")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.ac = ActionChains(self.driver)
        self.items_found_xpath = "//div[@class=normalize-space('QSCKDh dLgFEE')]/div"
        self.item_name_xpath = "//a/div[2]/div[1]/div[1]"
        self.item_price_xpath = "//a/div[2]/div[2]/div[1]/div/div"
        try:
            login_window = self.driver.find_element(By.XPATH, "//span[@class='b3wTlE']")
        except NoSuchElementException:
            print("No login window found")
        else:
            login_window.click()

    def search(self, keyword):
        search_field = self.driver.find_element(By.NAME, "q")
        search_field.send_keys(keyword)
        search_field.send_keys(Keys.RETURN)

    def get_names_prices_all_items(self):

        total_items = self.driver.find_elements(By.XPATH, self.items_found_xpath)
        print("Total items: ", len(total_items))
        names_prices = {}
        for i in range(2,len(total_items)+2):
            try:
                name_found = self.driver.find_element(By.XPATH, self.items_found_xpath + "[" + str(
                    i) + "]" + self.item_name_xpath)
                price_found = price = self.driver.find_element(By.XPATH,
                                                               self.items_found_xpath + "[" + str(
                                                                   i) + "]" + self.item_price_xpath)
            except NoSuchElementException:
                print("This component has issue", i)
                continue

            self.ac.scroll_to_element(name_found).perform()
            name = name_found.text
            price = float(price_found.text.strip("₹").strip(","))
            # print(name, price)
            names_prices[name] = price

        print("Total items retrieved = ", len(names_prices), "from", len(total_items))
        return names_prices

    def get_prices_all_items(self):
        prices_found = self.driver.find_elements(By.XPATH, "//div[@class='QSCKDh dLgFEE']/div")
        print("Total items: ", len(prices_found))
        prices = []
        for i in range(2,len(prices_found)+2):
            try:
                element = self.driver.find_element(By.XPATH, "//div[@class='QSCKDh dLgFEE']/div" + "[" + str(i)
                                            + "]" + "//div[@class='oFEPlD']")
            except NoSuchElementException:
                break
            self.ac.scroll_to_element(element).perform()
            sleep(1)
            price_found = element.text
            if '%' in price_found:
                final_price_found = self.driver.find_element(By.XPATH, "//div[@class='QSCKDh dLgFEE']/div" + "[" + str(i)
                                                       + "]" + "//div[@class='hZ3P6w DeU9vF']").text
            else:
                final_price_found = price_found

            price_int = int(final_price_found.replace("₹", "").replace(",", ""))
            prices.append(price_int)
        print("No of prices taken: ", len(prices))
        return prices

    def get_names_all_items(self):
        names_found = self.driver.find_elements(By.XPATH, "//div[@class='RG5Slk']")
        print("Total items: ", len(names_found))
        names = []
        for name in names_found:
            self.ac.scroll_to_element(name).perform()
            names.append(name.text)
        return names

    def click_on(self, text):
        try:
            self.driver.find_element(By.XPATH, '//div[text()="' + text +'"]').click()
            print("Successfully clicked on", text)
            sleep(5)
        except NoSuchElementException:
            print("element not found for clicking")
            print("check the link test provided", text)


    def close(self):
        self.driver.close()




class Test_Flipkart:

    @pytest.mark.skip
    def test_one(self):
        test = Flipkart()
        search_value = "Iphone 17 pro max"
        test.search(search_value)
        names = test.get_names_all_items()
        assert search_value.lower() in names[0].lower()
        test.close()

    def test_two(self):
        test = Flipkart()
        search_value = "Iphone 17 pro max"
        test.search(search_value)
        test.click_on("Price -- Low to High")
        prices = list(test.get_prices_all_items())
        prices_asc = sorted(prices)
        assert prices == prices_asc
        test.close()


