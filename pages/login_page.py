from playwright.sync_api import Page
import os

from pages.base_page import BasePage


class LoginPage(BasePage):

    # Locators
    USERNAME_INPUT = "//input[@id='user-name']"
    PASSWORD_INPUT = "//input[@id='password']"
    LOGIN_BUTTON = "//input[@id='login-button']"
    ERROR_MESSAGE = "//h3[@data-test='error']"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open(self):
        super().open("/")

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_selector(
            "//div[@data-test='inventory-item']",
            state="visible",
            timeout=10000
          )



    def expect_error(self, text: str):
        self.expect_visible(self.ERROR_MESSAGE)
        self.expect_text(self.ERROR_MESSAGE, text)

    def expect_login_form_visible(self):
        """Assert the login form is visible."""
        self.expect_visible(self.LOGIN_BUTTON)