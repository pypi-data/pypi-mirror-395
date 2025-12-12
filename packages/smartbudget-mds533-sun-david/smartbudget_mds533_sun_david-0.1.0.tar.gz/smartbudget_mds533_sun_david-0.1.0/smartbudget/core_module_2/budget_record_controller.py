"""
BudgetRecordController (Step 3 Enhanced)
---------------------------------------

Enhancements added for Step 3:
    - Robust error and exception handling
    - All failures converted into SmartBudgetError
    - Defensive input validation
    - Ensures CLI never crashes due to bad input
"""

from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense
from smartbudget.entity.base_record import SmartBudgetError

from smartbudget.analysis_module_1.summary import (
    total_income, total_expenses, budget_balance
)
from smartbudget.analysis_module_1.insights import (
    income_details, expense_details, plot_expense_by_category
)

from smartbudget.file_io_module_3 import append_to_json


class BudgetRecordController:
    """Controller for managing financial records and user-facing operations."""

    def __init__(self):
        self.incomes = []
        self.expenses = []

    # --------------------------------------------------------
    # Display Functions
    # --------------------------------------------------------
    def show_summary(self):
        try:
            print("\n=== Budget Summary ===")
            print("Total Income:", total_income())
            print("Total Expenses:", total_expenses())
            print("Balance:", budget_balance())
            print("=======================\n")
        except Exception as e:
            raise SmartBudgetError(f"Failed to display summary: {e}")

    def show_income_details(self):
        try:
            print("\n=== Income Details ===")
            details = income_details()
            if not details:
                print("No incomes recorded.\n")
                return
            for d in details:
                print(" -", d)
            print()
        except Exception as e:
            raise SmartBudgetError(f"Failed to show income details: {e}")

    def show_expense_details(self):
        try:
            print("\n=== Expense Details ===")
            details = expense_details()
            if not details:
                print("No expenses recorded.\n")
                return
            for d in details:
                print(" -", d)
            print()
        except Exception as e:
            raise SmartBudgetError(f"Failed to show expense details: {e}")

    def show_expense_plot(self):
        try:
            print("\n=== Expense Visualization ===")
            print("Generating chart...")
            plot_expense_by_category()
            print("\n✔ Chart displayed!\n")
        except Exception as e:
            raise SmartBudgetError(f"Failed to display expense chart: {e}")

    # --------------------------------------------------------
    # Record Creation
    # --------------------------------------------------------
    def add_income(self):
        try:
            print("\n--- Add Income ---")
            name = input("Enter income name: ").strip()

            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                raise SmartBudgetError("Amount must be numeric.")

            source = input("Enter source: ").strip()

            inc = Income(name, amount, source)
            self.incomes.append(inc)

            try:
                append_to_json([inc])
            except Exception as e:
                raise SmartBudgetError(f"Failed to save income: {e}")

            print("\n✔ Income added:", inc.describe(), "\n")

        except SmartBudgetError as e:
            print(f"❌ Failed to add income: {e}")

        except Exception as e:
            print(f"❌ Unexpected add_income error: {e}")

    def add_expense(self):
        try:
            print("\n--- Add Expense ---")
            name = input("Enter expense name: ").strip()

            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                raise SmartBudgetError("Amount must be numeric.")

            category = input("Enter category: ").strip()

            exp = Expense(name, amount, category)
            self.expenses.append(exp)

            try:
                append_to_json([exp])
            except Exception as e:
                raise SmartBudgetError(f"Failed to save expense: {e}")

            print("\n✔ Expense added:", exp.describe(), "\n")

        except SmartBudgetError as e:
            print(f"❌ Failed to add expense: {e}")

        except Exception as e:
            print(f"❌ Unexpected add_expense error: {e}")
