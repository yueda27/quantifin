import yahoofinancials as yf
import datetime
class Stock:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.YfApi = yf.YahooFinancials(self.stock_code)
        self.__beta = None 
        self.__cash_flow = None
        self.__income = None
        self.__balance_sheets = None

    @property
    def beta(self):
        if self.__beta == None:
            self.__beta = self.YfApi.get_beta()
        return self.__beta

    @property
    def cash_flow_stmts(self):
        if self.__cash_flow == None:
            self.__cash_flow =  self.YfApi.get_financial_stmts("annual", "cash")['cashflowStatementHistory'][self.stock_code]
        return self.__cash_flow
    
    @property
    def income_stmts(self):
        if self.__income == None:
            self.__income = self.YfApi.get_financial_stmts("annual", "income")['incomeStatementHistory'][self.stock_code]
        return self.__income
    
    @property
    def balance_sheet_stmts(self):
        if self.__balance_sheets == None:
            self.__balance_sheets = self.YfApi.get_financial_stmts("annual", "balance")['balanceSheetHistory'][self.stock_code]
        return self.__balance_sheets


    def full_year_dividend(self):
        now_date = datetime.datetime.now()
        start_of_year, end_of_year = self._get_FY_dividend_period(now_date)
        dividend_resp = self.YfApi.get_daily_dividend_data(start_of_year.strftime("%Y-%m-%d"), end_of_year.strftime("%Y-%m-%d"))
        return self._calculate_full_dividend(dividend_resp)
    
    def _get_FY_dividend_period(self, now: datetime.datetime):
        def current_year(now: datetime.datetime):
            this_year = now.year
            return [datetime.datetime(this_year, 1, 1), now]
        
        def previous_year(now: datetime.datetime):
            year = now.year - 1
            return [datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 30)]

        if (now.month == 12):
            return current_year(now) 
        return previous_year(now)

    def _calculate_full_dividend(self, dividend_resp: dict):
        dividends = [payout['amount'] for payout in dividend_resp[self.stock_code]]
        return round(sum(dividends), 3)

    def get_dividend_payout_ratio_history(self):
        ###Helper functions
        def get_date_key(input_dict: dict):
            return (list(input_dict.keys())[0])
        
        def calculate_payout(cash_flow):
            div_payout = abs(int(cash_flow['dividendsPaid']))
            net_income = int(cash_flow['netIncome'])
            if net_income < 0:
                return None
            return round(div_payout/net_income, 3)

        def get_payout_ratios(cf_stmts_list):
            result = {}
            for cash_flow in self.cash_flow_stmts:
                date_key = get_date_key(cash_flow)
                result[date_key] = calculate_payout(cash_flow[date_key])
            return result
        ## End of helper functions
        return get_payout_ratios(self.cash_flow_stmts)
    
    def get_avg_dividend_payout_ratio(self):
        div_history = self.get_dividend_payout_ratio_history()
        payout_list = [payout for payout in div_history.values()]
        return round(sum(payout_list) / len(payout_list), 3)
    

    

