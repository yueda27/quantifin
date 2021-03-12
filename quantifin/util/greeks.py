from statistics import stdev
from functools import reduce
from math import sqrt

def price_returns(price_list):
    combined_price = zip(price_list, price_list[1:])
    returns = []
    for i in combined_price:
        returns.append((i[0] / i[1]) - 1)
    return returns

def stdev_excess_return(price_returns, risk_free):
    def excess_returns(re, rf):
        return re - rf
    def calc_variance(accum, excess):
        return accum + (excess ** 2)
    excess = [excess_returns(re, risk_free) for re in price_returns]
    variance = reduce(calc_variance, excess,0)

    return round(sqrt(variance / (len(price_returns) - 1)), 5)

def sharpe_ratio_ex_post(price_list, risk_free):
    '''Calculating after the fact sharpe ratio'''
    re = price_returns(price_list)
    average_return = sum(re) / len(re)
    sigma = stdev_excess_return(re, risk_free)

    return round((average_return - risk_free) / sigma, 3)

def sharpe_ratio_ex_ante(expected_return, benchmark_rate, sigma):
    '''Predicting future sharpe ratio'''
    return round((expected_return - benchmark_rate) / sigma, 5)
    










'''TODO:
    Alpha
    Jensen Alpha
    R-Squared
'''