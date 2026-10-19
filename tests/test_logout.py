import allure
import pytest

from utils.users import STANDARD_USER

@allure.feature("Logout")
@allure.title("Cart is preserved after logout and re-login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_cart_preserved_after_logout(inventory_page, login_page):
    with allure.step("Verify cart is empty before adding"):
        inventory_page.expect_cart_count(0)

    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)
        inventory_page.expect_cart_count(1)
        inventory_page.take_screenshot("Cart before logout — 1 item")

    with allure.step("Log out"):
        inventory_page.logout()

    with allure.step("Verify redirect to login page"):
        login_page.expect_url_contains("/")
        login_page.expect_login_form_visible()

    with allure.step("Log in again as the same user"):
        login_page.login(STANDARD_USER.username, STANDARD_USER.password)

    with allure.step("Verify cart still shows 1 item (preserved)"):
        inventory_page.expect_cart_count(1)
        inventory_page.take_screenshot("Cart after re-login — still 1 item")


@allure.feature("Logout")
@allure.title("User is redirected to login page after logout")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_logout_redirects_to_login(inventory_page, login_page):
    with allure.step("Log out"):
        inventory_page.logout()

    with allure.step("Verify redirect to login page"):
        login_page.expect_url_contains("/")
        login_page.expect_login_form_visible()
        login_page.take_screenshot("Login page after logout")




