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
        self.sample_return = [-0.06, 0.2, -0.1, 0.24, -0.14, 0.2, 0.2, 0.16, 0.14]
        self.period_benchmark =  [0.02, 0.03, 0.026, 0.01, 0.022, 0.022, 0.01, 0.04, 0.01]
    
    def test_calculate_differential_return(self):
        self.assertRaises(ValueError, calculate_differential_returns, self.sample_return, self.period_benchmark[:-1])
        correct_result = [0.08, 0.17, 0.126, 0.23, 0.162, 0.178, 0.19, 0.12, 0.13]
        self.assertEqual(calculate_differential_returns(self.sample_return, self.period_benchmark, absolute=True), correct_result)
        self.assertEqual(calculate_differential_returns(self.sample_return, self.period_benchmark, absolute=False), [-0.08, 0.17, -0.126, 0.23, -0.162, 0.178, 0.19, 0.12, 0.13])

    def test_sharpe_ratio_ex_post(self):
        returns = price_returns(self.price_list)
        benchmark = [0.02 for i in range(len(self.sample_return))]
        self.assertEqual(sharpe_ratio_ex_post(self.sample_return, benchmark), 3.6141)
        self.assertEqual(sharpe_ratio_ex_post(returns, [0.005 for i in range(len(returns))]), 1.06527)
    
    def test_sharpe_ratio_ex_ante(self):
        self.assertEqual(sharpe_ratio_ex_ante(0.1, 0.03, 0.16), 0.43750)

    def test_sortino_ratio(self):
        return_rates = [0.17, 0.15, 0.23, -0.05, 0.12, 0.09, 0.13, -0.04]
        self.assertRaises(ValueError, sortino_ratio, self.sample_return, self.period_benchmark[:-1])
        self.assertEqual(sortino_ratio(return_rates, [0 for i in range(len(return_rates))]), 4.417)
        self.assertEqual(sortino_ratio(return_rates, [0.03 for i in range(len(return_rates))]), 1.863)
    
    def test_alpha(self):
        self.assertEqual(alpha(0.1, 0.08, 0.03, 1.2), 0.01) 
    
def read_price_list(path):
    with open(path, "r") as r:
        return json.load(r)
