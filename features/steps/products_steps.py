import json
import logging
import os
from typing import Dict, Any, List
from behave import given, when, then
from behave.runner import Context
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def _load_users() -> Dict[str, Any]:
    data_path = os.path.join(os.getcwd(), "data", "users.json")
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


@given('user is logged in as "{user_name}"')
def login_as_user(context: Context, user_name: str) -> None:
    users = _load_users()
    user = users[user_name]
    context.login_page = LoginPage(context.driver)
    context.products_page = ProductsPage(context.driver)
    context.login_page.open()
    context.login_page.login(user["username"], user["password"])
    assert context.products_page.is_loaded() is True


@then("product listing should be visible")
def listing_visible(context: Context) -> None:
    assert context.products_page.is_loaded() is True, "Failed to load products page"


@then("all product names should be non-empty")
def verify_products_names_are_populated(context: Context) -> None:
    names: List[str] = context.products_page.get_product_names()
    logging.info(f"names: {names}")
    assert names
    assert all(name for name in names), "Product name is empty"


@then("all product prices should be greater than 0")
def verify_products_prices_are_positive(context: Context) -> None:
    prices: List[float] = context.products_page.get_product_prices()
    logging.info(f"prices_positive: {prices}")
    assert prices
    assert all(price > 0 for price in prices), f"Expected prices to be greater than 0, but got {prices} instead"


@when('sorting products by "{sort_option}"')
def sort_products(context: Context, sort_option: str) -> None:
    context.products_page.sort_by_visible_text(sort_option)


@then("product prices should be sorted {direction}")
def verify_products_prices_are_sorted(context: Context, direction: str) -> None:
    prices: List[float] = context.products_page.get_product_prices()
    print(f"prices: {prices}")
    logging.info(f"prices: {prices}")

    direction = direction.strip().lower()
    if direction == "ascending":
        assert prices == sorted(prices), "Expected prices to be sorted by ascending order"
    elif direction == "descending":
        assert prices == sorted(prices, reverse=True), "Expected prices to be sorted by descending order"
    else:
        raise AssertionError(
            f'Unknown sort direction "{direction}". Expected "ascending" or "descending".'
        )
