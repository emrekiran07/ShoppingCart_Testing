import pytest


from checkout_and_payment import User, Product, ShoppingCart, check_cart

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

def test_check_cart_insufficient_funds(sample_user, sample_cart, capsys, monkeypatch):
    # Test check_cart with insufficient funds.
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    sample_cart.add_item(Product("Product1", 5.0, 1))
    sample_user.wallet = 1.0  # Set a low wallet balance
    assert not check_cart(sample_user, sample_cart)
    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out


def test_check_cart_zero_wallet_balance(sample_user, sample_cart, capsys, monkeypatch):
    # Test check_cart with zero wallet balance
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    sample_cart.add_item(Product("Product1", 5.0, 1))
    sample_user.wallet = 0.0
    assert not check_cart(sample_user, sample_cart)
    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out


def test_check_cart_negative_wallet_balance(sample_user, sample_cart, capsys, monkeypatch):
    # Test check_cart with negative wallet balance.
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    sample_cart.add_item(Product("Product1", 5.0, 1))
    sample_user.wallet = -10.0
    assert not check_cart(sample_user, sample_cart)
    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out


def test_cart_total_price():
    # Test calculating the total price of items in the cart
    cart = ShoppingCart()
    product1 = Product("Product1", 5.0, 10)
    product2 = Product("Product2", 3.0, 8)
    cart.add_item(product1)
    cart.add_item(product2)
    assert cart.get_total_price() == 8.0

def test_remove_item_from_cart():
    # Test removing an item from the cart
    cart = ShoppingCart()
    product = Product("Product1", 5.0, 10)
    cart.add_item(product)
    cart.remove_item(product)
    assert product not in cart.items