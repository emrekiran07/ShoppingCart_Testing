import pytest
from checkout_and_payment import load_products_from_csv, Product
import os
import json
from user_management import load_users, save_users, update_user_details

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

