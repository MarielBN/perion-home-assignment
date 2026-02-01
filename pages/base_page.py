from typing import Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import EXPLICIT_WAIT_TIMEOUT


Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, EXPLICIT_WAIT_TIMEOUT)

    def wait_for_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_all_visible(self, locator: Locator) -> List[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))
