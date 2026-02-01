from typing import List
from behave import when, then
from behave.runner import Context
from selenium.webdriver.support.ui import WebDriverWait
from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from utils.config import CART_ITEMS_WAIT_TIMEOUT


@when('adding {count:d} products to the cart')
def add_products(context: Context, count: int) -> None:
    context.products_page = ProductsPage(context.driver)
    context.products_page.add_first_n_products(count)


@then('cart badge should show {count:d} items')
def verify_cart_badge_count(context: Context, count: int) -> None:
    assert context.products_page.get_cart_badge_count() == count, f"Expected badge count to be {count}, but got {context.products_page.get_cart_badge_count()} instead"


@when('opening the cart')
def open_cart(context: Context) -> None:
    context.products_page.open_cart()
    context.cart_page = CartPage(context.driver)


@when('removing the product at position {position:d} from the cart')
def remove_product_at_position(context: Context, position: int) -> None:
    product_ids: List[str] = context.cart_page.get_cart_product_ids()
    index = position - 1
    assert 0 <= index < len(product_ids), f"Position {position} is out of range for {len(product_ids)} items"
    context.removed_product_id = product_ids[index]
    context.expected_remaining_ids = [pid for i, pid in enumerate(product_ids) if i != index]
    context.cart_page.remove_item_by_id(context.removed_product_id)


@then('cart should have {count:d} items')
def verify_cart_count(context: Context, count: int) -> None:
    WebDriverWait(context.driver, CART_ITEMS_WAIT_TIMEOUT).until(
        lambda d: context.cart_page.get_cart_items_count() == count
    )
    assert context.cart_page.get_cart_items_count() == count, f"Expected cart items count to be {count}, but got {context.products_page.get_cart_items_count()} instead"


@then('the removed product should not be in the cart')
def verify_removed_product_not_in_cart(context: Context) -> None:
    current_ids: List[str] = context.cart_page.get_cart_product_ids()
    assert context.removed_product_id not in current_ids, (
        f"Removed product '{context.removed_product_id}' is still in the cart: {current_ids}"
    )


@then('the cart should contain only the other products')
def verify_cart_contains_only_remaining_products(context: Context) -> None:
    current_ids: List[str] = context.cart_page.get_cart_product_ids()
    expected: List[str] = context.expected_remaining_ids
    assert set(current_ids) == set(expected) and len(current_ids) == len(expected), (
        f"Cart contents mismatch: expected {expected}, got {current_ids}"
    )