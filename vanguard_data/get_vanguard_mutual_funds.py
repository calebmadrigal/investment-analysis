# Parses one of the AJAX responses from this page:
#     https://investor.vanguard.com/mutual-funds/list#/mutual-funds/asset-class/month-end-returns
# Apparently, it's 300 tickers, so it's probably more than just the 127 advertised mutual funds

import re

with open('vanguard_fund_list_raw.txt', 'r') as f:
    raw_data = f.read()
    ticker_symbols = re.findall(r'"ticker":"(\w+)"', raw_data)
    with open('vanguard_mutual_funds.txt', 'w') as outf:
        outf.write('\n'.join(ticker_symbols)+'\n')

