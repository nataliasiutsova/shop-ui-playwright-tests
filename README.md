# Shop UI Playwright Test Framework

Layered UI test framework for the **SauceDemo** web application built with **Python**, **Playwright**, and **Allure**. Covers **41 tests** including smoke, regression, and end-to-end business flows.

[![Tests](https://github.com/nataliasiutsova/shop-ui-playwright-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/nataliasiutsova/shop-ui-playwright-tests/actions)
[![Latest Allure Report](https://img.shields.io/badge/latest_allure_report-orange)](https://nataliasiutsova.github.io/shop-ui-playwright-tests/)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Playwright](https://img.shields.io/badge/playwright-1.40-green)
![pytest](https://img.shields.io/badge/pytest-8.0-green)

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              Tests (pytest)                 │
│   tests/test_login.py  tests/test_cart.py   │
│   tests/test_inventory.py  ...              │
└───────────────────┬─────────────────────────┘
                    │ fixtures (DI)
                    ▼
┌─────────────────────────────────────────────┐
│            Page Object Model                │
│  LoginPage  InventoryPage  CartPage         │
│  CheckoutPage (encapsulate locators)        │
└───────────────────┬─────────────────────────┘
                    │ inherits
                    ▼
┌─────────────────────────────────────────────┐
│               BasePage                      │
│  (common actions: click, waits, screenshot) │
└───────────────────┬─────────────────────────┘
                    │ uses
                    ▼
┌─────────────────────────────────────────────┐
│       Playwright (Browser Context)          │
└─────────────────────────────────────────────┘
```

**Design principles:**

- **Tests** verify user behavior. They don't know about CSS selectors or XPath.
- **Page Objects** encapsulate locators and page-specific actions. If the UI changes, only one file changes.
- **BasePage** provides shared utilities (waits, screenshots, assertions) for all pages.
- **Browser Context** is isolated per test to prevent state leakage (localStorage, cookies).

---

## Test Coverage

| Area | Tests  | Scope |
| :--- |:-------| :--- |
| **Login** | 7      | Valid/invalid credentials, locked user, empty fields |
| **Inventory** | 12     | Product list, sorting, add/remove cart, button states |
| **Cart** | 8      | Empty cart, add/remove items, navigation, checkout |
| **Checkout** | 11     | Form validation, overview, total calc, complete order |
| **Logout** | 2      | Session persistence, redirect, access control |
| **E2E** | 2      | Full purchase flow (login → cart → checkout → complete) |
| **Total** | **41** | |

**Common coverage:** Allure steps, screenshots, negative cases (validation errors, access denied).

---

## Tech Stack

| Layer | Tool |
| :--- | :--- |
| Language | Python 3.12 |
| Browser Automation | Playwright |
| Test Runner | pytest |
| Reporting | Allure |
| Parallel Execution | pytest-xdist |
| CI/CD | GitHub Actions |

---

## Run Tests

### 🤖 1. Via GitHub Actions (no local setup)

1. Open **Actions → UI Tests**.
2. Click **Run workflow**.
3. Choose marker: `smoke` / `regression` / `e2e` / `all`.
4. Click **Run workflow**.
5. Open the **Summary** tab — direct link to the Allure report.

**→ [Latest report](https://nataliasiutsova.github.io/shop-ui-playwright-tests/)**

### 🐍 2. Locally (requires Python + Allure CLI)

```bash
# 1. Clone the repository
git clone git@github.com:YOUR_USERNAME/shop-ui-playwright-tests.git
cd shop-ui-playwright-tests

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium

# 4. Make the runner executable
chmod +x run_tests.sh

# 5. Run all tests (with script)
./run_tests.sh

# Or run specific marker
pytest -m smoke -v
pytest -m regression -v

# Or run in parallel (4 workers)
pytest -m "(regression or e2e) and not smoke" -n 4 --dist loadfile -v

# Or watch the browser
pytest -m smoke --headed --slowmo=500 -v
```

---

## Test Markers

| Marker | Purpose | Run |
| :--- | :--- | :--- |
| `smoke` | Critical path, fast feedback | `pytest -m smoke` |
| `regression` | Full regression suite | `pytest -m regression` |
| `e2e` | End-to-end business flows | `pytest -m e2e` |

---

## Allure Reports

- **Live:** [nataliasiutsova.github.io/shop-ui-playwright-tests](https://nataliasiutsova.github.io/shop-ui-playwright-tests/)
- **Trend:** History preserved across CI runs
- **Categories:** Product defects / Test defects / Infrastructure
- **Environment:** Browser, executor, OS

---

## Author

**Natalia Siutsova**
- GitHub: [@nataliasiutsova](https://github.com/nataliasiutsova)
- LinkedIn: [linkedin.com/in/natalia-siutsova](https://linkedin.com/in/natalia-siutsova)

## License

[MIT](LICENSE)