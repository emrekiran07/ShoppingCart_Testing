import os
import json
import pytest
from checkout_and_payment import User, Product, ShoppingCart, check_cart, checkout
from user_management import load_users, save_users, update_user_details

@pytest.fixture
def users_file_path(tmp_path):
    return os.path.join(tmp_path, "users.json")


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
def sample_user():
    return User("TestUser", 100.0)

@pytest.fixture
def users_file_path(tmp_path):
    return os.path.join(tmp_path, "users.json")





#5 Existing tests for checkout_and_payment


def test_add_item_to_cart():
    # Test adding an item to the cart
    cart = ShoppingCart()
    product = Product("Product1", 5.0, 10)
    cart.add_item(product)
    assert product in cart.items

def test_cart_creation():
    # Test shopping cart creation
    cart = ShoppingCart()
    assert cart.items == []

def test_check_cart_empty_cart(sample_user, sample_cart, capsys, monkeypatch):
    #Test check_cart with an empty cart
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    assert not check_cart(sample_user, sample_cart)
    captured = capsys.readouterr()
    assert "Your basket is empty. Please add items before checking out." in captured.out


def test_check_cart_cancel_checkout(sample_user, sample_cart, capsys, monkeypatch):
    # Test check_cart with items and cancel checkout
    monkeypatch.setattr('builtins.input', lambda _: 'N')
    sample_cart.add_item(Product("Product1", 5.0, 1))
    assert not check_cart(sample_user, sample_cart)
    captured = capsys.readouterr()
    assert "Thank you for your purchase" not in captured.out


def test_check_cart_logout(sample_user, sample_cart, monkeypatch):
    # Test check_cart with logout
    monkeypatch.setattr('builtins.input', lambda _: 'L')
    assert not check_cart(sample_user, sample_cart)


#New tests for check_cart with updated user details"""


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

