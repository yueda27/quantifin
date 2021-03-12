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

def sortino_ratio(returns_list, benchmark):
    avg_return = (sum(returns_list) / len(returns_list)) - benchmark
    differential_return = [re - benchmark for re in returns_list]
    downside_deviation = __calculate_downside_deviation(returns_list, benchmark)
    return round(avg_return / downside_deviation, 3)

def __calculate_downside_deviation(iterable, benchmark):
    downside_deviation_list = [abs((it - benchmark) ** 2) for it in iterable if (it - benchmark) < 0]
    return sqrt(sum(downside_deviation_list)/ len(iterable))







'''TODO:
    Alpha
    Jensen Alpha
    R-Squared
'''