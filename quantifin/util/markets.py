import yahoofinancials as yf 
from enum import Enum

EXCHANGES = {"NasdaqGS": "^IXIC",
            }
    

def returns(index: str, market_price_list: list):
    market_price_list = market_price_list[index]['prices']
    start_price = market_price_list[0]['close']
    end_price = market_price_list[-1]['close']
    market_return = ((end_price - start_price) / start_price)
    return market_return
