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
        try:
          self.page.wait_for_selector(
            "//div[@data-test='inventory-item']",
            state="visible",
            timeout=30000
          )
        except Exception as e:
            # Создаем папку, если ее нет
            os.makedirs("test-results", exist_ok=True)
            # Сохраняем скриншот
            self.page.screenshot(path="test-results/error_screenshot.png", full_page=True)
            # Сохраняем HTML
            with open("test-results/error_page.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            raise e


    def expect_error(self, text: str):
        self.expect_visible(self.ERROR_MESSAGE)
        self.expect_text(self.ERROR_MESSAGE, text)

    def expect_login_form_visible(self):
        """Assert the login form is visible."""
        self.expect_visible(self.LOGIN_BUTTON)