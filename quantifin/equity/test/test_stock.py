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
    
    #################
    #Dividend testing
    #################
    def test_get_FY_dividend_period(self, MockGetBeta):
        stock = Stock("AAPL")
        dec = datetime(2019, 12, 10)
        self.assertEqual(stock._get_FY_dividend_period(dec), [datetime(2019, 1, 1), dec])

        not_dec = datetime(2019, 11, 29)
        self.assertEqual(stock._get_FY_dividend_period(not_dec), [datetime(2018, 1, 1), datetime(2018, 12, 30)])

    def test_calculate_dividend(self, MockGetBeta):
        stock = Stock("D05.SI")
        dividend_resp = self.read_json(str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json")
        self.assertEqual(stock._calculate_full_dividend(dividend_resp), 1.35)

    @patch.object(yf.YahooFinancials, 'get_daily_dividend_data')
    def test_get_current_dividend(self, MockDividend, MockGetBeta):
            
        MockDividend.side_effect = self.get_dividend_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.full_year_dividend(), 1.35)
    
    #Payout Ratio tests
    @patch.object(yf.YahooFinancials, 'get_financial_stmts')
    def test_get_avg_payout_ratio(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_annual_CF_side_effect
        stock = Stock("D05.SI")
        cf = stock.YfApi.get_financial_stmts('annual', 'cash')
        correct = {'2020-12-31': 0.511, '2019-12-31': 0.615, '2018-12-31': 0.565, '2017-12-31': 0.315}
        self.assertEqual(stock.get_dividend_payout_ratio_history(), correct)
        self.assertEqual(stock.get_avg_dividend_payout_ratio(), 0.501)



    @patch.object(yf.YahooFinancials, 'get_daily_dividend_data')
    def test_gordon_growth_valuation(self, MockDividend, MockGetBeta):
        MockDividend.side_effect = self.get_dividend_side_effect
        stock = Stock('D05.SI')
        current_dividend = stock.full_year_dividend()
        req_rate = CAPM(0.02, 0.10, 1.2)
        growth_rate = 0.1 #NEEDS IMPLEMENTATION

        self.assertRaises(ValueError, gordon_growth_valuation, -2, req_rate, growth_rate)
        self.assertRaises(ValueError, gordon_growth_valuation, current_dividend, -0.116, growth_rate)
        self.assertEqual(gordon_growth_valuation(current_dividend, req_rate, growth_rate), 92.81)
    

    def get_dividend_side_effect(self, start_date, end_date):
        dividend_path = str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json"
        return self.read_json(dividend_path)
    
    def get_annual_CF_side_effect(self, period, stmt_type):
        if( stmt_type == "cash"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/cash_flow_stmts.json'))
        

