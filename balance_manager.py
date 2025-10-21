# balance_manager.py
import json
from datetime import date

BALANCE_FILENAME = "balance.json"

def load_balance():
    """Load the current balance from file"""
    try:
        with open(BALANCE_FILENAME, "r") as f:
            data = json.load(f)
            return data.get("balance", 0)
    except FileNotFoundError:
        return 0

def save_balance(balance):
    """Save the current balance to file"""
    data = {
        "balance": balance,
        "last_updated": str(date.today())
    }
    with open(BALANCE_FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def set_balance(balance):
    """Set the current balance"""
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    save_balance(balance)

def add_to_balance(amount):
    """Add money to the current balance"""
    current_balance = load_balance()
    new_balance = current_balance + amount
    save_balance(new_balance)
    return new_balance

def subtract_from_balance(amount):
    """Subtract money from the current balance"""
    current_balance = load_balance()
    new_balance = current_balance - amount
    if new_balance < 0:
        raise ValueError("Insufficient balance")
    save_balance(new_balance)
    return new_balance

def get_balance():
    """Get the current balance"""
    return load_balance()

def get_balance_info():
    """Get balance information including last updated date"""
    try:
        with open(BALANCE_FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"balance": 0, "last_updated": str(date.today())}