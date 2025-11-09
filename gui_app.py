# gui_app.py
"""
Enhanced Smart Expense Tracker GUI
Integrates all advanced features: reports, goals, budgets, insights
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# Import existing modules
from tracker import (add_expense, load_expenses, get_summary, get_total_spent, 
                     get_remaining_balance, get_categories, export_expenses_to_csv, delete_expense)
from balance_manager import get_balance, set_balance, add_to_balance, get_balance_info

# Import new modules
from reports import show_report_window, export_report_to_file
from goals import (add_goal, get_active_goals, get_goal_progress, update_goal_progress,
                   check_goal_alerts, get_goal_summary, delete_goal, cancel_goal)
from budgets import (add_budget, get_active_budgets, check_budget_alerts, 
                     get_budget_status, delete_budget, get_budget_summary)
from insights import get_all_insights, detect_spending_anomalies, get_cost_saving_suggestions

# --- Window setup ---
root = tk.Tk()
root.title("Smart Expense Tracker Pro")
root.geometry("900x650")
root.config(bg="#f5f5f5")

# --- Menu Bar ---
menubar = tk.Menu(root)
root.config(menu=menubar)

# File Menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Export Expenses (CSV)", command=lambda: export_data("csv"))
file_menu.add_command(label="Export Report (TXT)", command=lambda: export_data("report"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# View Menu
view_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Weekly Report", command=lambda: show_report_window("week"))
view_menu.add_command(label="Monthly Report", command=lambda: show_report_window("month"))
view_menu.add_command(label="View Goals", command=lambda: show_goals_window())
view_menu.add_command(label="View Budgets", command=lambda: show_budgets_window())
view_menu.add_command(label="View Insights", command=lambda: show_insights_window())

# --- Top Info Bar ---
info_bar = tk.Frame(root, bg="#1976d2", height=40)
info_bar.pack(fill="x", pady=(0, 5))

alerts_label = tk.Label(info_bar, text="💡 Welcome! Check insights for smart suggestions", 
                        font=("Arial", 10), bg="#1976d2", fg="white", anchor="w")
alerts_label.pack(fill="x", padx=10, pady=8)

# --- Balance Frame ---
balance_frame = tk.Frame(root, bg="#e3f2fd", relief="ridge", bd=2)
balance_frame.pack(pady=5, padx=10, fill="x")

balance_label = tk.Label(balance_frame, text="Current Balance: ₹0", 
                         font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1976d2")
balance_label.pack(pady=5)

balance_btn_frame = tk.Frame(balance_frame, bg="#e3f2fd")
balance_btn_frame.pack(pady=5)

def update_balance_gui():
    """Open dialog to set/update balance"""
    dialog = tk.Toplevel(root)
    dialog.title("Update Balance")
    dialog.geometry("300x200")
    dialog.config(bg="#f5f5f5")
    dialog.transient(root)
    dialog.grab_set()
    
    tk.Label(dialog, text="Enter new balance amount:", bg="#f5f5f5").pack(pady=10)
    balance_entry = tk.Entry(dialog, width=20)
    balance_entry.pack(pady=5)
    balance_entry.focus()
    
    def set_new_balance():
        try:
            new_balance = float(balance_entry.get())
            if new_balance < 0:
                messagebox.showerror("Error", "Balance cannot be negative!")
                return
            set_balance(new_balance)
            messagebox.showinfo("Success", f"Balance updated to ₹{new_balance}")
            dialog.destroy()
            refresh_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    tk.Button(dialog, text="Set Balance", command=set_new_balance, 
              bg="#2196f3", fg="white").pack(pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy, 
              bg="#f44336", fg="white").pack()

def add_money_gui():
    """Open dialog to add money to balance"""
    dialog = tk.Toplevel(root)
    dialog.title("Add Money")
    dialog.geometry("300x200")
    dialog.config(bg="#f5f5f5")
    dialog.transient(root)
    dialog.grab_set()
    
    tk.Label(dialog, text="Enter amount to add:", bg="#f5f5f5").pack(pady=10)
    amount_entry = tk.Entry(dialog, width=20)
    amount_entry.pack(pady=5)
    amount_entry.focus()
    
    def add_money():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
            new_balance = add_to_balance(amount)
            messagebox.showinfo("Success", f"₹{amount} added. New balance: ₹{new_balance}")
            dialog.destroy()
            refresh_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    tk.Button(dialog, text="Add Money", command=add_money, 
              bg="#4caf50", fg="white").pack(pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy, 
              bg="#f44336", fg="white").pack()

tk.Button(balance_btn_frame, text="Update Balance", command=update_balance_gui, 
          bg="#2196f3", fg="white", padx=10).pack(side="left", padx=5)
tk.Button(balance_btn_frame, text="Add Money", command=add_money_gui, 
          bg="#4caf50", fg="white", padx=10).pack(side="left", padx=5)

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#ffffff", relief="ridge", bd=2)
input_frame.pack(pady=10, padx=10, fill="x")

tk.Label(input_frame, text="💰 Add New Expense", font=("Arial", 11, "bold"), 
         bg="#ffffff").grid(row=0, column=0, columnspan=4, pady=5)

tk.Label(input_frame, text="Category:", bg="#ffffff").grid(row=1, column=0, padx=5, sticky="e")
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(input_frame, textvariable=category_var, 
                                 values=get_categories(), state="readonly", width=18)
category_dropdown.grid(row=1, column=1, padx=5, pady=5)
category_dropdown.current(0)

tk.Label(input_frame, text="Amount (₹):", bg="#ffffff").grid(row=1, column=2, padx=5, sticky="e")
amount_entry = tk.Entry(input_frame, width=15)
amount_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Note:", bg="#ffffff").grid(row=2, column=0, padx=5, sticky="e")
note_entry = tk.Entry(input_frame, width=50)
note_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

expense_options_frame = tk.Frame(input_frame, bg="#ffffff")
expense_options_frame.grid(row=3, column=0, columnspan=4, pady=5)

deduct_balance_var = tk.BooleanVar(value=True)
tk.Checkbutton(expense_options_frame, text="Deduct from balance", 
               variable=deduct_balance_var, bg="#ffffff").pack()

def add_expense_gui():
    category = category_var.get()
    note = note_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    if not category:
        messagebox.showwarning("Missing Info", "Please select a category.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Amount must be positive!")
        return

    try:
        deduct_from_balance = deduct_balance_var.get()
        add_expense(category, amount, note, deduct_from_balance=deduct_from_balance)
        
        if deduct_from_balance:
            messagebox.showinfo("Success", f"Expense of ₹{amount} added and deducted from balance!")
        else:
            messagebox.showinfo("Success", f"Expense of ₹{amount} added (balance unchanged)!")
            
        amount_entry.delete(0, tk.END)
        note_entry.delete(0, tk.END)
        refresh_data()
        check_alerts()
    except ValueError as e:
        messagebox.showerror("Insufficient Balance", str(e))

tk.Button(input_frame, text="➕ Add Expense", command=add_expense_gui, 
          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
          padx=20, pady=5).grid(row=4, column=0, columnspan=4, pady=10)

# --- Quick Actions Frame ---
actions_frame = tk.Frame(root, bg="#f5f5f5")
actions_frame.pack(pady=5, padx=10, fill="x")

tk.Label(actions_frame, text="Quick Actions:", font=("Arial", 10, "bold"), 
         bg="#f5f5f5").pack(side="left", padx=5)

tk.Button(actions_frame, text="📊 Reports", command=lambda: show_report_window("week"), 
          bg="#9c27b0", fg="white", padx=10).pack(side="left", padx=2)
tk.Button(actions_frame, text="🎯 Goals", command=lambda: show_goals_window(), 
          bg="#ff9800", fg="white", padx=10).pack(side="left", padx=2)
tk.Button(actions_frame, text="💵 Budgets", command=lambda: show_budgets_window(), 
          bg="#f44336", fg="white", padx=10).pack(side="left", padx=2)
tk.Button(actions_frame, text="💡 Insights", command=lambda: show_insights_window(), 
          bg="#00bcd4", fg="white", padx=10).pack(side="left", padx=2)
tk.Button(actions_frame, text="💾 Export", command=lambda: export_data("csv"), 
          bg="#607d8b", fg="white", padx=10).pack(side="left", padx=2)

# --- Display Frame ---
display_frame = tk.Frame(root, bg="#ffffff", relief="ridge", bd=2)
display_frame.pack(padx=10, pady=5, fill="both", expand=True)

tk.Label(display_frame, text="Recent Expenses", font=("Arial", 11, "bold"), 
         bg="#ffffff").pack(pady=5)

tree = ttk.Treeview(display_frame, columns=("date", "category", "amount", "note"), 
                    show="headings", height=10)
tree.heading("date", text="Date")
tree.heading("category", text="Category")
tree.heading("amount", text="Amount (₹)")
tree.heading("note", text="Note")

tree.column("date", width=100)
tree.column("category", width=150)
tree.column("amount", width=100)
tree.column("note", width=300)

scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True, padx=5)

# Context menu for tree
context_menu = tk.Menu(tree, tearoff=0)
context_menu.add_command(label="Delete Expense", command=lambda: delete_selected_expense())

def show_context_menu(event):
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

tree.bind("<Button-3>", show_context_menu)

def delete_selected_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an expense to delete.")
        return
    
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
        item = tree.item(selected[0])
        expenses = load_expenses()
        # Find index by matching all values
        values = item["values"]
        for i, expense in enumerate(expenses):
            # Remove ₹ symbol from display value for comparison
            amount_str = values[2].replace("₹", "")
            try:
                amount = float(amount_str)
                if (expense["date"], expense["category"], expense["amount"], expense["note"]) == (values[0], values[1], amount, values[3]):
                    delete_expense(i)
                    messagebox.showinfo("Success", "Expense deleted!")
                    refresh_data()
                    break
            except:
                pass

# --- Summary Frame ---
summary_frame = tk.Frame(root, bg="#fff3e0", relief="ridge", bd=2)
summary_frame.pack(fill="x", pady=5, padx=10)

total_label = tk.Label(summary_frame, text="Total Spent: ₹0", 
                       font=("Arial", 11, "bold"), bg="#fff3e0")
total_label.pack(side="left", padx=20, pady=5)

stats_label = tk.Label(summary_frame, text="", font=("Arial", 9), bg="#fff3e0")
stats_label.pack(side="left", padx=10)

# --- Functions for new features ---

def show_goals_window():
    """Display goals management window"""
    window = tk.Toplevel(root)
    window.title("Financial Goals")
    window.geometry("700x500")
    window.config(bg="#f5f5f5")
    
    # Title
    tk.Label(window, text="🎯 Your Financial Goals", font=("Arial", 16, "bold"), 
             bg="#f5f5f5", fg="#ff9800").pack(pady=10)
    
    # Summary
    summary = get_goal_summary()
    summary_text = f"Active: {summary['active_goals']} | Completed: {summary['completed_goals']} | Total Progress: {summary['overall_progress']:.1f}%"
    tk.Label(window, text=summary_text, font=("Arial", 10), bg="#f5f5f5").pack()
    
    # Goals list
    goals_frame = tk.Frame(window, bg="#ffffff", relief="ridge", bd=2)
    goals_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    goals_tree = ttk.Treeview(goals_frame, columns=("id", "name", "target", "current", "progress"), 
                              show="headings", height=10)
    goals_tree.heading("id", text="ID")
    goals_tree.heading("name", text="Goal Name")
    goals_tree.heading("target", text="Target (₹)")
    goals_tree.heading("current", text="Current (₹)")
    goals_tree.heading("progress", text="Progress %")
    
    # Hide ID column but keep it for reference
    goals_tree.column("id", width=0, stretch=False)
    
    goals_tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Context menu for right-click delete
    goal_context_menu = tk.Menu(goals_tree, tearoff=0)
    goal_context_menu.add_command(label="Add Progress", command=lambda: add_progress_to_goal())
    goal_context_menu.add_separator()
    goal_context_menu.add_command(label="Delete Goal", command=lambda: delete_selected_goal())
    
    def show_goal_context_menu(event):
        try:
            # Select the item under cursor
            item = goals_tree.identify_row(event.y)
            if item:
                goals_tree.selection_set(item)
                goal_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            goal_context_menu.grab_release()
    
    goals_tree.bind("<Button-3>", show_goal_context_menu)  # Right-click
    
    def refresh_goals():
        for item in goals_tree.get_children():
            goals_tree.delete(item)
        
        goals = get_active_goals()
        for goal in goals:
            progress = get_goal_progress(goal["id"])
            goals_tree.insert("", "end", values=(
                goal["id"],  # Store ID (hidden)
                goal["name"], 
                f"₹{goal['target_amount']:.2f}", 
                f"₹{goal['current_amount']:.2f}",
                f"{progress['percentage']:.1f}%"
            ))
    
    def add_goal_gui():
        dialog = tk.Toplevel(window)
        dialog.title("Add New Goal")
        dialog.geometry("400x300")
        dialog.config(bg="#f5f5f5")
        dialog.transient(window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Goal Name:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Target Amount (₹):", bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        amount_entry = tk.Entry(dialog, width=30)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Deadline (YYYY-MM-DD):", bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        deadline_entry = tk.Entry(dialog, width=30)
        deadline_entry.grid(row=2, column=1, padx=10, pady=5)
        deadline_entry.insert(0, "Optional")
        
        lock_var = tk.BooleanVar(value=False)
        tk.Checkbutton(dialog, text="Lock amount from balance", variable=lock_var, 
                      bg="#f5f5f5").grid(row=3, column=0, columnspan=2, pady=5)
        
        def save_goal():
            try:
                name = name_entry.get()
                target = float(amount_entry.get())
                deadline = deadline_entry.get() if deadline_entry.get() != "Optional" else None
                
                if not name:
                    messagebox.showerror("Error", "Please enter a goal name!")
                    return
                
                if target <= 0:
                    messagebox.showerror("Error", "Target amount must be positive!")
                    return
                
                add_goal(name, target, deadline, lock_var.get())
                messagebox.showinfo("Success", f"Goal '{name}' added!")
                dialog.destroy()
                refresh_goals()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values!")
        
        tk.Button(dialog, text="Add Goal", command=save_goal, 
                 bg="#4caf50", fg="white", padx=20).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_selected_goal():
        """Delete the selected goal"""
        selected = goals_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a goal to delete.")
            return
        
        # Get the goal details
        item = goals_tree.item(selected[0])
        goal_id = item["values"][0]  # ID is first value (hidden column)
        goal_name = item["values"][1]  # Name is second value
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the goal '{goal_name}'?"):
            if delete_goal(goal_id):
                messagebox.showinfo("Success", f"Goal '{goal_name}' deleted successfully!")
                refresh_goals()
            else:
                messagebox.showerror("Error", "Failed to delete goal.")
    
    def add_progress_to_goal():
        """Add money toward a selected goal"""
        selected = goals_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a goal to add progress to.")
            return
        
        # Get the goal details
        item = goals_tree.item(selected[0])
        goal_id = item["values"][0]  # ID is first value (hidden column)
        goal_name = item["values"][1]  # Name is second value
        current_amount = float(item["values"][3].replace("₹", ""))  # Current amount
        target_amount = float(item["values"][2].replace("₹", ""))  # Target amount
        remaining = target_amount - current_amount
        
        # Create dialog to add amount
        dialog = tk.Toplevel(window)
        dialog.title(f"Add Progress to '{goal_name}'")
        dialog.geometry("400x320")
        dialog.config(bg="#f5f5f5")
        dialog.transient(window)
        dialog.grab_set()
        
        # Display goal info
        tk.Label(dialog, text=f"Goal: {goal_name}", font=("Arial", 11, "bold"),
                bg="#f5f5f5").pack(pady=5)
        tk.Label(dialog, text=f"Current: ₹{current_amount:.2f} / ₹{target_amount:.2f}",
                bg="#f5f5f5").pack(pady=2)
        tk.Label(dialog, text=f"Remaining: ₹{remaining:.2f}",
                bg="#f5f5f5", fg="#ff9800").pack(pady=2)
        
        # Show current balance
        current_balance = get_balance()
        tk.Label(dialog, text=f"Available Balance: ₹{current_balance:.2f}",
                bg="#f5f5f5", fg="#2196f3", font=("Arial", 9)).pack(pady=2)
        
        tk.Label(dialog, text="Amount to Add (₹):", bg="#f5f5f5",
                font=("Arial", 10, "bold")).pack(pady=10)
        amount_entry = tk.Entry(dialog, width=30, font=("Arial", 11))
        amount_entry.pack(pady=5)
        amount_entry.focus()
        
        # Checkbox to deduct from balance
        deduct_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dialog, text="Deduct from balance", variable=deduct_var,
                      bg="#f5f5f5", font=("Arial", 9)).pack(pady=5)
        
        def save_progress():
            try:
                amount = float(amount_entry.get())
                
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive!")
                    return
                
                # Check if we should deduct from balance
                if deduct_var.get():
                    current_balance = get_balance()
                    if amount > current_balance:
                        messagebox.showerror("Insufficient Balance", 
                                           f"You only have ₹{current_balance:.2f} in your balance.\n"
                                           f"You're trying to add ₹{amount:.2f} to the goal.")
                        return
                    
                    # Deduct from balance
                    try:
                        from balance_manager import subtract_from_balance
                        subtract_from_balance(amount)
                    except ValueError as e:
                        messagebox.showerror("Error", f"Cannot deduct from balance: {str(e)}")
                        return
                
                # Update goal progress
                updated_goal = update_goal_progress(goal_id, amount)
                
                if updated_goal:
                    new_current = updated_goal["current_amount"]
                    percentage = (new_current / target_amount * 100)
                    
                    # Build success message
                    balance_msg = f"(deducted from balance)" if deduct_var.get() else "(balance unchanged)"
                    
                    if updated_goal["status"] == "completed":
                        messagebox.showinfo("Goal Completed! 🎉", 
                                          f"Congratulations! You've reached your goal '{goal_name}'!\n"
                                          f"Total saved: ₹{new_current:.2f}\n"
                                          f"Amount added: ₹{amount:.2f} {balance_msg}")
                    else:
                        messagebox.showinfo("Progress Added!", 
                                          f"Added ₹{amount:.2f} to '{goal_name}' {balance_msg}\n"
                                          f"New total: ₹{new_current:.2f} ({percentage:.1f}%)\n"
                                          f"Remaining: ₹{target_amount - new_current:.2f}")
                    
                    dialog.destroy()
                    refresh_goals()
                    refresh_data()  # Refresh main window to update balance display
                else:
                    messagebox.showerror("Error", "Failed to update goal progress.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
        
        tk.Button(dialog, text="Add Progress", command=save_progress, 
                 bg="#ff9800", fg="white", padx=20, pady=8,
                 font=("Arial", 10, "bold")).pack(pady=20)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, 
                 bg="#757575", fg="white", padx=20).pack()
    
    # Buttons
    btn_frame = tk.Frame(window, bg="#f5f5f5")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Add New Goal", command=add_goal_gui, 
             bg="#4caf50", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Add Progress", command=add_progress_to_goal, 
             bg="#ff9800", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected_goal, 
             bg="#f44336", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_goals, 
             bg="#2196f3", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Close", command=window.destroy, 
             bg="#757575", fg="white", padx=15).pack(side="left", padx=5)
    
    refresh_goals()

def show_budgets_window():
    """Display budgets management window"""
    window = tk.Toplevel(root)
    window.title("Budget Management")
    window.geometry("800x500")
    window.config(bg="#f5f5f5")
    
    tk.Label(window, text="💵 Your Budgets", font=("Arial", 16, "bold"), 
             bg="#f5f5f5", fg="#f44336").pack(pady=10)
    
    summary = get_budget_summary()
    summary_text = f"Total Budgets: {summary['total_budgets']} | Safe: {summary['safe_count']} | Warning: {summary['warning_count']} | Exceeded: {summary['exceeded_count']}"
    tk.Label(window, text=summary_text, font=("Arial", 10), bg="#f5f5f5").pack()
    
    budgets_frame = tk.Frame(window, bg="#ffffff", relief="ridge", bd=2)
    budgets_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    budgets_tree = ttk.Treeview(budgets_frame, columns=("id", "category", "period", "budget", "spent", "remaining", "status"), 
                                show="headings", height=10)
    budgets_tree.heading("id", text="ID")
    budgets_tree.heading("category", text="Category")
    budgets_tree.heading("period", text="Period")
    budgets_tree.heading("budget", text="Budget (₹)")
    budgets_tree.heading("spent", text="Spent (₹)")
    budgets_tree.heading("remaining", text="Remaining (₹)")
    budgets_tree.heading("status", text="Status")
    
    # Hide ID column but keep it for reference
    budgets_tree.column("id", width=0, stretch=False)
    budgets_tree.column("category", width=120, anchor="w")
    budgets_tree.column("period", width=70, anchor="center")
    budgets_tree.column("budget", width=100, anchor="e")
    budgets_tree.column("spent", width=100, anchor="e")
    budgets_tree.column("remaining", width=100, anchor="e")
    budgets_tree.column("status", width=150, anchor="center")
    
    budgets_tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Context menu for right-click delete
    budget_context_menu = tk.Menu(budgets_tree, tearoff=0)
    budget_context_menu.add_command(label="Delete Budget", command=lambda: delete_selected_budget())
    
    def show_budget_context_menu(event):
        try:
            # Select the item under cursor
            item = budgets_tree.identify_row(event.y)
            if item:
                budgets_tree.selection_set(item)
                budget_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            budget_context_menu.grab_release()
    
    budgets_tree.bind("<Button-3>", show_budget_context_menu)  # Right-click
    
    def refresh_budgets():
        for item in budgets_tree.get_children():
            budgets_tree.delete(item)
        
        budgets = get_active_budgets()
        for budget in budgets:
            status = get_budget_status(budget)
            budgets_tree.insert("", "end", values=(
                budget["id"],  # Store ID (hidden)
                budget["category"],
                budget["period"],
                f"₹{budget['amount']:.2f}",
                f"₹{status['spent']:.2f}",
                f"₹{status['remaining']:.2f}",
                f"{status['percentage']:.1f}% ({status['status_level']})"
            ))
    
    def add_budget_gui():
        dialog = tk.Toplevel(window)
        dialog.title("Add New Budget")
        dialog.geometry("400x300")
        dialog.config(bg="#f5f5f5")
        dialog.transient(window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Category:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        cat_var = tk.StringVar()
        categories = ["Overall"] + get_categories()
        cat_combo = ttk.Combobox(dialog, textvariable=cat_var, values=categories, state="readonly", width=27)
        cat_combo.grid(row=0, column=1, padx=10, pady=5)
        cat_combo.current(0)
        
        tk.Label(dialog, text="Budget Amount (₹):", bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        amount_entry = tk.Entry(dialog, width=30)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Period:", bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        period_var = tk.StringVar(value="month")
        ttk.Radiobutton(dialog, text="Weekly", variable=period_var, value="week").grid(row=2, column=1, sticky="w", padx=10)
        ttk.Radiobutton(dialog, text="Monthly", variable=period_var, value="month").grid(row=3, column=1, sticky="w", padx=10)
        
        tk.Label(dialog, text="Alert at (%):", bg="#f5f5f5").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        alert_entry = tk.Entry(dialog, width=30)
        alert_entry.grid(row=4, column=1, padx=10, pady=5)
        alert_entry.insert(0, "80")
        
        def save_budget():
            try:
                category = cat_var.get()
                amount = float(amount_entry.get())
                period = period_var.get()
                alert_threshold = float(alert_entry.get())
                
                if amount <= 0:
                    messagebox.showerror("Error", "Budget amount must be positive!")
                    return
                
                add_budget(category, amount, period, alert_threshold)
                messagebox.showinfo("Success", f"Budget for '{category}' added!")
                dialog.destroy()
                refresh_budgets()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values!")
        
        tk.Button(dialog, text="Add Budget", command=save_budget, 
                 bg="#4caf50", fg="white", padx=20).grid(row=5, column=0, columnspan=2, pady=20)
    
    def delete_selected_budget():
        """Delete the selected budget"""
        selected = budgets_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a budget to delete.")
            return
        
        # Get the budget details
        item = budgets_tree.item(selected[0])
        budget_id = item["values"][0]  # ID is first value (hidden column)
        budget_category = item["values"][1]  # Category is second value
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the '{budget_category}' budget?"):
            if delete_budget(budget_id):
                messagebox.showinfo("Success", f"'{budget_category}' budget deleted successfully!")
                refresh_budgets()
            else:
                messagebox.showerror("Error", "Failed to delete budget.")
    
    btn_frame = tk.Frame(window, bg="#f5f5f5")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Add New Budget", command=add_budget_gui, 
             bg="#4caf50", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected_budget, 
             bg="#f44336", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_budgets, 
             bg="#2196f3", fg="white", padx=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Close", command=window.destroy, 
             bg="#757575", fg="white", padx=15).pack(side="left", padx=5)
    
    refresh_budgets()

def show_insights_window():
    """Display insights and smart suggestions"""
    window = tk.Toplevel(root)
    window.title("Smart Insights & Suggestions")
    window.geometry("700x600")
    window.config(bg="#f5f5f5")
    
    tk.Label(window, text="💡 Smart Insights", font=("Arial", 16, "bold"), 
             bg="#f5f5f5", fg="#00bcd4").pack(pady=10)
    
    # Scrollable text area for insights
    text_frame = tk.Frame(window, bg="#ffffff", relief="ridge", bd=2)
    text_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")
    
    text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 10), 
                         yscrollcommand=scrollbar.set, bg="#ffffff")
    text_widget.pack(fill="both", expand=True, padx=5, pady=5)
    scrollbar.config(command=text_widget.yview)
    
    # Get all insights
    insights = get_all_insights()
    
    # Display anomalies
    text_widget.insert("end", "🔍 SPENDING ANOMALIES\n", "heading")
    text_widget.insert("end", "=" * 60 + "\n\n")
    
    if insights["anomalies"]:
        for anomaly in insights["anomalies"]:
            text_widget.insert("end", f"{anomaly['message']}\n\n")
    else:
        text_widget.insert("end", "✅ No unusual spending patterns detected.\n\n")
    
    # Display suggestions
    text_widget.insert("end", "\n💰 COST-SAVING SUGGESTIONS\n", "heading")
    text_widget.insert("end", "=" * 60 + "\n\n")
    
    if insights["suggestions"]:
        for i, suggestion in enumerate(insights["suggestions"][:5], 1):  # Show top 5
            text_widget.insert("end", f"{i}. {suggestion['suggestion']}\n\n")
    else:
        text_widget.insert("end", "✅ Keep up the good work!\n\n")
    
    # Display trends
    text_widget.insert("end", "\n📈 SPENDING TRENDS\n", "heading")
    text_widget.insert("end", "=" * 60 + "\n\n")
    
    trend = insights["trends"]
    text_widget.insert("end", f"Overall Trend: {trend['trend'].upper()}\n")
    text_widget.insert("end", f"Average Weekly Spending: ₹{trend.get('average_weekly', 0):.2f}\n\n")
    
    # Display comparison
    text_widget.insert("end", "\n📊 MONTH-OVER-MONTH COMPARISON\n", "heading")
    text_widget.insert("end", "=" * 60 + "\n\n")
    
    comparison = insights["comparison"]
    text_widget.insert("end", f"Current Month: ₹{comparison['current_month_spending']:.2f}\n")
    text_widget.insert("end", f"Previous Month: ₹{comparison['previous_month_spending']:.2f}\n")
    text_widget.insert("end", f"Change: ₹{comparison['change_amount']:.2f} ({comparison['change_percentage']:.1f}%)\n")
    text_widget.insert("end", f"Direction: {comparison['direction'].upper()}\n\n")
    
    # Configure tags for formatting
    text_widget.tag_config("heading", font=("Arial", 12, "bold"), foreground="#1976d2")
    text_widget.config(state="disabled")
    
    tk.Button(window, text="Close", command=window.destroy, 
             bg="#f44336", fg="white", padx=20, pady=5).pack(pady=10)

def export_data(export_type):
    """Export data to file"""
    try:
        if export_type == "csv":
            filename = export_expenses_to_csv()
            messagebox.showinfo("Success", f"Expenses exported to {filename}")
        elif export_type == "report":
            filename = export_report_to_file("month")
            messagebox.showinfo("Success", f"Report exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {str(e)}")

def check_alerts():
    """Check for budget and goal alerts"""
    alerts = []
    
    # Check budget alerts
    budget_alerts = check_budget_alerts()
    alerts.extend([a["message"] for a in budget_alerts[:2]])  # Show top 2
    
    # Check goal alerts
    goal_alerts = check_goal_alerts()
    alerts.extend([a["message"] for a in goal_alerts[:2]])  # Show top 2
    
    # Get insights
    anomalies = detect_spending_anomalies()
    if anomalies:
        alerts.append(anomalies[0]["message"])
    
    # Update alert bar
    if alerts:
        alerts_label.config(text=" | ".join(alerts))
    else:
        alerts_label.config(text="💡 All good! No alerts at the moment.")

def refresh_data():
    """Refresh all data in the GUI"""
    # Clear old data
    for row in tree.get_children():
        tree.delete(row)

    # Load new data
    expenses = load_expenses()
    for e in expenses[-20:]:  # Show last 20 expenses
        tree.insert("", "end", values=(e["date"], e["category"], f"₹{e['amount']:.2f}", e["note"]))

    # Update balance and total spent
    current_balance = get_balance()
    total = get_total_spent()
    balance_label.config(text=f"Current Balance: ₹{current_balance:.2f}")
    total_label.config(text=f"Total Spent: ₹{total:.2f}")
    
    # Update stats
    num_expenses = len(expenses)
    avg = total / num_expenses if num_expenses > 0 else 0
    stats_label.config(text=f"Transactions: {num_expenses} | Average: ₹{avg:.2f}")
    
    # Check alerts
    check_alerts()

# Initial data load
refresh_data()

# Auto-check alerts every 30 seconds
def periodic_alert_check():
    check_alerts()
    root.after(30000, periodic_alert_check)

periodic_alert_check()

root.mainloop()
