"""
SmartBudget: A simple household budget / smart budgeting package.

Subpackages:
- entity: entity record classes for incomes and expenses.
- analysis_module_1: functions for summaries and trends.
- file_io_module_3: helper functions to save and load data.
"""

from smartbudget.entity.income import Income
from smartbudget.entity.expense import  Expense
from .analysis_module_1.summary import total_income, total_expenses, budget_balance

__all__ = [
    "Expense",
    "Income",
    "total_income",
    "total_expenses",
    "budget_balance",
]
