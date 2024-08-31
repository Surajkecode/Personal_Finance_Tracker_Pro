import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from tabulate import tabulate
import json
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, amount):
        self.expenses.append({
            'category': category,
            'amount': amount,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]

    def add_month(self):
        current_month = datetime.now().strftime('%Y-%m')
        messagebox.showinfo("New Month", f"Month {current_month} has been added!")

    def calculate_total_expenses(self):
        return sum(expense['amount'] for expense in self.expenses)

    def calculate_expenses_by_category_and_month(self, month):
        expenses_by_category = {}
        for expense in self.expenses:
            expense_month = datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
            if expense_month == month:
                category = expense['category']
                amount = expense['amount']
                if category in expenses_by_category:
                    expenses_by_category[category] += amount
                else:
                    expenses_by_category[category] = amount
        return expenses_by_category

    def generate_report(self):
        headers = ['Date', 'Category', 'Amount']
        self.expenses.sort(key=lambda x: x['date'], reverse=True)
        data = [[expense['date'], expense['category'], expense['amount']] for expense in self.expenses]
        return tabulate(data, headers=headers, tablefmt='grid')

    def generate_monthly_report(self, month):
        headers = ['Category', 'Total Amount']
        expenses_by_category = self.calculate_expenses_by_category_and_month(month)
        data = [[category, amount] for category, amount in expenses_by_category.items()]
        total_spent = sum(amount for amount in expenses_by_category.values())
        data.append(['Total', total_spent])
        return tabulate(data, headers=headers, tablefmt='grid')

    def save_expenses(self):
        try:
            with open('expenses.json', 'w') as file:
                json.dump(self.expenses, file, indent=4)
            messagebox.showinfo("Success", "Expenses saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save expenses: {e}")

    def load_expenses(self):
        file_path = 'expenses.json'
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    self.expenses = json.load(file)
                messagebox.showinfo("Success", "Expenses loaded successfully!")
                return True  # Indicate that loading was successful
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Failed to decode expenses data.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        else:
            messagebox.showinfo("Info", "No expenses file found. Starting fresh.")
        return False  # Indicate that loading was unsuccessful

    def plot_monthly_report(self, month):
        expenses_by_category = self.calculate_expenses_by_category_and_month(month)
        categories = list(expenses_by_category.keys())
        amounts = list(expenses_by_category.values())

        plt.figure(figsize=(10, 5))
        plt.bar(categories, amounts, color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Amount Spent')
        plt.title(f'Expenses for {month}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

# Initialize tkinter app
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("600x450")

# Load and display the background image
bg_image = Image.open("finance.jpg")
bg_image = bg_image.resize((600, 450), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create ExpenseTracker instance
tracker = ExpenseTracker()

# UI components
category_label = tk.Label(root, text="Category:", bg="#E0E0E0", font=("Helvetica", 12, "bold"))
category_label.place(x=50, y=50)

category_entry = tk.Entry(root, font=("Helvetica", 12))
category_entry.place(x=150, y=50)

amount_label = tk.Label(root, text="Amount:", bg="#E0E0E0", font=("Helvetica", 12, "bold"))
amount_label.place(x=50, y=100)

amount_entry = tk.Entry(root, font=("Helvetica", 12))
amount_entry.place(x=150, y=100)

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

add_button = tk.Button(root, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
add_button.place(x=50, y=150)

save_button = tk.Button(root, text="Save Expenses", command=tracker.save_expenses, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
save_button.place(x=200, y=150)

def load_expenses():
    if tracker.load_expenses():
        update_report()

load_button = tk.Button(root, text="Load Expenses", command=load_expenses, bg="#FF9800", fg="white", font=("Helvetica", 12, "bold"))
load_button.place(x=350, y=150)

def delete_expense():
    try:
        index = simpledialog.askinteger("Delete Expense", "Enter the index of the expense to delete (starting from 0):")
        if index is not None:
            tracker.delete_expense(index)
            update_report()
    except ValueError:
        messagebox.showerror("Error", "Invalid index!")

delete_button = tk.Button(root, text="Delete Entry", command=delete_expense, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"))
delete_button.place(x=50, y=200)

def add_month():
    tracker.add_month()

month_button = tk.Button(root, text="Add Month", command=add_month, bg="#9C27B0", fg="white", font=("Helvetica", 12, "bold"))
month_button.place(x=200, y=200)

def show_report_popup():
    report = tracker.generate_report()
    popup = tk.Toplevel(root)
    popup.title("Expense Report")
    popup.geometry("500x400")
    popup.config(bg="#E0E0E0")
    
    report_text = tk.Text(popup, height=20, width=60, font=("Helvetica", 10), bg="#FFF8E1", fg="#212121")
    report_text.pack(padx=10, pady=10)
    report_text.insert(tk.END, report)

report_button = tk.Button(root, text="Show Report", command=show_report_popup, bg="#3F51B5", fg="white", font=("Helvetica", 12, "bold"))
report_button.place(x=350, y=200)

def update_report():
    # Optionally update the main screen report if needed
    pass

# Monthly report section
def select_month():
    month = simpledialog.askstring("Select Month", "Enter the month in format YYYY-MM:")
    if month:
        generate_monthly_report(month)

def generate_monthly_report(month):
    report = tracker.generate_monthly_report(month)
    popup = tk.Toplevel(root)
    popup.title(f"Monthly Report - {month}")
    popup.geometry("500x400")
    popup.config(bg="#E0E0E0")

    report_text = tk.Text(popup, height=20, width=60, font=("Helvetica", 10), bg="#FFF8E1", fg="#212121")
    report_text.pack(padx=10, pady=10)
    report_text.insert(tk.END, report)

    plot_button = tk.Button(popup, text="Show Bar Graph", command=lambda: tracker.plot_monthly_report(month), bg="#3F51B5", fg="white", font=("Helvetica", 12, "bold"))
    plot_button.pack(pady=10)

select_month_button = tk.Button(root, text="Select Month", command=select_month, bg="#3F51B5", fg="white", font=("Helvetica", 12, "bold"))
select_month_button.place(x=200, y=250)

# Load initial expenses if any
tracker.load_expenses()

# Start the tkinter main loop
root.mainloop()
