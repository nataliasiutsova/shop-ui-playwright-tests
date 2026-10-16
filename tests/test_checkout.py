import allure
import pytest


@allure.title("Checkout page opens with form")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_checkout_step_one_opens(inventory_page, cart_page, checkout_page):
    with allure.step("Add product and proceed to checkout"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Verify checkout step one page is shown"):
        checkout_page.expect_url_contains("/checkout-step-one.html")
        checkout_page.expect_page_title("Checkout: Your Information")
        checkout_page.take_screenshot("Checkout step one")


@allure.title("Valid form data proceeds to step two")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_checkout_valid_form(inventory_page, cart_page, checkout_page):
    with allure.step("Add product and proceed to checkout"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Fill form and click Continue"):
        checkout_page.complete_step_one("John", "Doe", "12345")
        checkout_page.take_screenshot("Step two after valid form")

    with allure.step("Verify redirect to step two"):
        checkout_page.expect_url_contains("/checkout-step-two.html")
        checkout_page.expect_page_title("Checkout: Overview")


@allure.title("Overview page shows correct item count")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_overview_shows_items(inventory_page, cart_page, checkout_page):
    with allure.step("Add 2 products to cart"):
        inventory_page.add_item_by_index(0)
        inventory_page.add_item_by_index(1)

    with allure.step("Proceed to checkout step two"):
        cart_page.open()
        cart_page.proceed_to_checkout()
        checkout_page.complete_step_one("John", "Doe", "12345")

    with allure.step("Verify step two shows 2 items"):
        checkout_page.expect_item_count(2)
        checkout_page.take_screenshot("Overview with 2 items")


@allure.title("Total equals subtotal + tax")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_total_calculation(inventory_page, cart_page, checkout_page):
    with allure.step("Add product and proceed to step two"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()
        checkout_page.complete_step_one("John", "Doe", "12345")

    with allure.step("Verify total = subtotal + tax"):
        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()
        expected = round(subtotal + tax, 2)
        assert abs(total - expected) < 0.01, (
            f"Expected total {expected}, got {total}"
        )
        checkout_page.take_screenshot("Overview with total")


@allure.title("Complete order shows confirmation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_complete_order(inventory_page, cart_page, checkout_page):
    with allure.step("Proceed to step two"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()
        checkout_page.complete_step_one("John", "Doe", "12345")

    with allure.step("Click Finish"):
        checkout_page.click_finish()

    with allure.step("Verify checkout complete page"):
        checkout_page.expect_url_contains("/checkout-complete.html")
        checkout_page.expect_complete()
        checkout_page.take_screenshot("Order complete")


@allure.title("Cancel on step one returns to cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_cancel_step_one(inventory_page, cart_page, checkout_page):
    with allure.step("Proceed to checkout"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Click Cancel"):
        checkout_page.click_cancel()

    with allure.step("Verify redirect to cart"):
        checkout_page.expect_url_contains("/cart.html")
        checkout_page.take_screenshot("Back to cart after cancel")


@allure.title("Back Home button after completion returns to inventory")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_back_home_after_complete(inventory_page, cart_page, checkout_page):
    with allure.step("Complete the order"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()
        checkout_page.complete_step_one("John", "Doe", "12345")
        checkout_page.click_finish()

    with allure.step("Click Back Home"):
        checkout_page.click_back_home()

    with allure.step("Verify redirect to inventory"):
        checkout_page.expect_url_contains("/inventory.html")
        checkout_page.take_screenshot("Back to inventory")


# ============================================================
# REGRESSION — negative cases
# ============================================================

@allure.title("Empty first name is rejected")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_empty_first_name(inventory_page, cart_page, checkout_page):
    with allure.step("Proceed to checkout step one"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Submit form with empty First Name"):
        checkout_page.complete_step_one("", "Doe", "12345")

    with allure.step("Verify 'First Name is required' error"):
        checkout_page.expect_error("First Name is required")
        checkout_page.take_screenshot("Error: empty first name")


@allure.title("Empty last name is rejected")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_empty_last_name(inventory_page, cart_page, checkout_page):
    with allure.step("Proceed to checkout step one"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Submit form with empty Last Name"):
        checkout_page.complete_step_one("John", "", "12345")

    with allure.step("Verify 'Last Name is required' error"):
        checkout_page.expect_error("Last Name is required")
        checkout_page.take_screenshot("Error: empty last name")


@allure.title("Empty postal code is rejected")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_empty_postal_code(inventory_page, cart_page, checkout_page):
    with allure.step("Proceed to checkout step one"):
        inventory_page.add_item_by_index(0)
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Submit form with empty Postal Code"):
        checkout_page.complete_step_one("John", "Doe", "")

    with allure.step("Verify 'Postal Code is required' error"):
        checkout_page.expect_error("Postal Code is required")
        checkout_page.take_screenshot("Error: empty postal code")


@allure.title("Checkout page is not accessible without login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_checkout_redirects_to_login(page, base_url, login_page):
    with allure.step("Open checkout URL without login"):
        page.goto(f"{base_url}/checkout-step-one.html")

    with allure.step("Verify redirect to login"):
        login_page.expect_url_contains("/")
        login_page.expect_login_form_visible()
        login_page.take_screenshot("Redirect to login from checkout")