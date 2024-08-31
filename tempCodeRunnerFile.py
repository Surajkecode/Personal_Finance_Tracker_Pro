import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tabulate import tabulate
import json
import os

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, amount):
        self.expenses.append({
            'category': category,
            'amount': amount,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def calculate_total_expenses(self):
        return sum(expense['amount'] for expense in self.expenses)

    def calculate_expenses_by_category(self):
        expenses_by_category = {}
        for expense in self.expenses:
            category = expense['category']
            if category in expenses_by_category:
                expenses_by_category[category] += expense['amount']
            else:
                expenses_by_category[category] = expense['amount']
        return expenses_by_category

    def generate_report(self):
        headers = ['Category', 'Total Amount']
        expenses_by_category = self.calculate_expenses_by_category()
        data = [[category, amount] for category, amount in expenses_by_category.items()]
        total_spent = self.calculate_total_expenses()
        data.append(['Total', total_spent])
        return tabulate(data, headers=headers, tablefmt='grid')

    def save_expenses(self):
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def load_expenses(self):
        if os.path.exists('expenses.json'):
            with open('expenses.json', 'r') as file:
                self.expenses = json.load(file)

# Initialize tkinter app
root = tk.Tk()
root.title("Personal Finance Tracker")

# Create ExpenseTracker instance
tracker = ExpenseTracker()

# UI components
category_label = tk.Label(root, text="Category:")
category_label.grid(row=0, column=0, padx=10, pady=10)

category_entry = tk.Entry(root)
category_entry.grid(row=0, column=1, padx=10, pady=10)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=1, column=0, padx=10, pady=10)

amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=10, pady=10)

def add_expense():
    category = category_entry.get()
    amount_str = amount_entry.get()
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        
        tracker.add_expense(category, amount)
        update_report()
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

save_button = tk.Button(root, text="Save Expenses", command=tracker.save_expenses)
save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

load_button = tk.Button(root, text="Load Expenses", command=tracker.load_expenses)
load_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

report_label = tk.Label(root, text="Expense Report:")
report_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

report_text = tk.Text(root, height=10, width=50)
report_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def update_report():
    report_text.delete(1.0, tk.END)
    report = tracker.generate_report()
    report_text.insert(tk.END, report)

# Load initial expenses if any
tracker.load_expenses()
update_report()

# Start the tkinter main loop
root.mainloop()
