import unittest
import logging
from unittest.mock import patch
from smartbudget.analysis_module_1.insights import income_details, expense_details

logger = logging.getLogger(__name__)


class TestInsights(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=== [TestInsights] Preparing shared mocks ===")

    def setUp(self):
        logger.debug("[TestInsights] setUp: resetting temporary state")

    @patch("smartbudget.analysis_module_1.insights._load_split")
    def test_income_details(self, mock_load):
        logger.debug("[TestInsights] Running test_income_details")
        mock_load.return_value = (
            [type("Inc", (), {"describe": lambda self=None: "Income A"})()],
            []
        )
        output = income_details()
        self.assertEqual(len(output), 1)
        self.assertIn("Income", output[0])
        self.assertIsInstance(output, list)
        self.assertTrue(len(output[0]) > 0)

    @patch("smartbudget.analysis_module_1.insights._load_split")
    def test_expense_details(self, mock_load):
        logger.debug("[TestInsights] Running test_expense_details")
        mock_load.return_value = (
            [],
            [type("Exp", (), {"describe": lambda self=None: "Expense X"})()]
        )
        output = expense_details()
        self.assertEqual(len(output), 1)
        self.assertIn("Expense", output[0])
        self.assertIsInstance(output, list)
        self.assertTrue(len(output[0]) > 0)

    def tearDown(self):
        logger.debug("[TestInsights] tearDown: no state to clear")

    @classmethod
    def tearDownClass(cls):
        logger.info("=== [TestInsights] Cleanup complete ===")
