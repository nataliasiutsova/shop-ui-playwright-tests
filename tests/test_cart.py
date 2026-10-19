import allure
import pytest


@allure.feature("Cart")
@allure.title("Cart is empty by default")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_cart_empty_by_default(cart_page):
    with allure.step("Open cart page"):
        cart_page.open()

    with allure.step("Verify page title is 'Your Cart'"):
        cart_page.expect_page_title("Your Cart")

    with allure.step("Verify cart is empty"):
        cart_page.expect_empty()
        cart_page.take_screenshot("Empty cart")


@allure.feature("Cart")
@allure.title("Product added on inventory appears in cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_added_product_appears_in_cart(inventory_page, cart_page):
    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)
        inventory_page.expect_cart_count(1)

    with allure.step("Open cart page"):
        cart_page.open()

    with allure.step("Verify cart contains 1 item"):
        cart_page.expect_item_count(1)
        cart_page.take_screenshot("Cart with 1 item")


@allure.feature("Cart")
@allure.title("Cart shows correct product name and price")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_cart_item_details(inventory_page, cart_page):
    with allure.step("Get name of product at index 0 from inventory"):
        names = inventory_page.get_item_names()
        expected_name = names[0]

    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)

    with allure.step("Open cart page"):
        cart_page.open()

    with allure.step(f"Verify cart contains '{expected_name}'"):
        cart_page.expect_item_in_cart(expected_name)
        cart_page.take_screenshot("Cart with product details")


@allure.feature("Cart")
@allure.title("Product can be removed from cart page")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_remove_item_from_cart_page(inventory_page, cart_page):
    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)

    with allure.step("Open cart page"):
        cart_page.open()
        cart_page.expect_item_count(1)

    with allure.step("Remove first item"):
        cart_page.remove_first_item()

    with allure.step("Verify cart is empty"):
        cart_page.expect_empty()
        cart_page.take_screenshot("Cart after removing item")


@allure.feature("Cart")
@allure.title("Two products appear in cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_two_products_in_cart(inventory_page, cart_page):
    with allure.step("Add products at indices 0 and 1"):
        inventory_page.add_item_by_index(0)
        inventory_page.add_item_by_index(1)

    with allure.step("Open cart page"):
        cart_page.open()

    with allure.step("Verify cart has 2 items"):
        cart_page.expect_item_count(2)
        cart_page.take_screenshot("Cart with 2 items")


@allure.feature("Cart")
@allure.title("Continue shopping returns to inventory")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_continue_shopping(cart_page):
    with allure.step("Open cart page"):
        cart_page.open()

    with allure.step("Click 'Continue Shopping'"):
        cart_page.continue_shopping()

    with allure.step("Verify redirect to inventory page"):
        cart_page.expect_url_contains("/inventory.html")
        cart_page.take_screenshot("Back to inventory")


@allure.feature("Cart")
@allure.title("Checkout button opens checkout page")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_checkout_button(inventory_page, cart_page):
    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)

    with allure.step("Open cart page"):
        cart_page.open()

    with allure.step("Click 'Checkout'"):
        cart_page.proceed_to_checkout()

    with allure.step("Verify redirect to checkout step one"):
        cart_page.expect_url_contains("/checkout-step-one.html")
        cart_page.take_screenshot("Checkout step one")


@allure.feature("Cart")
@allure.title("Cart page is not accessible without login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_cart_redirects_to_login_without_auth(page, base_url, login_page):
    with allure.step("Open cart URL directly without login"):
        page.goto(f"{base_url}/cart.html")

    with allure.step("Verify redirect to login page"):
        login_page.expect_url_contains("/")

    with allure.step("Verify login form is shown"):
        login_page.expect_login_form_visible()
        login_page.take_screenshot("Redirected to login from cart")