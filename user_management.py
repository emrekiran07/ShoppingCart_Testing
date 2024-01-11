import json


def load_users(file_path="users.json"):
    with open(file_path, "r") as file:
        users = json.load(file)
    return users

def save_users(users, file_path="users.json"):
    with open(file_path, "w") as file:
        json.dump(users, file, indent=2)

def update_user_details(username, new_details, file_path="users.json"):
    users = load_users(file_path)

    user_found = False
    for user in users:
        if user["username"] == username:
            user.update(new_details)
            user_found = True
            break

    if not user_found:
        raise ValueError(f"User with username '{username}' not found.")

    save_users(users, file_path)

# Example usage:
# Suppose Ramanathan wants to update his address and add a new credit card.
update_details = {
    "address": "456 Oak St, Townsville",
    "credit_cards": [
        {
            "card_number": "9876-5432-1098-7654",
            "expiry_date": "05/23",
            "name_on_card": "Ramanathan",
            "cvv": "456"
        }
    ]
}

update_user_details("Ramanathan", update_details)
