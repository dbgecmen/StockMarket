from super_simple_stocks import Trade, Stock, PreferredStock, get_all_share_index
from datetime import datetime
from decimal import getcontext
import pandas


if __name__ == '__main__':
    getcontext().prec = 9
    time_stamp = datetime.now()

    stocks = {'TEA': Stock('TEA', 0, 100),
              'POP': Stock('POP', 8, 100),
              'ALE': Stock('ALE', 23, 60),
              'GIN': PreferredStock('GIN', 8, 0.02, 100),
              'JOE': Stock('JOE', 13, 250)
              }

    stocks['TEA'].add_trade_record(Trade(time_stamp, 2, 'SELL', 15.20))
    stocks['TEA'].add_trade_record(Trade(time_stamp, 8, 'BUY', 30.45))
    stocks['POP'].add_trade_record(Trade(time_stamp, 5, 'BUY', 80.40))
    stocks['POP'].add_trade_record(Trade(time_stamp, 17, 'BUY', 8.90))
    stocks['ALE'].add_trade_record(Trade(time_stamp, 13, 'SELL', 7.20))
    stocks['ALE'].add_trade_record(Trade(time_stamp, 30, 'BUY', 48.30))
    stocks['GIN'].add_trade_record(Trade(time_stamp, 19, 'SELL', 10.00))
    stocks['GIN'].add_trade_record(Trade(time_stamp, 3, 'BUY', 2.46))
    stocks['JOE'].add_trade_record(Trade(time_stamp, 15, 'BUY', 40.67))
    stocks['JOE'].add_trade_record(Trade(time_stamp, 30, 'SELL', 39.50))

    data = [[stocks['TEA'].get_dividend_yield(10.20), stocks['TEA'].get_pe_ratio(10.20),
             stocks['TEA'].get_volume_weighted_stock_price()],
            [stocks['POP'].get_dividend_yield(20.15), stocks['POP'].get_pe_ratio(20.15),
             stocks['POP'].get_volume_weighted_stock_price()],
            [stocks['ALE'].get_dividend_yield(40.50), stocks['ALE'].get_pe_ratio(40.50),
             stocks['ALE'].get_volume_weighted_stock_price()],
            [stocks['GIN'].get_dividend_yield(15.45), stocks['GIN'].get_pe_ratio(15.45),
             stocks['GIN'].get_volume_weighted_stock_price()],
            [stocks['JOE'].get_dividend_yield(90.40), stocks['JOE'].get_pe_ratio(90.40),
             stocks['JOE'].get_volume_weighted_stock_price()]
            ]
    symbols = ['TEA', 'POP', 'ALE', 'GIN', 'JOE']
    headers = ["Dividend Yield", "P/E Ratio", "Stock Price"]

    print(pandas.DataFrame(data, columns=headers, index=symbols))
    print('\nGBCE All Share Index:')
    print(get_all_share_index(stocks))
