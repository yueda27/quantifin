import unittest
from unittest.mock import patch
from pathlib import Path
import json
import statistics

from quantifin.util.greeks import *


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.price_list = read_price_list(str(self.base_path) + "/resource/price_list.json")[::-1]
    
    def test_price_return(self):
        price_list_count = len(self.price_list)
        correct_price_returns = read_price_list(str(self.base_path) + "/resource/price_return.json")

        self.assertEqual(price_returns(self.price_list), correct_price_returns)
        self.assertEqual(len(price_returns(self.price_list)), price_list_count - 1)
    
    def test_stdev_excess_return(self):
        price_return = [0.0818, 0.1047, 0.0247, 0.044, 0.2524, 0.0520, 0.2278, 0.28, 0.0387, 0.0598, 0.0183, 0.0586, 0.0051, 0.0541, 0.0617]
        self.assertEqual(stdev_excess_return(price_return, 0.03), 0.08804)
    
    def test_sharpe_ratio(self):
        self.assertEqual(sharpe_ratio(self.price_list, 0.0001), 0.194)
    
    
def read_price_list(path):
    with open(path, "r") as r:
        return json.load(r)
