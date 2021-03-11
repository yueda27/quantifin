
import unittest
from unittest.mock import patch
from pathlib import Path
import json

from quantifin.util import RiskFree


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
    
    def test_mapping(self):
        ten_year = RiskFree(10)
        self.assertEqual(ten_year.market_code, "^TNX")
        thirty_year = RiskFree(30)
        self.assertEqual(thirty_year.market_code, "^TYX")
        five_year = RiskFree(5)
        self.assertEqual(five_year.market_code, "^FVX")
        self.assertRaises(KeyError, RiskFree, 3)

