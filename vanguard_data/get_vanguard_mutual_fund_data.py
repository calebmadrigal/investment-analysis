import time
import datetime
import urllib
from urllib.request import urlopen

def get_date_filter(start_date_str, end_date_str):
    """ Given date strings in this format: 2016-01-01, return the filters needed for yahoo finance charts. """
    (start_year, start_month, start_day) = start_date_str.split('-')
    (end_year, end_month, end_day) = end_date_str.split('-')

    # Yahoo finance starts months with '0', so subtract 1 from the months
    start_month = str(int(start_month) - 1)
    end_month = str(int(end_month) - 1)

    date_filter_str = '&a={}&b={}&c={}&d={}&e={}&f={}'.format(start_month, start_day, start_year,
                                                              end_month, end_day, end_year)
    return date_filter_str

def get_csv_data(symbol, start_date, end_date):
    """ Get mutual fund CSV data from Yahoo Finance.

    Parameters:
        symbol - e.g. VTSAX

    Request URL will look like:
        http://chart.finance.yahoo.com/table.csv?s=VTSAX&a=0&b=2&c=2000&d=8&e=14&f=2016&g=d&ignore=.csv

    """
    url_template = 'http://chart.finance.yahoo.com/table.csv?s={}{}&g=d&ignore=.csv'
    request_url = url_template.format(symbol, get_date_filter(start_date, end_date))
    print('Getting symbol: {} from {} to {} with url: {}'.format(symbol, start_date, end_date, request_url))
    csv_data = urlopen(request_url).read()
    return csv_data

if __name__ == '__main__':
    start_date = '1990-01-01'
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')  # Today's date
    vanguard_mutual_fund_symbols = [line.strip() for line in open('vanguard_mutual_funds.txt', 'r').readlines()]

    for symbol in vanguard_mutual_fund_symbols:
        try:
            csv_data = get_csv_data(symbol, start_date, end_date)
            print('\tSaved data to {}'.format(symbol+'.csv'))
            with open(symbol+'.csv', 'wb') as f:
                f.write(csv_data)
        except urllib.error.HTTPError as e:
            print('Error getting {}: {}'.format(symbol, e))

        time.sleep(2)  # Don't freak out Yahoo Finance

