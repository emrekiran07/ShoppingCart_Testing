import pytest
from checkout_and_payment import load_products_from_csv, Product

@pytest.fixture
def csv_filename():
    # Calling the  CSV file for testing
    return 'products.csv'

def test_check_total_products(csv_filename):
    # Load products from the CSV file
    products = load_products_from_csv(csv_filename)

    # Verify the loaded products
    assert len(products) == 71 # Update with the correct number of products


def test_check_product_details(csv_filename):
    # Check the details of each product
    products = load_products_from_csv(csv_filename)

    # Check the details of each product
    for product in products:
        # Check the details of a specific product
        assert isinstance(product, Product)
        # More specific assertions based on your data and requirements
        assert isinstance(product.name, str)
        assert isinstance(product.price, float)
        assert isinstance(product.units, int)

# New 8 test functions

def test_check_product_prices(csv_filename):
    # Check that all product prices are positive floats
    products = load_products_from_csv(csv_filename)
    for product in products:
        assert isinstance(product.price, float) and product.price > 0


def test_check_product_units(csv_filename):
    # Check that all product units are non-negative integers
    products = load_products_from_csv(csv_filename)
    for product in products:
        assert isinstance(product.units, int) and product.units >= 0


def test_check_total_units_greater_than_zero(csv_filename):
    # Check that the sum of units for all products is greater than zero
    products = load_products_from_csv(csv_filename)
    total_units = sum(product.units for product in products)
    assert total_units > 0


def test_check_total_price_greater_than_zero(csv_filename):
    # Check that the sum of prices for all products is greater than zero
    products = load_products_from_csv(csv_filename)
    total_price = sum(product.price for product in products)
    assert total_price > 0


def test_check_product_availability(csv_filename):
    # Check that the availability (units) of each product is not negative
    products = load_products_from_csv(csv_filename)
    for product in products:
        assert product.units >= 0, f"Negative units found for product {product.name}"


def test_check_product_price_format(csv_filename):
    # Check that the price of each product is formatted with at most two decimal places
    products = load_products_from_csv(csv_filename)
    for product in products:
        assert str(product.price).count('.') <= 2, f"Invalid price format found for product {product.name}"


def test_check_product_price_range(csv_filename):
    # Check that the price of each product falls within a reasonable range
    products = load_products_from_csv(csv_filename)
    for product in products:
        assert 0 < product.price < 1000, f"Invalid price range found for product {product.name}"


def test_check_unique_product_entries(csv_filename):
    # Check that there are no duplicate entries for products
    products = load_products_from_csv(csv_filename)

    seen_products = set()
    for product in products:
        product_entry = (product.name, product.price, product.units)
        assert product_entry not in seen_products, f"Duplicate entry found for product {product.name}"
        seen_products.add(product_entry)