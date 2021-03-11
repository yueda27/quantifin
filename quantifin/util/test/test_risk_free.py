
import unittest
from unittest.mock import patch
from pathlib import Path
import json

from quantifin.util import RiskFree


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.ten_year = RiskFree(10)
    
    def test_mapping(self):
        ten_year = RiskFree(10)
        self.assertEqual(ten_year.market_code, "^TNX")
        thirty_year = RiskFree(30)
        self.assertEqual(thirty_year.market_code, "^TYX")
        five_year = RiskFree(5)
        self.assertEqual(five_year.market_code, "^FVX")
        self.assertRaises(KeyError, RiskFree, 3)

    @patch.object(RiskFree, "get_prev_close_price", return_value = 1.52)
    def test_spot_yield(self, MockPrevPrice):
        self.assertEqual(self.ten_year.spot_yield, 0.0152)
        self.assertTrue(MockPrevPrice.called)
    
    @patch.object(RiskFree, "get_prev_close_price", return_value = None)
    def test_spot_yield_none(self, MockPrevPrice):
        self.assertEqual(self.ten_year.spot_yield, None)
