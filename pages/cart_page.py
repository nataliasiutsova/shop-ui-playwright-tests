from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for SauceDemo cart page."""

    # Locators (XPath)
    CART_ITEM = "//div[@class='cart_item']"
    ITEM_NAME = "//div[@data-test='inventory-item-name']"
    ITEM_PRICE = "//div[@data-test='inventory-item-price']"
    ITEM_QUANTITY = "//div[@class='cart_quantity']"
    REMOVE_BUTTON = "//button[starts-with(@data-test, 'remove')]"
    CONTINUE_SHOPPING_BUTTON = "//button[@id='continue-shopping']"
    CHECKOUT_BUTTON = "//button[@id='checkout']"
    CART_BADGE = "//span[@class='shopping_cart_badge']"
    PAGE_TITLE = "//span[@class='title']"

    def open(self):
        """Open the cart page."""
        super().open("/cart.html")

    # ----- Actions -----

    def remove_item_by_index(self, index: int):
        """Remove a cart item by its index (0-based)."""
        self.page.locator(self.REMOVE_BUTTON).nth(index).click()

    def remove_first_item(self):
        """Remove the first item from the cart."""
        self.page.locator(self.REMOVE_BUTTON).first.click()

    def continue_shopping(self):
        """Click 'Continue Shopping' button."""
        self.page.click(self.CONTINUE_SHOPPING_BUTTON)

    def proceed_to_checkout(self):
        """Click 'Checkout' button."""
        self.page.click(self.CHECKOUT_BUTTON)

    # ----- Getters -----

    def get_item_count(self) -> int:
        """Return number of items in the cart."""
        return self.page.locator(self.CART_ITEM).count()

    def get_item_names(self) -> list[str]:
        """Return list of item names in the cart."""
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def get_item_prices(self) -> list[float]:
        """Return list of item prices as floats."""
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def get_item_quantities(self) -> list[int]:
        """Return list of item quantities."""
        raw = self.page.locator(self.ITEM_QUANTITY).all_inner_texts()
        return [int(q) for q in raw]

    def get_cart_count(self) -> int:
        """Return cart badge count (0 if badge is missing)."""
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    # ----- Assertions -----

    def expect_page_title(self, title: str = "Your Cart"):
        """Assert page title."""
        self.expect_text(self.PAGE_TITLE, title)

    def expect_item_count(self, count: int):
        """Assert number of items in the cart."""
        self.expect_count(self.CART_ITEM, count)

    def expect_cart_count(self, count: int):
        """Assert cart badge count. count=0 → badge hidden."""
        if count == 0:
            self.expect_first_hidden(self.CART_BADGE)
        else:
            self.expect_first_text(self.CART_BADGE, str(count))

    def expect_item_in_cart(self, name: str):
        """Assert item with given name is present in the cart."""
        self.expect_visible(f"xpath=//div[@class='cart_item'][.//div[text()='{name}']]")

    def expect_item_not_in_cart(self, name: str):
        """Assert item with given name is absent from the cart."""
        self.expect_hidden(f"xpath=//div[@class='cart_item'][.//div[text()='{name}']]")

    def expect_empty(self):
        """Assert the cart is empty."""
        self.expect_item_count(0)
        self.expect_cart_count(0)