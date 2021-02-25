import unittest
from unittest.mock import patch, MagicMock
import yahoofinancials as yf
from quantifin.equity import Stock
from quantifin.equity.valuation import CAPM

class TestCase(unittest.TestCase):

    @patch('yahoofinancials.YahooFinancials.get_beta')
    def test_initialise_stock(self, MockGetBeta):
        MockGetBeta.return_value = 1.2
        apple = Stock("AAPL")
        self.assertEqual(yf.YahooFinancials.get_beta, MockGetBeta)
        self.assertTrue(MockGetBeta.called)
    
    def test_CAPM(self):
        req_rate_CAPM = CAPM(2, 10, 1.2)
        self.assertEqual(req_rate_CAPM, 11.6)
    
    
    
    

