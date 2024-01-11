import pytest
@pytest.fixture
def user():
    return User("TestUser", 100.0)

@pytest.fixture
def cart():
    return ShoppingCart()

from checkout_and_payment import checkout, ShoppingCart, User, Product


# Test case for a successful checkout
def test_successful_checkout(user, cart, capsys):
    # Add items to the cart
    product1 = Product("Product1", 10.0, 3)
    product2 = Product("Product2", 5.0, 2)
    cart.add_item(product1)
    cart.add_item(product2)

    # Set the initial user wallet balance
    user.wallet = 30.0

    # Call the checkout function
    checkout(user, cart)

    # Capture the printed output
    captured = capsys.readouterr()

    # Assertions
    assert "Thank you for your purchase" in captured.out
    assert f"Your remaining balance is {user.wallet}" in captured.out

    # Additional assertions based on your specific requirements
    # For example, check if the cart is cleared, product units are updated, etc.
    assert not cart.items
    assert product1.units == 2
    assert product2.units == 1

# Test case for an empty cart
def test_checkout_empty_cart(user, cart, capsys):
    # Call the checkout function with an empty cart
    checkout(user, cart)

    # Capture the printed output
    captured = capsys.readouterr()

    # Assertions
    assert "Your basket is empty. Please add items before checking out." in captured.out


# Test case for successful checkout with multiple products
def test_successful_checkout_multiple_products(user, cart, capsys):
    # Add items to the cart
    product1 = Product("Product1", 10.0, 3)
    product2 = Product("Product2", 5.0, 2)
    cart.add_item(product1)
    cart.add_item(product2)

    # Set the initial user wallet balance
    user.wallet = 30.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "Thank you for your purchase" in captured.out
    assert f"Your remaining balance is {user.wallet}" in captured.out
    assert not cart.items
    assert product1.units == 2
    assert product2.units == 1



# Test case for checkout with zero wallet balance
def test_checkout_zero_wallet_balance(user, cart, capsys):
    # Add items to the cart
    product1 = Product("Product1", 10.0, 2)
    cart.add_item(product1)

    # Set the initial user wallet balance
    user.wallet = 0.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "You don't have enough money to complete the purchase." in captured.out
    assert "Please try again!" in captured.out
    assert product1.units == 2


# Test case for checkout with negative wallet balance
def test_checkout_negative_wallet_balance(user, cart, capsys):
    # Add items to the cart
    product1 = Product("Product1", 10.0, 2)
    cart.add_item(product1)

    # Set the initial user wallet balance
    user.wallet = -5.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "You don't have enough money to complete the purchase." in captured.out
    assert "Please try again!" in captured.out
    assert product1.units == 2  # Product units should not be updated


# Test case for checkout with products having negative units
def test_checkout_negative_units(user, cart, capsys):
    # Add items to the cart with negative units
    product1 = Product("Product1", 10.0, -1)
    product2 = Product("Product2", 5.0, -2)
    cart.add_item(product1)
    cart.add_item(product2)

    # Set the initial user wallet balance
    user.wallet = 20.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "Thank you for your purchase" in captured.out
    assert f"Your remaining balance is {user.wallet}" in captured.out


# Test case for checkout with multiple identical products
def test_checkout_multiple_identical_products(user, cart, capsys):
    # Add multiple identical items to the cart
    product = Product("Product1", 10.0, 3)
    cart.add_item(product)
    cart.add_item(product)

    # Set the initial user wallet balance
    user.wallet = 60.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "Thank you for your purchase" in captured.out
    assert f"Your remaining balance is {user.wallet}" in captured.out
    assert not cart.items
    assert product.units == 1


# Test case for checkout with negative initial wallet balance
def test_checkout_negative_initial_balance(user, cart, capsys):
    # Add items to the cart
    product1 = Product("Product1", 10.0, 2)
    product2 = Product("Product2", 5.0, 1)
    cart.add_item(product1)
    cart.add_item(product2)

    # Set the initial user wallet balance to a negative value
    user.wallet = -5.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "You don't have enough money to complete the purchase." in captured.out
    assert "Please try again!" in captured.out
    assert cart.items  # Cart should still contain the items
    assert product1.units == 2  # Product units should not be updated
    assert product2.units == 1



# Test case for a single item in the cart and insufficient funds
def test_checkout_single_item_insufficient_funds(user, cart, capsys):
    # Add a single item to the cart
    product = Product("Product1", 10.0, 1)
    cart.add_item(product)

    # Set the initial user wallet balance to less than the product price
    user.wallet = 5.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "You don't have enough money to complete the purchase." in captured.out
    assert "Please try again!" in captured.out
    assert cart.items  # Cart should still contain the item
    assert product.units == 1  # Product units should not be updated



# Test case for checkout with a product having multiple units
def test_checkout_multiple_units_product(user, cart, capsys):
    # Add a product with multiple units to the cart
    product = Product("MultiUnitsProduct", 8.0, 3)
    cart.add_item(product)

    # Set the initial user wallet balance
    user.wallet = 24.0

    # Call the checkout function
    checkout(user, cart)
    captured = capsys.readouterr()

    # Assertions
    assert "Thank you for your purchase" in captured.out
    assert f"Your remaining balance is {user.wallet}" in captured.out
    assert not cart.items  # Cart should be cleared
    assert product.units == 2
