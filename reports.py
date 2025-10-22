# reports.py
"""
Financial Insights and Visualization Module
Generates weekly and monthly reports with charts and statistics
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def load_expenses():
    """Load expenses from JSON file"""
    try:
        with open("expenses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_date_range(period="week"):
    """
    Get start and end dates for the specified period
    Args:
        period: "week" or "month"
    Returns:
        tuple: (start_date, end_date) as datetime objects
    """
    today = datetime.now()
    
    if period == "week":
        start_date = today - timedelta(days=7)
    elif period == "month":
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(days=7)
    
    return start_date, today

def filter_expenses_by_date(expenses, start_date, end_date):
    """
    Filter expenses within a date range
    Args:
        expenses: list of expense dictionaries
        start_date: datetime object
        end_date: datetime object
    Returns:
        list of filtered expenses
    """
    filtered = []
    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        if start_date <= expense_date <= end_date:
            filtered.append(expense)
    return filtered

def calculate_category_totals(expenses):
    """
    Calculate total spending per category
    Args:
        expenses: list of expense dictionaries
    Returns:
        dict: {category: total_amount}
    """
    category_totals = defaultdict(float)
    for expense in expenses:
        category = expense.get("category", "Uncategorized")
        amount = expense.get("amount", 0)
        category_totals[category] += amount
    return dict(category_totals)

def get_top_categories(category_totals, n=3):
    """
    Get top N spending categories
    Args:
        category_totals: dict of {category: amount}
        n: number of top categories to return
    Returns:
        list of tuples: [(category, amount), ...]
    """
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    return sorted_categories[:n]

def calculate_daily_average(expenses, num_days):
    """
    Calculate daily average spending
    Args:
        expenses: list of expense dictionaries
        num_days: number of days in the period
    Returns:
        float: daily average
    """
    total = sum(expense.get("amount", 0) for expense in expenses)
    return total / num_days if num_days > 0 else 0

def generate_report(period="week"):
    """
    Generate comprehensive financial report
    Args:
        period: "week" or "month"
    Returns:
        dict: report data with statistics and category breakdowns
    """
    expenses = load_expenses()
    start_date, end_date = get_date_range(period)
    filtered_expenses = filter_expenses_by_date(expenses, start_date, end_date)
    
    # Calculate statistics
    category_totals = calculate_category_totals(filtered_expenses)
    top_categories = get_top_categories(category_totals)
    total_spent = sum(category_totals.values())
    num_days = 7 if period == "week" else 30
    daily_avg = calculate_daily_average(filtered_expenses, num_days)
    
    # Load balance
    try:
        with open("balance.json", "r") as f:
            balance_data = json.load(f)
            remaining_balance = balance_data.get("balance", 0)
    except FileNotFoundError:
        remaining_balance = 0
    
    report = {
        "period": period,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_spent": total_spent,
        "daily_average": daily_avg,
        "remaining_balance": remaining_balance,
        "category_totals": category_totals,
        "top_categories": top_categories,
        "num_expenses": len(filtered_expenses)
    }
    
    return report

def create_pie_chart(category_totals, parent_frame):
    """
    Create a pie chart showing spending distribution by category
    Args:
        category_totals: dict of {category: amount}
        parent_frame: tkinter frame to display chart
    Returns:
        FigureCanvasTkAgg: chart canvas
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    if not category_totals:
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    else:
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        colors = plt.cm.Set3.colors[:len(categories)]
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title('Spending Distribution by Category')
    
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    return canvas

def create_bar_chart(category_totals, parent_frame):
    """
    Create a bar chart showing spending by category
    Args:
        category_totals: dict of {category: amount}
        parent_frame: tkinter frame to display chart
    Returns:
        FigureCanvasTkAgg: chart canvas
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    if not category_totals:
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    else:
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        colors = plt.cm.Pastel1.colors[:len(categories)]
        bars = ax.bar(categories, amounts, color=colors)
        ax.set_xlabel('Category')
        ax.set_ylabel('Amount (₹)')
        ax.set_title('Spending by Category')
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'₹{height:.0f}',
                   ha='center', va='bottom', fontsize=9)
    
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    return canvas

def show_report_window(period="week"):
    """
    Display a comprehensive report window with charts and statistics
    Args:
        period: "week" or "month"
    """
    report = generate_report(period)
    
    # Create window
    window = tk.Toplevel()
    window.title(f"{period.capitalize()}ly Financial Report")
    window.geometry("800x700")
    window.config(bg="#f5f5f5")
    
    # Title
    title_text = f"{period.capitalize()}ly Report ({report['start_date']} to {report['end_date']})"
    tk.Label(window, text=title_text, font=("Arial", 16, "bold"), 
             bg="#f5f5f5", fg="#1976d2").pack(pady=10)
    
    # Statistics Frame
    stats_frame = tk.Frame(window, bg="#e3f2fd", relief="ridge", bd=2)
    stats_frame.pack(pady=10, padx=20, fill="x")
    
    tk.Label(stats_frame, text="📊 Key Statistics", font=("Arial", 12, "bold"),
             bg="#e3f2fd").grid(row=0, column=0, columnspan=2, pady=5)
    
    stats = [
        ("Total Spent:", f"₹{report['total_spent']:.2f}"),
        ("Daily Average:", f"₹{report['daily_average']:.2f}"),
        ("Remaining Balance:", f"₹{report['remaining_balance']:.2f}"),
        ("Number of Expenses:", str(report['num_expenses']))
    ]
    
    for i, (label, value) in enumerate(stats, start=1):
        tk.Label(stats_frame, text=label, font=("Arial", 10, "bold"),
                bg="#e3f2fd", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        tk.Label(stats_frame, text=value, font=("Arial", 10),
                bg="#e3f2fd", anchor="e").grid(row=i, column=1, sticky="e", padx=10, pady=2)
    
    # Top Categories Frame
    if report['top_categories']:
        top_frame = tk.Frame(window, bg="#fff3e0", relief="ridge", bd=2)
        top_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(top_frame, text="🏆 Top 3 Expense Categories", font=("Arial", 12, "bold"),
                bg="#fff3e0").pack(pady=5)
        
        for i, (category, amount) in enumerate(report['top_categories'], start=1):
            tk.Label(top_frame, text=f"{i}. {category}: ₹{amount:.2f}",
                    font=("Arial", 10), bg="#fff3e0").pack(pady=2)
    
    # Charts Frame
    charts_frame = tk.Frame(window, bg="#f5f5f5")
    charts_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Create notebook for multiple charts
    notebook = ttk.Notebook(charts_frame)
    notebook.pack(fill="both", expand=True)
    
    # Pie chart tab
    pie_frame = tk.Frame(notebook, bg="white")
    notebook.add(pie_frame, text="Pie Chart")
    if report['category_totals']:
        pie_canvas = create_pie_chart(report['category_totals'], pie_frame)
        pie_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Bar chart tab
    bar_frame = tk.Frame(notebook, bg="white")
    notebook.add(bar_frame, text="Bar Chart")
    if report['category_totals']:
        bar_canvas = create_bar_chart(report['category_totals'], bar_frame)
        bar_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Close button
    tk.Button(window, text="Close", command=window.destroy,
             bg="#f44336", fg="white", padx=20, pady=5).pack(pady=10)

def export_report_to_file(period="week", filename=None):
    """
    Export report data to a text file
    Args:
        period: "week" or "month"
        filename: output filename (auto-generated if None)
    Returns:
        str: filename of exported report
    """
    report = generate_report(period)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{period}_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(f"{'='*50}\n")
        f.write(f"{period.upper()} FINANCIAL REPORT\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Period: {report['start_date']} to {report['end_date']}\n\n")
        
        f.write(f"KEY STATISTICS:\n")
        f.write(f"-" * 30 + "\n")
        f.write(f"Total Spent: ₹{report['total_spent']:.2f}\n")
        f.write(f"Daily Average: ₹{report['daily_average']:.2f}\n")
        f.write(f"Remaining Balance: ₹{report['remaining_balance']:.2f}\n")
        f.write(f"Number of Expenses: {report['num_expenses']}\n\n")
        
        if report['top_categories']:
            f.write(f"TOP 3 CATEGORIES:\n")
            f.write(f"-" * 30 + "\n")
            for i, (category, amount) in enumerate(report['top_categories'], start=1):
                f.write(f"{i}. {category}: ₹{amount:.2f}\n")
            f.write("\n")
        
        if report['category_totals']:
            f.write(f"ALL CATEGORIES:\n")
            f.write(f"-" * 30 + "\n")
            for category, amount in sorted(report['category_totals'].items(), 
                                          key=lambda x: x[1], reverse=True):
                f.write(f"{category}: ₹{amount:.2f}\n")
    
    return filename
