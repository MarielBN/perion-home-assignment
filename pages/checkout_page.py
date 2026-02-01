from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    SUMMARY_TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    SUMMARY_TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    OVERVIEW_ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.wait_for_visible(self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)

    def continue_checkout(self) -> None:
        self.wait_for_clickable(self.CONTINUE_BUTTON).click()

    def finish_checkout(self) -> None:
        self.wait_for_clickable(self.FINISH_BUTTON).click()

    def get_item_total(self) -> float:
        text = self.wait_for_visible(self.SUMMARY_SUBTOTAL).text
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self.wait_for_visible(self.SUMMARY_TAX).text
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.wait_for_visible(self.SUMMARY_TOTAL).text
        return float(text.split("$")[-1])

    def get_success_message(self) -> str:
        return self.wait_for_visible(self.COMPLETE_HEADER).text

    def get_overview_item_prices(self) -> List[float]:
        elements: List[WebElement] = self.wait_for_all_visible(self.OVERVIEW_ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]
