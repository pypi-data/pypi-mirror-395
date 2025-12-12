"""
Income (Step 3 Enhanced)
------------------------

Enhancements required for Project Step 3:
    - Robust try/except safety checks
    - All validation errors mapped to SmartBudgetError
    - Defensive programming for bad inputs
    - Fully compatible with unittest mocking
"""

from .base_record import RecordBase, SmartBudgetError


class Income(RecordBase):
    """
    Represents a single income record (always positive amount).

    Step 3 Enhancements:
        - Exception handling for invalid inputs
        - Convert all failures into SmartBudgetError
        - Safe normalization and defensive attribute access
    """

    def __init__(self, name: str, amount: float, source: str):
        try:
            # -------- Validation --------
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Income name must be a non-empty string.")

            if not isinstance(amount, (int, float)):
                raise TypeError("Income amount must be numeric.")

            if amount <= 0:
                raise ValueError("Income amount must be positive.")

            if not isinstance(source, str) or not source.strip():
                raise ValueError("Income source must be a non-empty string.")

            # -------- Call base class --------
            super().__init__(name.strip(), float(abs(amount)))

            # -------- Normalize --------
            self._source = source.strip().lower()

        except (TypeError, ValueError) as e:
            raise SmartBudgetError(f"Invalid Income initialization: {e}") from e
        except Exception as e:
            raise SmartBudgetError(f"Unexpected error creating Income: {e}") from e

    # --------------------------------------------------------
    # Properties — safe attribute access
    # --------------------------------------------------------
    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, value: str):
        try:
            if not isinstance(value, str):
                raise TypeError("Source must be a string.")
            if not value.strip():
                raise ValueError("Source must be a non-empty string.")

            self._source = value.strip().lower()

        except Exception as e:
            raise SmartBudgetError(f"Invalid income source: {e}") from e

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------
    def describe(self) -> str:
        try:
            return (
                "Income Record\n"
                f"  Name   : {self.name}\n"
                f"  Source : {self.source}\n"
                f"  Amount : {self.amount:.2f}\n"
            )
        except Exception as e:
            raise SmartBudgetError(f"Error generating Income description: {e}")

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        try:
            return {
                "type": "Income",
                "name": self.name,
                "amount": float(self.amount),
                "source": self.source,
            }
        except Exception as e:
            raise SmartBudgetError(f"Error serializing Income: {e}")
