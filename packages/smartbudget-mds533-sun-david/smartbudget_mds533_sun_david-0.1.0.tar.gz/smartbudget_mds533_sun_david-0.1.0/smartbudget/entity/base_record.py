from smartbudget.entity.constants import Limits
from smartbudget.customized_exception import SmartBudgetError





class RecordBase:
    """
    Base class for financial records such as Income and Expense.

    Added in Step 3:
        - Robust error handling (try/except wrappers)
        - Custom SmartBudgetError exception
        - More descriptive validation errors
    """

    def __init__(self, name: str, amount: float):
        try:
            self.name = name       # triggers validation
            self.amount = amount   # triggers validation
        except (ValueError, TypeError) as e:
            # convert all validation failures into app-level exception
            raise SmartBudgetError(f"Invalid record initialization: {e}") from e
        except Exception as e:
            raise SmartBudgetError(f"Unexpected error creating RecordBase: {e}") from e

    # --------------------------------------------------------
    # Properties — safe attribute access
    # --------------------------------------------------------
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        try:
            self._validate_name(value)
            self._name = value.strip()
        except Exception as e:
            raise SmartBudgetError(f"Invalid name: {e}") from e

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        try:
            self._validate_amount(value)
            self._amount = float(value)
        except Exception as e:
            raise SmartBudgetError(f"Invalid amount: {e}") from e

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------
    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if len(name) > Limits.MAX_NAME_LEN:
            raise ValueError(
                f"Name cannot exceed {Limits.MAX_NAME_LEN} characters."
            )

    def _validate_amount(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be numeric.")
        if amount == 0:
            raise ValueError("Amount cannot be zero.")

    # --------------------------------------------------------
    # Public Interface
    # --------------------------------------------------------
    def show(self) -> str:
        try:
            return f"{self.name}: {self.amount:.2f}"
        except Exception as e:
            raise SmartBudgetError(f"Error generating display string: {e}")

    def to_dict(self) -> dict:
        try:
            return {
                "type": self.__class__.__name__,
                "name": self.name,
                "amount": float(self.amount),
            }
        except Exception as e:
            raise SmartBudgetError(f"Serialization failed: {e}")

    # --------------------------------------------------------
    # Debug & Utility
    # --------------------------------------------------------
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, amount={self.amount!r})"

    def __str__(self):
        return self.show()
