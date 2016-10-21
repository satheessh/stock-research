import json

import datetime
import requests


def get_ticker_from_yahoo(tickers):
    # r = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/%s?lang=en-US&region=US&modules=financialData,calendarEvents&corsDomain=finance.yahoo.com' % 'ticker')
    split_array = lambda A, n=30: [A[i:i + n] for i in range(0, len(A), n)]
    ticker_arrays = split_array(tickers)
    ticker_map = {}
    for ticker_array in ticker_arrays:
        r = requests.get(
            "http://query.yahooapis.com/v1/public/yql?q=select symbol, LastTradePriceOnly from yahoo.finance.quotes where symbol in (\"%s\")&env=store://datatables.org/alltableswithkeys&format=json" % ",".join(
                ticker_array))
        for info in r.json()['query']['results']['quote']:
            ticker_map[info['symbol']] = info

    return ticker_map



def api_json_dump(r):
    try:
        return json.dumps(r.json(), indent=4, sort_keys=True)
    except:
        return str(r)

