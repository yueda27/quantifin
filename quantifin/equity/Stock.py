import yahoofinancials as yf
import datetime
class Stock:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.YfApi = yf.YahooFinancials(self.stock_code)
        self.beta = self.YfApi.get_beta()
    
    def full_year_dividend(self):
        now_date = datetime.datetime.now()
        start_of_year, end_of_year = self._get_full_year_dividend(now_date)
        dividend_resp = self.YfApi.get_daily_dividend_data(start_of_year.strftime("%Y-%m-%d"), end_of_year.strftime("%Y-%m-%d"))
        return self._calculate_full_dividend(dividend_resp)
    

    def _calculate_full_dividend(self, dividend_resp: dict):
        dividends = [payout['amount'] for payout in dividend_resp[self.stock_code]]
        return round(sum(dividends), 3)

    def _get_full_year_dividend(self, now: datetime.datetime):
        def current_year(now: datetime.datetime):
            this_year = now.year
            return [datetime.datetime(this_year, 1, 1), now]
        
        def previous_year(now: datetime.datetime):
            year = now.year - 1
            return [datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 30)]

        if (now.month == 12):
            return current_year(now) 
        return previous_year(now)