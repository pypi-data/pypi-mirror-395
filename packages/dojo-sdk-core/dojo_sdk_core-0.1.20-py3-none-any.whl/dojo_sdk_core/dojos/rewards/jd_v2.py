"""
Reward functions for JD (JingDong) e-commerce SPA tasks - V2 Architecture.

This version includes both frontend and backend validation with bundled reward functions.
Each task exports a bundle containing:
  - state_key: Dict defining backend queries (collection + filter)
  - validate_backend: Function (state_key, final_state) -> (float, str)
  - validate_frontend: Function (initial_state, final_state) -> (float, str)
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, TypedDict

logger = logging.getLogger(__name__)


# =============================================================================
# Type Definitions
# =============================================================================


class StateKeyQuery(TypedDict):
    collection: str
    filter: Dict[str, Any]


StateKey = Dict[str, StateKeyQuery]
ValidatorFunc = Callable[[Dict[str, Any], Dict[str, Any]], Tuple[float, str]]


class ValidateTask(TypedDict):
    state_key: StateKey
    validate_backend: ValidatorFunc
    validate_frontend: ValidatorFunc


# =============================================================================
# Helper Functions - Frontend State
# =============================================================================


def _check_page(final_state: Dict[str, Any], expected_page: str) -> Tuple[bool, str]:
    """Check if the current page matches the expected page."""
    page = final_state.get("page")
    if page != expected_page:
        return False, f"page='{page}' expected '{expected_page}'"
    return True, ""


def _check_search_query_contains(final_state: Dict[str, Any], expected_text: str) -> Tuple[bool, str]:
    """Check if the search query contains the expected text."""
    search_query = final_state.get("searchQuery", "")
    if expected_text not in search_query:
        return False, f"searchQuery='{search_query}' expected to contain '{expected_text}'"
    return True, ""


def _check_search_query_contains_any(final_state: Dict[str, Any], expected_texts: List[str]) -> Tuple[bool, str]:
    """Check if the search query contains any of the expected texts."""
    search_query = final_state.get("searchQuery", "")
    if not any(text in search_query for text in expected_texts):
        return False, f"searchQuery='{search_query}' expected to contain one of {expected_texts}"
    return True, ""


def _check_selected_product_id(final_state: Dict[str, Any], expected_id: str) -> Tuple[bool, str]:
    """Check if the selected product ID matches."""
    selected_id = final_state.get("selectedProductId")
    if selected_id != expected_id:
        return False, f"selectedProductId='{selected_id}' expected '{expected_id}'"
    return True, ""


def _check_home_feed_category(final_state: Dict[str, Any], expected_category: str) -> Tuple[bool, str]:
    """Check if the home feed category matches."""
    category = final_state.get("homeFeedCategory")
    if category != expected_category:
        return False, f"homeFeedCategory='{category}' expected '{expected_category}'"
    return True, ""


# =============================================================================
# Helper Functions - Backend State
# =============================================================================


def _find_cart_item_backend(final_state: Dict[str, Any], product_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Find a cart item in backend state by productId."""
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return None, "Cart array missing in backend final state"
    for item in cart:
        if item.get("productId") == product_id:
            return item, ""
    return None, f"Cart item with productId '{product_id}' not found in backend"


def _no_backend_validation(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Placeholder for tasks that don't require backend validation."""
    return 1.0, "No backend validation required"


def _no_frontend_validation(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Placeholder for tasks that don't require frontend validation."""
    return 1.0, "Frontend validation skipped (data not in UI state)"


# =============================================================================
# NAVIGATION TASKS (Frontend-only)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: go-to-the-cart-page-from-the-homepage
# -----------------------------------------------------------------------------


def _validate_backend_go_to_the_cart_page_from_the_homepage(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_go_to_the_cart_page_from_the_homepage(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to cart page from homepage"


_validate_go_to_the_cart_page_from_the_homepage: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_go_to_the_cart_page_from_the_homepage,
    "validate_frontend": _validate_frontend_go_to_the_cart_page_from_the_homepage,
}


# -----------------------------------------------------------------------------
# Task: go-to-a-product-page-from-home
# -----------------------------------------------------------------------------


def _validate_backend_go_to_a_product_page_from_home(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_go_to_a_product_page_from_home(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-m4n5o6")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to product page from home"


_validate_go_to_a_product_page_from_home: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_go_to_a_product_page_from_home,
    "validate_frontend": _validate_frontend_go_to_a_product_page_from_home,
}


# -----------------------------------------------------------------------------
# Task: go-to-homepage-from-product-page
# -----------------------------------------------------------------------------


def _validate_backend_go_to_homepage_from_product_page(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_go_to_homepage_from_product_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "home")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to homepage from product page"


_validate_go_to_homepage_from_product_page: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_go_to_homepage_from_product_page,
    "validate_frontend": _validate_frontend_go_to_homepage_from_product_page,
}


# -----------------------------------------------------------------------------
# Task: go-to-cart-page-from-product-detail-page
# -----------------------------------------------------------------------------


def _validate_backend_go_to_cart_page_from_product_detail_page(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_go_to_cart_page_from_product_detail_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to cart page from product detail"


_validate_go_to_cart_page_from_product_detail_page: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_go_to_cart_page_from_product_detail_page,
    "validate_frontend": _validate_frontend_go_to_cart_page_from_product_detail_page,
}


# -----------------------------------------------------------------------------
# Task: go-to-product-detail-from-search
# -----------------------------------------------------------------------------


def _validate_backend_go_to_product_detail_from_search(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_go_to_product_detail_from_search(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-m4n5o6")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to product detail from search"


_validate_go_to_product_detail_from_search: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_go_to_product_detail_from_search,
    "validate_frontend": _validate_frontend_go_to_product_detail_from_search,
}


# -----------------------------------------------------------------------------
# Task: navigate-from-cart-back-to-homepage
# -----------------------------------------------------------------------------


def _validate_backend_navigate_from_cart_back_to_homepage(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_from_cart_back_to_homepage(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "home")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated from cart back to homepage"


_validate_navigate_from_cart_back_to_homepage: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_from_cart_back_to_homepage,
    "validate_frontend": _validate_frontend_navigate_from_cart_back_to_homepage,
}


# -----------------------------------------------------------------------------
# Task: navigate-from-search-to-homepage
# -----------------------------------------------------------------------------


def _validate_backend_navigate_from_search_to_homepage(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_from_search_to_homepage(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "home")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated from search to homepage"


_validate_navigate_from_search_to_homepage: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_from_search_to_homepage,
    "validate_frontend": _validate_frontend_navigate_from_search_to_homepage,
}


# -----------------------------------------------------------------------------
# Task: navigate-to-cart-from-product-page-via-header
# -----------------------------------------------------------------------------


def _validate_backend_navigate_to_cart_from_product_page_via_header(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_to_cart_from_product_page_via_header(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to cart from product page via header"


_validate_navigate_to_cart_from_product_page_via_header: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_to_cart_from_product_page_via_header,
    "validate_frontend": _validate_frontend_navigate_to_cart_from_product_page_via_header,
}


# -----------------------------------------------------------------------------
# Task: navigate-to-cart-from-search-page
# -----------------------------------------------------------------------------


def _validate_backend_navigate_to_cart_from_search_page(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_to_cart_from_search_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to cart from search page"


_validate_navigate_to_cart_from_search_page: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_to_cart_from_search_page,
    "validate_frontend": _validate_frontend_navigate_to_cart_from_search_page,
}


# -----------------------------------------------------------------------------
# Task: navigate-from-product-to-another-product
# -----------------------------------------------------------------------------


def _validate_backend_navigate_from_product_to_another_product(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_from_product_to_another_product(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-y7z8a9")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains(final_state, "华丰京觅")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated from product to another product"


_validate_navigate_from_product_to_another_product: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_from_product_to_another_product,
    "validate_frontend": _validate_frontend_navigate_from_product_to_another_product,
}


# -----------------------------------------------------------------------------
# Task: navigate-to-product-from-homepage-section
# -----------------------------------------------------------------------------


def _validate_backend_navigate_to_product_from_homepage_section(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_to_product_from_homepage_section(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-a1b2c3")
    if not ok:
        return 0.0, error
    ok, error = _check_home_feed_category(final_state, "电脑数码")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to product from homepage section"


_validate_navigate_to_product_from_homepage_section: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_to_product_from_homepage_section,
    "validate_frontend": _validate_frontend_navigate_to_product_from_homepage_section,
}


# -----------------------------------------------------------------------------
# Task: navigate-via-category-sidebar-menu
# -----------------------------------------------------------------------------


def _validate_backend_navigate_via_category_sidebar_menu(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_via_category_sidebar_menu(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains(final_state, "自动制冰")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated via category sidebar menu"


_validate_navigate_via_category_sidebar_menu: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_via_category_sidebar_menu,
    "validate_frontend": _validate_frontend_navigate_via_category_sidebar_menu,
}


# -----------------------------------------------------------------------------
# Task: multi-step-navigation-home-to-product-to-cart
# -----------------------------------------------------------------------------


def _validate_backend_multi_step_navigation_home_to_product_to_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_multi_step_navigation_home_to_product_to_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    ok, error = _check_home_feed_category(final_state, "服饰鞋包")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully completed multi-step navigation"


_validate_multistep_navigation_home_to_product_to_cart: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_multi_step_navigation_home_to_product_to_cart,
    "validate_frontend": _validate_frontend_multi_step_navigation_home_to_product_to_cart,
}


# -----------------------------------------------------------------------------
# Task: filter-homepage-feed-by-category
# -----------------------------------------------------------------------------


def _validate_backend_filter_homepage_feed_by_category(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for feed filter"


def _validate_frontend_filter_homepage_feed_by_category(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "home")
    if not ok:
        return 0.0, error
    category = final_state.get("homeFeedCategory", "")
    valid_categories = ["服饰鞋包", "手机通讯", "电脑数码"]
    if category not in valid_categories:
        return 0.0, f"homeFeedCategory='{category}' expected one of {valid_categories}"
    return 1.0, f"Successfully filtered homepage feed by category '{category}'"


_validate_filter_homepage_feed_by_category: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_filter_homepage_feed_by_category,
    "validate_frontend": _validate_frontend_filter_homepage_feed_by_category,
}


# =============================================================================
# SEARCH TASKS (Frontend-only)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: search-吉普衬衫
# -----------------------------------------------------------------------------


def _validate_backend_search_吉普衬衫(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_吉普衬衫(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_search_query_contains(final_state, "吉普衬衫")
    if not ok:
        return 0.0, error
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for 吉普衬衫"


_validate_search_吉普衬衫: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_吉普衬衫,
    "validate_frontend": _validate_frontend_search_吉普衬衫,
}


# -----------------------------------------------------------------------------
# Task: find-a-product-using-search-from-homepage
# -----------------------------------------------------------------------------


def _validate_backend_find_a_product_using_search_from_homepage(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_find_a_product_using_search_from_homepage(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains(final_state, "吉普衬衫")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-m4n5o6")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for product and navigated to detail page"


_validate_find_a_product_using_search_from_homepage: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_find_a_product_using_search_from_homepage,
    "validate_frontend": _validate_frontend_find_a_product_using_search_from_homepage,
}


# -----------------------------------------------------------------------------
# Task: search-a-product-from-another-product-page
# -----------------------------------------------------------------------------


def _validate_backend_search_a_product_from_another_product_page(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_a_product_from_another_product_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-y7z8a9")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for product and navigated to detail page"


_validate_search_a_product_from_another_product_page: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_a_product_from_another_product_page,
    "validate_frontend": _validate_frontend_search_a_product_from_another_product_page,
}


# -----------------------------------------------------------------------------
# Task: search-using-multi-term-query
# -----------------------------------------------------------------------------


def _validate_backend_search_using_multi_term_query(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_using_multi_term_query(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    search_query = final_state.get("searchQuery", "")
    if "JEEP 衬衫 男" not in search_query and "JEEP" not in search_query:
        return 0.0, f"searchQuery='{search_query}' expected to contain 'JEEP 衬衫 男'"
    return 1.0, "Successfully searched with multi-term query"


_validate_search_using_multiterm_query: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_using_multi_term_query,
    "validate_frontend": _validate_frontend_search_using_multi_term_query,
}


# -----------------------------------------------------------------------------
# Task: search-from-search-history
# -----------------------------------------------------------------------------


def _validate_backend_search_from_search_history(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_from_search_history(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    search_query = final_state.get("searchQuery", "")
    history_items = ["漂亮的裙子", "历史记录", "京东品酒会"]
    if not any(item in search_query for item in history_items):
        return 0.0, f"searchQuery='{search_query}' expected from history {history_items}"
    return 1.0, "Successfully searched from search history"


_validate_search_from_search_history: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_from_search_history,
    "validate_frontend": _validate_frontend_search_from_search_history,
}


# -----------------------------------------------------------------------------
# Task: search-using-suggestion-dropdown
# -----------------------------------------------------------------------------


def _validate_backend_search_using_suggestion_dropdown(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_using_suggestion_dropdown(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    search_query = final_state.get("searchQuery", "")
    if "iPhone" not in search_query:
        return 0.0, f"searchQuery='{search_query}' expected to contain 'iPhone'"
    return 1.0, "Successfully searched using suggestion dropdown"


_validate_search_using_suggestion_dropdown: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_using_suggestion_dropdown,
    "validate_frontend": _validate_frontend_search_using_suggestion_dropdown,
}


# -----------------------------------------------------------------------------
# Task: search-for-apple-iphone
# -----------------------------------------------------------------------------


def _validate_backend_search_for_apple_iphone(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_for_apple_iphone(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains_any(final_state, ["Apple", "iPhone"])
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for Apple iPhone"


_validate_search_for_apple_iphone: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_for_apple_iphone,
    "validate_frontend": _validate_frontend_search_for_apple_iphone,
}


# -----------------------------------------------------------------------------
# Task: search-for-华丰方便面
# -----------------------------------------------------------------------------


def _validate_backend_search_for_华丰方便面(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_for_华丰方便面(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains_any(final_state, ["华丰", "方便面"])
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for 华丰方便面"


_validate_search_for_华丰方便面: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_for_华丰方便面,
    "validate_frontend": _validate_frontend_search_for_华丰方便面,
}


# -----------------------------------------------------------------------------
# Task: search-for-奥克斯按摩椅
# -----------------------------------------------------------------------------


def _validate_backend_search_for_奥克斯按摩椅(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_for_奥克斯按摩椅(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains_any(final_state, ["奥克斯", "按摩椅"])
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for 奥克斯按摩椅"


_validate_search_for_奥克斯按摩椅: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_for_奥克斯按摩椅,
    "validate_frontend": _validate_frontend_search_for_奥克斯按摩椅,
}


# -----------------------------------------------------------------------------
# Task: search-for-爱仕达炒锅
# -----------------------------------------------------------------------------


def _validate_backend_search_for_爱仕达炒锅(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_for_爱仕达炒锅(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains_any(final_state, ["爱仕达", "炒锅"])
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched for 爱仕达炒锅"


_validate_search_for_爱仕达炒锅: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_for_爱仕达炒锅,
    "validate_frontend": _validate_frontend_search_for_爱仕达炒锅,
}


# -----------------------------------------------------------------------------
# Task: search-for-活力-28-洗衣液
# -----------------------------------------------------------------------------


def _validate_backend_search_for_活力_28_洗衣液(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_for_活力_28_洗衣液(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    search_query = final_state.get("searchQuery", "")
    if "活力28" not in search_query and "洗衣液" not in search_query and "活力 28" not in search_query:
        return 0.0, f"searchQuery='{search_query}' expected to contain '活力28' or '洗衣液'"
    return 1.0, "Successfully searched for 活力28洗衣液"


_validate_search_for_活力_28_洗衣液: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_for_活力_28_洗衣液,
    "validate_frontend": _validate_frontend_search_for_活力_28_洗衣液,
}


# -----------------------------------------------------------------------------
# Task: search-and-navigate-to-product-detail
# -----------------------------------------------------------------------------


def _validate_backend_search_and_navigate_to_product_detail(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_and_navigate_to_product_detail(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    selected_id = final_state.get("selectedProductId", "")
    if selected_id not in ["prod-q7r8s9", "prod-y1z2a3b4"]:
        return 0.0, f"selectedProductId='{selected_id}' expected 'prod-q7r8s9' or 'prod-y1z2a3b4'"
    ok, error = _check_search_query_contains(final_state, "紫苏酱")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully searched and navigated to product detail"


_validate_search_and_navigate_to_product_detail: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_and_navigate_to_product_detail,
    "validate_frontend": _validate_frontend_search_and_navigate_to_product_detail,
}


# =============================================================================
# FILTER & SORT TASKS (Frontend-only)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: apply-price-range-filter
# -----------------------------------------------------------------------------


def _validate_backend_apply_price_range_filter(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for filter"


def _validate_frontend_apply_price_range_filter(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    price_filter = final_state.get("searchPriceFilter")
    if price_filter is None:
        return 0.0, "searchPriceFilter is null, expected to be set"
    if "min" not in price_filter or "max" not in price_filter:
        return 0.0, f"searchPriceFilter={price_filter} missing 'min' or 'max'"
    return 1.0, f"Successfully applied price range filter {price_filter}"


_validate_apply_price_range_filter: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_apply_price_range_filter,
    "validate_frontend": _validate_frontend_apply_price_range_filter,
}


# -----------------------------------------------------------------------------
# Task: apply-brand-filter-single-brand
# -----------------------------------------------------------------------------


def _validate_backend_apply_brand_filter_single_brand(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for filter"


def _validate_frontend_apply_brand_filter_single_brand(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    brand_filter = final_state.get("searchBrandFilter", [])
    if len(brand_filter) != 1:
        return 0.0, f"searchBrandFilter has {len(brand_filter)} brands, expected 1"
    if brand_filter[0] != "JEEP":
        return 0.0, f"searchBrandFilter={brand_filter} expected ['JEEP']"
    return 1.0, "Successfully applied single brand filter"


_validate_apply_brand_filter_single_brand: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_apply_brand_filter_single_brand,
    "validate_frontend": _validate_frontend_apply_brand_filter_single_brand,
}


# -----------------------------------------------------------------------------
# Task: apply-brand-filter-multiple-brands
# -----------------------------------------------------------------------------


def _validate_backend_apply_brand_filter_multiple_brands(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for filter"


def _validate_frontend_apply_brand_filter_multiple_brands(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    brand_filter = final_state.get("searchBrandFilter", [])
    if len(brand_filter) < 2:
        return 0.0, f"searchBrandFilter has {len(brand_filter)} brands, expected at least 2"
    valid_combinations = [{"JEEP", "Apple"}, {"ASD", "AUX"}]
    brand_set = set(brand_filter)
    if not any(brand_set == combo for combo in valid_combinations):
        return 0.0, f"searchBrandFilter={brand_filter} expected ['JEEP', 'Apple'] or ['ASD', 'AUX']"
    return 1.0, f"Successfully applied multiple brand filter {brand_filter}"


_validate_apply_brand_filter_multiple_brands: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_apply_brand_filter_multiple_brands,
    "validate_frontend": _validate_frontend_apply_brand_filter_multiple_brands,
}


# -----------------------------------------------------------------------------
# Task: apply-multiple-filters-price-and-brand
# -----------------------------------------------------------------------------


def _validate_backend_apply_multiple_filters_price_and_brand(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for filter"


def _validate_frontend_apply_multiple_filters_price_and_brand(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    price_filter = final_state.get("searchPriceFilter")
    brand_filter = final_state.get("searchBrandFilter", [])
    if price_filter is None:
        return 0.0, "searchPriceFilter is null, expected to be set"
    if len(brand_filter) == 0:
        return 0.0, "searchBrandFilter is empty, expected at least one brand"
    return 1.0, f"Successfully applied multiple filters (price: {price_filter}, brands: {brand_filter})"


_validate_apply_multiple_filters_price_and_brand: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_apply_multiple_filters_price_and_brand,
    "validate_frontend": _validate_frontend_apply_multiple_filters_price_and_brand,
}


# -----------------------------------------------------------------------------
# Task: clear-price-filter
# -----------------------------------------------------------------------------


def _validate_backend_clear_price_filter(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for filter"


def _validate_frontend_clear_price_filter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    price_filter = final_state.get("searchPriceFilter")
    if price_filter is not None:
        return 0.0, f"searchPriceFilter={price_filter} expected null"
    return 1.0, "Successfully cleared price filter"


_validate_clear_price_filter: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_clear_price_filter,
    "validate_frontend": _validate_frontend_clear_price_filter,
}


# -----------------------------------------------------------------------------
# Task: clear-brand-filter
# -----------------------------------------------------------------------------


def _validate_backend_clear_brand_filter(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for filter"


def _validate_frontend_clear_brand_filter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    brand_filter = final_state.get("searchBrandFilter", [])
    if len(brand_filter) != 0:
        return 0.0, f"searchBrandFilter={brand_filter} expected empty []"
    return 1.0, "Successfully cleared brand filter"


_validate_clear_brand_filter: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_clear_brand_filter,
    "validate_frontend": _validate_frontend_clear_brand_filter,
}


# -----------------------------------------------------------------------------
# Task: filter-and-navigate-to-product
# -----------------------------------------------------------------------------


def _validate_backend_filter_and_navigate_to_product(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_filter_and_navigate_to_product(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    selected_id = final_state.get("selectedProductId")
    if not selected_id:
        return 0.0, "selectedProductId is missing"
    price_filter = final_state.get("searchPriceFilter")
    brand_filter = final_state.get("searchBrandFilter", [])
    if price_filter is None and len(brand_filter) == 0:
        return 0.0, "Expected at least one filter (price or brand) to be applied"
    return 1.0, f"Successfully filtered and navigated to product '{selected_id}'"


_validate_filter_and_navigate_to_product: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_filter_and_navigate_to_product,
    "validate_frontend": _validate_frontend_filter_and_navigate_to_product,
}


# -----------------------------------------------------------------------------
# Task: sort-by-price-ascending
# -----------------------------------------------------------------------------


def _validate_backend_sort_by_price_ascending(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for sort"


def _validate_frontend_sort_by_price_ascending(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    sort_type = final_state.get("searchSortType")
    if sort_type != "price":
        return 0.0, f"searchSortType='{sort_type}' expected 'price'"
    sort_order = final_state.get("searchSortOrder")
    if sort_order != "asc":
        return 0.0, f"searchSortOrder='{sort_order}' expected 'asc'"
    return 1.0, "Successfully sorted by price ascending"


_validate_sort_by_price_ascending: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_sort_by_price_ascending,
    "validate_frontend": _validate_frontend_sort_by_price_ascending,
}


# -----------------------------------------------------------------------------
# Task: sort-by-price-descending
# -----------------------------------------------------------------------------


def _validate_backend_sort_by_price_descending(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for sort"


def _validate_frontend_sort_by_price_descending(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    sort_type = final_state.get("searchSortType")
    if sort_type != "price":
        return 0.0, f"searchSortType='{sort_type}' expected 'price'"
    sort_order = final_state.get("searchSortOrder")
    if sort_order != "desc":
        return 0.0, f"searchSortOrder='{sort_order}' expected 'desc'"
    return 1.0, "Successfully sorted by price descending"


_validate_sort_by_price_descending: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_sort_by_price_descending,
    "validate_frontend": _validate_frontend_sort_by_price_descending,
}


# -----------------------------------------------------------------------------
# Task: sort-by-sales
# -----------------------------------------------------------------------------


def _validate_backend_sort_by_sales(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for sort"


def _validate_frontend_sort_by_sales(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "search")
    if not ok:
        return 0.0, error
    sort_type = final_state.get("searchSortType")
    if sort_type != "sales":
        return 0.0, f"searchSortType='{sort_type}' expected 'sales'"
    return 1.0, "Successfully sorted by sales"


_validate_sort_by_sales: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_sort_by_sales,
    "validate_frontend": _validate_frontend_sort_by_sales,
}


# =============================================================================
# CART TASKS (Backend validation)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: add-a-product-to-cart
# -----------------------------------------------------------------------------


def _validate_backend_add_a_product_to_cart(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item:
        return 0.0, error
    if item.get("qty") != 1:
        return 0.0, f"Cart item qty={item.get('qty')} expected 1"
    return 1.0, "Backend: Successfully added product to cart"


def _validate_frontend_add_a_product_to_cart(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "Frontend validation skipped (cart data not in UI state)"


_validate_add_a_product_to_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_add_a_product_to_cart,
    "validate_frontend": _validate_frontend_add_a_product_to_cart,
}


# -----------------------------------------------------------------------------
# Task: add-a-product-from-search-result-to-cart
# -----------------------------------------------------------------------------


def _validate_backend_add_a_product_from_search_result_to_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item:
        return 0.0, error
    if item.get("qty") != 1:
        return 0.0, f"Cart item qty={item.get('qty')} expected 1"
    return 1.0, "Backend: Successfully added product from search to cart"


def _validate_frontend_add_a_product_from_search_result_to_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    ok, error = _check_selected_product_id(final_state, "prod-m4n5o6")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to product detail page"


_validate_add_a_product_from_search_result_to_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_add_a_product_from_search_result_to_cart,
    "validate_frontend": _validate_frontend_add_a_product_from_search_result_to_cart,
}


# -----------------------------------------------------------------------------
# Task: add-an-item-from-the-homepage
# -----------------------------------------------------------------------------


def _validate_backend_add_an_item_from_the_homepage(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-q7r8s9")
    if not item:
        return 0.0, error
    if item.get("qty") != 1:
        return 0.0, f"Cart item qty={item.get('qty')} expected 1"
    return 1.0, "Backend: Successfully added item from homepage to cart"


def _validate_frontend_add_an_item_from_the_homepage(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "home")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on homepage"


_validate_add_an_item_from_the_homepage: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_add_an_item_from_the_homepage,
    "validate_frontend": _validate_frontend_add_an_item_from_the_homepage,
}


# -----------------------------------------------------------------------------
# Task: add-an-item-with-3-quantity
# -----------------------------------------------------------------------------


def _validate_backend_add_an_item_with_3_quantity(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item:
        return 0.0, error
    if item.get("qty") != 3:
        return 0.0, f"Cart item qty={item.get('qty')} expected 3"
    return 1.0, "Backend: Successfully added item with qty 3"


def _validate_frontend_add_an_item_with_3_quantity(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on product page"


_validate_add_an_item_with_3_quantity: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_add_an_item_with_3_quantity,
    "validate_frontend": _validate_frontend_add_an_item_with_3_quantity,
}


# -----------------------------------------------------------------------------
# Task: add-product-with-specific-variant-to-cart
# -----------------------------------------------------------------------------


def _validate_backend_add_product_with_specific_variant_to_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item:
        return 0.0, error
    if item.get("qty") != 1:
        return 0.0, f"Cart item qty={item.get('qty')} expected 1"
    variants = item.get("selectedVariants", {})
    if variants.get("颜色") != "深蓝" or variants.get("尺码") != "XL":
        return 0.0, f"selectedVariants={variants} expected {{'颜色': '深蓝', '尺码': 'XL'}}"
    return 1.0, "Backend: Successfully added product with specific variant"


def _validate_frontend_add_product_with_specific_variant_to_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on product page"


_validate_add_product_with_specific_variant_to_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_add_product_with_specific_variant_to_cart,
    "validate_frontend": _validate_frontend_add_product_with_specific_variant_to_cart,
}


# -----------------------------------------------------------------------------
# Task: select-variant-and-add-to-cart
# -----------------------------------------------------------------------------


def _validate_backend_select_variant_and_add_to_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item:
        return 0.0, error
    if item.get("qty") != 1:
        return 0.0, f"Cart item qty={item.get('qty')} expected 1"
    variants = item.get("selectedVariants", {})
    if "颜色" not in variants or "尺码" not in variants:
        return 0.0, f"selectedVariants={variants} missing '颜色' or '尺码'"
    if variants.get("颜色") != "卡其色" or variants.get("尺码") != "M":
        return 0.0, f"selectedVariants={variants} expected {{'颜色': '卡其色', '尺码': 'M'}}"
    return 1.0, "Backend: Successfully selected variant and added to cart"


def _validate_frontend_select_variant_and_add_to_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "product")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on product page"


_validate_select_variant_and_add_to_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_select_variant_and_add_to_cart,
    "validate_frontend": _validate_frontend_select_variant_and_add_to_cart,
}


# -----------------------------------------------------------------------------
# Task: remove-one-item-from-cart
# -----------------------------------------------------------------------------


def _validate_backend_remove_one_item_from_cart(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    cart = final_state.get("cart")
    # Cart can be null or empty list when all items are removed
    if cart is None:
        return 1.0, "Backend: Successfully removed item from cart (cart is null)"
    if not isinstance(cart, list):
        return 0.0, "Cart is not a list or null"
    if len(cart) != 0:
        return 0.0, f"Cart has {len(cart)} items, expected 0"
    return 1.0, "Backend: Successfully removed item from cart"


def _validate_frontend_remove_one_item_from_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "Frontend validation skipped (cart data not in UI state)"


_validate_remove_one_item_from_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_remove_one_item_from_cart,
    "validate_frontend": _validate_frontend_remove_one_item_from_cart,
}


# -----------------------------------------------------------------------------
# Task: remove-multiple-items-in-the-cart
# -----------------------------------------------------------------------------


def _validate_backend_remove_multiple_items_in_the_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    # Cart can be null or empty list when all items are removed
    if cart is None:
        return 1.0, "Backend: Successfully removed all items from cart (cart is null)"
    if not isinstance(cart, list):
        return 0.0, "Cart is not a list or null"
    if len(cart) != 0:
        return 0.0, f"Cart has {len(cart)} items, expected 0"
    return 1.0, "Backend: Successfully removed all items from cart"


def _validate_frontend_remove_multiple_items_in_the_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on cart page"


_validate_remove_multiple_items_in_the_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_remove_multiple_items_in_the_cart,
    "validate_frontend": _validate_frontend_remove_multiple_items_in_the_cart,
}


# -----------------------------------------------------------------------------
# Task: reduce-an-item-quantity-in-the-cart
# -----------------------------------------------------------------------------


def _validate_backend_reduce_an_item_quantity_in_the_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item:
        return 0.0, error
    if item.get("qty") != 2:
        return 0.0, f"Cart item qty={item.get('qty')} expected 2"
    return 1.0, "Backend: Successfully reduced item quantity to 2"


def _validate_frontend_reduce_an_item_quantity_in_the_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "Frontend validation skipped (cart data not in UI state)"


_validate_reduce_an_item_quantity_in_the_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_reduce_an_item_quantity_in_the_cart,
    "validate_frontend": _validate_frontend_reduce_an_item_quantity_in_the_cart,
}


# -----------------------------------------------------------------------------
# Task: increase-an-item-and-reduce-another-item
# -----------------------------------------------------------------------------


def _validate_backend_increase_an_item_and_reduce_another_item(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"

    item1, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item1:
        return 0.0, error
    if item1.get("qty") != 4:
        return 0.0, f"Cart item prod-m4n5o6 qty={item1.get('qty')} expected 4"

    item2, error = _find_cart_item_backend(final_state, "prod-y7z8a9")
    if not item2:
        return 0.0, error
    if item2.get("qty") != 1:
        return 0.0, f"Cart item prod-y7z8a9 qty={item2.get('qty')} expected 1"

    return 1.0, "Backend: Successfully increased one item and reduced another"


def _validate_frontend_increase_an_item_and_reduce_another_item(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on cart page"


_validate_increase_an_item_and_reduce_another_item: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_increase_an_item_and_reduce_another_item,
    "validate_frontend": _validate_frontend_increase_an_item_and_reduce_another_item,
}


# -----------------------------------------------------------------------------
# Task: search-and-add-two-items-to-cart
# -----------------------------------------------------------------------------


def _validate_backend_search_and_add_two_items_to_cart(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    if len(cart) < 2:
        return 0.0, f"Cart has {len(cart)} items, expected at least 2"

    item1, error = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if not item1:
        return 0.0, error
    if item1.get("qty") != 3:
        return 0.0, f"Cart item prod-m4n5o6 qty={item1.get('qty')} expected 3"

    item2, error = _find_cart_item_backend(final_state, "prod-y7z8a9")
    if not item2:
        return 0.0, error
    if item2.get("qty") != 3:
        return 0.0, f"Cart item prod-y7z8a9 qty={item2.get('qty')} expected 3"

    return 1.0, "Backend: Successfully added two items with qty 3 each"


def _validate_frontend_search_and_add_two_items_to_cart(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on cart page"


_validate_search_and_add_two_items_to_cart: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_search_and_add_two_items_to_cart,
    "validate_frontend": _validate_frontend_search_and_add_two_items_to_cart,
}


# -----------------------------------------------------------------------------
# Task: search-and-add-item-to-cart-and-back-to-home
# -----------------------------------------------------------------------------


def _validate_backend_search_and_add_item_to_cart_and_back_to_home(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    item, error = _find_cart_item_backend(final_state, "prod-q7r8s9")
    if not item:
        return 0.0, error
    return 1.0, "Backend: Successfully added item to cart"


def _validate_frontend_search_and_add_item_to_cart_and_back_to_home(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "home")
    if not ok:
        return 0.0, error
    ok, error = _check_search_query_contains(final_state, "紫苏酱新")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on homepage with search query"


_validate_search_and_add_item_to_cart_and_back_to_home: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_search_and_add_item_to_cart_and_back_to_home,
    "validate_frontend": _validate_frontend_search_and_add_item_to_cart_and_back_to_home,
}


# -----------------------------------------------------------------------------
# Task: remove-item-from-cart-then-search-and-add-item
# -----------------------------------------------------------------------------


def _validate_backend_remove_item_from_cart_then_search_and_add_item(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    if len(cart) != 1:
        return 0.0, f"Cart has {len(cart)} items, expected 1"

    item, error = _find_cart_item_backend(final_state, "prod-y7z8a9")
    if not item:
        return 0.0, error

    # Verify the old item is not in cart
    old_item, _ = _find_cart_item_backend(final_state, "prod-m4n5o6")
    if old_item:
        return 0.0, "Cart still contains prod-m4n5o6, expected it to be removed"

    return 1.0, "Backend: Successfully removed old item and added new item"


def _validate_frontend_remove_item_from_cart_then_search_and_add_item(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on cart page"


_validate_remove_item_from_cart_then_search_and_add_item: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_remove_item_from_cart_then_search_and_add_item,
    "validate_frontend": _validate_frontend_remove_item_from_cart_then_search_and_add_item,
}


# -----------------------------------------------------------------------------
# Task: use-homepage-to-navigate-and-add-items
# -----------------------------------------------------------------------------


def _validate_backend_use_homepage_to_navigate_and_add_items(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    cart = final_state.get("cart")
    if not isinstance(cart, list):
        return 0.0, "Cart array missing in backend state"
    if len(cart) < 2:
        return 0.0, f"Cart has {len(cart)} items, expected at least 2"

    item1, error = _find_cart_item_backend(final_state, "prod-k1l2m3")
    if not item1:
        return 0.0, error

    item2, error = _find_cart_item_backend(final_state, "prod-y7z8a9")
    if not item2:
        return 0.0, error

    return 1.0, "Backend: Successfully added two items from homepage"


def _validate_frontend_use_homepage_to_navigate_and_add_items(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_page(final_state, "cart")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully on cart page"


_validate_use_homepage_to_navigate_and_add_items: ValidateTask = {
    "state_key": {
        "cart": {"collection": "cart", "filter": {}},
    },
    "validate_backend": _validate_backend_use_homepage_to_navigate_and_add_items,
    "validate_frontend": _validate_frontend_use_homepage_to_navigate_and_add_items,
}


# =============================================================================
# Registry of all V2 Reward Functions
# =============================================================================

REWARD_FUNCTIONS_JD_V2: Dict[str, ValidateTask] = {
    # Navigation Tasks
    "_validate_go_to_the_cart_page_from_the_homepage": _validate_go_to_the_cart_page_from_the_homepage,
    "_validate_go_to_a_product_page_from_home": _validate_go_to_a_product_page_from_home,
    "_validate_go_to_homepage_from_product_page": _validate_go_to_homepage_from_product_page,
    "_validate_go_to_cart_page_from_product_detail_page": _validate_go_to_cart_page_from_product_detail_page,
    "_validate_go_to_product_detail_from_search": _validate_go_to_product_detail_from_search,
    "_validate_navigate_from_cart_back_to_homepage": _validate_navigate_from_cart_back_to_homepage,
    "_validate_navigate_from_search_to_homepage": _validate_navigate_from_search_to_homepage,
    "_validate_navigate_to_cart_from_product_page_via_header": _validate_navigate_to_cart_from_product_page_via_header,
    "_validate_navigate_to_cart_from_search_page": _validate_navigate_to_cart_from_search_page,
    "_validate_navigate_from_product_to_another_product": _validate_navigate_from_product_to_another_product,
    "_validate_navigate_to_product_from_homepage_section": _validate_navigate_to_product_from_homepage_section,
    "_validate_navigate_via_category_sidebar_menu": _validate_navigate_via_category_sidebar_menu,
    "_validate_multistep_navigation_home_to_product_to_cart": _validate_multistep_navigation_home_to_product_to_cart,
    "_validate_filter_homepage_feed_by_category": _validate_filter_homepage_feed_by_category,
    # Search Tasks
    "_validate_search_吉普衬衫": _validate_search_吉普衬衫,
    "_validate_find_a_product_using_search_from_homepage": _validate_find_a_product_using_search_from_homepage,
    "_validate_search_a_product_from_another_product_page": _validate_search_a_product_from_another_product_page,
    "_validate_search_using_multiterm_query": _validate_search_using_multiterm_query,
    "_validate_search_from_search_history": _validate_search_from_search_history,
    "_validate_search_using_suggestion_dropdown": _validate_search_using_suggestion_dropdown,
    "_validate_search_for_apple_iphone": _validate_search_for_apple_iphone,
    "_validate_search_for_华丰方便面": _validate_search_for_华丰方便面,
    "_validate_search_for_奥克斯按摩椅": _validate_search_for_奥克斯按摩椅,
    "_validate_search_for_爱仕达炒锅": _validate_search_for_爱仕达炒锅,
    "_validate_search_for_活力_28_洗衣液": _validate_search_for_活力_28_洗衣液,
    "_validate_search_and_navigate_to_product_detail": _validate_search_and_navigate_to_product_detail,
    # Filter & Sort Tasks
    "_validate_apply_price_range_filter": _validate_apply_price_range_filter,
    "_validate_apply_brand_filter_single_brand": _validate_apply_brand_filter_single_brand,
    "_validate_apply_brand_filter_multiple_brands": _validate_apply_brand_filter_multiple_brands,
    "_validate_apply_multiple_filters_price_and_brand": _validate_apply_multiple_filters_price_and_brand,
    "_validate_clear_price_filter": _validate_clear_price_filter,
    "_validate_clear_brand_filter": _validate_clear_brand_filter,
    "_validate_filter_and_navigate_to_product": _validate_filter_and_navigate_to_product,
    "_validate_sort_by_price_ascending": _validate_sort_by_price_ascending,
    "_validate_sort_by_price_descending": _validate_sort_by_price_descending,
    "_validate_sort_by_sales": _validate_sort_by_sales,
    # Cart Tasks
    "_validate_add_a_product_to_cart": _validate_add_a_product_to_cart,
    "_validate_add_a_product_from_search_result_to_cart": _validate_add_a_product_from_search_result_to_cart,
    "_validate_add_an_item_from_the_homepage": _validate_add_an_item_from_the_homepage,
    "_validate_add_an_item_with_3_quantity": _validate_add_an_item_with_3_quantity,
    "_validate_add_product_with_specific_variant_to_cart": _validate_add_product_with_specific_variant_to_cart,
    "_validate_select_variant_and_add_to_cart": _validate_select_variant_and_add_to_cart,
    "_validate_remove_one_item_from_cart": _validate_remove_one_item_from_cart,
    "_validate_remove_multiple_items_in_the_cart": _validate_remove_multiple_items_in_the_cart,
    "_validate_reduce_an_item_quantity_in_the_cart": _validate_reduce_an_item_quantity_in_the_cart,
    "_validate_increase_an_item_and_reduce_another_item": _validate_increase_an_item_and_reduce_another_item,
    "_validate_search_and_add_two_items_to_cart": _validate_search_and_add_two_items_to_cart,
    "_validate_search_and_add_item_to_cart_and_back_to_home": _validate_search_and_add_item_to_cart_and_back_to_home,
    "_validate_remove_item_from_cart_then_search_and_add_item": _validate_remove_item_from_cart_then_search_and_add_item,
    "_validate_use_homepage_to_navigate_and_add_items": _validate_use_homepage_to_navigate_and_add_items,
}


__all__ = [
    "REWARD_FUNCTIONS_JD_V2",
    "ValidateTask",
    "StateKey",
    "StateKeyQuery",
]
