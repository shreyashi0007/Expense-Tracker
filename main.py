import json
import os
from datetime import datetime, timedelta

FILE = "expense_data.json"

transactions = []
budgets = {}


# Load saved data
def load_data():
    global transactions, budgets

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            data = json.load(f)

        transactions = data.get("transactions", [])
        budgets = data.get("budgets", {})


# Save data
def save_data():
    data = {
        "transactions": transactions,
        "budgets": budgets
    }

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# Add income or expense
def add_transaction():
    print("\n1. Income")
    print("2. Expense")

    choice = input("Choose transaction type: ")

    if choice not in ["1", "2"]:
        print("Invalid choice!")
        return

    amount = float(input("Enter amount: ₹"))

    if amount <= 0:
        print("Amount must be greater than zero!")
        return

    if choice == "1":
        category = "Income"
        transaction_type = "Income"
    else:
        print("\nCategories:")
        print("Food, Travel, Shopping, Bills, Entertainment, Education, Healthcare, Other")

        category = input("Enter category: ").title()
        transaction_type = "Expense"

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date!")
        return

    description = input("Enter description: ")

    transaction = {
        "id": len(transactions) + 1,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date,
        "description": description
    }

    transactions.append(transaction)
    save_data()

    print("Transaction added successfully!")


# View all transactions
def view_transactions():
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n========== TRANSACTION HISTORY ==========")

    for t in transactions:
        print(
            f"ID: {t['id']} | {t['date']} | {t['type']} | "
            f"{t['category']} | ₹{t['amount']} | {t['description']}"
        )


# Calculate balance
def show_balance():
    income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = income - expenses

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Income   : ₹{income:.2f}")
    print(f"Total Expenses : ₹{expenses:.2f}")
    print(f"Balance       : ₹{balance:.2f}")


# Edit a transaction
def edit_transaction():
    view_transactions()

    if not transactions:
        return

    try:
        tid = int(input("\nEnter transaction ID to edit: "))
    except ValueError:
        print("Invalid ID!")
        return

    for t in transactions:
        if t["id"] == tid:
            print("Press Enter to keep the old value.")

            amount = input("New amount: ")
            category = input("New category: ")
            date = input("New date (YYYY-MM-DD): ")
            description = input("New description: ")

            if amount:
                t["amount"] = float(amount)

            if category:
                t["category"] = category.title()

            if date:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    t["date"] = date
                except ValueError:
                    print("Invalid date. Old date kept.")

            if description:
                t["description"] = description

            save_data()
            print("Transaction updated successfully!")
            return

    print("Transaction ID not found.")


# Delete a transaction
def delete_transaction():
    view_transactions()

    if not transactions:
        return

    try:
        tid = int(input("\nEnter transaction ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    for t in transactions:
        if t["id"] == tid:
            transactions.remove(t)
            save_data()
            print("Transaction deleted successfully!")
            return

    print("Transaction ID not found.")


# Search transactions
def search_transaction():
    keyword = input("\nEnter date, category or description to search: ").lower()

    found = False

    for t in transactions:
        if (keyword in t["date"].lower()
                or keyword in t["category"].lower()
                or keyword in t["description"].lower()
                or keyword in t["type"].lower()):

            print(
                f"ID: {t['id']} | {t['date']} | {t['type']} | "
                f"{t['category']} | ₹{t['amount']} | {t['description']}"
            )
            found = True

    if not found:
        print("No matching transactions found.")


# Set monthly category budget
def set_budget():
    category = input("\nEnter category: ").title()

    try:
        amount = float(input("Enter monthly budget: ₹"))

        if amount <= 0:
            print("Budget must be greater than zero!")
            return

        budgets[category] = amount
        save_data()

        print("Budget set successfully!")

    except ValueError:
        print("Invalid amount!")


# View budgets
def view_budgets():
    if not budgets:
        print("\nNo budgets set.")
        return

    month = datetime.today().strftime("%Y-%m")

    print("\n========== MONTHLY BUDGET ==========")

    for category, limit in budgets.items():

        spent = sum(
            t["amount"]
            for t in transactions
            if t["type"] == "Expense"
            and t["category"] == category
            and t["date"].startswith(month)
        )

        remaining = limit - spent

        print(f"\nCategory: {category}")
        print(f"Budget : ₹{limit:.2f}")
        print(f"Spent  : ₹{spent:.2f}")
        print(f"Left   : ₹{remaining:.2f}")

        if spent > limit:
            print("Warning: Budget exceeded!")
        else:
            print("Within budget.")


# Expense category report
def category_report():
    report = {}

    for t in transactions:
        if t["type"] == "Expense":
            category = t["category"]
            report[category] = report.get(category, 0) + t["amount"]

    if not report:
        print("\nNo expenses recorded.")
        return

    print("\n========== CATEGORY REPORT ==========")

    for category, amount in report.items():
        print(f"{category}: ₹{amount:.2f}")


# Daily, weekly and monthly reports
def generate_report():
    print("\n1. Daily Report")
    print("2. Weekly Report")
    print("3. Monthly Report")

    choice = input("Choose report: ")

    today = datetime.today().date()

    if choice == "1":
        start = today
        end = today

    elif choice == "2":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)

    elif choice == "3":
        start = today.replace(day=1)

        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)

        end = next_month - timedelta(days=1)

    else:
        print("Invalid choice!")
        return

    income = 0
    expenses = 0

    for t in transactions:
        transaction_date = datetime.strptime(t["date"], "%Y-%m-%d").date()

        if start <= transaction_date <= end:
            if t["type"] == "Income":
                income += t["amount"]
            else:
                expenses += t["amount"]

    print("\n========== REPORT ==========")
    print(f"From: {start}")
    print(f"To  : {end}")
    print(f"Income  : ₹{income:.2f}")
    print(f"Expenses: ₹{expenses:.2f}")
    print(f"Balance : ₹{income - expenses:.2f}")


# Simple text-based expense graph
def expense_graph():
    report = {}

    for t in transactions:
        if t["type"] == "Expense":
            category = t["category"]
            report[category] = report.get(category, 0) + t["amount"]

    if not report:
        print("\nNo expenses to display.")
        return

    print("\n========== EXPENSE GRAPH ==========")

    for category, amount in report.items():
        bars = int(amount / 100)

        print(f"{category:15} | {'█' * bars} ₹{amount:.2f}")


# Main menu
def main():
    load_data()

    while True:
        print("\n================================")
        print("         EXPENSE TRACKER")
        print("================================")
        print("1. Add Income / Expense")
        print("2. View Transactions")
        print("3. View Balance")
        print("4. Edit Transaction")
        print("5. Delete Transaction")
        print("6. Search Transactions")
        print("7. Set Budget")
        print("8. View Budgets")
        print("9. Category Report")
        print("10. Generate Daily/Weekly/Monthly Report")
        print("11. Expense Graph")
        print("12. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_transaction()

        elif choice == "2":
            view_transactions()

        elif choice == "3":
            show_balance()

        elif choice == "4":
            edit_transaction()

        elif choice == "5":
            delete_transaction()

        elif choice == "6":
            search_transaction()

        elif choice == "7":
            set_budget()

        elif choice == "8":
            view_budgets()

        elif choice == "9":
            category_report()

        elif choice == "10":
            generate_report()

        elif choice == "11":
            expense_graph()

        elif choice == "12":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice! Try again.")


main()