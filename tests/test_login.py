import allure
import pytest

from utils.users import LOCKED_USER, STANDARD_USER

EMPTY = ""
WRONG_PASSWORD = "wrong_password"


@allure.feature("Login")
@allure.title("Valid user logs in successfully")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_login_success(login_page):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step(f"Log in as '{STANDARD_USER.username}'"):
        login_page.login(STANDARD_USER.username, STANDARD_USER.password)

    with allure.step("Verify redirect to inventory page"):
        login_page.expect_url_contains("/inventory.html")
        login_page.take_screenshot("Inventory page loaded")


@allure.feature("Login")
@allure.title("Invalid password is rejected")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_login_invalid_password(login_page):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in with wrong password"):
        login_page.login(STANDARD_USER.username, WRONG_PASSWORD)

    with allure.step("Verify 'do not match' error is shown"):
        login_page.expect_error("Username and password do not match any user in this service")
        login_page.take_screenshot("Error: invalid password")


@allure.feature("Login")
@allure.title("Locked user cannot log in")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_login_locked_user(login_page):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step(f"Log in as '{LOCKED_USER.username}'"):
        login_page.login(LOCKED_USER.username, LOCKED_USER.password)

    with allure.step("Verify 'locked out' error is shown"):
        login_page.expect_error("Sorry, this user has been locked out")
        login_page.take_screenshot("Error: user is locked out")


@allure.feature("Login")
@allure.title("Empty username is rejected")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_login_empty_username(login_page):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Submit with empty username"):
        login_page.login(EMPTY, STANDARD_USER.password)

    with allure.step("Verify 'Username is required' error"):
        login_page.expect_error("Username is required")
        login_page.take_screenshot("Error: empty username")


@allure.feature("Login")
@allure.title("Empty password is rejected")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_login_empty_password(login_page):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Submit with empty password"):
        login_page.login(STANDARD_USER.username, EMPTY)

    with allure.step("Verify 'Password is required' error"):
        login_page.expect_error("Password is required")
        login_page.take_screenshot("Error: empty password")


@allure.feature("Login")
@allure.title("Both fields empty are rejected")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_login_both_empty(login_page):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Submit with both fields empty"):
        login_page.login(EMPTY, EMPTY)

    with allure.step("Verify 'Username is required' error"):
        login_page.expect_error("Username is required")
        login_page.take_screenshot("Error: both fields empty")