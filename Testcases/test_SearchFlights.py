from Pages.Login import Login
import pytest
from Utilities.Utilities import Utils


class Test_Stop_Values:
    # log = Utils.custom_logger(newlog=True)


    @pytest.fixture(autouse=True)
    def object_setup(self, browser_setup):
        self.driver = browser_setup
        self.login = Login(self.driver)
        self.utils = Utils()


    # @ddt(("Chennai", "Kuwait", "15/01/2026", "1 Stop"))
    # @unpack
    @pytest.mark.parametrize(("s", "d", "j", "v"),[("Chennai", "Kuwait", "15/04/2026", "1 Stop"), ("Bangalore", "Kuwait", "13/04/2026", "1 Stop"), ("New Delhi", "Kuwait", "17/04/2026", "1 Stop")])
    # @pytest.mark.parametrize(("s", "d", "j", "v"), [("Chennai", "Kuwait", "15/03/2026", "1 Stop")])
    def test_onestop(self, s, d, j, v):
        print("*********************************** Started testing test_onestop******************************************")
        search =self.login.exclude_login()
        flight_results = search.search_for_flights(s, d, j)
        flight_results.onestop()
        flight_results.page_scroll_down()
        stop_values = flight_results.fetch_stop_values_in_results()
        print(len(stop_values))
        fail = self.utils.compare_text_of_elements(list(stop_values), v)
        if fail > 0:
            self.driver.save_screenshot("../Screenshots/test_onestop_fail.png")
        else:
            self.driver.save_screenshot("../Screenshots/test_onestop_pass.png")
        assert fail < len(stop_values)
        print( "***********************************test_onestop completed*****************************************")