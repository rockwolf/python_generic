#!/usr/bin/env python
"""
See LICENSE file for copyright and license details.
"""

"""
Unit test for calculator_finance.py
"""
from calculator_finance import CalculatorFinance
import unittest
from decimal import Decimal, getcontext
from function import *
from constant import *
import sys

class Functions():
    """
        Helper functions
    """
    def __init__(self):
        """
            Initialization
        """
        pass

    def test_conversion_from(self, price, exchange_rate):
        """
            Returns original price.
        """
        return pric / exchange_rate

    def test_conversion_to(self, price_orig, exchange_rate):
        """
            Returns converted price price.
        """
        return price_orig * exchange_rate

    def test_margin_of_pool(self, pool, margin):
        """
            Returns the pool minus a margin.
        """
        return pool*(1-margin/Decimal(100.0))


class TestValues(unittest.TestCase):
    """
        Test the calculations with an example.
    """
    test_values = [] 
    # Loss - short
    #3	1	cfd other non-share	SBH4.cfd	2013-10-11	2013-10-09	0	13.93	13.7	550	550	3	3	0.0000	0	3	3	151.62	0.02	144.31	1.9	129.41	1.71	13.96	18.94	-129.41	-1.71	-0.9R	-0.90	0	1	33.33	7663.1	7533.69	2	2	7	18.9	18.5	USD	0.74	0.74	7581.23	?
    test_values.append({
        'i_market_name':'ebr',
        'i_market_description':'Europe Brussels',
        'i_stock_name':'devg',
        'i_stock_description':'Devgen N.V.',
        'i_account_from':'assets:current_assets:whsi00', #Note: Get account_id from T_ACCOUNT for final insert
        'i_account_to':'assets:stock:ebr.devg',
        'i_date_buy':string_to_date("2013-10-11"),
        'i_date_sell':string_to_date("2013-10-09"),
        'i_price_buy':DEFAULT_DECIMAL,
        'i_price_sell':DEFAULT_DECIMAL,
        'i_price_buy_orig':Decimal('18.9'),
        'i_price_sell_orig':Decimal('18.5'),
        'i_shares_buy':550,
        'i_shares_sell':550,
        'i_amount_buy':DEFAULT_DECIMAL,
        'i_amount_sell':Decimal('7533.69'),
        'i_comment':'test comment',
        'i_commission_buy':Decimal('3.0'),
        'i_commission_sell':Decimal('3.0'),
        'i_tax_buy':DEFAULT_DECIMAL,
        'i_tax_sell':DEFAULT_DECIMAL,
        'i_risk_input':Decimal('2.0'),
        'i_currency_from':'USD',
        'i_currency_to':'EUR',
        'i_exchange_rate_buy':Decimal('0.737191301'),
        'i_exchange_rate_sell':Decimal('0.740411669'),
        'i_automatic_flag':0,
        'i_date_expiration':string_to_date("2014-01-01"),
        'i_periodic':0,
        'i_periodic_start':string_to_date("1900-01-01"),
        'i_periodic_end':string_to_date("1900-01-01"),
        'i_pool':Decimal('10108.3066666666667'),
        'i_margin':Decimal('25.0'),
        'i_long_bool':False,
        'result_values': {
            'stoploss': Decimal('13.96')
            ,'stoploss_orig': Decimal('18.94')
            ,'risk_input': Decimal('151.625')
            ,'risk_initial': Decimal('144.31')
            ,'risk_initial_percent': Decimal('1.91')
            ,'risk_actual': Decimal('129.41')
            ,'risk_actual_percent': Decimal('1.71')
            ,'r_multiple': Decimal('-0.94')
            ,'amount_buy_simple':Decimal('7663.1')
            ,'amount_sell_simple':Decimal('7533.69')
            ,'amount_buy':Decimal('7666.1')
            ,'amount_sell':Decimal('7533.69')
            ,'cost_transaction_buy': Decimal('3.0')
            ,'cost_transaction_sell': Decimal('3.0')
            ,'cost_tax_buy': DEFAULT_DECIMAL
            ,'cost_tax_sell': DEFAULT_DECIMAL
            ,'amount_with_tax_buy':Decimal('7666.1')
            ,'amount_with_tax_sell':Decimal('7533.69')
            ,'profit_loss': Decimal('-135.41')
            ,'cost_other': DEFAULT_DECIMAL
            ,'shares_recommended': 550
            ,'price_buy':Decimal('13.93')
            ,'price_sell':Decimal('13.7')
            ,'price_buy_orig':Decimal('18.9')
            ,'price_sell_orig':Decimal('18.5')
            ,'commission_buy':Decimal('3.0')
            ,'commission_sell':Decimal('3.0')
            ,'cost_total': DEFAULT_DECIMAL
        } 
    })
   
    def test_calculate_percentage_of(self):
        """
            Test calculate_percentage_of
        """
        calc = CalculatorFinance()
        result = calc.calculate_percentage_of(
                Decimal('25.45'),
                Decimal('100.0'))
        self.assertAlmostEqual(float(25.45), float(result), 4)
        calc = None
    
    def test_calculate_stoploss(self):
        """
            Test calculate_stoploss
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            print("test calc_stoploss -- price_sell=",
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']))
            print("test calc_stoploss -- shares_sell=", value['i_shares_sell'])
            print("test calc_stoploss -- tax_sell=", value['i_tax_sell'])
            print("test calc_stoploss -- commission_sell=", value['i_commission_sell'])
            print("test calc_stoploss -- risk_input=", value['i_risk_input'])
            print("test calc_stoploss -- pool=", value['i_pool'])
            print("test calc_stoploss -- pool2=", func.test_margin_of_pool(value['i_pool'], value['i_margin']))
            result = calc.calculate_stoploss(
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'],
                    value['i_tax_sell'],
                    value['i_commission_sell'],
                    value['i_risk_input'],
                    func.test_margin_of_pool(value['i_pool'], value['i_margin']),
                    value['i_long_bool'])
            self.assertAlmostEqual(float(value['result_values']['stoploss']), float(result), 4)
        func = None
        calc = None

    def test_calculate_risk_input(self):
        """
            Test calculate_risk_input
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_risk_input(
                        func.test_margin_of_pool(
                            value['i_pool'],
                            value['i_margin']),
                        value['i_risk_input'])
            self.assertAlmostEqual(float(value['result_values']['risk_input']), float(result), 4)
        func = None
        calc = None

#    def calculate_risk_initial(self):
#        """
#            Test calculate_risk_initial
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_risk_initial(
#                    self.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
#                    value['i_shares'],
#                    value['result_values']['stoploss'])
#            self.assertAlmostEqual(float(value['result_values']['risk_initial']), float(result), 4)
#        calc = None
#                    
#
#    def calculate_risk_actual(self):
#        """
#            Test calculate_risk_actual
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_risk_actual(
#                    value['result_values']['price_buy'],
#                    value['i_shares_buy'],
#                    self.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
#                    value['i_shares_sell'],
#                    value['result_values']['stoploss'],
#                    value['result_values']['risk_initial'])
#            self.assertAlmostEqual(float(value['result_values']['risk_actual']), float(result), 4)
#        calc = None
#
#    def calculate_r_multiple(self):
#        """
#            Test calculate_r_multiple
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_r_multiple(
#                    value['result_values']['i_price_buy'],
#                    self.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
#                    value['result_values']['stoploss'])
#            self.assertAlmostEqual(float(value['result_values']['r_multiple']), float(result), 4)
#        calc = None
#
#    def calculate_cost_total(self):
#        """
#            Test calculate_cost_total
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_cost_total(
#                    value['result_values']['tax_buy'],
#                    value['result_values']['commission_buy'],
#                    value['i_tax_sell'],
#                    value['i_commission_sell'])
#            self.assertAlmostEqual(float(value['result_values']['cost_total']), float(result), 4)
#        calc = None
#
#    def test_calculate_amount_buy_simple(self):
#        """
#            Test calculate_amount_simpel for buying
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            print("test --- ",
#                    self.test_conversion_to(value['i_price_buy_orig'],
#                        value['i_exchange_rate_buy']))
#            result = calc.calculate_amount_simple(
#                    value['i_shares_buy'],
#                    self.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']))
#            self.assertAlmostEqual(float(value['result_values']['amount_buy_simple']), float(result), 4)
#        calc = None
#
#    def test_calculate_amount_sell_simple(self):
#        """
#            Test calculate_amount_simpel for selling
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_amount_simple(
#                    self.test_conversion(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
#                    value['i_shares_sell'])
#            self.assertAlmostEqual(float(value['result_values']['amount_sell_simple']), float(result), 4)
#        calc = None
#    
#    def test_calculate_amount_buy(self):
#        """
#            Test calculate_amount for buying
#        """
#        calc = CalculatorFinance()
#        # AMT = SP + SPT + C
#        #     = SP * (1 + T) + C
#        #     = 100 * 25.0 * (1 + 0.0025) + 7.25
#        #     = 2513.5
#        for value in self.test_values:
#            result = calc.calculate_amount(
#                    value['i_price_buy'],
#                    value['i_shares_buy'],
#                    Transaction.BUY,
#                    value['i_tax_buy'],
#                    value['i_commission_buy'])
#            self.assertAlmostEqual(float(value['result_values']['amount_buy']), float(result), 4)
#        calc = None
#                    
#    def test_calculate_amount_sell(self):
#        """
#            Test calculate_amount for selling
#        """
#        calc = CalculatorFinance()
#        # AMT = SP - SPT - C
#        #     = SP * (1 - T) - C
#        #     = 100 * 25.0 * (1 - 0.0025) - 7.25
#        #     = 2486.50
#        for value in self.test_values:
#            result = calc.calculate_amount(
#                    value['i_price_sell'],
#                    value['i_shares_sell'],
#                    Transaction.SELL,
#                    value['i_tax_sell'],
#                    value['i_commission_sell'])
#            self.assertAlmostEqual(float(value['result_values']['amount_sell']), float(result), 4)
#        calc = None
#    
#    def test_cost_transaction_buy(self):
#        """
#            Test cost_transaction for buying
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.cost_transaction(
#                    Transaction.BUY,
#                    value['i_price_buy'],
#                    value['i_shares_buy'],
#                    value['i_tax_buy'],
#                    value['i_commission_buy'])
#            self.assertAlmostEqual(float(value['result_values']['cost_transaction_buy']), float(result), 4)
#        calc = None
#
#    def test_cost_transaction_sell(self):
#        """
#            Test cost_transaction for selling
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.cost_transaction(
#                    Transaction.SELL,
#                    value['i_price_sell'],
#                    value['i_shares_sell'],
#                    value['i_tax_sell'],
#                    value['i_commission_sell'])
#            self.assertAlmostEqual(float(value['result_values']['cost_transaction_sell']), float(result), 4)
#        calc = None
#
#    def test_cost_tax_buy(self):
#        """
#            Test cost_tax for buying
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            print("-- test_cost_tax_buy:", value['i_amount_buy'])
#            print("-- test_cost_tax_buy:", value['i_commission_buy'])
#            print("-- test_cost_tax_buy:", value['i_shares_buy'])
#            print("-- test_cost_tax_buy:", value['i_price_buy'])
#            result = calc.cost_tax(
#                    Transaction.BUY,
#                    value['i_amount_buy'],
#                    value['i_commission_buy'],
#                    value['i_shares_buy'],
#                    value['i_price_buy'])
#            self.assertAlmostEqual(float(value['result_values']['cost_tax_buy']), float(result), 4)
#        calc = None
#
#    def test_cost_tax_sell(self):
#        """
#            Test cost_tax for selling
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.cost_tax(
#                    Transaction.SELL,
#                    value['i_amount_sell'],
#                    value['i_commission_sell'],
#                    value['i_shares_sell'],
#                    value['i_price_sell'])
#            self.assertAlmostEqual(float(value['result_values']['cost_tax_sell']), float(result), 4)
#        calc = None
#
#    def test_calculate_amount_with_tax_buy(self):
#        """
#            Test calculate_amount_with_tax for buying
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_amount_with_tax(
#                    value['i_tax_buy'],
#                    value['i_shares_buy'],
#                    value['i_price_buy'])
#            self.assertAlmostEqual(float(value['result_values']['amount_with_tax_buy']), float(result), 4)
#        calc = None
#
#    def test_calculate_profit_loss(self):
#        """
#            Test calculate_profit_loss
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_profit_loss(
#                    value['result_values']['price_buy'],
#                    value['i_shares_buy'],
#                    value['result_values']['price_sell'],
#                    value['i_shares_sell'],
#                    value['i_tax_buy'],
#                    value['i_tax_sell'],
#                    value['i_commission_buy'],
#                    value['i_commission_sell'],
#                    value['i_long_bool'])
#            self.assertAlmostEqual(float(value['result_values']['profit_loss']), float(result), 4)
#        calc = None
#
#    def test_calculate_cost_other(self):
#        """
#            Test calculate_cost_other
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_cost_other(
#                    value['result_values']['cost_total'],
#                    value['result_values']['profit_loss'])
#            self.assertAlmostEqual(float(value['result_values']['cost_other']), float(result), 4)
#        calc = None
#
#    def test_calculate_shares_recommended(self):
#        """
#            Test calculate_shares_recommended
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            print("test_shares_recommended - i_pool =", value['i_pool'])
#            print("test_shares_recommended - i_risk_input =", value['i_risk_input'])
#            print("test_shares_recommended - i_commission_sell =",
#                    value['i_commission_sell'])
#            print("test_shares_recommended - i_tax_sell =", value['i_tax_buy'])
#            print("test_shares_recommended - i_price_sell =",
#                    self.test_conversion(value['i_price_sell_orig'],
#                        value['i_exchange_rate_sell']))
#            result = calc.calculate_shares_recommended(
#                    value['i_pool'],
#                    value['i_risk_input'],
#                    value['i_commission_sell'],
#                    value['i_tax_sell'],
#                    self.test_conversion(value['i_price_sell_orig'], value['i_exchange_rate_sell'])
#                    )
#            self.assertAlmostEqual(float(value['result_values']['shares_recommended']), float(result), 4)
#        calc = None
#
#    def test_calculate_price_buy(self):
#        """
#            Test calculate_price at buying.
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_price(
#                    Transaction.BUY,
#                    value['i_amount_buy'],
#                    value['i_shares_buy'],
#                    value['i_tax_buy'],
#                    value['i_commission_buy'])
#            self.assertAlmostEqual(float(value['result_values']['price_buy']), float(result), 4)
#        calc = None
#
#    def test_calculate_price_sell(self):
#        """
#            Test calculate_price at selling.
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_price(
#                    Transaction.SELL,
#                    value['i_amount_sell'],
#                    value['i_shares_sell'],
#                    value['i_tax_sell'],
#                    value['i_commission_sell'])
#            self.assertAlmostEqual(float(value['result_values']['price_sell']), float(result), 4)
#        calc = None
#
#    def test_calculate_commission_buy(self):
#        """
#            Test calculate_commission for buying
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_commission(
#                    value['i_account_to'],
#                    value['i_market_name'],
#                    value['i_stock_name'],
#                    value['i_price_buy'],
#                    value['i_shares_buy'])
#            self.assertAlmostEqual(float(value['result_values']['commission_buy']), float(result), 4)
#        calc = None
#
#    def test_calculate_commission_sell(self):
#        """
#            Test calculate_commission for selling
#        """
#        calc = CalculatorFinance()
#        for value in self.test_values:
#            result = calc.calculate_commission(
#                    value['i_account_to'],
#                    value['i_market_name'],
#                    value['i_stock_name'],
#                    value['i_price_sell'],
#                    value['i_shares_sell'])
#            self.assertAlmostEqual(float(value['result_values']['commission_sell']), float(result), 4)
#        calc = None
#
if __name__ == "__main__":
    getcontext().prec = 6
    #test = TestValues()
    #test.run()
    unittest.main(verbosity=2)
