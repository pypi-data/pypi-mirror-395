# Structural adjustments reapplied by Yifu
"""
Summary functions for incomes and expenses.
Provides aggregation helpers and defensive handling for numeric amounts.

Additional inline comments clarify key processing steps.
"""
import logging
from typing import Iterable, List
from smartbudget.entity.income import Income
from smartbudget.entity.expense import  Expense
from smartbudget.file_io_module_3.json_io import load_from_json
from smartbudget.analysis_module_1.insights import _load_split



logger = logging.getLogger(__name__)


# ============================
# Internal validators
# ============================

def _validate_amounts(records: Iterable) -> None:
    """
    Ensures that all Income/Expense entries contain valid numeric amounts.
    Logs warnings if corrupted entries are detected.
    """
    for r in records:
        if not hasattr(r, "amount"):
            logger.warning(f"[summary] Record missing amount field: {r}")
        elif not isinstance(r.amount, (int, float)):
            logger.warning(f"[summary] Invalid amount type: {r.amount} ({type(r.amount)})")


def _safe_sum(records: List) -> float:
    """
    Safely sum the amounts of Income or Expense objects.
    Gracefully handles corrupted or unreadable entries.
    """
    total = 0.0

    for r in records:
        try:
            value = float(r.amount)
            total += value
        except Exception as exc:
            logger.error(f"[summary] Failed to read amount from {r}: {exc}")

    return round(total, 2)


# ============================
# Public API
# ============================

def total_income() -> float:
    """
    Return total income amount.
    Includes:
    - type validation
    - defensive summation
    - logging
    """
    incomes, _ = _load_split()

    logger.info(f"[summary] Calculating total income for {len(incomes)} entries.")
    _validate_amounts(incomes)

    total = _safe_sum(incomes)
    logger.debug(f"[summary] Total income computed: {total}")
    return total


def total_expenses() -> float:
    """
    Return total expense amount.
    Includes:
    - type validation
    - safe summation
    - logging
    """
    _, expenses = _load_split()

    logger.info(f"[summary] Calculating total expenses for {len(expenses)} entries.")
    _validate_amounts(expenses)

    total = _safe_sum(expenses)
    logger.debug(f"[summary] Total expenses computed: {total}")
    return total


def budget_balance() -> float:
    """
    Returns the final balance (income minus expenses).
    Includes error handling to ensure a fallback result is returned when needed.
    """
    try:
        income = total_income()
        expenses = total_expenses()
    except Exception as exc:
        logger.error(f"[summary] Failed to compute budget balance: {exc}")
        return 0.0

    balance = income - expenses
    logger.info(f"[summary] Budget balance computed: {balance}")

    return balance