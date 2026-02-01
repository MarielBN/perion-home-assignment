import json
import os
from typing import Dict, Any
from behave import given, when, then, use_step_matcher
from behave.runner import Context
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def _load_users() -> Dict[str, Any]:
    data_path = os.path.join(os.getcwd(), "data", "users.json")
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


@given('login page is displayed')
def open_login(context: Context) -> None:
    context.login_page = LoginPage(context.driver)
    context.products_page = ProductsPage(context.driver)
    context.login_page.open()


@when('login is performed using "{user_name}"')
def login(context: Context, user_name: str) -> None:
    users = _load_users()
    user = users[user_name]
    context.login_page.login(user["username"], user["password"])


use_step_matcher("re")


@then(r'login should succeed')
def login_success(context: Context) -> None:
    assert context.products_page.is_loaded(), "login failed"


@then(r'login should fail with error "(?P<error_message>[^"]*)"')
def login_fail(context: Context, error_message: str) -> None:
    actual = context.login_page.get_error_message()
    assert actual == error_message, "Expected to get an error message, " f"but navigated to: {context.driver.current_url}"


use_step_matcher("parse")
