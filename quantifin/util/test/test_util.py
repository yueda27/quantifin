import unittest
from pathlib import Path
import json

from quantifin.util import markets


class TestCase(unittest.TestCase):
    def setUp(self):
        #self.stock = Stock("AAPL")
        self.base_path = Path(__file__).parent
    
    def test_get_market_return(self):
        file_path = str(self.base_path) + "/resource/market_price.json" 
        with open (file_path) as f:
            index_price = json.load(f)

        annual_return = (13597.9658203125 - 7729.31982421875) / 7729.31982421875

        index_code = list(index_price.keys())[0]
        self.assertAlmostEqual(markets.returns(index_code, index_price), annual_return, 3)

    # def test_get_required_rate_of_return(self):
    #     self.stock.beta = 1.3
    #     self.stock.risk_free = 2
    #     self.assertEqual(self.stock.required_rate_of_return(), 2 + 1.3())

