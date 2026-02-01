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

Run all tests:

```bash
docker run --rm behave-tests
```

Run with custom options (e.g. one feature, format):

```bash
docker run --rm behave-tests behave features/login.feature -f pretty
```

By default the container writes:

- **Screenshots**: `/app/screenshots`

## Configuration

- **Base URL**: Set `SAUCEDEMO_URL` (default: `https://www.saucedemo.com`)
- **Headless**: Set `HEADLESS=true`
- **Browser**: Set `BROWSER=chrome` or `BROWSER=firefox`
- **Waits**: `utils/config.py` – `EXPLICIT_WAIT_TIMEOUT`

## Screenshots on Failure

On any step failure, a screenshot is saved under the `screenshots/` directory (created automatically), with a filename derived from the scenario name and timestamp.

