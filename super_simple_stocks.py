from decimal import getcontext, Decimal
from datetime import datetime


class Trade:
    """
    A class to represent a Trade
    """

    def __init__(self, timestamp, quantity, indicator, traded_price):
        """
        :param datetime timestamp: Timestamp of the trade
        :param int quantity: Amount of shares exchanged
        :param str indicator: Indicator to BUY or SELL
        :param float traded_price: The traded price of each share
        :raise: ValueError if a parameter is not the correct input type
        """

        if isinstance(timestamp, datetime):
            self.timestamp = timestamp
        else:
            raise ValueError(f'Timestamp is not a datetime object. Input timestamp is {timestamp}')

        if quantity > 0:
            self.quantity = quantity
        else:
            raise ValueError(f'The amount of shares should not be less than one. Input amount of shares is {quantity}')

        if traded_price >= 0:
            self.price = Decimal(traded_price)
        else:
            raise ValueError(f'Stock price should not be negative. Input stock price is {traded_price}.')

        if indicator in ['BUY', 'SELL']:
            self.indicator = indicator
        else:
            raise ValueError(f'Indicator should be BUY or SELL. Input indicator is {indicator}')


class Stock:
    """
    A class to represent a Common Stock
    """

    def __init__(self, symbol, last_dividend, par_value):
        """
        :param str symbol: symbol representing the stock
        :param float last_dividend: most recent dividend payment
        :param float par_value: face value of the stock
        :raise: ValueError if symbol is not a string
        """

        if isinstance(symbol, str):
            self.symbol = symbol
        else:
            raise ValueError(f'Stock symbol is not a string. Input symbol is {symbol}')
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.stock_trades = []

    def get_dividend_yield(self, price):
        """
        Method to calculate the dividend yield for a given stock price

        :param float price: Input price to calculate the dividend yield
        :raise: ValueError if price is negative or equal to zero
        :return: The dividend yield is returned
        :rtype: Decimal
        """

        if price <= 0:
            raise ValueError(f'Stock price should not be negative or zero. Stock price of {self.symbol} is {price}.')
        return Decimal(self.last_dividend) / Decimal(price)

    def get_pe_ratio(self, price):
        """
        Method to calculate the P/E ratio for a given stock price

        :param float price: Input price to calculate the dividend yield
        :raise: ValueError if price is negative
        :return: The price-to-earnings (P/E) ratio
        :rtype: Decimal
        """
        if price <= 0:
            raise ValueError(f'Stock price should not be negative or zero. Stock price of {self.symbol} is {price}.')
        try:
            return Decimal(price) / self.get_dividend_yield(price)
        except ZeroDivisionError:
            return Decimal(0)

    #  Record a trade, with timestamp, quantity, buy or sell indicator and price
    def add_trade_record(self, trade):
        """
        Method to record a trade for the stock

        :param Trade trade: The trade to be recorded
        """
        if isinstance(trade, Trade):
            self.stock_trades.append(trade)
        else:
            raise ValueError(f'Input trade should be a Trade object. The input type is {type(trade)}')

    def get_volume_weighted_stock_price(self, bound=300):
        """
        Method to calculate the Volume Weighted Stock Price based on trades in the past 5 minutes/ 300 seconds

        :param int bound: The default value is set to 300 seconds
        :return: The Volume Weighted Stock Price
        :rtype: Decimal
        """

        current_timestamp = datetime.now()
        total_price = 0
        total_quantity = 0

        for trade in self.stock_trades:
            timedelta = current_timestamp - trade.timestamp
            if timedelta.total_seconds() <= bound:
                total_price += trade.price * trade.quantity
                total_quantity += trade.quantity

        if total_price == 0 or total_quantity == 0:
            return Decimal(0)
        return total_price / total_quantity


class PreferredStock(Stock):
    """
    A class to represent a Preferred Stock. Child class from the Stock class.
    """
    def __init__(self, symbol, last_dividend, fixed_dividend, par_value):
        super().__init__(symbol, last_dividend, par_value)
        self.fixed_dividend = fixed_dividend

    def get_dividend_yield(self, price):
        """
        Method to calculate the dividend yield for a given stock price

        :param float price: Input price to calculate the dividend yield
        :raise: ValueError if price is negative or equal to zero
        :return: The dividend yield is returned
        :rtype: Decimal
        """

        if price <= 0:
            raise ValueError(f'Stock price should not be negative or zero. Stock price of {self.symbol} is {price}.')
        return Decimal(self.fixed_dividend)*Decimal(self.par_value) / Decimal(price)


def get_all_share_index(traded_stocks):
    """
    Method to calculate the GBCE All Share Index

    :param dct traded_stocks: The stocks for which we calculate the All Share Index
    :return: The geometric mean of the Volume Weighted Stock Price for all stocks
    """

    if not isinstance(traded_stocks, dict):
        raise ValueError(f'Input type should be a dictionary. The input type is {type(traded_stocks)}')

    if not traded_stocks:
        return Decimal(0)

    total_stocks = 0
    total_weighted_stock_price = 1

    for stock in traded_stocks.values():
        if stock.get_volume_weighted_stock_price() != 0:
            total_weighted_stock_price *= stock.get_volume_weighted_stock_price(float('inf'))
            total_stocks += 1

    if total_weighted_stock_price == 0 or total_stocks == 0:
        return Decimal(0)
    return total_weighted_stock_price**(Decimal(1)/Decimal(total_stocks))



