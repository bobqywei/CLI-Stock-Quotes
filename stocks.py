import datetime
import time
from termcolor import colored, cprint
import os
import urllib.request

with open('stocks.txt', 'r') as f:
    lines = f.readlines()

STOCKS = [l.strip() for l in lines]

URL = 'https://web.tmxmoney.com/quote.php?qm_symbol={}'

headers = ['SYMBOL', 'PRICE', '%-CHANGE', 'CHANGE', 'DAY-HI', 'DAY-LO', 'YEAR-HI', 'YEAR-LO']

def get_next_number(s):
    out = ""
    found = False
    for c in s:
        if c.isdigit() or c == '.' or c == '-':
            out += c
            found = True
        elif found is True and c != ',':
            return out
    raise NotImplementedError
        
class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price = 0.0
        self.change = 0.0
        self.change_pct = 0.0
        self.prev = 0.0
        self.high = 0.0
        self.low = 0.0
        self.year_high = 0.0
        self.year_low = 0.0
        self.colour = 'green'

    def update(self):
        with urllib.request.urlopen(URL.format(self.symbol)) as url:
            page = url.read().decode('utf8')

        self.price = float(get_next_number(page.split('Last Price:')[-1]))
        self.high = float(get_next_number(page.split('Day High:')[-1]))
        self.low = float(get_next_number(page.split('Day Low:')[-1]))
        self.prev = float(get_next_number(page.split('Prev. Close: ')[-1]))
        self.change = self.price - self.prev
        self.change_pct = (self.change / self.prev) * 100.0
        self.year_low = float(get_next_number(page.split('52 Week Low: ')[-1]))
        self.year_high = float(get_next_number(page.split('52 Week High: ')[-1]))
        self.colour = 'green' if self.change >= 0 else 'red'

    def print(self):
        output = '{:>12s}|{}|{}|{}|{:12.2f}|{:12.2f}|{:12.2f}|{:12.2f}'.format(
            self.symbol,
            colored('{:12.2f}'.format(self.price), self.colour),
            colored('{:11.2f}%'.format(self.change_pct), self.colour),
            colored('{:12.2f}'.format(self.change), self.colour),
            self.high, self.low, self.year_high, self.year_low
        )
        print(output)
        print('_'*(13*len(headers)-1))


def printall(statuses, stocks):
    os.system('clear')
    print('{}\n'.format(' - '.join(statuses)))
    print('|'.join(['{:>12s}'.format(x) for x in headers]))
    print('='*(13*len(headers)-1))
    for stock in stocks:
        stock.print()

stocks = [Stock(s) for s in STOCKS]

while True:
    for stock in stocks:
        now = datetime.datetime.now()
        stock.update()
        printall([str(now)], stocks)
    time.sleep(10)
