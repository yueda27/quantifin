from statistics import stdev
from functools import reduce
from math import sqrt

def price_returns(price_list):
    combined_price = zip(price_list, price_list[1:])
    returns = []
    for i in combined_price:
        returns.append((i[0] / i[1]) - 1)
    return returns


def sharpe_ratio_ex_ante(expected_return, benchmark_rate, sigma):
    '''Predicting future sharpe ratio'''
    return round((expected_return - benchmark_rate) / sigma, 5)


def sharpe_ratio_ex_post(returns_list, benchmark):
    differential_return = [__calculate_differential_return(re, benchmark) for re in returns_list]
    sigma = stdev(differential_return)
    return round(__sample_average(differential_return) / sigma, 5)

def __calculate_differential_return(returns, benchmark):
    return abs(returns - benchmark)

def __sample_average(iterable):
    return sum(iterable) / len(iterable)








'''TODO:
    Alpha
    Jensen Alpha
    R-Squared
'''