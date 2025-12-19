import pytest
from Pages.Login import Login
from Utilities.Utilities import Utils

class TestLogin:

    @pytest.fixture(autouse=True, scope="function")
    def class_setup(self, browser_setup):
        self.url = "https://practicetestautomation.com/practice-test-login/"
        self.driver = browser_setup
        self.logger = Utils.custom_logger()
        self.loginpage = Login(self.driver)
        self.case = 0
        self.file_name = "Login_Test_Data"
        self.sheet_name = "Login_Test_Data"


    test_data_2 = Utils.dataquery("pavan", "select test_id, user_name, user_password, message, login from login_test")
    @pytest.mark.database
    @pytest.mark.parametrize(("test_id", "username", "password", "user_message_validation", "login_indicator"),
                             test_data_2)
    def test_login_3(self, test_id, username, password, user_message_validation, login_indicator):
        self.case += 1
        user_message, login_ind = self.loginpage.login(username, password)
        try:
            if (user_message_validation in user_message) and (login_indicator == login_ind):
                assert True
            else:
                assert False
        except AssertionError as e:
            self.logger.error("Test failed")
            self.logger.error(e)
            assert False
        else:
            self.logger.info("Test completed successfully")