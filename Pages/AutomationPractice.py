from selenium.webdriver.common.by import By

class GUI_Elements:
    def __init__(self, driver):
        self.driver = driver
        self.name = driver.find_element(By.ID, "name")
        self.email = driver.find_element(By.ID, "email")
        self.phone = driver.find_element(By.ID, "phone")
        self.address = driver.find_element(By.ID, "textarea")

    def set_name(self, name):
        self.name.send_keys(name)
        if self.name.get_attribute("value") == name:
            print("Name is set to " + name)
    
    def set_email(self, emai**



    .....):
        self.email.send_keys(email)

    def set_phone(self, phone):
        self.phone.send_keys(phone)

    def set_address(self, address):
        self.address.send_keys(address)