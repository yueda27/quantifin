from quantifin.equity import Stock
from quantifin.util import markets

def CAPM(risk_free: float, market_premium: float, beta: float):
    return risk_free + beta * (market_premium - risk_free)

def gordon_growth_valuation(current_dividend: float, req_rate: float, growth_rate: float):
    if  __any_negative_value([current_dividend, req_rate]):
        raise ValueError("Invalid value. Either current_dividend or required rate is negative")
    return round((current_dividend * (growth_rate + 1)) / (req_rate - growth_rate), 3)

def __any_negative_value(values: list):
    for val in values:
        if val < 0:
             return True
    return False

def forward_pe(payout_ratio: float, growth_rate: float, req_rate: float, eps: float):
    if __any_negative_value([payout_ratio, growth_rate, eps]):
        raise Warning("One or more of the values supplied is negative. This may reduce the effectiveness of the result")
    exp_payout = payout_ratio * (1 + growth_rate)
    forward_pe = exp_payout / (req_rate - growth_rate)
    return round(forward_pe * eps, 3)

'''
 TODO:
    Three stage Dividend Discount
 ''' 