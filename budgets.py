# budgets.py
"""
Smart Budget Reminders Module
Allows users to set and track weekly/monthly budgets with alerts
"""

import json
from datetime import datetime, timedelta, date
from tracker import load_expenses

BUDGETS_FILENAME = "budgets.json"

def load_budgets():
    """
    Load all budgets from JSON file
    Returns:
        list: list of budget dictionaries
    """
    try:
        with open(BUDGETS_FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_budgets(budgets):
    """
    Save budgets to JSON file
    Args:
        budgets: list of budget dictionaries
    """
    with open(BUDGETS_FILENAME, "w") as f:
        json.dump(budgets, f, indent=4)

def add_budget(category, amount, period="month", alert_threshold=80):
    """
    Add a new budget
    Args:
        category: budget category (e.g., "Food", "Transport", or "Overall")
        amount: budget amount limit
        period: "week" or "month"
        alert_threshold: percentage at which to send alerts (default 80%)
    Returns:
        dict: the created budget
    """
    budgets = load_budgets()
    
    # Calculate start and end dates based on period
    today = date.today()
    if period == "week":
        start_date = today
        end_date = today + timedelta(days=7)
    else:  # month
        start_date = today
        end_date = today + timedelta(days=30)
    
    budget = {
        "id": len(budgets) + 1,
        "category": category,
        "amount": amount,
        "period": period,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "alert_threshold": alert_threshold,
        "status": "active",  # active, expired
        "created_date": str(today)
    }
    
    budgets.append(budget)
    save_budgets(budgets)
    return budget

def get_active_budgets():
    """
    Get all active budgets (not expired)
    Returns:
        list: list of active budget dictionaries
    """
    budgets = load_budgets()
    today = date.today()
    active = []
    
    for budget in budgets:
        if budget["status"] == "active":
            try:
                end_date = datetime.strptime(budget["end_date"], "%Y-%m-%d").date()
                if end_date >= today:
                    active.append(budget)
                else:
                    # Mark as expired
                    budget["status"] = "expired"
            except ValueError:
                pass  # Invalid date format
    
    # Save updated statuses
    save_budgets(budgets)
    return active

def calculate_spending_for_budget(budget):
    """
    Calculate current spending for a specific budget
    Args:
        budget: budget dictionary
    Returns:
        float: total spending for the budget period and category
    """
    expenses = load_expenses()
    
    try:
        start_date = datetime.strptime(budget["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(budget["end_date"], "%Y-%m-%d")
    except ValueError:
        return 0
    
    total_spent = 0
    category = budget["category"]
    
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            
            # Check if expense is within budget period
            if start_date <= expense_date <= end_date:
                # If budget is for specific category or "Overall"
                if category == "Overall" or expense.get("category") == category:
                    total_spent += expense.get("amount", 0)
        except ValueError:
            continue  # Skip invalid dates
    
    return total_spent

def get_budget_status(budget):
    """
    Get detailed status of a budget
    Args:
        budget: budget dictionary
    Returns:
        dict: status information with spending, percentage, remaining, etc.
    """
    spent = calculate_spending_for_budget(budget)
    budget_amount = budget["amount"]
    percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
    remaining = max(0, budget_amount - spent)
    
    # Determine status level
    alert_threshold = budget.get("alert_threshold", 80)
    if percentage >= 100:
        status_level = "exceeded"
    elif percentage >= alert_threshold:
        status_level = "warning"
    elif percentage >= alert_threshold * 0.5:
        status_level = "caution"
    else:
        status_level = "safe"
    
    return {
        "budget": budget,
        "spent": spent,
        "budget_amount": budget_amount,
        "percentage": percentage,
        "remaining": remaining,
        "status_level": status_level,
        "is_exceeded": percentage >= 100
    }

def check_budget_alerts():
    """
    Check all active budgets for alerts
    Returns:
        list: list of alert dictionaries
    """
    budgets = get_active_budgets()
    alerts = []
    
    for budget in budgets:
        status = get_budget_status(budget)
        percentage = status["percentage"]
        alert_threshold = budget.get("alert_threshold", 80)
        
        category = budget["category"]
        period = budget["period"]
        
        # Alert if threshold reached
        if alert_threshold <= percentage < 100:
            alerts.append({
                "type": "warning",
                "budget": budget,
                "status": status,
                "message": f"⚠️ {category} {period}ly budget at {percentage:.1f}% (₹{status['remaining']:.2f} left)"
            })
        
        # Alert if budget exceeded
        elif percentage >= 100:
            overspent = status["spent"] - status["budget_amount"]
            alerts.append({
                "type": "exceeded",
                "budget": budget,
                "status": status,
                "message": f"🚨 {category} {period}ly budget exceeded by ₹{overspent:.2f}!"
            })
    
    return alerts

def update_budget(budget_id, **kwargs):
    """
    Update an existing budget
    Args:
        budget_id: ID of the budget to update
        **kwargs: fields to update (amount, alert_threshold, etc.)
    Returns:
        bool: True if updated, False if not found
    """
    budgets = load_budgets()
    
    for budget in budgets:
        if budget["id"] == budget_id:
            for key, value in kwargs.items():
                if key in budget:
                    budget[key] = value
            save_budgets(budgets)
            return True
    
    return False

def delete_budget(budget_id):
    """
    Delete a budget
    Args:
        budget_id: ID of the budget to delete (int or string)
    Returns:
        bool: True if deleted, False if not found
    """
    budgets = load_budgets()
    initial_length = len(budgets)
    
    # Support deleting by numeric id or by category name string for GUI convenience
    # If a string is passed that represents an integer, convert it.
    match_by = None
    try:
        # If budget_id is an int or a numeric string, treat as id
        if isinstance(budget_id, str) and budget_id.isdigit():
            budget_id_int = int(budget_id)
            match_by = ("id", budget_id_int)
        elif isinstance(budget_id, int):
            match_by = ("id", budget_id)
        elif isinstance(budget_id, str):
            # treat as category name
            match_by = ("category", budget_id)
    except Exception:
        match_by = ("id", budget_id)
    
    if match_by[0] == "id":
        budgets = [b for b in budgets if b.get("id") != match_by[1]]
    else:
        budgets = [b for b in budgets if b.get("category") != match_by[1]]
    
    if len(budgets) < initial_length:
        save_budgets(budgets)
        return True
    
    return False

def renew_budget(budget_id):
    """
    Renew an expired budget for the next period
    Args:
        budget_id: ID of the budget to renew
    Returns:
        dict: new budget or None if not found
    """
    budgets = load_budgets()
    
    for budget in budgets:
        if budget["id"] == budget_id:
            # Create new budget with same parameters
            return add_budget(
                category=budget["category"],
                amount=budget["amount"],
                period=budget["period"],
                alert_threshold=budget.get("alert_threshold", 80)
            )
    
    return None

def get_budget_summary():
    """
    Get summary of all budgets
    Returns:
        dict: summary with counts and status overview
    """
    budgets = get_active_budgets()
    
    total_budget = sum(b["amount"] for b in budgets)
    total_spent = sum(calculate_spending_for_budget(b) for b in budgets)
    
    safe_count = 0
    warning_count = 0
    exceeded_count = 0
    
    for budget in budgets:
        status = get_budget_status(budget)
        level = status["status_level"]
        
        if level == "exceeded":
            exceeded_count += 1
        elif level in ["warning", "caution"]:
            warning_count += 1
        else:
            safe_count += 1
    
    return {
        "total_budgets": len(budgets),
        "safe_count": safe_count,
        "warning_count": warning_count,
        "exceeded_count": exceeded_count,
        "total_budget_amount": total_budget,
        "total_spent": total_spent,
        "overall_percentage": (total_spent / total_budget * 100) if total_budget > 0 else 0
    }

def get_category_budget(category, period="month"):
    """
    Get the budget for a specific category and period
    Args:
        category: category name
        period: "week" or "month"
    Returns:
        dict: budget dictionary or None if not found
    """
    budgets = get_active_budgets()
    
    for budget in budgets:
        if budget["category"] == category and budget["period"] == period:
            return budget
    
    return None
