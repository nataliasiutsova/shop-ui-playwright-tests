from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for SauceDemo checkout pages (step one, two, complete)."""

    PAGE_TITLE = "xpath=//span[@class='title']"

    # ----- Step One: Your Information -----

    FIRST_NAME_INPUT = "//input[@id='first-name']"
    LAST_NAME_INPUT = "//input[@id='last-name']"
    POSTAL_CODE_INPUT = "//input[@id='postal-code']"
    CANCEL_BUTTON = "//button[@id='cancel']"
    CONTINUE_BUTTON = "//input[@id='continue']"
    ERROR_MESSAGE = "//h3[@data-test='error']"

    # ----- Step Two: Overview -----

    CART_ITEM = "//div[@class='cart_item']"
    ITEM_NAME = "//div[@class='inventory_item_name']"
    ITEM_PRICE = "//div[@class='inventory_item_price']"
    SUBTOTAL_LABEL = "//div[@class='summary_subtotal_label']"
    TAX_LABEL = "//div[@class='summary_tax_label']"
    TOTAL_LABEL = "//div[@class='summary_total_label']"
    FINISH_BUTTON = "//button[@id='finish']"

    # ----- Step Three: Complete -----

    COMPLETE_HEADER = "//h2[@class='complete-header']"
    COMPLETE_TEXT = "//div[@class='complete-text']"
    BACK_HOME_BUTTON = "//button[@id='back-to-products']"


    def open_step_one(self):
        super().open("/checkout-step-one.html")

    def open_step_two(self):
        super().open("/checkout-step-two.html")

    def open_complete(self):
        super().open("/checkout-complete.html")

    # ----- Step One actions -----

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill First Name, Last Name, Zip on step one."""
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self):
        self.page.click(self.CONTINUE_BUTTON)

    def click_cancel(self):
        self.page.click(self.CANCEL_BUTTON)

    def complete_step_one(self, first_name: str, last_name: str, postal_code: str):
        """Fill form and click Continue."""
        self.fill_customer_info(first_name, last_name, postal_code)
        self.click_continue()

    # ----- Step Two actions -----

    def click_finish(self):
        self.page.click(self.FINISH_BUTTON)

    def get_subtotal(self) -> float:
        """Return subtotal value from summary."""
        text = self.page.locator(self.SUBTOTAL_LABEL).inner_text()
        return float(text.replace("Item total: $", ""))

    def get_tax(self) -> float:
        text = self.page.locator(self.TAX_LABEL).inner_text()
        return float(text.replace("Tax: $", ""))

    def get_total(self) -> float:
        text = self.page.locator(self.TOTAL_LABEL).inner_text()
        return float(text.replace("Total: $", ""))

    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    # ----- Step Three actions -----

    def click_back_home(self):
        self.page.click(self.BACK_HOME_BUTTON)

    # ----- Assertions -----

    def expect_page_title(self, title: str):
        self.expect_text(self.PAGE_TITLE, title)

    def expect_error(self, text: str):
        self.expect_visible(self.ERROR_MESSAGE)
        self.expect_text(self.ERROR_MESSAGE, text)

    def expect_item_count(self, count: int):
        self.expect_count(self.CART_ITEM, count)

    def expect_total(self, expected: float):
        actual = self.get_total()
        assert abs(actual - expected) < 0.01, (
            f"Expected total {expected}, got {actual}"
        )

    def expect_complete(self):
        """Assert checkout completion page is shown."""
        self.expect_visible(self.COMPLETE_HEADER)
        self.expect_text(self.COMPLETE_HEADER, "Thank you for your order!")