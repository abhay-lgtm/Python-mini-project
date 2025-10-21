# tracker.py
import json
from datetime import date
from balance_manager import get_balance, subtract_from_balance

FILENAME = "expenses.json"

def load_expenses():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILENAME, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(category, amount, note="", deduct_from_balance=True):
    expenses = load_expenses()
    expense = {
        "date": str(date.today()),
        "category": category,
        "amount": amount,
        "note": note
    }
    
    # Optionally deduct from balance
    if deduct_from_balance:
        try:
            subtract_from_balance(amount)
        except ValueError as e:
            raise ValueError(f"Cannot add expense: {str(e)}")
    
    expenses.append(expense)
    save_expenses(expenses)

def get_summary():
    expenses = load_expenses()
    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]
    return summary

def get_total_spent():
    expenses = load_expenses()
    return sum(e["amount"] for e in expenses)

def get_remaining_balance():
    """Get the remaining balance after all expenses"""
    return get_balance()



