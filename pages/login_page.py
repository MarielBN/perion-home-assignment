from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    URL = f"{BASE_URL}/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> None:
        self.driver.get(self.URL)

    def login(self, username: str, password: str) -> None:
        self.wait_for_visible(self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_clickable(self.LOGIN_BUTTON).click()

    def get_error_message(self) -> str:
        return self.wait_for_visible(self.ERROR_MESSAGE).text
