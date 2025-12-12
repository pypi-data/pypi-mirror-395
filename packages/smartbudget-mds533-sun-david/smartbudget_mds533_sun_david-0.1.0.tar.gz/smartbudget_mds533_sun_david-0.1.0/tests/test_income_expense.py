import unittest
import logging
from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense
from smartbudget.entity.base_record import SmartBudgetError

logger = logging.getLogger(__name__)


class TestIncomeExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=== [TestIncomeExpense] setUpClass ===")
        cls.sample_income = Income("Salary", 3000, "Work")
        cls.sample_expense = Expense("Food", 20, "Groceries")

    def setUp(self):
        logger.debug("[TestIncomeExpense] setUp")
        self.income = Income("Gift", 100, "Friend")
        self.expense = Expense("Taxi", 15, "Transport")

    # ------------------------------------------------------
    # Income — 正常行为
    # ------------------------------------------------------
    def test_income_normal(self):
        self.assertEqual(self.income.name, "Gift")
        self.assertEqual(self.income.amount, 100)
        # source 会被规范成小写
        self.assertEqual(self.income.source, "friend")
        self.assertIn("Income Record", self.income.describe())

    def test_income_to_dict(self):
        d = self.income.to_dict()
        self.assertEqual(d["type"], "Income")
        self.assertEqual(d["name"], "Gift")
        self.assertEqual(d["amount"], 100)
        self.assertEqual(d["source"], "friend")

    # ------------------------------------------------------
    # Expense — 正常行为
    # ------------------------------------------------------
    def test_expense_normal(self):
        self.assertEqual(self.expense.name, "Taxi")
        self.assertEqual(self.expense.amount, 15)
        self.assertEqual(self.expense.category, "transport")
        self.assertIn("Expense Record", self.expense.describe())

    def test_expense_to_dict(self):
        d = self.expense.to_dict()
        self.assertEqual(d["type"], "Expense")
        self.assertEqual(d["name"], "Taxi")
        self.assertEqual(d["amount"], 15)
        self.assertEqual(d["category"], "transport")

    # ------------------------------------------------------
    # Income — 非法输入，触发 SmartBudgetError
    # ------------------------------------------------------
    def test_income_invalid_init(self):
        # name 为空
        with self.assertRaises(SmartBudgetError):
            Income("", 10, "Work")

        # amount 为 0
        with self.assertRaises(SmartBudgetError):
            Income("Pay", 0, "Work")

        # amount 非数字
        with self.assertRaises(SmartBudgetError):
            Income("Pay", "XYZ", "Work")

        # source 为空
        with self.assertRaises(SmartBudgetError):
            Income("Pay", 10, "")

    def test_income_invalid_source_setter(self):
        with self.assertRaises(SmartBudgetError):
            self.income.source = ""    # 空字符串

        with self.assertRaises(SmartBudgetError):
            self.income.source = 123   # 非字符串

    # ------------------------------------------------------
    # Expense — 非法输入，触发 SmartBudgetError
    # ------------------------------------------------------
    def test_expense_invalid_init(self):
        with self.assertRaises(SmartBudgetError):
            Expense("", 10, "Food")    # name 为空

        with self.assertRaises(SmartBudgetError):
            Expense("Cat", 0, "Food")  # amount 为 0

        with self.assertRaises(SmartBudgetError):
            Expense("Cat", "XYZ", "Food")  # amount 非数字

        with self.assertRaises(SmartBudgetError):
            Expense("Cat", 10, "")     # category 为空

    def test_expense_invalid_category_setter(self):
        with self.assertRaises(SmartBudgetError):
            self.expense.category = ""   # 空字符串

        with self.assertRaises(SmartBudgetError):
            self.expense.category = 999  # 非字符串

    def tearDown(self):
        logger.debug("[TestIncomeExpense] tearDown")
        self.income = None
        self.expense = None

    @classmethod
    def tearDownClass(cls):
        logger.info("=== [TestIncomeExpense] tearDownClass ===")
