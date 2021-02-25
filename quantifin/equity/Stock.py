import yahoofinancials as yf
class Stock:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.YfApi = yf.YahooFinancials(self.stock_code)
        self.beta = self.YfApi.get_beta()