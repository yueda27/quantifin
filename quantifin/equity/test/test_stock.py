import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from json import load
import yahoofinancials as yf
from quantifin.equity import Stock
from quantifin.equity.valuation import *
from quantifin.util import markets

@patch.object(yf.YahooFinancials, 'get_beta', return_value = 1.2)
class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = load(f)
        return json_dict

    def test_initialise_stock(self, MockGetBeta):
        apple = Stock("AAPL")
        self.assertEqual(yf.YahooFinancials.get_beta, MockGetBeta)
        self.assertTrue(MockGetBeta.called)
    
    def test_current_dividend(self, MockGetBeta):
        apple= Stock("AAPL")

        def get_current_dividend_side_effect():
            dividend_path = str(self.base_path) + "/resource/market_price.json"
            return self.read_json(dividend_path)
    
    def test_CAPM(self, MockGetBeta):
        req_rate_CAPM = CAPM(0.02, 0.1, 1.2)
        self.assertEqual(req_rate_CAPM, 0.116)
    
    def test_gordon_growth_model(self, MockGetBeta):
        current_dividend = 2.0 #NEEDS IMPLEMENTATION
        req_rate = CAPM(0.02, 0.10, 1.2)
        print(req_rate)
        growth_rate = 0.1 #NEEDS IMPLEMENTATION

        self.assertRaises(ValueError, gordon_growth_model, -2, req_rate, growth_rate)
        self.assertRaises(ValueError, gordon_growth_model, current_dividend, -0.116, growth_rate)
        self.assertEqual(gordon_growth_model(current_dividend, req_rate, growth_rate), 137.5)
        
        

