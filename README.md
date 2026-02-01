# SauceDemo Automated Tests (Behave + Selenium)

Automated tests for [SauceDemo](https://www.saucedemo.com) using **Behave** (BDD) and **Selenium WebDriver**, with Page Object Model, data-driven login (JSON), checkout data (CSV), and Docker support.

## Features Covered

- **Login**: Valid/invalid/locked-out users (data-driven with Scenario Outline)
- **Products**: Listing, names/prices validation, sort (Low→High, High→Low)
- **Cart**: Add 3 products, badge count, remove 1, cart updates
- **Checkout**: Full flow with details from CSV file, order summary (subtotal + tax), success message
- **Negative**: Empty cart checkout prevented, locked-out user error message

## Project Structure

```
data/
  users.json
  checkout_data.csv
features/
  steps/
    cart_steps.py
    checkout_steps.py
    login_steps.py
    products_steps.py
  cart.feature
  checkout.feature
  environment.py
  login.feature
  products.feature
pages/
  base_page.py
  cart_page.py
  checkout_page.py
  login_page.py
  products_page.py
utils/
  config.py
  driver_factory.py
Dockerfile
README.md
requirements.txt
```

## Prerequisites

- Python 3.11+
- Chrome or Firefox
- ChromeDriver / geckodriver on PATH (or use Selenium 4’s built-in manager)

## Setup

```bash
# From project root
pip install -r requirements.txt
```

Ensure Chrome or Firefox is installed. Selenium 4 can manage drivers automatically in many setups.

## How to Run Tests Locally

```bash
behave -f pretty --color
```

Run a single feature:

```bash
behave features/login.feature -f pretty --color
```

## How to Run Tests Headless

Use the `HEADLESS` environment variable:

**Windows (PowerShell):**

```powershell
$env:HEADLESS="true"; behave -f pretty --color
```

**Linux/macOS:**

```bash
HEADLESS=true behave -f pretty --color
```

## Browser Selection

Default is Chrome. To use Firefox:

**Windows (PowerShell):**

```powershell
$env:BROWSER="firefox"; behave -f pretty --color
```

**Linux/macOS:**

```bash
BROWSER=firefox behave -f pretty --color
```

## How to Build and Run with Docker

Build the image:

```bash
docker build -t behave-tests .
```

Run all tests (Chrome inside the container):

```bash
docker run --rm behave-tests
```

Note:
- The Docker image runs Chrome in a virtual display (Xvfb) by default for stability.
- A fresh browser session is started per scenario to avoid cross-scenario state bleed.
- You can still force headless mode with `-e HEADLESS=true`.

Run with custom options (e.g. one feature, format):

```bash
docker run --rm behave-tests behave features/login.feature -f pretty
```

By default the container writes:

- **Screenshots**: `/app/screenshots`
- **HTML report**: `/app/reports/report.html`

### Windows (PowerShell)

```powershell
docker run --rm `
  -v ${PWD}\screenshots:/app/screenshots `
  -v ${PWD}\reports:/app/reports `
  behave-tests
```

If tests error in Docker, check the saved screenshot(s) and the printed URL/title to see where the browser is stuck.

### Linux/macOS

```bash
docker run --rm \
  -v "$(pwd)/screenshots:/app/screenshots" \
  -v "$(pwd)/reports:/app/reports" \
  behave-tests
```

## HTML Report

Install a reporter and run with it.

**Using `behave-html-formatter`:**

```bash
pip install behave-html-formatter
behave -f behave_html_formatter:HTMLFormatter -o report.html
```

Then open `report.html` in a browser.

### Docker HTML report

```powershell
docker run --rm `
  -v ${PWD}\reports:/app/reports `
  behave-tests behave -f behave_html_formatter:HTMLFormatter -o /app/reports/report.html
```

**Using `allure-behave` (Allure):**

```bash
pip install allure-behave
behave -f allure_behave.formatter:AllureFormatter -o allure_results
allure serve allure_results
```

## Configuration

- **Base URL**: Set `SAUCEDEMO_URL` (default: `https://www.saucedemo.com`)
- **Headless**: Set `HEADLESS=true`
- **Browser**: Set `BROWSER=chrome` or `BROWSER=firefox`
- **Waits**: `utils/config.py` – `EXPLICIT_WAIT_TIMEOUT` (default 10 seconds)

## Screenshots on Failure

On any step failure, a screenshot is saved under the `screenshots/` directory (created automatically), with a filename derived from the scenario name and timestamp.

