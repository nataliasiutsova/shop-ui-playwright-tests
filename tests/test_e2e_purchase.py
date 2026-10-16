import allure
import pytest

from utils.users import STANDARD_USER


@allure.title("E2E: full purchase flow — login → add → checkout → complete")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_full_purchase_flow(login_page, inventory_page, cart_page, checkout_page):
    with allure.step("Login as standard_user"):
        login_page.open()
        login_page.login(STANDARD_USER.username, STANDARD_USER.password)
        login_page.expect_url_contains("/inventory.html")

    with allure.step("Add product at index 0 to cart"):
        inventory_page.add_item_by_index(0)
        inventory_page.expect_cart_count(1)

    with allure.step("Open cart and proceed to checkout"):
        cart_page.open()
        cart_page.expect_item_count(1)
        cart_page.proceed_to_checkout()

    with allure.step("Fill shipping info"):
        checkout_page.complete_step_one("John", "Doe", "12345")
        checkout_page.expect_url_contains("/checkout-step-two.html")

    with allure.step("Verify overview shows 1 item"):
        checkout_page.expect_item_count(1)

    with allure.step("Complete the order"):
        checkout_page.click_finish()
        checkout_page.expect_url_contains("/checkout-complete.html")
        checkout_page.expect_complete()
        checkout_page.take_screenshot("Order completed")

@allure.title("E2E: purchase with checkout cancellation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
def test_purchase_with_cancel(login_page, inventory_page, cart_page, checkout_page):
    with allure.step("Login and add product"):
        login_page.open()
        login_page.login(STANDARD_USER.username, STANDARD_USER.password)
        inventory_page.add_item_by_index(0)

    with allure.step("Go to checkout"):
        cart_page.open()
        cart_page.proceed_to_checkout()

    with allure.step("Cancel checkout"):
        checkout_page.click_cancel()

    with allure.step("Verify back to cart with item still there"):
        cart_page.expect_url_contains("/cart.html")
        cart_page.expect_item_count(1)
        cart_page.take_screenshot("Cancelled — item in cart")