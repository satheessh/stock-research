import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import demjson


def convert_string_to_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y')


def convert_string_to_float(str):
    return float(str)


def convert_date_to_string(dt):
    return dt.strftime("%Y-%b-%d")


def scrap_dividend_from_nasdaq(ex_date):
    r = requests.get(
        'http://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=' + convert_date_to_string(ex_date))
    soup = BeautifulSoup(r.text)
    dividend_table = soup.find('table', class_='DividendCalendar')
    data = []
    if dividend_table:
        table_body = dividend_table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            result = {}
            result['ticker'] = cols[0].find('a')['href'].split('/')[4]
            result['ex-dividend-date'] = (cols[1].text.strip())
            result['dividend'] = convert_string_to_float(cols[2].text.strip())
            result['annual-dividend'] = convert_string_to_float(cols[3].text.strip())
            result['announced-dividend-date'] = (cols[5].text.strip())
            data.append(result)
    return data


def scrap_dividend_from_thestreet(ex_date):
    r = requests.get(
        'https://www.thestreet.com/util/divs.jsp?date=' + ex_date.strftime("%m_%d_%Y"),
        headers={"User-Agent": "curl/7.49.1"})
    data = []
    if r.text:
        results = demjson.decode(r.text)
        for dividend_scrapped in results['results']:
            result = {}
            result['ticker'] = dividend_scrapped['symbol']
            result['ex-dividend-date'] = dividend_scrapped['exdate']
            result['dividend'] = convert_string_to_float(dividend_scrapped['amount'])
            data.append(result)
    return data


def get_next_30_days():
    start_date = datetime.now()
    data = []
    for num in range(1, 80):
        data = data + scrap_dividend_from_nasdaq(start_date + timedelta(days=num))
        data = data + scrap_dividend_from_thestreet(start_date + timedelta(days=num))
    # print(data)
    return data

# get_next_30_days()
