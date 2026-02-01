import os
import traceback
from datetime import datetime

from utils.driver_factory import create_driver
from utils.config import BASE_URL, EXPLICIT_WAIT_TIMEOUT, IMPLICIT_WAIT


def before_all(context):
    context.base_url = BASE_URL
    context.wait_timeout = EXPLICIT_WAIT_TIMEOUT

    context.screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(context.screenshot_dir, exist_ok=True)


def before_scenario(context, scenario):
    context.driver = create_driver()
    context.driver.implicitly_wait(IMPLICIT_WAIT)
    context._scenario_name = getattr(scenario, "name", "scenario")


def after_scenario(context, scenario):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()


def after_step(context, step):
    if step.status not in ("failed", "error"):
        return

    if not (hasattr(context, "driver") and context.driver):
        return

    try:
        try:
            print(f"\nURL at failure: {context.driver.current_url}")
            print(f"Title at failure: {context.driver.title}")
        except Exception:
            pass

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scenario_name = getattr(context, "_scenario_name", "failure")
        name = str(scenario_name).replace(" ", "_")[:50]
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(context.screenshot_dir, filename)
        context.driver.save_screenshot(filepath)
        print(f"\nScreenshot saved: {filepath}")
    except Exception as e:
        print(f"Failed to save screenshot: {e}")
        traceback.print_exc()

