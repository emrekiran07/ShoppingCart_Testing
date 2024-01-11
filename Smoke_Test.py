import pytest
from checkout_and_payment import User, Product, ShoppingCart, check_cart, checkout, load_products_from_csv

@pytest.fixture
def sample_user():
    return User("TestUser", 100.0)

@pytest.fixture
def sample_products():
    return [
        Product("Product1", 5.0, 10),
        Product("Product2", 3.0, 8),
        Product("Product3", 2.5, 5),
    ]

@pytest.fixture
def sample_cart():
    return ShoppingCart()

@pytest.fixture
def csv_filename():
    # Calling the CSV file for testing
    return 'products.csv'

def test_smoke_checkout_and_products(sample_user, sample_cart, capsys, sample_products, csv_filename):
    # Add items to the cart
    product1, product2, product3 = sample_products
    sample_cart.add_item(product1)
    sample_cart.add_item(product2)

    # Set the initial user wallet balance
    sample_user.wallet = 30.0

    # Call the checkout function
    checkout(sample_user, sample_cart)

    # Capture the printed output
    captured = capsys.readouterr()

    # Assertions for checkout
    assert "Thank you for your purchase" in captured.out
    assert f"Your remaining balance is {sample_user.wallet}" in captured.out
    assert not sample_cart.items
    assert product1.units == 9
    assert product2.units == 7

    # Check total products
    products = load_products_from_csv(csv_filename)
    assert len(products) == 71  # Update with the correct number of products

    # Check product details
    for product in products:
        assert isinstance(product, Product)
        assert isinstance(product.name, str)
        assert isinstance(product.price, float)
        assert isinstance(product.units, int)

    # Check product prices
    for product in products:
        assert isinstance(product.price, float) and product.price > 0
