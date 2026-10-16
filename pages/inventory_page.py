from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):

    # Locators
    INVENTORY_ITEM = "//div[@class='inventory_item']"
    ITEM_NAME = "//div[@data-test='inventory-item-name']"
    ITEM_PRICE = "//div[@data-test='inventory-item-rice']"
    ADD_TO_CART_BUTTON = "//button[starts-with(@data-test, 'add-to-cart')]"
    REMOVE_BUTTON = "//button[starts-with(@data-test, 'remove')]"
    CART_BADGE = "//span[@class='shopping_cart_badge']"
    CART_LINK = "//a[@class='shopping_cart_link']"
    SORT_DROPDOWN = "//select[@data-test='product-sort-container']"
    PAGE_TITLE = "//span[@class='title']"

    def open(self):
        super().open("/inventory.html")

    # ----- Actions -----

    def sort_by(self, value: str):
        self.page.select_option(self.SORT_DROPDOWN, value)

    def add_item_by_index(self, index: int):
        """Add a product by its index (0-based)."""
        self.page.locator(self.ADD_TO_CART_BUTTON).nth(index).click()

    def remove_item_by_index(self, index: int):
        """Remove a product by its index (0-based)."""
        self.page.locator(self.REMOVE_BUTTON).nth(index).click()


    # ----- Getters -----

    def get_item_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEM).count()

    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def get_item_prices(self) -> list[float]:
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def get_cart_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    # ----- Assertions -----

    def expect_page_title(self, title: str = "Products"):
        self.expect_text(self.PAGE_TITLE, title)


    def expect_cart_count(self, count: int):
        """Assert cart badge count."""
        if count == 0:
            self.expect_first_hidden(self.CART_BADGE)
        else:
            self.expect_first_text(self.CART_BADGE, str(count))

    def expect_sorted_by_name_asc(self):
        """Assert products are sorted A → Z."""
        names = self.get_item_names()
        assert names == sorted(names), f"Expected A-Z, got: {names}"

    def expect_sorted_by_name_desc(self):
        """Assert products are sorted Z → A."""
        names = self.get_item_names()
        assert names == sorted(names, reverse=True), f"Expected Z-A, got: {names}"

    def expect_sorted_by_price_asc(self):
        """Assert products are sorted by price ascending."""
        prices = self.get_item_prices()
        assert prices == sorted(prices), f"Expected low-high, got: {prices}"

    def expect_sorted_by_price_desc(self):
        """Assert products are sorted by price descending."""
        prices = self.get_item_prices()
        assert prices == sorted(prices, reverse=True), f"Expected high-low, got: {prices}"





