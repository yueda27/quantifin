import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from json import load
import yahoofinancials as yf
from datetime import datetime

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

    def test_get_full_year(self, MockGetBeta):
        stock = Stock("AAPL")
        dec = datetime(2019, 12, 10)
        self.assertEqual(stock._get_full_year(dec), [datetime(2019, 1, 1), dec])

        not_dec = datetime(2019, 11, 29)
        self.assertEqual(stock._get_full_year(not_dec), [datetime(2018, 1, 1), datetime(2018, 12, 30)])

    def test_calculate_dividend(self, MockGetBeta):
        stock = Stock("D05.SI")
        dividend_resp = self.read_json(str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json")
        self.assertEqual(stock._calculate_full_dividend(dividend_resp), 1.35)

    @patch.object(yf.YahooFinancials, 'get_daily_dividend_data')
    def test_get_current_dividend(self, MockDividend, MockGetBeta):
        def get_dividend_side_effect(start_date, end_date):
            dividend_path = str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json"
            return self.read_json(dividend_path)
            
        MockDividend.side_effect = get_dividend_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.full_year_dividend(), 1.35)

    def test_gordon_growth_valuation(self, MockGetBeta):
        current_dividend = 2.0 #NEEDS IMPLEMENTATION
        req_rate = CAPM(0.02, 0.10, 1.2)
        growth_rate = 0.1 #NEEDS IMPLEMENTATION

        self.assertRaises(ValueError, gordon_growth_valuation, -2, req_rate, growth_rate)
        self.assertRaises(ValueError, gordon_growth_valuation, current_dividend, -0.116, growth_rate)
        self.assertEqual(gordon_growth_valuation(current_dividend, req_rate, growth_rate), 137.5)
        
        

