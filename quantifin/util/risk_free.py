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

