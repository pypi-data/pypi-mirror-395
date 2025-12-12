class SmartBudgetError(Exception):
    """SmartBudget project custom error type."""

    def __init__(self, message: str, context=None):
        super().__init__(message)
        self.message = f"[SmartBudget] {message}"   # 项目特色标签
        self.context = context

    def __str__(self):
        if self.context is not None:
            return f"{self.message} | Context: {self.context}"
        return self.message
