from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:

    def __init__(self):

        self.driver = None

    # =====================================================
    # Launch Browser
    # =====================================================
    def launch_browser(self):

        chrome_options = Options()

        chrome_options.add_argument("--start-maximized")

        # Automatically downloads latest compatible ChromeDriver
        service = Service(
            ChromeDriverManager().install()
        )

        self.driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

        print("Browser launched successfully")

    # =====================================================
    # Open URL
    # =====================================================
    def open_url(self, url: str):

        if not self.driver:
            raise Exception("Browser is not launched")

        self.driver.get(url)

        print(f"Opened URL : {url}")

    # =====================================================
    # Get Page Title
    # =====================================================
    def get_page_title(self):

        if not self.driver:
            raise Exception("Browser is not launched")

        title = self.driver.title

        return title

    # =====================================================
    # Close Browser
    # =====================================================
    def close_browser(self):

        if self.driver:
            self.driver.quit()
            print("Browser closed successfully")


# =====================================================
# Example Usage
# =====================================================

browser = BrowserManager()

browser.launch_browser()

browser.open_url("https://www.google.com")

page_title = browser.get_page_title()

print(f"Page Title : {page_title}")

browser.close_browser()