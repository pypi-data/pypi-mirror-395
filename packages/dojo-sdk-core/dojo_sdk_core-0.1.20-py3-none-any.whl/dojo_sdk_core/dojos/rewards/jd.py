"""
Reward functions for JD (JingDong) e-commerce SPA tasks.
"""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def _validate_go_to_the_cart_page_from_the_homepage(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate navigation from homepage to cart page."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "cart":
            return 0.0, f"Expected page='cart', got page='{final_state['page']}'"

        return 1.0, "Successfully navigated to cart page"
    except Exception as e:
        logger.error(f"Error in _validate_go_to_the_cart_page_from_the_homepage: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_go_to_a_product_page_from_home(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate navigation from homepage to a product page."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "product":
            return 0.0, f"Expected page='product', got page='{final_state['page']}'"

        if "selectedProductId" not in final_state:
            return 0.0, "Missing 'selectedProductId' in final state"

        if final_state["selectedProductId"] != "2":
            return 0.0, f"Expected selectedProductId='2', got '{final_state['selectedProductId']}'"

        return 1.0, "Successfully navigated to product page with correct product"
    except Exception as e:
        logger.error(f"Error in _validate_go_to_a_product_page_from_home: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_go_to_homepage_from_product_page(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate navigation from product page to homepage."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "home":
            return 0.0, f"Expected page='home', got page='{final_state['page']}'"

        return 1.0, "Successfully navigated to homepage"
    except Exception as e:
        logger.error(f"Error in _validate_go_to_homepage_from_product_page: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_go_to_cart_page_from_product_detail_page(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate navigation from product detail page to cart page."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "cart":
            return 0.0, f"Expected page='cart', got page='{final_state['page']}'"

        return 1.0, "Successfully navigated to cart page from product detail"
    except Exception as e:
        logger.error(f"Error in _validate_go_to_cart_page_from_product_detail_page: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_go_to_product_detail_from_search(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate navigation from search page to product detail page."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "product":
            return 0.0, f"Expected page='product', got page='{final_state['page']}'"

        if "selectedProductId" not in final_state:
            return 0.0, "Missing 'selectedProductId' in final state"

        if not final_state["selectedProductId"]:
            return 0.0, "selectedProductId is empty"

        return 1.0, "Successfully navigated to product detail from search"
    except Exception as e:
        logger.error(f"Error in _validate_go_to_product_detail_from_search: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_find_a_product_using_search_from_homepage(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate searching for a product and navigating to its detail page."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "product":
            return 0.0, f"Expected page='product', got page='{final_state['page']}'"

        if "searchQuery" not in final_state:
            return 0.0, "Missing 'searchQuery' in final state"

        if "吉普衬衫" not in final_state["searchQuery"]:
            return 0.0, f"Expected search query to contain '吉普衬衫', got '{final_state['searchQuery']}'"

        if "selectedProductId" not in final_state:
            return 0.0, "Missing 'selectedProductId' in final state"

        if final_state["selectedProductId"] != "2":
            return 0.0, f"Expected selectedProductId='2', got '{final_state['selectedProductId']}'"

        return 1.0, "Successfully searched for product and navigated to detail page"
    except Exception as e:
        logger.error(f"Error in _validate_find_a_product_using_search_from_homepage: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_search_吉普衬衫(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate searching for '吉普衬衫' (JEEP shirt)."""
    try:
        if "searchQuery" not in final_state:
            return 0.0, "Missing 'searchQuery' in final state"

        if "吉普衬衫" not in final_state["searchQuery"]:
            return 0.0, f"Expected search query to contain '吉普衬衫', got '{final_state['searchQuery']}'"

        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "search":
            return 0.0, f"Expected page='search', got page='{final_state['page']}'"

        return 1.0, "Successfully searched for 吉普衬衫"
    except Exception as e:
        logger.error(f"Error in _validate_search_吉普衬衫: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_search_a_product_from_another_product_page(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate searching for a product from another product page and navigating to it."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "product":
            return 0.0, f"Expected page='product', got page='{final_state['page']}'"

        if "searchQuery" not in final_state:
            return 0.0, "Missing 'searchQuery' in final state"

        if not final_state["searchQuery"]:
            return 0.0, "searchQuery is empty"

        if "selectedProductId" not in final_state:
            return 0.0, "Missing 'selectedProductId' in final state"

        if final_state["selectedProductId"] != "3":
            return 0.0, f"Expected selectedProductId='3', got '{final_state['selectedProductId']}'"

        return 1.0, "Successfully searched for product and navigated to detail page"
    except Exception as e:
        logger.error(f"Error in _validate_search_a_product_from_another_product_page: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_add_a_product_to_cart(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate adding a product to cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        # Check if product with id "2" is in cart with qty=1
        product_in_cart = False
        for item in cart:
            if item.get("productId") == "2" and item.get("qty") == 1:
                product_in_cart = True
                break

        if not product_in_cart:
            return 0.0, "Expected product with id '2' and qty=1 in cart"

        return 1.0, "Successfully added product to cart"
    except Exception as e:
        logger.error(f"Error in _validate_add_a_product_to_cart: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_add_a_product_from_search_result_to_cart(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate adding a product from search results to cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        # Check if any product is in cart
        if len(cart) == 0:
            return 0.0, "Cart is empty"

        # Check if at least one item has qty >= 1
        has_valid_item = False
        for item in cart:
            if item.get("qty", 0) >= 1:
                has_valid_item = True
                break

        if not has_valid_item:
            return 0.0, "No valid items in cart"

        return 1.0, "Successfully added product from search to cart"
    except Exception as e:
        logger.error(f"Error in _validate_add_a_product_from_search_result_to_cart: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_add_an_item_from_the_homepage(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate adding an item from the homepage to cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        if len(cart) == 0:
            return 0.0, "Cart is empty"

        # Check if any item was added
        initial_cart_len = len(initial_state.get("cart", []))
        if len(cart) <= initial_cart_len:
            return 0.0, "No new items added to cart"

        return 1.0, "Successfully added item from homepage to cart"
    except Exception as e:
        logger.error(f"Error in _validate_add_an_item_from_the_homepage: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_add_an_item_with_3_quantity(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate adding an item with quantity 3 to cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        # Check if any item has qty=3
        has_qty_3 = False
        for item in cart:
            if item.get("qty") == 3:
                has_qty_3 = True
                break

        if not has_qty_3:
            return 0.0, "No item with qty=3 found in cart"

        return 1.0, "Successfully added item with quantity 3"
    except Exception as e:
        logger.error(f"Error in _validate_add_an_item_with_3_quantity: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_remove_one_item_from_cart(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate removing one item from cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        if len(cart) != 0:
            return 0.0, f"Expected empty cart, but found {len(cart)} items"

        return 1.0, "Successfully removed item from cart"
    except Exception as e:
        logger.error(f"Error in _validate_remove_one_item_from_cart: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_remove_multiple_items_in_the_cart(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate removing multiple items from cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        if len(cart) != 0:
            return 0.0, f"Expected empty cart, but found {len(cart)} items"

        return 1.0, "Successfully removed all items from cart"
    except Exception as e:
        logger.error(f"Error in _validate_remove_multiple_items_in_the_cart: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_increase_an_item_and_reduce_another_item(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate increasing quantity of one item and reducing another."""
    try:
        if "cart" not in final_state or "cart" not in initial_state:
            return 0.0, "Missing 'cart' field in states"

        initial_cart = initial_state["cart"]
        final_cart = final_state["cart"]

        if not isinstance(initial_cart, list) or not isinstance(final_cart, list):
            return 0.0, "cart is not a list"

        # Build dictionaries for comparison
        initial_quantities = {item["productId"]: item["qty"] for item in initial_cart}
        final_quantities = {item["productId"]: item["qty"] for item in final_cart}

        increased_count = 0
        decreased_count = 0

        for product_id in set(initial_quantities.keys()) | set(final_quantities.keys()):
            initial_qty = initial_quantities.get(product_id, 0)
            final_qty = final_quantities.get(product_id, 0)

            if final_qty > initial_qty:
                increased_count += 1
            elif final_qty < initial_qty:
                decreased_count += 1

        if increased_count < 1:
            return 0.0, "No item quantity was increased"

        if decreased_count < 1:
            return 0.0, "No item quantity was decreased"

        return 1.0, "Successfully increased one item and reduced another"
    except Exception as e:
        logger.error(f"Error in _validate_increase_an_item_and_reduce_another_item: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_reduce_an_item_quantity_in_the_cart(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate reducing quantity of an item in cart."""
    try:
        if "cart" not in final_state or "cart" not in initial_state:
            return 0.0, "Missing 'cart' field in states"

        initial_cart = initial_state["cart"]
        final_cart = final_state["cart"]

        if not isinstance(initial_cart, list) or not isinstance(final_cart, list):
            return 0.0, "cart is not a list"

        # Build dictionaries for comparison
        initial_quantities = {item["productId"]: item["qty"] for item in initial_cart}
        final_quantities = {item["productId"]: item["qty"] for item in final_cart}

        # Check if any item quantity was reduced
        reduced = False
        for product_id in initial_quantities:
            if final_quantities.get(product_id, 0) < initial_quantities[product_id]:
                reduced = True
                break

        if not reduced:
            return 0.0, "No item quantity was reduced"

        return 1.0, "Successfully reduced item quantity"
    except Exception as e:
        logger.error(f"Error in _validate_reduce_an_item_quantity_in_the_cart: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_search_and_add_two_items_to_cart(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate searching and adding two items to cart."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        if len(cart) < 2:
            return 0.0, f"Expected at least 2 items in cart, found {len(cart)}"

        return 1.0, "Successfully added two items to cart"
    except Exception as e:
        logger.error(f"Error in _validate_search_and_add_two_items_to_cart: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_search_and_add_item_to_cart_and_back_to_home(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate searching, adding item to cart, and returning to homepage."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "home":
            return 0.0, f"Expected page='home', got page='{final_state['page']}'"

        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        if len(cart) == 0:
            return 0.0, "Cart is empty"

        return 1.0, "Successfully added item to cart and returned to homepage"
    except Exception as e:
        logger.error(f"Error in _validate_search_and_add_item_to_cart_and_back_to_home: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_remove_item_from_cart_then_search_and_add_item(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate removing item from cart, then searching and adding new item."""
    try:
        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        # Verify cart has items (should have new item added)
        if len(cart) == 0:
            return 0.0, "Cart is empty, expected new item"

        return 1.0, "Successfully removed old item and added new item"
    except Exception as e:
        logger.error(f"Error in _validate_remove_item_from_cart_then_search_and_add_item: {e}")
        return 0.0, f"Validation error: {str(e)}"


def _validate_use_homepage_to_navigate_and_add_items(initial_state: dict, final_state: dict) -> Tuple[float, str]:
    """Validate using homepage to navigate and add multiple items to cart."""
    try:
        if "page" not in final_state:
            return 0.0, "Missing 'page' field in final state"

        if final_state["page"] != "cart":
            return 0.0, f"Expected page='cart', got page='{final_state['page']}'"

        if "cart" not in final_state:
            return 0.0, "Missing 'cart' field in final state"

        cart = final_state["cart"]
        if not isinstance(cart, list):
            return 0.0, "cart is not a list"

        if len(cart) < 2:
            return 0.0, f"Expected at least 2 items in cart, found {len(cart)}"

        # Check for specific product IDs (3 and 4)
        product_ids = [item.get("productId") for item in cart]
        if "4" not in product_ids or "3" not in product_ids:
            return 0.0, "Expected products with IDs '3' and '4' in cart"

        return 1.0, "Successfully navigated and added multiple items to cart"
    except Exception as e:
        logger.error(f"Error in _validate_use_homepage_to_navigate_and_add_items: {e}")
        return 0.0, f"Validation error: {str(e)}"


# Registry of all reward functions
REWARD_FUNCTIONS_JD = {
    "_validate_go_to_the_cart_page_from_the_homepage": _validate_go_to_the_cart_page_from_the_homepage,
    "_validate_go_to_a_product_page_from_home": _validate_go_to_a_product_page_from_home,
    "_validate_go_to_homepage_from_product_page": _validate_go_to_homepage_from_product_page,
    "_validate_go_to_cart_page_from_product_detail_page": _validate_go_to_cart_page_from_product_detail_page,
    "_validate_go_to_product_detail_from_search": _validate_go_to_product_detail_from_search,
    "_validate_find_a_product_using_search_from_homepage": _validate_find_a_product_using_search_from_homepage,
    "_validate_search_吉普衬衫": _validate_search_吉普衬衫,
    "_validate_search_a_product_from_another_product_page": _validate_search_a_product_from_another_product_page,
    "_validate_add_a_product_to_cart": _validate_add_a_product_to_cart,
    "_validate_add_a_product_from_search_result_to_cart": _validate_add_a_product_from_search_result_to_cart,
    "_validate_add_an_item_from_the_homepage": _validate_add_an_item_from_the_homepage,
    "_validate_add_an_item_with_3_quantity": _validate_add_an_item_with_3_quantity,
    "_validate_remove_one_item_from_cart": _validate_remove_one_item_from_cart,
    "_validate_remove_multiple_items_in_the_cart": _validate_remove_multiple_items_in_the_cart,
    "_validate_increase_an_item_and_reduce_another_item": _validate_increase_an_item_and_reduce_another_item,
    "_validate_reduce_an_item_quantity_in_the_cart": _validate_reduce_an_item_quantity_in_the_cart,
    "_validate_search_and_add_two_items_to_cart": _validate_search_and_add_two_items_to_cart,
    "_validate_search_and_add_item_to_cart_and_back_to_home": _validate_search_and_add_item_to_cart_and_back_to_home,
    "_validate_remove_item_from_cart_then_search_and_add_item": _validate_remove_item_from_cart_then_search_and_add_item,
    "_validate_use_homepage_to_navigate_and_add_items": _validate_use_homepage_to_navigate_and_add_items,
}

__all__ = [
    "_validate_go_to_the_cart_page_from_the_homepage",
    "_validate_go_to_a_product_page_from_home",
    "_validate_go_to_homepage_from_product_page",
    "_validate_go_to_cart_page_from_product_detail_page",
    "_validate_go_to_product_detail_from_search",
    "_validate_find_a_product_using_search_from_homepage",
    "_validate_search_吉普衬衫",
    "_validate_search_a_product_from_another_product_page",
    "_validate_add_a_product_to_cart",
    "_validate_add_a_product_from_search_result_to_cart",
    "_validate_add_an_item_from_the_homepage",
    "_validate_add_an_item_with_3_quantity",
    "_validate_remove_one_item_from_cart",
    "_validate_remove_multiple_items_in_the_cart",
    "_validate_increase_an_item_and_reduce_another_item",
    "_validate_reduce_an_item_quantity_in_the_cart",
    "_validate_search_and_add_two_items_to_cart",
    "_validate_search_and_add_item_to_cart_and_back_to_home",
    "_validate_remove_item_from_cart_then_search_and_add_item",
    "_validate_use_homepage_to_navigate_and_add_items",
    "REWARD_FUNCTIONS_JD",
]
