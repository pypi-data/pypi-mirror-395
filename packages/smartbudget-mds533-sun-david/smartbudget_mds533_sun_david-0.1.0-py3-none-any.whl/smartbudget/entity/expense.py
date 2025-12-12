from .base_record import RecordBase, SmartBudgetError

from .base_record import  SmartBudgetError
class Expense(RecordBase):
    """
    Represents a single expense record.

    Step 3 Enhancements:
        - try/except wrapping for safer error handling
        - All validation errors converted into SmartBudgetError
        - Defensive programming: avoid bad category values
    """

    def __init__(self, name: str, amount: float, category: str):
        try:
            # ---- Validation ----
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Expense name must be a non-empty string.")

            if not isinstance(amount, (int, float)):
                raise TypeError("Expense amount must be numeric.")

            if amount <= 0:
                raise ValueError("Expense amount must be positive.")

            if not isinstance(category, str) or not category.strip():
                raise ValueError("Expense category must be a non-empty string.")

            # ---- Call base class (handles name + amount validation) ----
            super().__init__(name.strip(), float(abs(amount)))

            # ---- Normalize category ----
            self._category = category.strip().lower()

        except (TypeError, ValueError) as e:
            raise SmartBudgetError(f"Invalid Expense initialization: {e}") from e
        except Exception as e:
            raise SmartBudgetError(f"Unexpected error creating Expense: {e}") from e

    # --------------------------------------------------------
    # Properties (safe attribute access)
    # --------------------------------------------------------
    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        try:
            if not isinstance(value, str):
                raise TypeError("Category must be a string.")

            if not value.strip():
                raise ValueError("Category must be a non-empty string.")

            self._category = value.strip().lower()

        except Exception as e:
            raise SmartBudgetError(f"Invalid category: {e}") from e

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------
    def describe(self) -> str:
        try:
            return (
                "Expense Record\n"
                f"  Name     : {self.name}\n"
                f"  Category : {self.category}\n"
                f"  Amount   : {self.amount:.2f}\n"
            )
        except Exception as e:
            raise SmartBudgetError(f"Error generating Expense description: {e}")

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        try:
            return {
                "type": "Expense",
                "name": self.name,
                "amount": float(self.amount),
                "category": self.category,
            }
        except Exception as e:
            raise SmartBudgetError(f"Error serializing Expense: {e}")
