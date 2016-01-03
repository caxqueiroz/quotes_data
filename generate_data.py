import sqlite3
import json
import requests
from json import JSONDecodeError


def load_company(filename):
    sql = 'select symbol, name, exchange from companies'
    conn = sqlite3.connect(filename)
    c = conn.cursor().execute(sql)
    results = []
    columns = ['symbol', 'name', 'exchange']
    for row in c.fetchall():
        results.append(dict(zip(columns, row)))
    conn.close()
    return results


def get_quote(symbol):
    response = requests.get(quote_url % symbol)
    return response.text


def get_value(key, dict):
    if key in dict:
        return dict[key]


def create_stock():

    stock_internal = {}

    symbol = get_value('symbol', company)
    quote = json.loads(get_quote(symbol))
    stock_internal['Status'] = get_value('Status', quote)
    stock_internal['CompanyName'] = get_value('name', company)
    stock_internal['Exchange'] = get_value('exchange', company)
    stock_internal['Symbol'] = get_value('Symbol', quote)
    stock_internal['LastPrice'] = get_value('LastPrice', quote)
    stock_internal['Change'] = get_value('Change', quote)
    stock_internal['ChangePercent'] = get_value('ChangePercent', quote)
    stock_internal['Timestamp'] = get_value('Timestamp', quote)
    stock_internal['MSDate'] = get_value('MSDate', quote)
    stock_internal['MarketCap'] = get_value('MarketCap', quote)
    stock_internal['Volume'] = get_value('Volume', quote)
    stock_internal['ChangeYTD'] = get_value('ChangeYTD', quote)
    stock_internal['ChangePercentYTD'] = get_value('ChangePercentYTD', quote)
    stock_internal['High'] = get_value('High', quote)
    stock_internal['Low'] = get_value('Low', quote)
    stock_internal['Open'] = get_value('Open', quote)
    return stock_internal


if __name__ == '__main__':
    company_url = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=%s'
    quote_url = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=%s'
    companies = load_company('/Users/cq/Downloads/quotes_and_companies.sqlite')
    stocks = []
    f = open('data.json', 'w')

    for company in companies:
        try:

            stock = create_stock()
            f.write(json.dumps(stock) + '\n')
            f.flush()

        except JSONDecodeError as detail:
            print('error processing data: ', detail)

    f.close()
