import unittest
from pathlib import Path
import json

from quantifin.util import markets


class TestCase(unittest.TestCase):
    def setUp(self):
        #self.stock = Stock("AAPL")
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = json.load(f)
        return json_dict

    def test_get_market_price_list(self):
        index_price_list = markets.get_market_price_list(self.index_json)
        index_code = list(self.index_json.keys())[0]
        self.assertEqual(index_price_list, self.index_json[index_code]['prices']) 


    def test_get_market_return(self):
        annual_return = (13597.9658203125 - 7729.31982421875) / 7729.31982421875

        index_price_list = markets.get_market_price_list(self.index_json)
        self.assertAlmostEqual(markets.returns(index_price_list), annual_return, 3)

    # def test_get_required_rate_of_return(self):
    #     self.stock.beta = 1.3
    #     self.stock.risk_free = 2
    #     self.assertEqual(self.stock.required_rate_of_return(), 2 + 1.3())

