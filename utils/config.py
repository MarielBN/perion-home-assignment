import os

BASE_URL = os.environ.get("SAUCEDEMO_URL", "https://www.saucedemo.com")
HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"
BROWSER = os.environ.get("BROWSER", "chrome")
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
GECKODRIVER_PATH = os.environ.get("GECKODRIVER_PATH")  


IMPLICIT_WAIT = 0
EXPLICIT_WAIT_TIMEOUT = int(os.environ.get("EXPLICIT_WAIT_TIMEOUT", "10"))
CART_PAGE_WAIT_TIMEOUT = int(os.environ.get("CART_PAGE_WAIT_TIMEOUT", "3"))
CART_ITEMS_WAIT_TIMEOUT = int(os.environ.get("CART_ITEMS_WAIT_TIMEOUT", "5"))


ORDER_SUCCESS_MESSAGE = os.environ.get("ORDER_SUCCESS_MESSAGE", "Thank you for your order")


SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
