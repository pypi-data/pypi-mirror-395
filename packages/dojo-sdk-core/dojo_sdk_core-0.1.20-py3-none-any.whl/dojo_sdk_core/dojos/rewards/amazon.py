"""
Reward functions for Amazon app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_entering_pod_in_the_search_bar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully entered "pod" in the search bar and navigated to search results.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "pod"
    3. The filteredProducts contains a product with id "B09G9FPHY6"

    Args:
        initial_state: The initial state before the search
        final_state: The final state after the search

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "pod"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "pod":
            return (
                0.0,
                f"Expected searchQuery to be 'pod', got '{search_query}'",
            )

        # Check 3: filteredProducts should contain product with id "B09G9FPHY6"
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        product_found = any(product.get("id") == "B09G9FPHY6" for product in filtered_products)

        if not product_found:
            return (
                0.0,
                f"Product with id 'B09G9FPHY6' not found in filteredProducts. Found {len(filtered_products)} products.",
            )

        # All checks passed
        return 1.0, "Successfully entered 'pod' in search bar and navigated to search results"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_products_based_on_prime_delivery(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products based on "Ships from United States" filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has shipsFromUnitedStates: true, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains all expected product IDs

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("shipsFromUnitedStates") is not True:
            errors.append("shipsFromUnitedStates should be True")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B08N5WRWNW",
            "B09G9FPHY6",
            "B0BSHF7WHW",
            "B08L5VNJ2P",
            "B0B2QJZF8D",
            "CLOTH001",
            "CLOTH002",
            "ACC001",
            "BOOK001",
            "BEAUTY001",
            "SPORTS001",
            "PET001",
            "GARDEN001",
            "HEALTH001",
            "OFFICE001",
            "CLOTH003",
            "GROCERY001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))[:10]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products based on 'Ships from United States'. Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_products_based_on_single_day_delivery(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products based on "Get it within two days" filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has deliveryTomorrow: true, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains products with ids: B09G9FPHY6, HEALTH001

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("deliveryTomorrow") is not True:
            errors.append("deliveryTomorrow should be True")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B09G9FPHY6",
            "HEALTH001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products based on 'Get it within two days'. Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_products_on_two_day_delivery(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products based on "Get it within two days" filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has deliveryTwoDays: true, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains products with ids: B09G9FPHY6, HEALTH001

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("deliveryTwoDays") is not True:
            errors.append("deliveryTwoDays should be True")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B09G9FPHY6",
            "HEALTH001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products based on 'Get it within two days'. Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_products_on_free_delivery(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products based on "Free delivery" filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has freeDelivery: true, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains all expected product IDs

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("freeDelivery") is not True:
            errors.append("freeDelivery should be True")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B08N5WRWNW",
            "B09G9FPHY6",
            "B0BSHF7WHW",
            "B08L5VNJ2P",
            "B0B2QJZF8D",
            "CLOTH001",
            "CLOTH002",
            "BOOK001",
            "BEAUTY001",
            "SPORTS001",
            "PET001",
            "GARDEN001",
            "HEALTH001",
            "OFFICE001",
            "CLOTH003",
            "GROCERY001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))[:10]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products based on 'Free delivery'. Found {len(filtered_products)} matching products.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_customer_reviews_that_have_5_stars(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products based on "Top Rated" (5 stars) filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has minRating: 5, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains product with id: B0BSHF7WHW

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("minRating") != 5:
            errors.append(f"minRating should be 5, got {filters.get('minRating')}")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product ID
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product ID
        expected_product_id = "B0BSHF7WHW"

        # Check if the expected product is present
        product_found = any(product.get("id") == expected_product_id for product in filtered_products)

        if not product_found:
            return (
                0.0,
                f"Product with id '{expected_product_id}' not found in filteredProducts. Found {len(filtered_products)} products.",  # noqa: E501
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products based on 'Top Rated' (5 stars). Found {len(filtered_products)} matching products.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_customer_reviews_that_have_4_stars_and_above(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products based on "4 & Up" (4 stars and above) filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has minRating: 4, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains all expected product IDs

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("minRating") != 4:
            errors.append(f"minRating should be 4, got {filters.get('minRating')}")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B09G9FPHY6",
            "B0BSHF7WHW",
            "B09B9VFKH5",
            "B08L5VNJ2P",
            "B0B2QJZF8D",
            "CLOTH001",
            "CLOTH002",
            "ACC001",
            "BOOK001",
            "BEAUTY001",
            "SPORTS001",
            "PET001",
            "GARDEN001",
            "HEALTH001",
            "OFFICE001",
            "CLOTH003",
            "GROCERY001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))[:10]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products based on '4 & Up' (4 stars and above). Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_products_with_prices_between_99_and_204(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using price range slider (99-204).

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has minPrice: 99, maxPrice: 204, condition: [],
       and all other keys set to false
    4. The filteredProducts contains all expected product IDs

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("minPrice") != 99:
            errors.append(f"minPrice should be 99, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 204:
            errors.append(f"maxPrice should be 204, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B0BSHF7WHW",
            "B08L5VNJ2P",
            "CLOTH001",
            "CLOTH002",
            "HEALTH001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using price range slider (99-204). Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_products_prices_between_150_and_300(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using price range button ($150 to $350).

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has minPrice: 150, maxPrice: 300, condition: [],
       and all other keys set to false
    4. The filteredProducts contains all expected product IDs

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("minPrice") != 150:
            errors.append(f"minPrice should be 150, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 300:
            errors.append(f"maxPrice should be 300, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B08L5VNJ2P",
            "CLOTH002",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using price range button ($150 to $350). Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_product_prices_up_to_90(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using "Up to $90" price filter button.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has minPrice: 0, maxPrice: 90, condition: [],
       and all other keys set to false
    4. The filteredProducts contains expected product ids

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 90:
            errors.append(f"maxPrice should be 90, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = [
            "B0B2QJZF8D",
            "BOOK001",
            "BEAUTY001",
            "SPORTS001",
            "PET001",
            "GARDEN001",
            "OFFICE001",
            "CLOTH003",
            "GROCERY001",
        ]

        # Get actual product IDs
        actual_product_ids = [product.get("id") for product in filtered_products]

        # Check if all expected products are present
        missing_products = [pid for pid in expected_product_ids if pid not in actual_product_ids]

        if missing_products:
            return (
                0.0,
                f"Missing expected products: {missing_products}. Found {len(filtered_products)} products: {actual_product_ids}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using 'Up to $90' price filter. Found {len(filtered_products)} matching products.",
        )

    except Exception as e:
        logger.error(f"Error in reward function: {str(e)}", exc_info=True)
        return 0.0, f"Error evaluating task: {str(e)}"


def _validate_products_with_prices_greater_than_700(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using "$700 and above" price filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has minPrice: 700, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains product with id: B09B9VFKH5

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("minPrice") != 700:
            errors.append(f"minPrice should be 700, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product ID
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product ID
        expected_product_id = "B09B9VFKH5"

        # Check if the expected product is present
        product_found = any(product.get("id") == expected_product_id for product in filtered_products)

        if not product_found:
            return (
                0.0,
                f"Product with id '{expected_product_id}' not found in filteredProducts. Found {len(filtered_products)} products.",  # noqa: E501
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using '$700 and above' price filter. Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_on_products_condition_new(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using "New" condition filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has condition: ['new'], minPrice: 0, maxPrice: 1000000,
       and all other keys set to false
    4. The filteredProducts contains all expected product IDs

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        condition = filters.get("condition", [])
        if not isinstance(condition, list) or condition != ["new"]:
            errors.append(f"condition should be ['new'], got {condition}")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain expected product IDs
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Expected product IDs
        expected_product_ids = {
            "B08N5WRWNW",
            "B09G9FPHY6",
            "B0BSHF7WHW",
            "B09B9VFKH5",
            "B08L5VNJ2P",
            "B0B2QJZF8D",
            "CLOTH001",
            "CLOTH002",
            "ACC001",
            "BOOK001",
            "BEAUTY001",
            "SPORTS001",
            "PET001",
            "GARDEN001",
            "HEALTH001",
            "OFFICE001",
            "CLOTH003",
            "GROCERY001",
        }

        # Extract product IDs from filtered products
        actual_ids = {product.get("id") for product in filtered_products if product.get("id")}

        # Check if all expected products are present
        missing_ids = expected_product_ids - actual_ids

        if missing_ids:
            return (
                0.0,
                f"Missing {len(missing_ids)} expected products: {sorted(list(missing_ids))[:10]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using 'New' condition filter. Found {len(filtered_products)} matching products.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_on_product_condition_renewed(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using "Renewed" condition filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has condition: ['renewed'], minPrice: 0, maxPrice: 1000000,
       and all other keys set to false
    4. The filteredProducts contains objects that have condition 'renewed'

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        condition = filters.get("condition", [])
        if not isinstance(condition, list) or condition != ["renewed"]:
            errors.append(f"condition should be ['renewed'], got {condition}")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain objects with condition 'renewed'
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Check that all products have condition 'renewed'
        products_without_renewed = [
            product.get("id", "unknown") for product in filtered_products if product.get("condition") != "renewed"
        ]

        if products_without_renewed:
            return (
                0.0,
                f"Found {len(products_without_renewed)} products without condition 'renewed': {products_without_renewed[:5]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using 'Renewed' condition filter. Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_on_products_condition_used(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using "Used" condition filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has condition: ['used'], minPrice: 0, maxPrice: 1000000,
       and all other keys set to false
    4. The filteredProducts contains objects that have condition 'used'

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        condition = filters.get("condition", [])
        if not isinstance(condition, list) or condition != ["used"]:
            errors.append(f"condition should be ['used'], got {condition}")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain objects with condition 'used'
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Check that all products have condition 'used'
        products_without_used = [
            product.get("id", "unknown") for product in filtered_products if product.get("condition") != "used"
        ]

        if products_without_used:
            return (
                0.0,
                f"Found {len(products_without_used)} products without condition 'used': {products_without_used[:5]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using 'Used' condition filter. Found {len(filtered_products)} matching products.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_on_include_out_of_stock(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully enabled "Include Out of Stock" filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has includeOutOfStock: true, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains objects that have inStock key (can be True or False)

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("includeOutOfStock") is not True:
            errors.append("includeOutOfStock should be True")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "isGlobalStore",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain objects with inStock key
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Check that all products have inStock key (can be True or False)
        products_without_inStock = [product.get("id", "unknown") for product in filtered_products if "inStock" not in product]

        if products_without_inStock:
            return (
                0.0,
                f"Found {len(products_without_inStock)} products without 'inStock' key: {products_without_inStock[:5]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully enabled 'Include Out of Stock' filter. Found {len(filtered_products)} matching products.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_filter_on_amazon_global_store(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered products using "Amazon Global Store" filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has isGlobalStore: true, minPrice: 0, maxPrice: 1000000, condition: [],
       and all other keys set to false
    4. The filteredProducts contains objects that have isGlobalStore: True

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("isGlobalStore") is not True:
            errors.append("isGlobalStore should be True")

        if filters.get("minPrice") != 0:
            errors.append(f"minPrice should be 0, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 1000000:
            errors.append(f"maxPrice should be 1000000, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "shipsFromUnitedStates",
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "freeDelivery",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        # Check minRating should be null
        if filters.get("minRating") is not None:
            errors.append(f"minRating should be null, got {filters.get('minRating')}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts contain objects with isGlobalStore: True
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Check that all products have isGlobalStore: True
        products_without_global_store = [
            product.get("id", "unknown") for product in filtered_products if product.get("isGlobalStore") is not True
        ]

        if products_without_global_store:
            return (
                0.0,
                f"Found {len(products_without_global_store)} products without isGlobalStore=True: {products_without_global_store[:5]}",  # noqa: E501
            )

        # All checks passed
        return (
            1.0,
            f"Successfully filtered products using 'Amazon Global Store' filter. Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_multiple_filters(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully applied multiple filters simultaneously.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "a"
    3. The filters object has shipsFromUnitedStates: true, freeDelivery: true, minRating: 4,
       minPrice: 90, maxPrice: 150, condition: [], and all other keys set to false
    4. The filteredProducts contains objects that match all filter criteria

    Args:
        initial_state: The initial state before filtering
        final_state: The final state after filtering

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "a"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "a":
            return (
                0.0,
                f"Expected searchQuery to be 'a', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        errors = []

        # Check required filter values
        if filters.get("shipsFromUnitedStates") is not True:
            errors.append("shipsFromUnitedStates should be True")

        if filters.get("freeDelivery") is not True:
            errors.append("freeDelivery should be True")

        if filters.get("minRating") != 4:
            errors.append(f"minRating should be 4, got {filters.get('minRating')}")

        if filters.get("minPrice") != 90:
            errors.append(f"minPrice should be 90, got {filters.get('minPrice')}")

        if filters.get("maxPrice") != 150:
            errors.append(f"maxPrice should be 150, got {filters.get('maxPrice')}")

        condition = filters.get("condition", [])
        if not isinstance(condition, list) or len(condition) != 0:
            errors.append(f"condition should be empty array [], got {condition}")

        # Check that all other boolean filters are False
        boolean_filters_should_be_false = [
            "internationalShipping",
            "deliveryTomorrow",
            "deliveryTwoDays",
            "isGlobalStore",
            "includeOutOfStock",
        ]

        for filter_key in boolean_filters_should_be_false:
            if filters.get(filter_key) is not False:
                errors.append(f"{filter_key} should be False, got {filters.get(filter_key)}")

        if errors:
            return 0.0, "; ".join(errors)

        # Check 4: Validate filteredProducts match all filter criteria
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        # Validate each product matches all criteria
        invalid_products = []

        for product in filtered_products:
            product_id = product.get("id", "unknown")
            product_errors = []

            # Check shipsFromUnitedStates
            if product.get("shipsFromUnitedStates") is not True:
                product_errors.append("shipsFromUnitedStates != True")

            # Check rating >= 4
            rating = product.get("rating")
            if rating is None or rating < 4:
                product_errors.append(f"rating={rating} (expected >= 4)")

            # Check price between 90 and 150 (inclusive)
            price = product.get("price")
            if price is None or price < 90 or price > 150:
                product_errors.append(f"price={price} (expected 90 <= price <= 150)")

            # Check freeDelivery
            if product.get("freeDelivery") is not True:
                product_errors.append("freeDelivery != True")

            if product_errors:
                invalid_products.append(f"{product_id}: {', '.join(product_errors)}")

        if invalid_products:
            return (
                0.0,
                f"Found {len(invalid_products)} products that don't match all filter criteria: {invalid_products[:3]}",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully applied multiple filters (Ships from United States, Free Delivery, 4* & Up, $90-$150). Found {len(filtered_products)} matching products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_from_search_page_to_product_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from search page to a product page.

    This function checks:
    1. The currentPage is "product"
    2. The selectedProduct has id "OFFICE001"
    3. The searchQuery is "book" (preserved from search page)

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: selectedProduct should have id "OFFICE001"
        selected_product = final_state.get("selectedProduct")
        if selected_product is None:
            return 0.0, "Expected selectedProduct to be set, got null"

        product_id = selected_product.get("id")
        if product_id != "OFFICE001":
            return (
                0.0,
                f"Expected selectedProduct id to be 'OFFICE001', got '{product_id}'",
            )

        # Check 3: searchQuery should be "book" (preserved from search page)
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "book":
            return (
                0.0,
                f"Expected searchQuery to be 'book', got '{search_query}'",
            )

        # All checks passed
        product_name = selected_product.get("name", "Unknown Product")
        return (
            1.0,
            f"Successfully navigated from search page to product page for '{product_name}' (ID: {product_id})",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_from_home_to_product_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from home page to a product page.

    This function checks:
    1. The currentPage is "product"
    2. The selectedProduct has id "CLOTH002"
    3. The searchQuery is empty string "" (since navigation is from home page)

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: selectedProduct should have id "CLOTH002"
        selected_product = final_state.get("selectedProduct")
        if selected_product is None:
            return 0.0, "Expected selectedProduct to be set, got null"

        product_id = selected_product.get("id")
        if product_id != "CLOTH002":
            return (
                0.0,
                f"Expected selectedProduct id to be 'CLOTH002', got '{product_id}'",
            )

        # Check 3: searchQuery should be empty string (from home page)
        search_query = final_state.get("searchQuery", "")
        if search_query != "":
            return (
                0.0,
                f"Expected searchQuery to be empty string '', got '{search_query}'",
            )

        # All checks passed
        product_name = selected_product.get("name", "Unknown Product")
        return (
            1.0,
            f"Successfully navigated from home page to product page for '{product_name}' (ID: {product_id})",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_from_product_page_to_product_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from one product page to another product page.

    This function checks:
    1. The currentPage is "product"
    2. The selectedProduct has id "B08N5WRWNW"
    3. The searchQuery is empty string "" (since navigation is from product page)

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: selectedProduct should have id "B08N5WRWNW"
        selected_product = final_state.get("selectedProduct")
        if selected_product is None:
            return 0.0, "Expected selectedProduct to be set, got null"

        product_id = selected_product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected selectedProduct id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 3: searchQuery should be empty string (from product page)
        search_query = final_state.get("searchQuery", "")
        if search_query != "":
            return (
                0.0,
                f"Expected searchQuery to be empty string '', got '{search_query}'",
            )

        # All checks passed
        product_name = selected_product.get("name", "Unknown Product")
        return (
            1.0,
            f"Successfully navigated from product page to product page for '{product_name}' (ID: {product_id})",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_from_product_page_to_search_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from product page to search page.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "seven" (case-insensitive)
    3. The filteredProducts contains a product with id "BOOK001"

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "seven" (case-insensitive)
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "seven":
            return (
                0.0,
                f"Expected searchQuery to be 'seven', got '{search_query}'",
            )

        # Check 3: filteredProducts should contain product with id "BOOK001"
        filtered_products = final_state.get("filteredProducts", [])
        if not filtered_products:
            return 0.0, "No filtered products found in final state"

        product_found = any(product.get("id") == "BOOK001" for product in filtered_products)

        if not product_found:
            return (
                0.0,
                f"Product with id 'BOOK001' not found in filteredProducts. Found {len(filtered_products)} products.",
            )

        # All checks passed
        return (
            1.0,
            f"Successfully navigated from product page to search page with query 'seven'. Found {len(filtered_products)} products.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_add_an_item_to_the_cart(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully added an item to the cart.

    This function checks:
    1. The currentUser.cart length should be 1
    2. The product in the cart should have the id of 'B08N5WRWNW'
    3. The quantity should be 1

    Args:
        initial_state: The initial state before adding to cart
        final_state: The final state after adding to cart

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 2: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 3: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 4: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        # Check 5: product id should be 'B08N5WRWNW'
        product_id = product.get("id") if isinstance(product, dict) else None
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 6: quantity should be 1
        quantity = cart_item.get("quantity")
        if quantity != 1:
            return (
                0.0,
                f"Expected quantity to be 1, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully added product 'B08N5WRWNW' to cart with quantity 1",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_add_different_items_to_cart(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully added different items to the cart.

    This function checks:
    1. The currentPage is "product"
    2. The currentUser.cart length should be 2
    3. The cart should contain products with ids: B0BSHF7WHW, B08N5WRWNW
    4. Each product should have a quantity of 1

    Args:
        initial_state: The initial state before adding items to cart
        final_state: The final state after adding items to cart

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 2
        if len(cart) != 2:
            return (
                0.0,
                f"Expected cart length to be 2, got {len(cart)}",
            )

        # Check 5: Extract product IDs and quantities from cart
        product_ids = []
        quantities = []
        for cart_item in cart:
            if not isinstance(cart_item, dict):
                return 0.0, f"cart item should be a dict, got {type(cart_item)}"

            product = cart_item.get("product")
            if product is None:
                return 0.0, "cart item should have a 'product' field"

            if not isinstance(product, dict):
                return 0.0, f"product should be a dict, got {type(product)}"

            product_id = product.get("id")
            if product_id is None:
                return 0.0, "product should have an 'id' field"

            quantity = cart_item.get("quantity")
            if quantity is None:
                return 0.0, "cart item should have a 'quantity' field"

            product_ids.append(product_id)
            quantities.append(quantity)

        # Check 6: Cart should contain both expected product IDs
        expected_product_ids = {"B0BSHF7WHW", "B08N5WRWNW"}
        actual_product_ids = set(product_ids)

        missing_ids = expected_product_ids - actual_product_ids
        if missing_ids:
            return (
                0.0,
                f"Missing expected product IDs in cart: {sorted(list(missing_ids))}. Found: {sorted(list(actual_product_ids))}",
            )

        # Check 7: Each product should have quantity of 1
        for i, quantity in enumerate(quantities):
            if quantity != 1:
                return (
                    0.0,
                    f"Expected all products to have quantity 1, but product '{product_ids[i]}' has quantity {quantity}",
                )

        # All checks passed
        return (
            1.0,
            f"Successfully added different items to cart. Cart contains products {sorted(list(actual_product_ids))} with quantity 1 each.",  # noqa: E501
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_add_product_from_cart_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully increased the quantity of a product from the cart page.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 2

    Args:
        initial_state: The initial state before increasing quantity
        final_state: The final state after increasing quantity

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 2
        quantity = cart_item.get("quantity")
        if quantity != 2:
            return (
                0.0,
                f"Expected quantity to be 2, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully increased quantity of product 'B08N5WRWNW' to 2 from cart page",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_add_quantity_5_of_a_product(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully added a product with quantity 5 to the cart.

    This function checks:
    1. The currentPage is "product"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 5

    Args:
        initial_state: The initial state before adding to cart
        final_state: The final state after adding to cart

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 5
        quantity = cart_item.get("quantity")
        if quantity != 5:
            return (
                0.0,
                f"Expected quantity to be 5, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully added product 'B08N5WRWNW' to cart with quantity 5",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_buy_now_a_product_with_quantity_1(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully clicked Buy Now and navigated to cart page.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 1

    Args:
        initial_state: The initial state before clicking Buy Now
        final_state: The final state after clicking Buy Now

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 1
        quantity = cart_item.get("quantity")
        if quantity != 1:
            return (
                0.0,
                f"Expected quantity to be 1, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully clicked Buy Now and navigated to cart page. Product 'B08N5WRWNW' added with quantity 1",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_buy_now_quantity_5(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully changed quantity to 5 and clicked Buy Now.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 5

    Args:
        initial_state: The initial state before clicking Buy Now
        final_state: The final state after clicking Buy Now

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 5
        quantity = cart_item.get("quantity")
        if quantity != 5:
            return (
                0.0,
                f"Expected quantity to be 5, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully changed quantity to 5 and clicked Buy Now. Product 'B08N5WRWNW' added to cart with quantity 5",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_delete_product_from_cart_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully deleted a product from the cart page.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 0 (empty cart)

    Args:
        initial_state: The initial state before deleting from cart
        final_state: The final state after deleting from cart

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 0 (empty)
        if len(cart) != 0:
            return (
                0.0,
                f"Expected cart length to be 0 (empty), got {len(cart)}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully deleted product from cart page. Cart is now empty.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_delete_product_from_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully deleted a product from the cart sidebar.

    This function checks:
    1. The currentPage is "product"
    2. The currentUser.cart length should be 0

    Args:
        initial_state: The initial state before deleting from cart sidebar
        final_state: The final state after deleting from cart sidebar

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 0:
            return (
                0.0,
                f"Expected cart length to be 0, got {len(cart)}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully deleted product from cart sidebar. Cart now has 0 item remaining.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_increase_quantity_from_cart_sidebar(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully increased the quantity of a product from the cart sidebar.

    This function checks:
    1. The currentPage is "product"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 2

    Args:
        initial_state: The initial state before increasing quantity
        final_state: The final state after increasing quantity

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 1
        quantity = cart_item.get("quantity")
        if quantity != 2:
            return (
                0.0,
                f"Expected quantity to be 2, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully increased quantity from cart sidebar. Product 'B08N5WRWNW' has quantity 2",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_to_account_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the account page.

    This function checks:
    1. The currentPage is "account"

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "account"
        current_page = final_state.get("currentPage")
        if current_page != "account":
            return (
                0.0,
                f"Expected currentPage to be 'account', got '{current_page}'",
            )

        # All checks passed
        return (
            1.0,
            "Successfully navigated to account page",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_to_cart_page_from_cart_sidebar(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the cart page from the cart sidebar.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # All checks passed
        return (
            1.0,
            "Successfully navigated to cart page from cart sidebar. Cart contains product 'B08N5WRWNW'",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_to_cart_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the cart page.

    This function checks:
    1. The currentPage is "cart"

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # All checks passed
        return (
            1.0,
            "Successfully navigated to cart page",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_navigate_to_language_selection_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the language selection page.

    This function checks:
    1. The currentPage is "language"

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "language"
        current_page = final_state.get("currentPage")
        if current_page != "language":
            return (
                0.0,
                f"Expected currentPage to be 'language', got '{current_page}'",
            )

        # All checks passed
        return (
            1.0,
            "Successfully navigated to language selection page",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_reduce_quantity_of_item_on_cart_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully reduced the quantity of an item on the cart page.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 1

    Args:
        initial_state: The initial state before reducing quantity
        final_state: The final state after reducing quantity

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 1
        quantity = cart_item.get("quantity")
        if quantity != 1:
            return (
                0.0,
                f"Expected quantity to be 1, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully reduced quantity of product 'B08N5WRWNW' to 1 on cart page",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_reduce_quantity_of_item_to_zero(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully reduced the quantity of an item to zero, removing it from the cart.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 0 (empty cart)

    Args:
        initial_state: The initial state before reducing quantity to zero
        final_state: The final state after reducing quantity to zero

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 0 (empty)
        if len(cart) != 0:
            return (
                0.0,
                f"Expected cart length to be 0 (empty), got {len(cart)}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully reduced quantity of item to zero. Cart is now empty.",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_reduce_quantity_of_product_from_cart_sidebar(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully reduced the quantity of a product from the cart sidebar.

    This function checks:
    1. The currentPage is "product"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'B08N5WRWNW'
    4. The product should have a quantity of 2

    Args:
        initial_state: The initial state before reducing quantity
        final_state: The final state after reducing quantity

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "product"
        current_page = final_state.get("currentPage")
        if current_page != "product":
            return (
                0.0,
                f"Expected currentPage to be 'product', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product and quantity
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'B08N5WRWNW'
        product_id = product.get("id")
        if product_id != "B08N5WRWNW":
            return (
                0.0,
                f"Expected product id to be 'B08N5WRWNW', got '{product_id}'",
            )

        # Check 7: quantity should be 2
        quantity = cart_item.get("quantity")
        if quantity != 2:
            return (
                0.0,
                f"Expected quantity to be 2, got {quantity}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully reduced quantity of product 'B08N5WRWNW' to 2 from cart sidebar",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_search_with_changed_department(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully searched with a changed department.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "e"
    3. The filters department should be "Women's Fashion"
    4. The filteredProducts should have a length of 1
    5. The product should have id "CLOTH003"

    Args:
        initial_state: The initial state before searching
        final_state: The final state after searching

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "e"
        search_query = final_state.get("searchQuery", "")
        if search_query.lower() != "e":
            return (
                0.0,
                f"Expected searchQuery to be 'e', got '{search_query}'",
            )

        # Check 3: Validate filters object
        filters = final_state.get("filters", {})
        if not filters:
            return 0.0, "No filters found in final state"

        # Check 4: department should be "Women's Fashion"
        department = filters.get("department", "")
        if department != "Women's Fashion":
            return (
                0.0,
                f"Expected department to be 'Women's Fashion', got '{department}'",
            )

        # Check 5: filteredProducts should exist and be an array
        filtered_products = final_state.get("filteredProducts", [])
        if not isinstance(filtered_products, list):
            return 0.0, f"filteredProducts should be a list, got {type(filtered_products)}"

        # Check 6: filteredProducts length should be 1
        if len(filtered_products) != 1:
            return (
                0.0,
                f"Expected filteredProducts length to be 1, got {len(filtered_products)}",
            )

        # Check 7: product should have id "CLOTH003"
        product = filtered_products[0]
        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        product_id = product.get("id")
        if product_id != "CLOTH003":
            return (
                0.0,
                f"Expected product id to be 'CLOTH003', got '{product_id}'",
            )

        # All checks passed
        return (
            1.0,
            "Successfully searched with changed department 'Women's Fashion'. Found product 'CLOTH003'",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_deselect_product(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully deselected a product in the cart.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'CLOTH002'
    4. The product should have selected set to false

    Args:
        initial_state: The initial state before deselecting
        final_state: The final state after deselecting

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'CLOTH002'
        product_id = product.get("id")
        if product_id != "CLOTH002":
            return (
                0.0,
                f"Expected product id to be 'CLOTH002', got '{product_id}'",
            )

        # Check 7: selected should be false
        selected = cart_item.get("selected")
        if selected is not False:
            return (
                0.0,
                f"Expected selected to be False, got {selected}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully deselected product 'CLOTH002' in cart",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_open_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully opened the sidebar.

    This function checks:
    1. The sidebarVisible should be true

    Args:
        initial_state: The initial state before opening sidebar
        final_state: The final state after opening sidebar

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: sidebarVisible should be true
        sidebar_visible = final_state.get("sidebarVisible")
        if sidebar_visible is not True:
            return (
                0.0,
                f"Expected sidebarVisible to be True, got {sidebar_visible}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully opened sidebar",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_select_a_product(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully selected a product in the cart.

    This function checks:
    1. The currentPage is "cart"
    2. The currentUser.cart length should be 1
    3. The cart should contain a product with id 'CLOTH002'
    4. The product should have selected set to true

    Args:
        initial_state: The initial state before selecting
        final_state: The final state after selecting

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "cart"
        current_page = final_state.get("currentPage")
        if current_page != "cart":
            return (
                0.0,
                f"Expected currentPage to be 'cart', got '{current_page}'",
            )

        # Check 2: currentUser should exist
        current_user = final_state.get("currentUser")
        if current_user is None:
            return 0.0, "currentUser not found in final state"

        # Check 3: cart should exist and be an array
        cart = current_user.get("cart", [])
        if not isinstance(cart, list):
            return 0.0, f"cart should be a list, got {type(cart)}"

        # Check 4: cart length should be 1
        if len(cart) != 1:
            return (
                0.0,
                f"Expected cart length to be 1, got {len(cart)}",
            )

        # Check 5: cart item should have product
        cart_item = cart[0]
        if not isinstance(cart_item, dict):
            return 0.0, f"cart item should be a dict, got {type(cart_item)}"

        product = cart_item.get("product")
        if product is None:
            return 0.0, "cart item should have a 'product' field"

        if not isinstance(product, dict):
            return 0.0, f"product should be a dict, got {type(product)}"

        # Check 6: product id should be 'CLOTH002'
        product_id = product.get("id")
        if product_id != "CLOTH002":
            return (
                0.0,
                f"Expected product id to be 'CLOTH002', got '{product_id}'",
            )

        # Check 7: selected should be true
        selected = cart_item.get("selected")
        if selected is not True:
            return (
                0.0,
                f"Expected selected to be True, got {selected}",
            )

        # All checks passed
        return (
            1.0,
            "Successfully selected product 'CLOTH002' in cart",
        )

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


# Registry of all Amazon reward functions
REWARD_FUNCTIONS_AMAZON = {
    "_validate_entering_pod_in_the_search_bar": _validate_entering_pod_in_the_search_bar,
    "_validate_filter_products_based_on_prime_delivery": _validate_filter_products_based_on_prime_delivery,
    "_validate_filter_products_based_on_single_day_delivery": _validate_filter_products_based_on_single_day_delivery,
    "_validate_filter_products_on_two_day_delivery": _validate_filter_products_on_two_day_delivery,
    "_validate_filter_products_on_free_delivery": _validate_filter_products_on_free_delivery,
    "_validate_customer_reviews_that_have_5_stars": _validate_customer_reviews_that_have_5_stars,
    "_validate_customer_reviews_that_have_4_stars_and_above": _validate_customer_reviews_that_have_4_stars_and_above,
    "_validate_filter_products_with_prices_between_99_and_204": _validate_filter_products_with_prices_between_99_and_204,
    "_validate_product_prices_up_to_90": _validate_product_prices_up_to_90,
    "_validate_products_prices_between_150_and_300": _validate_products_prices_between_150_and_300,
    "_validate_products_with_prices_greater_than_700": _validate_products_with_prices_greater_than_700,
    "_validate_filter_on_products_condition_new": _validate_filter_on_products_condition_new,
    "_validate_filter_on_product_condition_renewed": _validate_filter_on_product_condition_renewed,
    "_validate_filter_on_products_condition_used": _validate_filter_on_products_condition_used,
    "_validate_filter_on_include_out_of_stock": _validate_filter_on_include_out_of_stock,
    "_validate_filter_on_amazon_global_store": _validate_filter_on_amazon_global_store,
    "_validate_multiple_filters": _validate_multiple_filters,
    "_validate_navigate_from_search_page_to_product_page": _validate_navigate_from_search_page_to_product_page,
    "_validate_navigate_from_home_to_product_page": _validate_navigate_from_home_to_product_page,
    "_validate_navigate_from_product_page_to_product_page": _validate_navigate_from_product_page_to_product_page,
    "_validate_navigate_from_product_page_to_search_page": _validate_navigate_from_product_page_to_search_page,
    "_validate_add_an_item_to_the_cart": _validate_add_an_item_to_the_cart,
    "_validate_add_different_items_to_cart": _validate_add_different_items_to_cart,
    "_validate_add_product_from_cart_page": _validate_add_product_from_cart_page,
    "_validate_add_quantity_5_of_a_product": _validate_add_quantity_5_of_a_product,
    "_validate_buy_now_a_product_with_quantity_1": _validate_buy_now_a_product_with_quantity_1,
    "_validate_buy_now_quantity_5": _validate_buy_now_quantity_5,
    "_validate_delete_product_from_cart_page": _validate_delete_product_from_cart_page,
    "_validate_delete_product_from_sidebar": _validate_delete_product_from_sidebar,
    "_validate_increase_quantity_from_cart_sidebar": _validate_increase_quantity_from_cart_sidebar,
    "_validate_navigate_to_account_page": _validate_navigate_to_account_page,
    "_validate_navigate_to_cart_page_from_cart_sidebar": _validate_navigate_to_cart_page_from_cart_sidebar,
    "_validate_navigate_to_cart_page": _validate_navigate_to_cart_page,
    "_validate_navigate_to_language_selection_page": _validate_navigate_to_language_selection_page,
    "_validate_reduce_quantity_of_item_on_cart_page": _validate_reduce_quantity_of_item_on_cart_page,
    "_validate_reduce_quantity_of_item_to_zero": _validate_reduce_quantity_of_item_to_zero,
    "_validate_reduce_quantity_of_product_from_cart_sidebar": _validate_reduce_quantity_of_product_from_cart_sidebar,
    "_validate_search_with_changed_department": _validate_search_with_changed_department,
    "_validate_deselect_product": _validate_deselect_product,
    "_validate_open_sidebar": _validate_open_sidebar,
    "_validate_select_a_product": _validate_select_a_product,
}

__all__ = [
    "REWARD_FUNCTIONS_AMAZON",
    "_validate_entering_pod_in_the_search_bar",
    "_validate_filter_products_based_on_prime_delivery",
    "_validate_filter_products_based_on_single_day_delivery",
    "_validate_filter_products_on_two_day_delivery",
    "_validate_filter_products_on_free_delivery",
    "_validate_customer_reviews_that_have_5_stars",
    "_validate_customer_reviews_that_have_4_stars_and_above",
    "_validate_filter_products_with_prices_between_99_and_204",
    "_validate_product_prices_up_to_90",
    "_validate_products_prices_between_150_and_300",
    "_validate_products_with_prices_greater_than_700",
    "_validate_filter_on_products_condition_new",
    "_validate_filter_on_product_condition_renewed",
    "_validate_filter_on_products_condition_used",
    "_validate_filter_on_include_out_of_stock",
    "_validate_filter_on_amazon_global_store",
    "_validate_multiple_filters",
    "_validate_navigate_from_search_page_to_product_page",
    "_validate_navigate_from_home_to_product_page",
    "_validate_navigate_from_product_page_to_product_page",
    "_validate_navigate_from_product_page_to_search_page",
    "_validate_add_an_item_to_the_cart",
    "_validate_add_different_items_to_cart",
    "_validate_add_product_from_cart_page",
    "_validate_add_quantity_5_of_a_product",
    "_validate_buy_now_a_product_with_quantity_1",
    "_validate_buy_now_quantity_5",
    "_validate_delete_product_from_cart_page",
    "_validate_delete_product_from_sidebar",
    "_validate_increase_quantity_from_cart_sidebar",
    "_validate_navigate_to_account_page",
    "_validate_navigate_to_cart_page_from_cart_sidebar",
    "_validate_navigate_to_cart_page",
    "_validate_navigate_to_language_selection_page",
    "_validate_reduce_quantity_of_item_on_cart_page",
    "_validate_reduce_quantity_of_item_to_zero",
    "_validate_reduce_quantity_of_product_from_cart_sidebar",
    "_validate_search_with_changed_department",
    "_validate_deselect_product",
    "_validate_open_sidebar",
    "_validate_select_a_product",
]
