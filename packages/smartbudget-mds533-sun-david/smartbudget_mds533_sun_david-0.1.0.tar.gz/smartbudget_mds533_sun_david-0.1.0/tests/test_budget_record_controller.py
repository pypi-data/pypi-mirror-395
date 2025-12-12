import unittest
from unittest.mock import patch, MagicMock

from smartbudget.core_module_2.budget_record_controller import BudgetRecordController
from smartbudget.entity.base_record import SmartBudgetError


class TestBudgetRecordController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[BudgetRecordController] setUpClass")

    def setUp(self):
        self.controller = BudgetRecordController()

    # ----------------------------------------------------------
    # add_income — normal path
    # ----------------------------------------------------------
    @patch("smartbudget.core_module_2.budget_record_controller.append_to_json")
    def test_add_income(self, mock_append):
        with patch("builtins.input", side_effect=["Salary", "3000", "Work"]):
            self.controller.add_income()

        self.assertEqual(len(self.controller.incomes), 1)
        inc = self.controller.incomes[0]

        self.assertEqual(inc.name, "Salary")
        self.assertEqual(inc.amount, 3000)
        self.assertEqual(inc.source, "work")

        mock_append.assert_called_once()

    # ----------------------------------------------------------
    # add_expense — normal path
    # ----------------------------------------------------------
    @patch("smartbudget.core_module_2.budget_record_controller.append_to_json")
    def test_add_expense(self, mock_append):
        with patch("builtins.input", side_effect=["Taxi", "15", "Transport"]):
            self.controller.add_expense()

        self.assertEqual(len(self.controller.expenses), 1)
        exp = self.controller.expenses[0]

        self.assertEqual(exp.name, "Taxi")
        self.assertEqual(exp.amount, 15)
        self.assertEqual(exp.category, "transport")

        mock_append.assert_called_once()

    # ----------------------------------------------------------
    # add_income — invalid numeric input (cover SmartBudgetError branch)
    # ----------------------------------------------------------
    def test_add_income_invalid_amount(self):
        with patch("builtins.input", side_effect=["Gift", "abc", "Friend"]):
            # Should not add to list
            self.controller.add_income()

        self.assertEqual(len(self.controller.incomes), 0)

    # ----------------------------------------------------------
    # add_expense — invalid numeric input
    # ----------------------------------------------------------
    def test_add_expense_invalid_amount(self):
        with patch("builtins.input", side_effect=["Lunch", "xx", "Food"]):
            self.controller.add_expense()

        self.assertEqual(len(self.controller.expenses), 0)

    # ----------------------------------------------------------
    # append_to_json fails — cover inner try/except
    # ----------------------------------------------------------
    @patch("smartbudget.core_module_2.budget_record_controller.append_to_json")
    def test_add_income_save_error(self, mock_append):
        mock_append.side_effect = Exception("disk write fail")

        with patch("builtins.input", side_effect=["Salary", "1000", "Work"]):
            self.controller.add_income()

        # Should record income, but print failure message
        self.assertEqual(len(self.controller.incomes), 1)

    @patch("smartbudget.core_module_2.budget_record_controller.append_to_json")
    def test_add_expense_save_error(self, mock_append):
        mock_append.side_effect = Exception("disk write fail")

        with patch("builtins.input", side_effect=["Taxi", "9", "Transport"]):
            self.controller.add_expense()

        self.assertEqual(len(self.controller.expenses), 1)

    # ----------------------------------------------------------
    # Display functions (print only)
    # ----------------------------------------------------------
    @patch("builtins.print")
    def test_show_summary(self, mock_print):
        self.controller.show_summary()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    def test_show_income_details(self, mock_print):
        self.controller.show_income_details()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    def test_show_expense_details(self, mock_print):
        self.controller.show_expense_details()
        self.assertTrue(mock_print.called)

    @patch("smartbudget.core_module_2.budget_record_controller.plot_expense_by_category")
    @patch("builtins.print")
    def test_show_expense_plot(self, mock_print, mock_plot):
        self.controller.show_expense_plot()
        mock_plot.assert_called_once()

    def tearDown(self):
        self.controller = None

    @classmethod
    def tearDownClass(cls):
        print("[BudgetRecordController] tearDownClass\n")
