import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from json import load
import yahoofinancials as yf

from quantifin.equity import Stock


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
        
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = load(f)
        return json_dict

    @patch.object(yf.YahooFinancials, "get_beta", return_value = 1.2)
    def test_get_beta(self, MockGetBeta):
        stock = Stock("D05.SI")
        self.assertFalse(MockGetBeta.called)

        self.assertEqual(stock.beta, 1.2)
        self.assertTrue(MockGetBeta.called)
    
    @patch.object(yf.YahooFinancials, 'get_financial_stmts')
    def test_cash_flow_resp(self, MockGetFnStmts):
        MockGetFnStmts.side_effect = self.get_annual_CF_side_effect
        stock = Stock("D05.SI")
        self.assertFalse(MockGetFnStmts.called)

        self.assertEqual(type(stock.cash_flow_stmts), list)
        self.assertTrue(MockGetFnStmts.called)

    def get_annual_CF_side_effect(self, period, stmt_type):
        if( stmt_type == "cash"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/cash_flow_stmts.json'))