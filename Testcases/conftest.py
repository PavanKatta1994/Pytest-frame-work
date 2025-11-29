from selenium import webdriver
import pytest
from Utilities.Utilities import Utils
from datetime import datetime
from pytest_html import extras
import os
import openpyxl

@pytest.fixture(scope="function")
def browser_setup(browser):
    log = Utils.custom_logger()
    if browser == "chrome":
        log.info("Opening Chrome browser")
        driver = chrome_module()
    elif browser == "edge":
        log.info("Opening edge browser")
        driver = edge_module()
    elif browser == "firefox":
        log.info("Opening firefox browser")
        driver = firefox_module()
    else:
        log.info("No browser specified in run time")
        log.info("Opening chrome browser")
        driver = edge_module("https://practicetestautomation.com/practice-test-login/")
    yield driver
    driver.close()


def chrome_module():
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    service = Service("D:\\TestFrameWork\\WebDrivers\\chromedriver.exe")
    options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 1}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.yatra.com/")
    return driver

def edge_module(url=None):
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.edge.options import Options
    service = Service("D:\\TestFrameWork\\WebDrivers\\msedgedriver.exe")
    options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 1}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=service, options=options)
    if url is None:
        driver.get("https://www.yatra.com/")
    else:
        driver.get(url)
    return driver

def firefox_module():
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options
    service = Service("D:\\TestFrameWork\\WebDrivers\\geckodriver.exe")
    options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 1}
    options.profile = "C:\\Users\\pavan\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\Eh0822ch.Profile 1"
    options.add_argument("--enable-notifications")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.yatra.com/")
    return driver

def pytest_addoption(parser):
    parser.addoption("--browser")

@pytest.fixture(autouse=True, scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            # Create screenshot folder if needed
            screenshot_dir = os.path.join(os.getcwd(), "Screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            # Build filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Save screenshot
            driver.save_screenshot(filepath)

            # Attach screenshot to pytest-html
            if hasattr(report, "extra"):
                # Option 1: Embed image directly
                report.extra.append(extras.image(filepath))
                # Option 2: Add clickable link
                report.extra.append(extras.url("file://" + filepath, name="Screenshot Link"))