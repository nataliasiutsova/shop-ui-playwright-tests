import os
import json
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.users import STANDARD_USER


load_dotenv()


BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

BROWSER_CONTEXT_OPTS = {
    "viewport": {"width": 1920, "height": 1080},
    "locale": "en-US",
    "timezone_id": "Europe/Minsk",
}


@pytest.fixture(scope="session", autouse=True)
def setup_allure_metadata(request):

    results_dir = request.config.getoption("--alluredir", default=None)
    if not results_dir:
        results_dir = os.getenv("ALLURE_DIR", "allure-results")

    try:
        os.makedirs(results_dir, exist_ok=True)
    except (PermissionError, OSError):
        return

    if not os.access(results_dir, os.W_OK):
        return

    # ---------- Executor ----------
    if os.getenv("GITHUB_ACTIONS") == "true":
        executor = {
            "name": "GitHub Actions",
            "type": "github",
            "buildName": f"CI #{os.getenv('GITHUB_RUN_NUMBER', 'unknown')}",
            "buildUrl": (
                f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/"
                f"{os.getenv('GITHUB_REPOSITORY', 'unknown')}/actions/runs/"
                f"{os.getenv('GITHUB_RUN_ID', 'unknown')}"
            ),
            "reportName": "GitHub Actions Report",
        }
    elif os.path.exists("/.dockerenv"):
        executor = {
            "name": "Docker",
            "type": "docker",
            "buildName": "docker-local",
            "buildUrl": "http://localhost",
            "reportName": "Docker Report",
        }
    else:
        executor = {
            "name": "Local",
            "type": "local",
            "buildName": "local-dev",
            "buildUrl": "http://localhost",
            "reportName": "Local Report",
        }

    try:
        with open(os.path.join(results_dir, "executor.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(executor, indent=2, ensure_ascii=False))
    except OSError:
        pass

    # ---------- Environment ----------
    environment = {
        "Base.URL": BASE_URL,
        "Environment": "CI" if os.getenv("GITHUB_ACTIONS") == "true"
                       else "Docker" if os.path.exists("/.dockerenv")
                       else "Local",
        "Executor": executor["name"],
        "Browser": "Chromium",
        "Python.Version": os.sys.version.split()[0],
    }

    try:
        with open(os.path.join(results_dir, "environment.properties"), "w", encoding="utf-8") as f:
            for k, v in environment.items():
                f.write(f"{k}={v}\n")
    except OSError:
        pass

    # ---------- Categories ----------
    categories = [
        {
            "name": "Product defects",
            "matchedStatuses": ["failed"],
        },
        {
            "name": "Test defects",
            "matchedStatuses": ["broken"],
        },
        {
            "name": "Infrastructure problems",
            "messageRegex": ".*Timeout.*|.*Connection.*|.*net::ERR.*",
            "matchedStatuses": ["broken", "failed"],
        },
        {
            "name": "Element not found",
            "messageRegex": ".*locator resolved to 0 elements.*",
            "matchedStatuses": ["failed"],
        },
    ]

    try:
        with open(os.path.join(results_dir, "categories.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(categories, indent=2, ensure_ascii=False))
    except OSError:
        pass


@pytest.fixture(scope="function")
def context(browser):
    """Create an isolated browser context with custom options."""
    context = browser.new_context(**BROWSER_CONTEXT_OPTS)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Create a new page inside the custom context."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def clean_cart(page: Page, base_url: str) -> Page:
    """Clear localStorage before each test to isolate cart state."""
    page.goto(base_url)
    page.evaluate("localStorage.clear()")
    page.reload()
    return page


@pytest.fixture
def login_page(clean_cart: Page, base_url: str) -> LoginPage:
    """Login page object fixture (with clean cart)."""
    return LoginPage(clean_cart, base_url)


@pytest.fixture
def logged_in_page(clean_cart: Page, base_url: str) -> Page:
    """Page with a logged-in standard user and clean cart."""
    login = LoginPage(clean_cart, base_url)
    login.open()
    login.login(STANDARD_USER.username, STANDARD_USER.password)
    return clean_cart


@pytest.fixture
def inventory_page(logged_in_page: Page, base_url: str) -> InventoryPage:
    """Inventory page object fixture (requires logged-in user)."""
    return InventoryPage(logged_in_page, base_url)

@pytest.fixture
def cart_page(logged_in_page: Page, base_url: str) -> CartPage:
    """Cart page object fixture (requires logged-in user)."""
    return CartPage(logged_in_page, base_url)

@pytest.fixture
def checkout_page(logged_in_page: Page, base_url: str) -> CheckoutPage:
    """Checkout page object fixture (requires logged-in user)."""
    return CheckoutPage(logged_in_page, base_url)