# insights.py
"""
Smart Suggestions Module
Provides intelligent spending insights and cost-saving recommendations
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict
from tracker import load_expenses

def get_spending_by_period(days=30):
    """
    Get spending data for a specific period
    Args:
        days: number of days to analyze
    Returns:
        dict: spending data grouped by category
    """
    expenses = load_expenses()
    cutoff_date = datetime.now() - timedelta(days=days)
    
    category_spending = defaultdict(list)
    
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if expense_date >= cutoff_date:
                category = expense.get("category", "Other")
                amount = expense.get("amount", 0)
                category_spending[category].append(amount)
        except ValueError:
            continue
    
    return category_spending

def calculate_average_spending(category, days=30):
    """
    Calculate average spending for a category over a period
    Args:
        category: category name
        days: number of days to analyze
    Returns:
        float: average spending amount
    """
    spending_data = get_spending_by_period(days)
    
    if category in spending_data and spending_data[category]:
        return sum(spending_data[category]) / len(spending_data[category])
    
    return 0

def detect_spending_anomalies(threshold_percentage=20):
    """
    Detect unusual spending patterns
    Args:
        threshold_percentage: percentage increase considered anomalous
    Returns:
        list: list of anomaly alerts
    """
    alerts = []
    
    # Compare this week vs last 4 weeks average
    this_week_data = get_spending_by_period(7)
    last_month_data = get_spending_by_period(30)
    
    for category in this_week_data:
        this_week_total = sum(this_week_data[category])
        
        if category in last_month_data:
            last_month_avg = sum(last_month_data[category]) / 4  # 4 weeks average
            
            if last_month_avg > 0:
                percentage_change = ((this_week_total - last_month_avg) / last_month_avg) * 100
                
                if percentage_change > threshold_percentage:
                    alerts.append({
                        "type": "high_spending",
                        "category": category,
                        "current": this_week_total,
                        "average": last_month_avg,
                        "change_percentage": percentage_change,
                        "message": f"📈 Your spending on {category} this week is {percentage_change:.0f}% higher than your average!"
                    })
    
    return alerts

def get_cost_saving_suggestions():
    """
    Generate smart cost-saving suggestions based on spending patterns
    Returns:
        list: list of suggestion dictionaries
    """
    suggestions = []
    expenses = load_expenses()
    
    if not expenses:
        return suggestions
    
    # Analyze recent spending (last 30 days)
    spending_data = get_spending_by_period(30)
    
    # Calculate totals per category
    category_totals = {cat: sum(amounts) for cat, amounts in spending_data.items()}
    
    if not category_totals:
        return suggestions
    
    total_spending = sum(category_totals.values())
    
    # Find high-spending categories (>20% of total)
    for category, amount in category_totals.items():
        percentage = (amount / total_spending * 100) if total_spending > 0 else 0
        
        if percentage > 20:
            suggestions.append({
                "type": "high_category_spending",
                "category": category,
                "amount": amount,
                "percentage": percentage,
                "suggestion": f"💡 {category} accounts for {percentage:.1f}% of your spending (₹{amount:.2f}). Consider setting a budget!"
            })
    
    # Check for frequent small expenses
    for category, amounts in spending_data.items():
        if len(amounts) > 10:  # More than 10 transactions
            avg_amount = sum(amounts) / len(amounts)
            if avg_amount < 100:  # Small frequent purchases
                suggestions.append({
                    "type": "frequent_small_expenses",
                    "category": category,
                    "count": len(amounts),
                    "average": avg_amount,
                    "suggestion": f"💡 You have {len(amounts)} small {category} expenses. Consider bulk purchases to save money!"
                })
    
    # Check for expensive single transactions
    for expense in expenses[-30:]:  # Last 30 expenses
        amount = expense.get("amount", 0)
        category = expense.get("category", "Other")
        
        if category in spending_data:
            avg = sum(spending_data[category]) / len(spending_data[category])
            if amount > avg * 2:  # More than 2x average
                suggestions.append({
                    "type": "high_single_expense",
                    "category": category,
                    "amount": amount,
                    "date": expense.get("date"),
                    "suggestion": f"💡 High {category} expense of ₹{amount:.2f} detected. Was this necessary?"
                })
                break  # Only show one to avoid spam
    
    # Suggest savings based on consistent spending
    for category, amounts in spending_data.items():
        if len(amounts) >= 4:  # At least 4 transactions
            total = sum(amounts)
            potential_savings = total * 0.1  # Suggest 10% reduction
            suggestions.append({
                "type": "potential_savings",
                "category": category,
                "current_spending": total,
                "potential_savings": potential_savings,
                "suggestion": f"💰 Reducing {category} spending by 10% could save you ₹{potential_savings:.2f} this month!"
            })
            break  # Show only one savings suggestion
    
    return suggestions

def get_spending_trends(days=30):
    """
    Analyze spending trends over time
    Args:
        days: number of days to analyze
    Returns:
        dict: trend information
    """
    expenses = load_expenses()
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Group spending by week
    weekly_spending = defaultdict(float)
    
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if expense_date >= cutoff_date:
                # Get week number
                week_num = expense_date.isocalendar()[1]
                weekly_spending[week_num] += expense.get("amount", 0)
        except ValueError:
            continue
    
    if not weekly_spending:
        return {"trend": "no_data", "direction": "unknown"}
    
    weeks = sorted(weekly_spending.keys())
    amounts = [weekly_spending[w] for w in weeks]
    
    # Simple trend detection
    if len(amounts) >= 2:
        if amounts[-1] > amounts[0] * 1.1:
            trend = "increasing"
        elif amounts[-1] < amounts[0] * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "trend": trend,
        "weekly_data": dict(weekly_spending),
        "average_weekly": sum(amounts) / len(amounts) if amounts else 0
    }

def get_spending_comparison(category=None):
    """
    Compare current month spending to previous month
    Args:
        category: specific category to compare (None for all)
    Returns:
        dict: comparison data
    """
    expenses = load_expenses()
    today = datetime.now()
    
    # Current month
    current_month_start = today.replace(day=1)
    current_month_expenses = []
    
    # Previous month
    if today.month == 1:
        prev_month_start = today.replace(year=today.year-1, month=12, day=1)
    else:
        prev_month_start = today.replace(month=today.month-1, day=1)
    
    prev_month_expenses = []
    
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            
            if category is None or expense.get("category") == category:
                if expense_date >= current_month_start:
                    current_month_expenses.append(expense)
                elif prev_month_start <= expense_date < current_month_start:
                    prev_month_expenses.append(expense)
        except ValueError:
            continue
    
    current_total = sum(e.get("amount", 0) for e in current_month_expenses)
    prev_total = sum(e.get("amount", 0) for e in prev_month_expenses)
    
    if prev_total > 0:
        change_percentage = ((current_total - prev_total) / prev_total) * 100
    else:
        change_percentage = 0
    
    return {
        "current_month_spending": current_total,
        "previous_month_spending": prev_total,
        "change_percentage": change_percentage,
        "change_amount": current_total - prev_total,
        "direction": "increase" if change_percentage > 0 else "decrease" if change_percentage < 0 else "stable"
    }

def get_all_insights():
    """
    Get all available insights and suggestions
    Returns:
        dict: comprehensive insights
    """
    return {
        "anomalies": detect_spending_anomalies(),
        "suggestions": get_cost_saving_suggestions(),
        "trends": get_spending_trends(),
        "comparison": get_spending_comparison()
    }
