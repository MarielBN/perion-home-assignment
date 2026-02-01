from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from utils.config import HEADLESS, BROWSER, CHROMEDRIVER_PATH, GECKODRIVER_PATH


def create_driver():
    browser_name = BROWSER.lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "profile.password_manager_leak_detection": False,
            },
        )
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        if CHROMEDRIVER_PATH:
            service = ChromeService(executable_path=CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        if GECKODRIVER_PATH:
            service = FirefoxService(executable_path=GECKODRIVER_PATH)
            driver = webdriver.Firefox(service=service, options=options)
        else:
            driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")

    if not HEADLESS:
        driver.maximize_window()
    return driver
