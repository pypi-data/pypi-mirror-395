# Structural adjustments reapplied by Yifu
from .summary import (
    total_income,
    total_expenses,
    budget_balance
)

from .insights import (
    expense_details,
    income_details,
    plot_expense_by_category
)




__all__ = [
    # summary
    "total_income",
    "total_expenses",
    "budget_balance",

    # insights
    "expense_details",
    "income_details",

    # optional plotting functions (if present)
    "plot_expense_by_category",
]

