import os
import json
from user_management import load_users, save_users, update_user_details

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



def test_update_user_details():
    # Create a temporary file path
    temp_file_path = "temp_users.json"

    # Sample users with initial details
    initial_users = [
        {"username": "User1", "wallet": 50},
        {"username": "User2", "wallet": 75}
    ]

    # Save initial users to the temporary file
    save_users(initial_users, temp_file_path)

    # Update details for a user
    update_details = {"wallet": 100}
    update_user_details("User1", update_details, temp_file_path)

    # Load the updated users
    updated_users = load_users(temp_file_path)

    # Assert that the details were updated
    assert updated_users[0]["wallet"] == 100

    # Clean up: remove the temporary file
    os.remove(temp_file_path)




def test_load_users():
    # Create a temporary file with sample user data
    temp_file_path = "temp_users.json"
    sample_users = [
        {"username": "User1", "wallet": 50},
        {"username": "User2", "wallet": 75}
    ]
    with open(temp_file_path, "w") as temp_file:
        json.dump(sample_users, temp_file)

    # Test loading users
    loaded_users = load_users(temp_file_path)

    # Assert that the loaded users match the expected data
    assert loaded_users == sample_users

    # Clean up: remove the temporary file
    os.remove(temp_file_path)

def test_save_users():
    # Create a temporary file path
    temp_file_path = "temp_users.json"

    # Sample users with initial details
    initial_users = [
        {"username": "User1", "wallet": 50},
        {"username": "User2", "wallet": 75}
    ]

    # Save initial users to the temporary file
    save_users(initial_users, temp_file_path)

    # Load users from the temporary file
    loaded_users = load_users(temp_file_path)

    # Assert that the loaded users match the expected initial data
    assert loaded_users == initial_users

    # Clean up: remove the temporary file
    os.remove(temp_file_path)

