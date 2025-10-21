# gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from tracker import add_expense, load_expenses, get_summary, get_total_spent, get_remaining_balance
from balance_manager import get_balance, set_balance, add_to_balance, get_balance_info

# --- Window setup ---
root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("700x500")
root.config(bg="#f5f5f5")

# --- Balance Frame ---
balance_frame = tk.Frame(root, bg="#e3f2fd", relief="ridge", bd=2)
balance_frame.pack(pady=5, padx=10, fill="x")

balance_label = tk.Label(balance_frame, text="Current Balance: ₹0", font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1976d2")
balance_label.pack(pady=5)

# Balance management buttons frame
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
    
    tk.Button(dialog, text="Set Balance", command=set_new_balance, bg="#2196f3", fg="white").pack(pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy, bg="#f44336", fg="white").pack()

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
    
    tk.Button(dialog, text="Add Money", command=add_money, bg="#4caf50", fg="white").pack(pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy, bg="#f44336", fg="white").pack()

tk.Button(balance_btn_frame, text="Update Balance", command=update_balance_gui, bg="#2196f3", fg="white", padx=10).pack(side="left", padx=5)
tk.Button(balance_btn_frame, text="Add Money", command=add_money_gui, bg="#4caf50", fg="white", padx=10).pack(side="left", padx=5)

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=5)
category_entry = tk.Entry(input_frame)
category_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Amount (₹):").grid(row=0, column=2, padx=5)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="Note:").grid(row=1, column=0, padx=5)
note_entry = tk.Entry(input_frame, width=40)
note_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

def add_expense_gui():
    category = category_entry.get()
    note = note_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    if not category:
        messagebox.showwarning("Missing Info", "Please enter a category.")
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
            
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        note_entry.delete(0, tk.END)
        refresh_data()
    except ValueError as e:
        messagebox.showerror("Insufficient Balance", str(e))

tk.Button(input_frame, text="Add Expense", command=add_expense_gui, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=4, pady=10)

# --- Display Frame ---
display_frame = tk.Frame(root, bg="#ffffff")
display_frame.pack(padx=10, pady=10, fill="both", expand=True)

tree = ttk.Treeview(display_frame, columns=("date", "category", "amount", "note"), show="headings")
tree.heading("date", text="Date")
tree.heading("category", text="Category")
tree.heading("amount", text="Amount (₹)")
tree.heading("note", text="Note")
tree.pack(fill="both", expand=True)

# --- Summary Frame ---
summary_frame = tk.Frame(root, bg="#f5f5f5")
summary_frame.pack(fill="x", pady=5)

total_label = tk.Label(summary_frame, text="Total Spent: ₹0", font=("Arial", 12, "bold"), bg="#f5f5f5")
total_label.pack()

# Add a checkbox to allow adding expenses without deducting from balance
expense_options_frame = tk.Frame(input_frame, bg="#f5f5f5")
expense_options_frame.grid(row=3, column=0, columnspan=4, pady=5)

deduct_balance_var = tk.BooleanVar(value=True)
tk.Checkbutton(expense_options_frame, text="Deduct from balance", variable=deduct_balance_var, 
               bg="#f5f5f5").pack()

def refresh_data():
    # Clear old data
    for row in tree.get_children():
        tree.delete(row)

    # Load new data
    expenses = load_expenses()
    for e in expenses:
        tree.insert("", "end", values=(e["date"], e["category"], e["amount"], e["note"]))

    # Update balance and total spent
    current_balance = get_balance()
    total = get_total_spent()
    balance_label.config(text=f"Current Balance: ₹{current_balance}")
    total_label.config(text=f"Total Spent: ₹{total}")

refresh_data()

root.mainloop()
