# goals.py
"""
Goal-Based Savings Feature Module
Allows users to set financial goals and track progress
"""

import json
from datetime import datetime, date

GOALS_FILENAME = "goals.json"

def load_goals():
    """
    Load all goals from JSON file
    Returns:
        list: list of goal dictionaries
    """
    try:
        with open(GOALS_FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_goals(goals):
    """
    Save goals to JSON file
    Args:
        goals: list of goal dictionaries
    """
    with open(GOALS_FILENAME, "w") as f:
        json.dump(goals, f, indent=4)

def add_goal(name, target_amount, deadline=None, lock_amount=False):
    """
    Add a new savings goal
    Args:
        name: goal name/description (e.g., "Save for earphones")
        target_amount: target amount to save
        deadline: optional deadline date (YYYY-MM-DD string)
        lock_amount: if True, reduce available balance by target amount
    Returns:
        dict: the created goal
    """
    goals = load_goals()
    
    goal = {
        "id": len(goals) + 1,
        "name": name,
        "target_amount": target_amount,
        "current_amount": 0,
        "deadline": deadline,
        "created_date": str(date.today()),
        "status": "active",  # active, completed, cancelled
        "lock_amount": lock_amount
    }
    
    goals.append(goal)
    save_goals(goals)
    
    # If lock_amount is True, we need to handle this in the balance manager
    # (This will be integrated in the GUI to warn users)
    
    return goal

def update_goal_progress(goal_id, amount_to_add):
    """
    Update progress toward a goal
    Args:
        goal_id: ID of the goal to update
        amount_to_add: amount to add to current progress
    Returns:
        dict: updated goal or None if not found
    """
    goals = load_goals()
    
    for goal in goals:
        if goal["id"] == goal_id and goal["status"] == "active":
            goal["current_amount"] += amount_to_add
            
            # Check if goal is reached
            if goal["current_amount"] >= goal["target_amount"]:
                goal["status"] = "completed"
                goal["completed_date"] = str(date.today())
            
            save_goals(goals)
            return goal
    
    return None

def get_goal_progress(goal_id):
    """
    Get progress information for a specific goal
    Args:
        goal_id: ID of the goal
    Returns:
        dict: progress information with percentage, remaining, etc.
    """
    goals = load_goals()
    
    for goal in goals:
        if goal["id"] == goal_id:
            current = goal["current_amount"]
            target = goal["target_amount"]
            percentage = (current / target * 100) if target > 0 else 0
            remaining = max(0, target - current)
            
            return {
                "goal": goal,
                "percentage": percentage,
                "remaining": remaining,
                "is_completed": goal["status"] == "completed"
            }
    
    return None

def get_active_goals():
    """
    Get all active goals
    Returns:
        list: list of active goal dictionaries
    """
    goals = load_goals()
    return [g for g in goals if g["status"] == "active"]

def get_completed_goals():
    """
    Get all completed goals
    Returns:
        list: list of completed goal dictionaries
    """
    goals = load_goals()
    return [g for g in goals if g["status"] == "completed"]

def cancel_goal(goal_id):
    """
    Cancel/delete a goal
    Args:
        goal_id: ID of the goal to cancel
    Returns:
        bool: True if cancelled, False if not found
    """
    goals = load_goals()
    
    for goal in goals:
        if goal["id"] == goal_id:
            goal["status"] = "cancelled"
            goal["cancelled_date"] = str(date.today())
            save_goals(goals)
            return True
    
    return False

def delete_goal(goal_id):
    """
    Permanently delete a goal
    Args:
        goal_id: ID of the goal to delete
    Returns:
        bool: True if deleted, False if not found
    """
    goals = load_goals()
    initial_length = len(goals)

    # Support deleting by numeric id or by name string for GUI convenience
    # If a string is passed that represents an integer, convert it.
    match_by = None
    try:
        # If goal_id is an int or a numeric string, treat as id
        if isinstance(goal_id, str) and goal_id.isdigit():
            goal_id_int = int(goal_id)
            match_by = ("id", goal_id_int)
        elif isinstance(goal_id, int):
            match_by = ("id", goal_id)
        elif isinstance(goal_id, str):
            # treat as name
            match_by = ("name", goal_id)
    except Exception:
        match_by = ("id", goal_id)

    if match_by[0] == "id":
        goals = [g for g in goals if g.get("id") != match_by[1]]
    else:
        goals = [g for g in goals if g.get("name") != match_by[1]]

    if len(goals) < initial_length:
        save_goals(goals)
        return True

    return False

def check_goal_alerts():
    """
    Check all active goals for alerts (near completion, deadline approaching)
    Returns:
        list: list of alert messages
    """
    goals = get_active_goals()
    alerts = []
    today = date.today()
    
    for goal in goals:
        current = goal["current_amount"]
        target = goal["target_amount"]
        percentage = (current / target * 100) if target > 0 else 0
        
        # Alert if 80% or more reached
        if percentage >= 80 and percentage < 100:
            remaining = target - current
            alerts.append({
                "type": "near_completion",
                "goal": goal,
                "message": f"🎯 Almost there! Only ₹{remaining:.2f} left to reach '{goal['name']}'"
            })
        
        # Alert if goal completed
        if percentage >= 100:
            alerts.append({
                "type": "completed",
                "goal": goal,
                "message": f"🎉 Congratulations! You've reached your goal: '{goal['name']}'"
            })
        
        # Alert if deadline is approaching (within 7 days)
        if goal.get("deadline"):
            try:
                deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d").date()
                days_left = (deadline - today).days
                
                if 0 <= days_left <= 7 and percentage < 100:
                    alerts.append({
                        "type": "deadline_approaching",
                        "goal": goal,
                        "message": f"⏰ {days_left} days left for '{goal['name']}' (₹{target - current:.2f} remaining)"
                    })
                elif days_left < 0 and percentage < 100:
                    alerts.append({
                        "type": "deadline_passed",
                        "goal": goal,
                        "message": f"⚠️ Deadline passed for '{goal['name']}'"
                    })
            except ValueError:
                pass  # Invalid deadline format
    
    return alerts

def get_total_locked_amount():
    """
    Calculate total amount locked in goals
    Returns:
        float: total locked amount
    """
    goals = get_active_goals()
    total = 0
    
    for goal in goals:
        if goal.get("lock_amount", False):
            remaining = max(0, goal["target_amount"] - goal["current_amount"])
            total += remaining
    
    return total

def get_available_balance_after_goals(current_balance):
    """
    Calculate available balance after subtracting locked goal amounts
    Args:
        current_balance: current total balance
    Returns:
        float: available balance
    """
    locked = get_total_locked_amount()
    return max(0, current_balance - locked)

def get_goal_summary():
    """
    Get summary of all goals
    Returns:
        dict: summary with counts and totals
    """
    all_goals = load_goals()
    active = [g for g in all_goals if g["status"] == "active"]
    completed = [g for g in all_goals if g["status"] == "completed"]
    
    total_target = sum(g["target_amount"] for g in active)
    total_saved = sum(g["current_amount"] for g in active)
    
    return {
        "total_goals": len(all_goals),
        "active_goals": len(active),
        "completed_goals": len(completed),
        "total_target_amount": total_target,
        "total_saved_amount": total_saved,
        "overall_progress": (total_saved / total_target * 100) if total_target > 0 else 0
    }
