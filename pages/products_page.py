from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class ProductsPage(BasePage):
    INVENTORY_LIST = (By.CSS_SELECTOR, "[data-test='inventory-list']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart-']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")

    def is_loaded(self) -> bool:
        self.wait_for_visible(self.INVENTORY_LIST)
        return True

    def get_product_names(self) -> List[str]:
        elements: List[WebElement] = self.wait_for_all_visible(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def get_product_prices(self) -> List[float]:
        elements: List[WebElement] = self.wait_for_all_visible(self.ITEM_PRICES)
        prices: List[float] = []
        for el in elements:
            text = el.text.replace("$", "").strip()
            prices.append(float(text))
        return prices

    def sort_by_visible_text(self, text: str) -> None:
        dropdown = self.wait_for_visible(self.SORT_DROPDOWN)
        Select(dropdown).select_by_visible_text(text)

    def add_first_n_products(self, count: int) -> None:
        buttons: List[WebElement] = self.wait_for_all_visible(self.ADD_TO_CART_BUTTONS)
        for button in buttons[:count]:
            button.click()

    def add_product_by_id(self, product_id: str) -> None:
        locator = (By.CSS_SELECTOR, f'[data-test="add-to-cart-{product_id}"]')
        self.wait_for_clickable(locator).click()

    def get_cart_badge_count(self) -> int:
        try:
            return int(self.wait_for_visible(self.CART_BADGE).text)
        except Exception:
            return 0

    def open_cart(self) -> None:
        self.wait_for_clickable(self.CART_LINK).click()
