import unittest
from super_simple_stocks import Trade, Stock, PreferredStock, get_all_share_index
from datetime import datetime, timedelta
from decimal import Decimal


class TestTrade(unittest.TestCase):
    """
    Unittests for the Trade Class
    """

    # Test each attribute of the trade class for raising a ValueError
    def test_trade_attributes(self):
        with self.assertRaises(ValueError):
            Trade('2021-10-13 20:32:55.425435', 2, 'SELL', 14.5)
        with self.assertRaises(ValueError):
            Trade(datetime.now(), -10, 'SELL', 14.5)
        with self.assertRaises(ValueError):
            Trade(datetime.now(), 2, 'sel', 14.5)
        with self.assertRaises(ValueError):
            Trade(datetime.now(), 2, 'SELL', -14.5)


class TestStock(unittest.TestCase):
    """
    Unittests for the Stock Class
    """

    def setUp(self):
        self.stocks = {'TEA': Stock('TEA', 0, 100),
                       'POP': Stock('POP', 8, 100),
                       'ALE': Stock('ALE', 23, 60),
                       'JOE': Stock('JOE', 13, 250)}

    # Test symbol attribute of the Stock class for raising a ValueError
    def test_symbol_attribute(self):
        with self.assertRaises(ValueError):
            Stock(0, 0, 100)

    # Test if dividend yield raises a ValueError when the market price is negative or zero
    def test_dividend_yield(self):
        with self.assertRaises(ValueError):
            self.stocks['TEA'].get_dividend_yield(-10)
        with self.assertRaises(ValueError):
            self.stocks['TEA'].get_dividend_yield(0)

    # Test pe_ratio
    def test_pe_ratio(self):
        # Test if pe ratio raises a ValueError when the market price is negative or zero
        with self.assertRaises(ValueError):
            self.stocks['TEA'].get_pe_ratio(-10)
        with self.assertRaises(ValueError):
            self.stocks['TEA'].get_pe_ratio(0)
        # Test if pe ratio catches the ZeroDivisionError
        self.assertEqual(Stock('TEA', Decimal(0), 100).get_pe_ratio(20), Decimal(0))

    # Test if trade record raises a ValueError when the input is not a Trade object
    def test_add_trade_record(self):
        with self.assertRaises(ValueError):
            self.stocks['TEA'].add_trade_record(None)

    # Test if get_volume_weighted_stock_price returns the right value
    def test_volume_weighted_stock_price(self):
        # Record two trades: One trade within 5 minutes ago from now and one trade longer than 5 minutes ago from now
        timestamp = datetime.now()
        self.stocks['TEA'].add_trade_record(Trade(timestamp-timedelta(minutes=3), 2, 'SELL', 15.20))
        self.stocks['TEA'].add_trade_record(Trade(timestamp-timedelta(minutes=6), 8, 'BUY', 30.45))
        self.assertAlmostEqual(self.stocks['TEA'].get_volume_weighted_stock_price(), Decimal(15.2000000), places=6)


class TestPreferredStock(unittest.TestCase):
    """
    Unittests for the Preferred Stock Class
    """

    def setUp(self):
        self.stock = {'GIN': PreferredStock('GIN', 8, 0.02, 100)}

    def test_dividend_yield(self):
        with self.assertRaises(ValueError):
            self.stock['GIN'].get_dividend_yield(-10)
        with self.assertRaises(ValueError):
            self.stock['GIN'].get_dividend_yield(0)
        self.assertAlmostEqual(self.stock['GIN'].get_dividend_yield(15.45), Decimal(0.1294498), places=6)


class TestGetAllShareIndexMethod(unittest.TestCase):
    """
    Unittests for the get_all_share_index method that calculates the GBCE All Share Index
    """

    def setUp(self):
        self.stocks = {'TEA': Stock('TEA', 0, 100),
                       'POP': Stock('POP', 8, 100),
                       'ALE': Stock('ALE', 23, 60),
                       'GIN': PreferredStock('GIN', 8, 0.02, 100)
                       }

        self.stocks1 = {'JOE': Stock('JOE', 13, 250)}

        self.stocks['TEA'].add_trade_record(Trade(datetime.now(), 2, 'SELL', 15.20))
        self.stocks['POP'].add_trade_record(Trade(datetime.now(), 5, 'BUY', 80.40))
        self.stocks['ALE'].add_trade_record(Trade(datetime.now(), 13, 'SELL', 7.20))
        self.stocks['GIN'].add_trade_record(Trade(datetime.now(), 19, 'SELL', 10.00))

    # Test for the correct input type to the method
    def test_input_type(self):
        with self.assertRaises(ValueError):
            get_all_share_index([])

    # Test if the method returns Decimal(0) if the input is an empty dictionary
    def test_empty_input(self):
        self.assertEqual(get_all_share_index({}), Decimal(0))

    # Test if the get_all_share_index method returns the correct value when trades are done
    def test_correct_index(self):
        self.assertAlmostEqual(get_all_share_index(self.stocks), Decimal(17.2229695), places=6)

    # Test if the get_all_share_index method returns Decimal(0) when no trades are done
    def test_no_trades(self):
        self.assertEqual(get_all_share_index(self.stocks1), Decimal(0))


if __name__ == '__main__':
    unittest.main()