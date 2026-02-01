import csv
import os
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any
from behave import given, when, then
from behave.runner import Context
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.products_page import ProductsPage
from utils.config import CART_PAGE_WAIT_TIMEOUT, EXPLICIT_WAIT_TIMEOUT, ORDER_SUCCESS_MESSAGE


def _load_checkout_row(csv_row_index: int) -> Dict[str, Any]:
    data_path = os.path.join(os.getcwd(), "data", "checkout_data.csv")
    with open(data_path, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    index = int(csv_row_index) - 1
    return rows[index]


def _round_price_to_two_decimals(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


@given('there are {count:d} products in the cart')
def add_products_to_cart(context: Context, count: int) -> None:
    context.products_page = ProductsPage(context.driver)
    context.products_page.add_first_n_products(count)
    context.products_page.open_cart()
    context.cart_page = CartPage(context.driver)


@when('proceeding to checkout')
def proceed_checkout(context: Context) -> None:
    context.cart_page.click_checkout()
    context.checkout_page = CheckoutPage(context.driver)


@when('entering checkout information from CSV row "{csv_row_index:d}"')
def enter_checkout_info(context: Context, csv_row_index: int) -> None:
    row = _load_checkout_row(csv_row_index)
    context.checkout_page.fill_information(
        row["first_name"], row["last_name"], row["postal_code"]
    )
    context.checkout_page.continue_checkout()
    wait = WebDriverWait(context.driver, EXPLICIT_WAIT_TIMEOUT)
    wait.until(EC.url_contains("checkout-step-two"))


@when('reviewing the order summary')
def review_order_summary(context: Context) -> None:
    wait = WebDriverWait(context.driver, EXPLICIT_WAIT_TIMEOUT)
    wait.until(EC.url_contains("checkout-step-two"))
    item_prices = context.checkout_page.get_overview_item_prices()
    context.items_sum = _round_price_to_two_decimals(sum(item_prices))
    context.summary_item_total = _round_price_to_two_decimals(context.checkout_page.get_item_total())
    context.summary_tax = _round_price_to_two_decimals(context.checkout_page.get_tax())
    context.summary_total = _round_price_to_two_decimals(context.checkout_page.get_total())


@then('item total should equal the sum of items plus tax')
def verify_summary(context: Context) -> None:
    assert context.summary_item_total == context.items_sum
    expected_total = _round_price_to_two_decimals(context.summary_item_total + context.summary_tax)
    assert context.summary_total == expected_total


@when('completing the order')
def complete_order(context: Context) -> None:
    context.checkout_page.finish_checkout()


@then('order success message should be displayed')
def verify_order_success_message(context: Context) -> None:
    message = context.checkout_page.get_success_message()
    assert ORDER_SUCCESS_MESSAGE in message


@given('having an empty cart')
def empty_cart(context: Context) -> None:
    context.products_page = ProductsPage(context.driver)
    context.products_page.open_cart()
    context.cart_page = CartPage(context.driver)


@when('attempting to checkout')
def attempt_to_checkout(context: Context) -> None:
    context.cart_page.click_checkout()


@then('checkout should be blocked for an empty cart')
def verify_checkout_is_blocked(context: Context) -> None:
    wait = WebDriverWait(context.driver, CART_PAGE_WAIT_TIMEOUT)
    wait.until(EC.url_contains("cart.html"))
    assert "cart.html" in context.driver.current_url, ("Expected to stay on cart page, " f"but navigated to: {context.driver.current_url}"
)
