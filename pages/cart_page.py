from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    REMOVE_BUTTON_BY_ID = (By.CSS_SELECTOR, "[data-test^='remove-']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']") 

    def get_cart_items_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_cart_product_ids(self) -> List[str]:
        buttons: List[WebElement] = self.driver.find_elements(*self.REMOVE_BUTTON_BY_ID)
        prefix = "remove-"
        ids: List[str] = []
        for btn in buttons:
            attr = btn.get_attribute("data-test")
            if attr and attr.startswith(prefix):
                ids.append(attr[len(prefix):])
        return ids

    def remove_item_by_id(self, product_id: str, timeout: int = 10) -> None:
        locator = (By.CSS_SELECTOR, f'[data-test="remove-{product_id}"]')
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    def remove_first_item(self) -> None:
        product_ids: List[str] = self.get_cart_product_ids()
        if product_ids:
            self.remove_item_by_id(product_ids[0])

    def get_cart_badge_count(self) -> int:
        try:
            return int(self.wait_for_visible(self.CART_BADGE).text)
        except Exception:
            return 0

    def click_checkout(self) -> None:
        self.wait_for_clickable(self.CHECKOUT_BUTTON).click()
