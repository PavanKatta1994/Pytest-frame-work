import pytest
from Pages.Login import Login
from Utilities.Utilities import Utils
import softest

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


    @pytest.mark.param
    @pytest.mark.parametrize(("username", "password", "user_message_validation", "login_indicator"),[("student","Password123","Congratulations","True"),
          ("incorrectUser","Password123","Your username is invalid!","False"),
          ("student","incorrectPassword","Your password is invalid!","False")])
    def test_login(self, username, password, user_message_validation, login_indicator):
        test = softest.TestCase()
        user_message, login_ind = self.loginpage.login(username,password)
        assert user_message_validation in user_message
        assert login_indicator == login_ind

    test_data = Utils.ExcelData("Login_Test_Data","Login_Test_Data")
    @pytest.mark.excel
    @pytest.mark.parametrize(("test_id","username", "password", "user_message_validation", "login_indicator"),test_data)
    def test_login_2(self, test_id,username, password, user_message_validation, login_indicator):
        self.case += 1
        user_message, login_ind = self.loginpage.login(username, password)
        try:
            if (user_message_validation in user_message) and (login_indicator == login_ind):
                Utils.update_excel(self.file_name, self.sheet_name, "Test Result", test_id, "Passed")
                assert True
            else:
                Utils.update_excel(self.file_name, self.sheet_name, "Test Result", test_id, "Failed")
                assert False
        except AssertionError as e:
            self.logger.error("Test failed")
            self.logger.error(e)
            Utils.update_excel(self.file_name, self.sheet_name, "Test Result",test_id, "Failed")
            assert False
        else:
            self.logger.info("Test completed successfully")
        finally:
            Utils.update_excel(self.file_name, self.sheet_name, "Test Status", test_id, "Tested")

    test_data_2 = Utils.dataquery("pavan", "select test_id, user_name, user_password, message, login from login_test")



    @pytest.mark.database
    @pytest.mark.parametrize(("test_id", "username", "password", "user_message_validation", "login_indicator"),
                             test_data_2)
    def test_login_3(self, test_id, username, password, user_message_validation, login_indicator):
        self.case += 1
        user_message, login_ind = self.loginpage.login(username, password)
        try:
            if (user_message_validation in user_message) and (login_indicator == login_ind):
                # Utils.update_excel(self.file_name, self.sheet_name, "Test Result", int(test_id), "Passed")
                assert True
            else:
                # Utils.update_excel(self.file_name, self.sheet_name, "Test Result",  int(test_id), "Failed")
                assert False
        except AssertionError as e:
            self.logger.error("Test failed")
            self.logger.error(e)
            # Utils.update_excel(self.file_name, self.sheet_name, "Test Result", test_id, "Failed")
            assert False
        else:
            self.logger.info("Test completed successfully")
        # finally:
        # Utils.update_excel(self.file_name, self.sheet_name, "Test Status", test_id, "Tested")