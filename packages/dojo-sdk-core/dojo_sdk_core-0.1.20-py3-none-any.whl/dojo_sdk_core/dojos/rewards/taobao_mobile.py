"""
Reward functions for Taobao app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

# Easy Tasks


def _validate_navigatetosearch(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user navigated to search page."""

    # Check if we're on search page
    if final_state.get("page") != "search":
        return 0.0, f"Not on search page, current page: {final_state.get('page')}"

    # Search query should be empty (just navigated, not searched yet)
    if final_state.get("searchQuery") != "":
        return 0.0, f"Search query should be empty, got: {final_state.get('searchQuery')}"

    return 1.0, "Successfully navigated to search page"


def _validate_viewproductfromhome(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user viewed product from homepage."""

    # Check if we're on preview page
    if final_state.get("page") != "preview":
        return 0.0, f"Not on preview page, current page: {final_state.get('page')}"

    # Check if a product is selected
    if not final_state.get("selectedProductId"):
        return 0.0, "No product selected"

    # Should have a valid product ID (numeric string)
    product_id = final_state.get("selectedProductId")
    if not product_id or not product_id.isdigit():
        return 0.0, f"Invalid product ID: {product_id}"

    return 1.0, f"Successfully viewing product {product_id} on preview page"


def _validate_viewshoppingcart(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user navigated to cart page."""

    # Check if we're on cart page
    if final_state.get("page") != "cart":
        return 0.0, f"Not on cart page, current page: {final_state.get('page')}"

    # Cart should exist and have items (since prompt says "you have items")
    cart = final_state.get("cart", [])
    if len(cart) == 0:
        return 0.0, "Cart should contain items but is empty"

    return 1.0, "Successfully navigated to cart page with items"


def _validate_navigateviarelatedproducts(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user navigated via related products."""

    # Check we're on product detail page
    if final_state.get("page") != "product":
        return 0.0, f"Should be on product detail page, got: {final_state.get('page')}"

    # Check correct product is selected (instant noodles - ID 3)
    if final_state.get("selectedProductId") != "3":
        return 0.0, f"Should be viewing instant noodles (product 3), got: {final_state.get('selectedProductId')}"

    return 1.0, "Successfully navigated to instant noodles via related products"


def _validate_browserelatedfromcart(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate browsing related products from cart page."""

    # Check we're on product page
    if final_state.get("page") != "product":
        return 0.0, f"Should be on preview page, got: {final_state.get('page')}"

    # Check a product is selected (any product from related)
    if not final_state.get("selectedProductId"):
        return 0.0, "No product selected from related products"

    # Should have a valid product ID
    product_id = final_state.get("selectedProductId")
    if not product_id or not product_id.isdigit():
        return 0.0, f"Invalid product ID selected: {product_id}"

    return 1.0, f"Successfully browsed to product {product_id} from cart related products"


def _validate_quickproductcomparison(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate quick product comparison using related products."""

    # Check we're on preview page for product 3
    if final_state.get("page") != "product":
        return 0.0, f"Should be on product page, got: {final_state.get('page')}"

    if final_state.get("selectedProductId") != "2":
        return 0.0, f"Should be viewing Jeep shirt (product 2), got: {final_state.get('selectedProductId')}"

    return 1.0, "Successfully compared multiple products using related products"


def _validate_returntosearchfromproduct(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate returning to search from product detail."""

    # Check we're on search page
    if final_state.get("page") != "search":
        return 0.0, f"Should be on search page, got: {final_state.get('page')}"

    # Search query should be preserved (not empty)
    search_query = final_state.get("searchQuery", "")
    if not search_query:
        return 0.0, "Search query should be preserved but is empty"

    return 1.0, f"Successfully returned to search with query: {search_query}"


def _validate_searchproduct(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user searched for sauce products."""

    # Check we're on search page
    if final_state.get("page") != "search":
        return 0.0, f"Should be on search page, got: {final_state.get('page')}"

    # Check search query is "sauce"
    search_query = final_state.get("searchQuery", "").lower()
    if "sauce" not in search_query:
        return 0.0, f"Search query should contain 'sauce', got: {final_state.get('searchQuery')}"

    return 1.0, "Successfully searched for sauce products"


# Medium Tasks


def _validate_searchfindiphone(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user searched for iPhone and found specific product."""

    # Check if we're on product page
    if final_state.get("page") != "product":
        return 0.0, f"Not on product page, current page: {final_state.get('page')}"

    # Check if correct product is selected
    if final_state.get("selectedProductId") != "1":
        return 0.0, f"Wrong product selected. Expected: 1, Got: {final_state.get('selectedProductId')}"

    # Check if search was performed with correct query
    search_query = final_state.get("searchQuery", "").lower()
    if "iphone" not in search_query:
        return 0.0, f"Search query doesn't contain 'iPhone': {final_state.get('searchQuery')}"

    return 1.0, "Successfully searched for iPhone and selected product 1"


def _validate_buynowfromdetails(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that product was added to cart from detail page."""

    # Check cart contains items
    cart = final_state.get("cart", [])
    if len(cart) == 0:
        return 0.0, "Cart is empty"

    # Find product with ID "2" in cart
    target_product = None
    for item in cart:
        if item.get("productId") == "2":
            target_product = item
            break

    if not target_product:
        return 0.0, f"Product 2 not found in cart. Cart contents: {cart}"

    # Check quantity is 1
    if target_product.get("qty", 0) != 1:
        return 0.0, f"Product 2 quantity should be 1, got: {target_product.get('qty')}"

    return 1.0, "Successfully added product 2 to cart with quantity 1"


def _validate_modifycartquantities(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user modified cart quantities correctly."""

    # Check we're on cart page
    if final_state.get("page") != "cart":
        return 0.0, f"Should be on cart page, got: {final_state.get('page')}"

    cart = final_state.get("cart", [])

    product_3 = next((item for item in cart if item.get("productId") == "3"), None)
    product_7 = next((item for item in cart if item.get("productId") == "7"), None)

    if not product_3:
        return 0.0, "Instant noodles (product 3) not found in cart"
    if not product_7:
        return 0.0, "Laundry detergent (product 7) not found in cart"

    # Check updated quantities
    if product_3.get("qty", 0) != 3:
        return 0.0, f"Product 3 quantity should be 3, got: {product_3.get('qty')}"
    if product_7.get("qty", 0) != 1:
        return 0.0, f"Product 7 quantity should be 1, got: {product_7.get('qty')}"

    return 1.0, "Successfully modified cart quantities"


def _validate_useaddtocartpopup(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that user used add to cart popup successfully."""

    # Check add to cart popup is closed
    if final_state.get("isAddToCartPopupOpen", False):
        return 0.0, "Add to cart popup should be closed but is still open"

    # Check cart contains product 2 with quantity 2
    cart = final_state.get("cart", [])
    product_2 = next((item for item in cart if item.get("productId") == "2"), None)

    if not product_2:
        return 0.0, "JEEP shirt (product 2) not found in cart"

    if product_2.get("qty", 0) != 2:
        return 0.0, f"Product 2 quantity should be 2, got: {product_2.get('qty')}"

    return 1.0, "Successfully used add to cart popup to add 2 quantities"


def _validate_relatedproductchain(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate navigation through related product chain."""

    # Check we're on product detail page for sauce
    if final_state.get("page") != "product":
        return 0.0, f"Should be on product detail page, got: {final_state.get('page')}"

    if final_state.get("selectedProductId") != "5":
        return 0.0, f"Should be viewing sauce (product 5), got: {final_state.get('selectedProductId')}"

    return 1.0, "Successfully navigated through related product chain to sauce details"


def _validate_addrelatedtocart(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate adding related product to cart."""

    # Check cart contains product 4 with quantity 2
    cart = final_state.get("cart", [])
    product_4 = next((item for item in cart if item.get("productId") == "4"), None)

    if not product_4:
        return 0.0, "Cooking pan (product 4) not found in cart"

    if product_4.get("qty", 0) != 2:
        return 0.0, f"Product 4 quantity should be 2, got: {product_4.get('qty')}"

    # Add to cart popup should be closed
    if final_state.get("isAddToCartPopupOpen", False):
        return 0.0, "Add to cart popup should be closed"

    return 1.0, "Successfully added related product to cart with correct quantity"


# Hard Tasks


def _validate_complexsearchaddmultiple(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate complex search and multiple product actions."""

    # Check 1: Currently viewing product 4
    if final_state.get("page") != "product":
        return 0.0, f"Should be on product page, got: {final_state.get('page')}"

    if final_state.get("selectedProductId") != "4":
        return 0.0, f"Should be viewing product 4, got: {final_state.get('selectedProductId')}"

    # Check 2: Search query is "no"
    search_query = final_state.get("searchQuery", "").lower()
    if "no" not in search_query:
        return 0.0, f"Search query should contain 'no', got: {final_state.get('searchQuery')}"

    # Check 3: Product 3 is in cart
    cart = final_state.get("cart", [])
    product_3_in_cart = any(item.get("productId") == "3" for item in cart)

    if not product_3_in_cart:
        return 0.0, f"Product 3 not found in cart. Cart contents: {cart}"

    return 1.0, "Successfully completed complex search and multiple product actions"


def _validate_multiproductcartmanagement(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate complex multi-product cart management."""

    # Check 1: Currently on cart page
    if final_state.get("page") != "cart":
        return 0.0, f"Should be on cart page, got: {final_state.get('page')}"

    # Check 2: Cart contains both products with correct quantities
    cart = final_state.get("cart", [])

    product_7 = next((item for item in cart if item.get("productId") == "7"), None)
    product_3 = next((item for item in cart if item.get("productId") == "3"), None)

    if not product_7:
        return 0.0, "活力28洗衣液 (product 7) not found in cart"
    if not product_3:
        return 0.0, "华丰方便面 (product 3) not found in cart"

    # Check quantities
    if product_7.get("qty", 0) != 2:
        return 0.0, f"Product 7 quantity should be 2, got: {product_7.get('qty')}"
    if product_3.get("qty", 0) != 1:
        return 0.0, f"Product 3 quantity should be 1, got: {product_3.get('qty')}"

    return 1.0, "Successfully managed multiple products in cart with correct quantities"


def _validate_completeshoppingworkflow(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate complete shopping workflow with cart modification."""

    # Check 1: Currently on cart page
    if final_state.get("page") != "cart":
        return 0.0, f"Should be on cart page, got: {final_state.get('page')}"

    # Check 2: Cart contains only product 6 (massage chair)
    cart = final_state.get("cart", [])

    product_6 = next((item for item in cart if item.get("productId") == "6"), None)
    product_4 = next((item for item in cart if item.get("productId") == "4"), None)

    # Product 6 should be in cart with quantity 1
    if not product_6:
        return 0.0, "奥克斯按摩椅 (product 6) not found in cart"
    if product_6.get("qty", 0) != 1:
        return 0.0, f"Product 6 quantity should be 1, got: {product_6.get('qty')}"

    # Product 4 should NOT be in cart (was removed)
    if product_4:
        return 0.0, "爱仕达炒锅 (product 4) should be removed from cart but is still present"

    # Should have exactly 1 item in cart
    if len(cart) != 1:
        return 0.0, f"Cart should have exactly 1 item, got: {len(cart)} items"

    return 1.0, "Successfully completed shopping workflow with correct cart contents"


def _validate_completeproductdiscovery(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate complete product discovery flow."""

    # Check we're on cart page
    if final_state.get("page") != "cart":
        return 0.0, f"Should be on cart page, got: {final_state.get('page')}"

    cart = final_state.get("cart", [])

    product_5 = next((item for item in cart if item.get("productId") == "5"), None)
    product_7 = next((item for item in cart if item.get("productId") == "7"), None)

    if not product_5:
        return 0.0, "Sauce (product 5) not found in cart"
    if not product_7:
        return 0.0, "Laundry detergent (product 7) not found in cart"

    # Check quantities
    if product_5.get("qty", 0) != 2:
        return 0.0, f"Product 5 quantity should be 2, got: {product_5.get('qty')}"
    if product_7.get("qty", 0) != 1:
        return 0.0, f"Product 7 quantity should be 1, got: {product_7.get('qty')}"

    # Should have exactly 2 items in cart
    if len(cart) != 2:
        return 0.0, f"Cart should have exactly 2 items, got: {len(cart)} items"

    return 1.0, "Successfully completed product discovery flow"


def _validate_relatedproductsshoppingspree(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate complete shopping spree using related products."""

    # Check we're on cart page
    if final_state.get("page") != "cart":
        return 0.0, f"Should be on cart page, got: {final_state.get('page')}"

    cart = final_state.get("cart", [])

    # Check all products with correct quantities
    products_expected = {
        "4": 1,  # cooking pan
        "5": 2,  # sauce
        "3": 3,  # noodles
        "2": 1,  # detergent
    }

    for product_id, expected_qty in products_expected.items():
        product = next((item for item in cart if item.get("productId") == product_id), None)
        if not product:
            return 0.0, f"Product {product_id} not found in cart"
        if product.get("qty", 0) != expected_qty:
            return 0.0, f"Product {product_id} quantity should be {expected_qty}, got: {product.get('qty')}"

    # Should have exactly 4 items in cart
    if len(cart) != 4:
        return 0.0, f"Cart should have exactly 4 items, got: {len(cart)} items"

    return 1.0, "Successfully completed related products shopping spree with all items"


# Registry
REWARD_FUNCTIONS_TAOBAO_MOBILE = {
    "_validate_navigatetosearch": _validate_navigatetosearch,
    "_validate_viewproductfromhome": _validate_viewproductfromhome,
    "_validate_viewshoppingcart": _validate_viewshoppingcart,
    "_validate_navigateviarelatedproducts": _validate_navigateviarelatedproducts,
    "_validate_browserelatedfromcart": _validate_browserelatedfromcart,
    "_validate_quickproductcomparison": _validate_quickproductcomparison,
    "_validate_returntosearchfromproduct": _validate_returntosearchfromproduct,
    "_validate_searchproduct": _validate_searchproduct,
    "_validate_searchfindiphone": _validate_searchfindiphone,
    "_validate_buynowfromdetails": _validate_buynowfromdetails,
    "_validate_modifycartquantities": _validate_modifycartquantities,
    "_validate_useaddtocartpopup": _validate_useaddtocartpopup,
    "_validate_relatedproductchain": _validate_relatedproductchain,
    "_validate_addrelatedtocart": _validate_addrelatedtocart,
    "_validate_complexsearchaddmultiple": _validate_complexsearchaddmultiple,
    "_validate_multiproductcartmanagement": _validate_multiproductcartmanagement,
    "_validate_completeshoppingworkflow": _validate_completeshoppingworkflow,
    "_validate_completeproductdiscovery": _validate_completeproductdiscovery,
    "_validate_relatedproductsshoppingspree": _validate_relatedproductsshoppingspree,
}
