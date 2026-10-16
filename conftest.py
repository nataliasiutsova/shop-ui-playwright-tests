import os

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