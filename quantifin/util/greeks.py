from statistics import stdev
from functools import partial

def price_returns(price_list):
    combined_price = zip(price_list, price_list[1:])
    returns = []
    for i in combined_price:
        returns.append((i[0] / i[1]) - 1)
    return returns

def stdev_excess_return(price_returns, risk_free):
    def excess_returns(re, rf):
        return re - rf

    excess = map(partial(excess_returns, rf=risk_free), price_returns)
    return round(stdev(excess), 5)

def sharpe_ratio(price_list, risk_free):
    re = price_returns(price_list)
    average_return = sum(re) / len(re)
    sigma = stdev_excess_return(re, risk_free)

    return round((average_return - risk_free) / sigma, 3)








'''TODO:
    Sharpe Ratio
    Sortino Ratio
    Alpha
    Jensen Alpha
    R-Squared
'''