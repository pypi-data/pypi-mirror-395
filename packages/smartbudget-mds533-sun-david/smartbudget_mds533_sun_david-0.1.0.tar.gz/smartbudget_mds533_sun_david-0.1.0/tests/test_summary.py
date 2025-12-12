import unittest
import logging
from unittest.mock import patch
from smartbudget.analysis_module_1.summary import total_income, total_expenses, budget_balance

logger = logging.getLogger(__name__)


class TestSummary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=== [TestSummary] Initializing shared resources ===")

    def setUp(self):
        logger.debug("[TestSummary] setUp: preparing mock data container")
        self.mock_income = [type("Obj", (), {"amount": 100})(),
                            type("Obj", (), {"amount": 50})()]
        self.mock_expense = [type("Obj", (), {"amount": 30})()]

    @patch("smartbudget.analysis_module_1.summary._load_split")
    def test_total_income(self, mock_load):
        logger.debug("[TestSummary] Running test_total_income")
        mock_load.return_value = (self.mock_income, [])
        self.assertEqual(total_income(), 150)
        self.assertIsInstance(total_income(), (int, float))
        self.assertGreater(total_income(), 0)
        self.assertNotEqual(total_income(), -999)

    @patch("smartbudget.analysis_module_1.summary._load_split")
    def test_budget_balance(self, mock_load):
        logger.debug("[TestSummary] Running test_budget_balance")
        mock_load.return_value = (self.mock_income, self.mock_expense)
        self.assertEqual(budget_balance(), 120)
        self.assertGreaterEqual(budget_balance(), 0)
        self.assertIsInstance(budget_balance(), (int, float))
        self.assertNotEqual(budget_balance(), None)

    def tearDown(self):
        logger.debug("[TestSummary] tearDown: clearing temporary containers")
        self.mock_income = None
        self.mock_expense = None

    @classmethod
    def tearDownClass(cls):
        logger.info("=== [TestSummary] Cleanup complete ===")
