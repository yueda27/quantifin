from yahoofinancials import YahooFinancials

YIELD_MAPPING = {
    5: "^FVX",
    10: "^TNX",
    30: "^TYX",
}

class RiskFree(YahooFinancials):
    def __init__(self, year):
        def __get_yield_mapping(year):
            try:
                return YIELD_MAPPING[year]
            except KeyError:
                raise KeyError(f"Year: {year} provided does not have an index")

        self.market_code = __get_yield_mapping(year)
        super().__init__(self.market_code)
        self.year = year
        self.__spot_yield = None

    @property
    def spot_yield(self):
        if not self.__spot_yield:
            self.__spot_yield = self.get_prev_close_price()

        if self.__spot_yield is None:
            return None
        return self.__spot_yield / 100