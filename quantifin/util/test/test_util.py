import unittest
from unittest.mock import patch
from pathlib import Path
import json
from yahoofinancials import YahooFinancials

from quantifin.util.markets import Market
from quantifin.util import extract_prices, price_returns


class TestCase(unittest.TestCase):
    def setUp(self):
        #self.stock = Stock("AAPL")
        self.base_path = Path(__file__).parent
        self.price_list = read_price_list(str(self.base_path) + "/resource/price_list.json")[::-1]
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = json.load(f)
        return json_dict

    def test_get_market_price_list(self):
        index_price_list = Market.get_market_price_list(self.index_json)
        index_code = list(self.index_json.keys())[0]
        self.assertEqual(index_price_list, self.index_json[index_code]['prices']) 


    def test_get_market_return(self):
        annual_return = 13597.9658203125  / 7729.31982421875

        index_price_list = Market.get_market_price_list(self.index_json)
        self.assertAlmostEqual(Market.returns(index_price_list), annual_return, 3)
    
    def test_get_annualised_market_return(self):
        market_returns = Market.returns(Market.get_market_price_list(self.index_json))
        annualised_return = Market.annualise(market_returns, 2)
        self.assertEqual(annualised_return, (((13597.9658203125  / 7729.31982421875) ** (1/2)) - 1))
    
    @patch.object(YahooFinancials, "get_historical_price_data")
    def test_Market_obj_init(self, MockGetPrice):
        nasdaq = Market("NasdaqGS")
        self.assertTrue(nasdaq.market_code, "^IXIC")


    @patch.object(YahooFinancials, "get_historical_price_data")
    def test_Market_get_annualised_return(self, MockGetPrice):
        def get_price_side_effect(start, end, period):
            file_path = str(self.base_path) + "/resource/s&p_10_year_price.json"
            return self.read_json(file_path)

        MockGetPrice.side_effect = get_price_side_effect
        sp500 = Market("S&P")
        self.assertEqual(sp500.get_annualised_return(10), 0.1334)
    
    def test_extract_price(self):
        resp = self.read_json(str(self.base_path) + "/resource/historical_yield.json")
        correct  =[1.5199999809265137,1.1269999742507935,0.6980000138282776,0.621999979019165,0.6480000019073486,0.652999997138977,0.5360000133514404,0.6930000185966492,0.6769999861717224,0.8600000143051147,0.843999981880188,0.9169999957084656]
        self.assertEqual(extract_prices(resp, "^TNX"), correct)

    def test_price_return(self):
        price_list_count = len(self.price_list)
        price_list = [100, 80, 70, 40]
        result = [0.25, 0.1428571428571428, 0.75]
        correct_price_returns = read_price_list(str(self.base_path) + "/resource/price_return.json")
        
        self.assertEqual(price_returns(price_list), result)
        self.assertEqual(price_returns(self.price_list), correct_price_returns)
        self.assertEqual(len(price_returns(self.price_list)), price_list_count - 1)

def read_price_list(path):
    with open(path, "r") as r:
        return json.load(r)