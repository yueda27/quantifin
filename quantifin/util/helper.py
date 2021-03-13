
def extract_prices(resp, code):
    return [period['close'] for period in resp[code]['prices']]