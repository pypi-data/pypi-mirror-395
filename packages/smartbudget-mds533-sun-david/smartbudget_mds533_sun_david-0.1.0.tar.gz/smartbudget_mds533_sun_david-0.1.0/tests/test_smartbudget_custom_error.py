import unittest
from smartbudget.customized_exception import SmartBudgetError


class TestSmartBudgetError(unittest.TestCase):

    def test_basic_message(self):
        err = SmartBudgetError("Something went wrong")
        self.assertIn("[SmartBudget] Something went wrong", str(err))

    def test_context_included(self):
        err = SmartBudgetError("Failed", context={"id": 10})
        out = str(err)
        self.assertIn("[SmartBudget] Failed", out)
        self.assertIn("Context: {'id': 10}", out)

    def test_no_context(self):
        err = SmartBudgetError("Hello")
        self.assertEqual(str(err), "[SmartBudget] Hello")

    def test_raise_and_catch(self):
        with self.assertRaises(SmartBudgetError):
            raise SmartBudgetError("Boom!", context="test-case")
