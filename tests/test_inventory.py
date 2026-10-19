import allure
import pytest
from playwright.sync_api import Page, expect


@allure.feature("Inventory")
@allure.title("Inventory page shows products after login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_inventory_page_shows_products(inventory_page):
    with allure.step("Verify page title is 'Products'"):
        inventory_page.expect_page_title("Products")

    with allure.step("Verify at least one product is displayed"):
        count = inventory_page.get_item_count()
        inventory_page.take_screenshot("Products list is displayed")
        assert count > 0, f"Expected products, got {count}"


@allure.feature("Inventory")
@allure.title("Product can be added to cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_add_product_to_cart(inventory_page):
    with allure.step("Verify cart is empty"):
        assert inventory_page.get_cart_count() == 0

    with allure.step("Add first product to cart"):
        inventory_page.add_item_by_index(0)
        inventory_page.take_screenshot("Product added to cart")

    with allure.step("Verify cart count is 1"):
        inventory_page.expect_cart_count(1)


@allure.feature("Inventory")
@allure.title("Products can be sorted by name A-Z")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_sort_by_name_asc(inventory_page):
    with allure.step("Sort by name A-Z"):
        inventory_page.sort_by("az")

    with allure.step("Verify products are sorted A-Z"):
        inventory_page.expect_sorted_by_name_asc()
        inventory_page.take_screenshot("Sorted A-Z")


@allure.feature("Inventory")
@allure.title("Products can be sorted by name Z-A")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_sort_by_name_desc(inventory_page):
    with allure.step("Sort by name Z-A"):
        inventory_page.sort_by("za")

    with allure.step("Verify products are sorted Z-A"):
        inventory_page.expect_sorted_by_name_desc()
        inventory_page.take_screenshot("Sorted Z-A")


@allure.feature("Inventory")
@allure.title("Products can be sorted by price low to high")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_sort_by_price_asc(inventory_page):
    with allure.step("Sort by price low to high"):
        inventory_page.sort_by("lohi")

    with allure.step("Verify products are sorted by price ascending"):
        inventory_page.expect_sorted_by_price_asc()
        inventory_page.take_screenshot("Sorted price low-high")


@allure.feature("Inventory")
@allure.title("Products can be sorted by price high to low")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_sort_by_price_desc(inventory_page):
    with allure.step("Sort by price high to low"):
        inventory_page.sort_by("hilo")

    with allure.step("Verify products are sorted by price descending"):
        inventory_page.expect_sorted_by_price_desc()
        inventory_page.take_screenshot("Sorted price high-low")


@allure.feature("Inventory")
@allure.title("Two products can be added to cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_add_two_products(inventory_page):
    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)

    with allure.step("Add product at index 1"):
        inventory_page.add_item_by_index(1)
        inventory_page.take_screenshot("One product in cart")

    with allure.step("Verify cart count is 2"):
        inventory_page.expect_cart_count(2)
        inventory_page.take_screenshot("Two products in cart")


@allure.feature("Inventory")
@allure.title("Product can be removed from cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_remove_product_from_cart(inventory_page):
    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)

    with allure.step("Verify cart count is 1"):
        inventory_page.expect_cart_count(1)
        inventory_page.take_screenshot("One product in cart")

    with allure.step("Remove product at index 0"):
        inventory_page.remove_item_by_index(0)

    with allure.step("Verify cart is empty"):
        inventory_page.expect_cart_count(0)
        inventory_page.take_screenshot("Product removed from cart")


@allure.feature("Inventory")
@allure.title("Removing second product keeps first in cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_remove_second_product_keeps_first(inventory_page):
    with allure.step("Add products at indices 0 and 1"):
        inventory_page.add_item_by_index(0)
        inventory_page.add_item_by_index(1)
        inventory_page.expect_cart_count(2)
        inventory_page.take_screenshot("Two product in cart")

    with allure.step("Remove product at index 1"):
        inventory_page.remove_item_by_index(1)

    with allure.step("Verify cart count is 1"):
        inventory_page.expect_cart_count(1)
        inventory_page.take_screenshot("One product left")


@allure.feature("Inventory")
@allure.title("Button changes from 'Add to cart' to 'Remove' after adding first product")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_button_changes_to_remove(inventory_page):
    with allure.step("Verify first 'Add to cart' button is visible"):
        inventory_page.expect_first_visible(inventory_page.ADD_TO_CART_BUTTON)

    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)

    with allure.step("Verify first 'Remove' button is visible"):
        inventory_page.expect_first_visible(inventory_page.REMOVE_BUTTON)
        inventory_page.take_screenshot("Product at index 0 — Remove button visible")


@allure.feature("Inventory")
@allure.title("First 'Remove' button becomes 'Add to cart' after removal")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_button_changes_back_after_remove(inventory_page):
    with allure.step("Add product at index 0"):
        inventory_page.add_item_by_index(0)
        inventory_page.expect_first_visible(inventory_page.REMOVE_BUTTON)
        inventory_page.take_screenshot("One product in cart")

    with allure.step("Remove product at index 0"):
        inventory_page.remove_item_by_index(0)

    with allure.step("Verify first 'Add to cart' button is visible again"):
        inventory_page.expect_first_visible(inventory_page.ADD_TO_CART_BUTTON)
        inventory_page.take_screenshot("Product at index 0 — Add visible again")

    with allure.step("Verify first 'Remove' button is hidden"):
        inventory_page.expect_first_hidden(inventory_page.REMOVE_BUTTON)


@allure.feature("Inventory")
@allure.title("Inventory is not accessible without login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_inventory_redirects_to_login_without_auth(page, base_url, login_page):
    with allure.step("Open inventory URL directly without login"):
        page.goto(f"{base_url}/inventory.html")

    with allure.step("Verify redirect to login page"):
        login_page.expect_url_contains("/")

    with allure.step("Verify login form is shown"):
        login_page.expect_login_form_visible()
        login_page.take_screenshot("Login page after redirect")


