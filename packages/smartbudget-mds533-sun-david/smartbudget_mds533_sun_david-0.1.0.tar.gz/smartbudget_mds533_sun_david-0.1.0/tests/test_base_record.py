import unittest
import logging
from smartbudget.entity.base_record import RecordBase, SmartBudgetError
from smartbudget.entity.constants import Limits

logger = logging.getLogger(__name__)


class TestRecordBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.default_name = "Sample"
        cls.default_amount = 20

    def setUp(self):
        self.record = RecordBase(self.default_name, self.default_amount)

    # --------------------------------------------------------
    # Normal behavior tests
    # --------------------------------------------------------
    def test_attributes(self):
        self.assertEqual(self.record.name, "Sample")
        self.assertEqual(self.record.amount, 20)
        self.assertIsInstance(self.record.name, str)
        self.assertGreaterEqual(self.record.amount, 0)

    def test_to_dict(self):
        d = self.record.to_dict()
        self.assertEqual(d["name"], "Sample")
        self.assertEqual(d["amount"], 20)
        self.assertEqual(d["type"], "RecordBase")

    def test_show(self):
        s = self.record.show()
        self.assertIn("Sample", s)
        self.assertIn("20.00", s)

    def test_repr_and_str(self):
        repr_str = repr(self.record)
        self.assertIn("RecordBase", repr_str)
        self.assertIn("Sample", repr_str)

        self.assertEqual(str(self.record), self.record.show())

    # --------------------------------------------------------
    # Validation error tests (name)
    # --------------------------------------------------------
    def test_empty_name_raises(self):
        with self.assertRaises(SmartBudgetError):
            RecordBase("", 10)

    def test_non_string_name_raises(self):
        with self.assertRaises(SmartBudgetError):
            RecordBase(123, 10)

    def test_long_name_raises(self):
        long_name = "X" * (Limits.MAX_NAME_LEN + 1)
        with self.assertRaises(SmartBudgetError):
            RecordBase(long_name, 10)

    # --------------------------------------------------------
    # Validation error tests (amount)
    # --------------------------------------------------------
    def test_amount_zero_raises(self):
        with self.assertRaises(SmartBudgetError):
            RecordBase("ABC", 0)

    def test_amount_non_numeric_raises(self):
        with self.assertRaises(SmartBudgetError):
            RecordBase("ABC", "hello")

    # --------------------------------------------------------
    # Exception raising inside show()
    # --------------------------------------------------------
    def test_show_error(self):
        # show() does not throw errors even with None name
        r = RecordBase("A", 10)
        r._name = None
        result = r.show()
        self.assertIn("None", result)

    # --------------------------------------------------------
    # Exception raising inside to_dict()
    # --------------------------------------------------------
    def test_to_dict_error(self):
        r = RecordBase("A", 10)
        r._amount = "INVALID"
        with self.assertRaises(SmartBudgetError):
            r.to_dict()

    @classmethod
    def tearDownClass(cls):
        pass
