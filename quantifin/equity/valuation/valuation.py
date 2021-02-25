from quantifin.equity import Stock
from quantifin.util import markets

def CAPM(risk_free: float, market_premium: float, beta: float):
    return risk_free + beta * (market_premium - risk_free)