from playwright.sync_api import Page, expect
import allure


class BasePage:
    BURGER_MENU = "//button[@id='react-burger-menu-btn']"
    LOGOUT_LINK = "//a[@id='logout_sidebar_link']"
    CART_LINK="//a[@data-test='shopping-cart-link']"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self, path: str = ""):
        self.page.goto(f"{self.base_url}{path}")

    def logout(self):
        """Open the burger menu and click Logout."""
        self.page.click(self.BURGER_MENU)
        self.page.click(self.LOGOUT_LINK)

    def go_to_cart(self):
        self.page.click(self.CART_LINK)

    def expect_url_contains(self, url_part: str):
        expect(self.page).to_have_url(f"{self.base_url}{url_part}")

    def expect_visible(self, selector: str):
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str):
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_count(self, selector: str, count: int):
        expect(self.page.locator(selector)).to_have_count(count)

    def expect_hidden(self, selector: str):
        """Assert the element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_first_visible(self, selector: str):
        """Assert the first matching element is visible."""
        expect(self.page.locator(selector).first).to_be_visible()

    def expect_first_hidden(self, selector: str):
        """Assert the first matching element is hidden."""
        expect(self.page.locator(selector).first).to_be_hidden()

    def expect_first_text(self, selector: str, text: str):
        """Assert the first matching element contains text."""
        expect(self.page.locator(selector).first).to_contain_text(text)

    def take_screenshot(self, name: str = "screenshot"):
        try:
         allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
         )
        except Exception as e:
            allure.attach(
                f"Failed to take screenshot: {e}",
                name=f"{name} — error",
                attachment_type=allure.attachment_type.TEXT,
            )
