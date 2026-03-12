import pytest
from Pages.Login import Login
from Utilities.Utilities import Utils
import softest

class TestLogin:

    @pytest.fixture(autouse=True, scope="function")
    def class_setup(self, browser_setup_2):
        self.url = "https://practicetestautomation.com/practice-test-login/"
        self.driver = browser_setup_2
        # self.logger = Utils.custom_logger()
        self.loginpage = Login(self.driver)
        self.case = 0
        self.file_name = "Login_Test_Data"
        self.sheet_name = "Login_Test_Data"


    @pytest.mark.param
    @pytest.mark.parametrize(("username", "password", "user_message_validation", "login_indicator"),[("student","Password123","Congratulations","True"),
          ("incorrectUser","Password123","Your username is invalid!","False"),
          ("student","incorrectPassword","Your password is invalid!","False")])
    # @pytest.mark.parametrize(("username", "password", "user_message_validation", "login_indicator"),
    #                          [("student", "Password123", "Congratulations", "True")])
    def test_login(self, username, password, user_message_validation, login_indicator):
        test = softest.TestCase()
        user_message, login_ind = self.loginpage.login(username,password)
        assert user_message_validation in user_message
        assert login_indicator == login_ind