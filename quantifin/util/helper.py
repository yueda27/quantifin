
def extract_prices(resp, code):
    return [period['close'] for period in resp[code]['prices']]

def price_returns(price_list):
    combined_price = zip(price_list, price_list[1:])
    returns = []
    for i in combined_price:
        returns.append((i[0] / i[1]) - 1)
    return returns