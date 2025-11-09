# tracker.py
"""
Enhanced Expense Tracker Module
Tracks expenses with improved categorization and data management
"""

import json
from datetime import date, datetime
from balance_manager import get_balance, subtract_from_balance

FILENAME = "expenses.json"

# Predefined expense categories
EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Healthcare",
    "Education",
    "Personal Care",
    "Groceries",
    "Rent",
    "Savings",
    "Other"
]

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

def get_expenses_by_category(category):
    """
    Get all expenses for a specific category
    Args:
        category: category name
    Returns:
        list: filtered expenses
    """
    expenses = load_expenses()
    return [e for e in expenses if e.get("category") == category]

def get_expenses_by_date_range(start_date, end_date):
    """
    Get expenses within a date range
    Args:
        start_date: datetime object or string (YYYY-MM-DD)
        end_date: datetime object or string (YYYY-MM-DD)
    Returns:
        list: filtered expenses
    """
    expenses = load_expenses()
    
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    filtered = []
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if start_date <= expense_date <= end_date:
                filtered.append(expense)
        except ValueError:
            continue
    
    return filtered

def delete_expense(expense_index):
    """
    Delete an expense by index
    Args:
        expense_index: index of the expense to delete
    Returns:
        bool: True if deleted, False if not found
    """
    from balance_manager import add_to_balance

    expenses = load_expenses()

    if 0 <= expense_index < len(expenses):
        deleted_expense = expenses[expense_index]
        amount = deleted_expense.get("amount", 0)

        # First, attempt to restore amount to balance
        try:
            # add_to_balance accepts numeric amounts
            add_to_balance(amount)
        except Exception as e:
            # Do not remove the expense if balance couldn't be adjusted
            raise RuntimeError(f"Failed to restore balance when deleting expense: {e}")

        # If balance restored successfully, remove expense and save
        expenses.pop(expense_index)
        save_expenses(expenses)
        return True

    return False

def edit_expense(expense_index, category=None, amount=None, note=None):
    """
    Edit an existing expense
    Args:
        expense_index: index of the expense to edit
        category: new category (optional)
        amount: new amount (optional)
        note: new note (optional)
    Returns:
        bool: True if edited, False if not found
    """
    from balance_manager import add_to_balance, subtract_from_balance

    expenses = load_expenses()

    if 0 <= expense_index < len(expenses):
        current = expenses[expense_index]
        old_amount = current.get("amount", 0)

        # Adjust balance if amount is changing
        if amount is not None and amount != old_amount:
            try:
                # If new amount is greater, subtract the extra from balance
                if amount > old_amount:
                    subtract_from_balance(amount - old_amount)
                # If new amount is smaller, add the difference back
                else:
                    add_to_balance(old_amount - amount)
            except Exception as e:
                # Do not persist changes if balance adjustment fails
                raise RuntimeError(f"Failed to adjust balance for edited expense: {e}")

            # Update the amount only after successful balance adjustment
            expenses[expense_index]["amount"] = amount

        # Update other fields
        if category is not None:
            expenses[expense_index]["category"] = category
        if note is not None:
            expenses[expense_index]["note"] = note

        save_expenses(expenses)
        return True

    return False

def get_categories():
    """
    Get list of predefined categories
    Returns:
        list: category names
    """
    return EXPENSE_CATEGORIES

def export_expenses_to_csv(filename="expenses_export.csv"):
    """
    Export all expenses to a CSV file
    Args:
        filename: output CSV filename
    Returns:
        str: filename of exported data
    """
    expenses = load_expenses()
    
    import csv
    with open(filename, "w", newline="", encoding="utf-8") as f:
        if expenses:
            fieldnames = ["date", "category", "amount", "note"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expenses)
    
    return filename

def get_expense_statistics():
    """
    Get comprehensive expense statistics
    Returns:
        dict: statistics including total, average, max, min, etc.
    """
    expenses = load_expenses()
    
    if not expenses:
        return {
            "total_expenses": 0,
            "total_spent": 0,
            "average_expense": 0,
            "max_expense": 0,
            "min_expense": 0,
            "categories_count": 0
        }
    
    amounts = [e["amount"] for e in expenses]
    categories = set(e["category"] for e in expenses)
    
    return {
        "total_expenses": len(expenses),
        "total_spent": sum(amounts),
        "average_expense": sum(amounts) / len(amounts),
        "max_expense": max(amounts),
        "min_expense": min(amounts),
        "categories_count": len(categories)
    }


