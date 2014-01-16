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
        return price / exchange_rate

    def test_conversion_to(self, price_orig, exchange_rate):
        """
            Returns converted price price.
        """
        return price_orig * exchange_rate

    def test_margin_of_pool(self, pool, margin):
        """
            Returns the pool minus a margin.
        """
        return pool*(Decimal('1.0')-margin/Decimal(100.0))

class TestValues_ShortWin(unittest.TestCase):
    """
        short - win
    """
    test_values = [] 
    test_values.append({
        'i_market_name':'.cfd other non-share',
        'i_market_description':'cfds on commodities',
        'i_stock_name':'SBH4.cfd',
        'i_stock_description':'London Sugar No. 11 (USD)',
        'i_account_from':'assets:current_assets:whsi00', #Note: Get account_id from T_ACCOUNT for final insert
        'i_account_to':'assets:commodity:SBH4.cfd',
        'i_date_buy':string_to_date("2013-10-24"),
        'i_date_sell':string_to_date("2013-10-21"),
        'i_price_buy_orig':Decimal('19.16'),
        'i_price_sell_orig':Decimal('19.46'),
        'i_shares_buy':522,
        'i_shares_sell':522,
        'i_comment':'test comment',
        'i_commission_buy':Decimal('3.0'),
        'i_commission_sell':Decimal('3.0'),
        'i_tax_buy':DEFAULT_DECIMAL,
        'i_tax_sell':DEFAULT_DECIMAL,
        'i_risk_input':Decimal('2.0'),
        'i_currency_from':'USD',
        'i_currency_to':'EUR',
        'i_exchange_rate_buy':Decimal('0.725373567'),
        'i_exchange_rate_sell':Decimal('0.730940721'),
        'i_automatic_flag':False,
        'i_date_expiration':string_to_date("2014-01-01"),
        'i_periodic':False,
        'i_pool': Decimal('9906.765901'),
        'i_margin':Decimal('25.0'),
        'i_long_bool':False,
        'result_values': {
            'stoploss': Decimal('14.4973')
            ,'stoploss_orig': Decimal('19.9862')
            ,'risk_input': Decimal('148.6015')
            ,'risk_initial': Decimal('148.6015')
            ,'risk_initial_percent': Decimal('2.00')
            ,'risk_actual': Decimal('148.6015')
            ,'risk_actual_percent': Decimal('2.00')
            ,'r_multiple': Decimal('1.1046')
            ,'amount_buy_simple':Decimal('7254.8382')
            ,'amount_sell_simple':Decimal('7424.9836')
            ,'amount_buy':Decimal('7257.8382')
            ,'amount_sell':Decimal('7421.9836')
            ,'cost_transaction_buy': Decimal('3.0')
            ,'cost_transaction_sell': Decimal('3.0')
            ,'cost_tax_buy': DEFAULT_DECIMAL
            ,'cost_tax_sell': DEFAULT_DECIMAL
            ,'amount_with_tax_buy':Decimal('7254.8382')
            ,'amount_with_tax_sell':Decimal('7424.9836')
            ,'profit_loss': Decimal('164.1453')
            ,'profit_loss_percent': Decimal('2.2')
            ,'cost_other': DEFAULT_DECIMAL
            ,'shares_recommended': 522
            ,'price_buy':Decimal('13.8982')
            ,'price_sell':Decimal('14.2241')
            ,'price_buy_orig':Decimal('19.16')
            ,'price_sell_orig':Decimal('19.46')
            ,'commission_buy':Decimal('3.0')
            ,'commission_sell':Decimal('3.0')
            ,'cost_total': Decimal('6.0')
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
        self.assertAlmostEqual(float(25.45), round(float(result), 4), 2)
        calc = None
    
    def test_calculate_stoploss(self):
        """
            Test calculate_stoploss
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
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

    def test_calculate_risk_initial(self):
        """
            Test calculate_risk_initial
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            print "price_sell_orig:", value['i_price_sell_orig']
            print "exchange_rate_sell:", value['i_exchange_rate_sell']
            print "conversion:", func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell'])
            print "stoploss:", value['result_values']['stoploss']
            result = calc.calculate_risk_initial(
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'],
                    value['i_tax_sell'],
                    value['i_commission_sell'],
                    value['result_values']['stoploss'],
                    value['i_long_bool'])
            self.assertAlmostEqual(float(value['result_values']['risk_initial']), float(result), 4)
            print "result = ", result
        func = None
        calc = None

    def test_calculate_risk_actual(self):
        """
            Test calculate_risk_actual
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_risk_actual(
                    value['result_values']['price_buy'],
                    value['i_shares_buy'],
                    value['i_tax_buy'],
                    value['i_commission_buy'],
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'],
                    value['i_tax_sell'],
                    value['i_commission_sell'],
                    value['result_values']['stoploss'],
                    value['result_values']['risk_initial'],
                    value['i_long_bool'])
            self.assertAlmostEqual(float(value['result_values']['risk_actual']), float(result), 4)
        func = None
        calc = None

    def test_calculate_r_multiple(self):
        """
            Test calculate_r_multiple
        """
        calc = CalculatorFinance()
        for value in self.test_values:
            result = calc.calculate_r_multiple(
                    value['result_values']['profit_loss'],
                    value['result_values']['risk_initial'])
            self.assertAlmostEqual(float(value['result_values']['r_multiple']), float(result), 4)
        calc = None

    def test_calculate_cost_total(self):
        """
            Test calculate_cost_total
        """
        calc = CalculatorFinance()
        for value in self.test_values:
            result = calc.calculate_cost_total(
                    value['i_tax_buy'],
                    value['i_commission_buy'],
                    value['i_tax_sell'],
                    value['i_commission_sell'])
            self.assertAlmostEqual(float(value['result_values']['cost_total']), float(result), 4)
        calc = None

    def test_calculate_amount_buy_simple(self):
        """
            Test calculate_amount_simpel for buying
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_amount_simple(
                    value['i_shares_buy'],
                    func.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']))
            self.assertAlmostEqual(float(value['result_values']['amount_buy_simple']), float(result), 4)
        func = None
        calc = None

    def test_calculate_amount_sell_simple(self):
        """
            Test calculate_amount_simpel for selling
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_amount_simple(
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'])
            self.assertAlmostEqual(float(value['result_values']['amount_sell_simple']), float(result), 4)
        func = None
        calc = None
    
    def test_calculate_amount_buy(self):
        """
            Test calculate_amount for buying
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_amount(
                    func.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']),
                    value['i_shares_buy'],
                    Transaction.BUY,
                    value['i_tax_buy'],
                    value['i_commission_buy'])
            self.assertAlmostEqual(float(value['result_values']['amount_buy']), float(result), 4)
        func = None
        calc = None
                    
    def test_calculate_amount_sell(self):
        """
            Test calculate_amount for selling
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_amount(
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'],
                    Transaction.SELL,
                    value['i_tax_sell'],
                    value['i_commission_sell'])
            self.assertAlmostEqual(float(value['result_values']['amount_sell']), float(result), 4)
        func = None
        calc = None
    
    def test_cost_transaction_buy(self):
        """
            Test cost_transaction for buying
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.cost_transaction(
                    Transaction.BUY,
                    func.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']),
                    value['i_shares_buy'],
                    value['i_tax_buy'],
                    value['i_commission_buy'])
            self.assertAlmostEqual(float(value['result_values']['cost_transaction_buy']), float(result), 4)
        func = None
        calc = None

    def test_cost_transaction_sell(self):
        """
            Test cost_transaction for selling
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.cost_transaction(
                    Transaction.SELL,
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'],
                    value['i_tax_sell'],
                    value['i_commission_sell'])
            self.assertAlmostEqual(float(value['result_values']['cost_transaction_sell']), float(result), 4)
        func = None
        calc = None

    def test_cost_tax_buy(self):
        """
            Test cost_tax for buying
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.cost_tax(
                    Transaction.BUY,
                    value['result_values']['amount_buy'],
                    value['i_commission_buy'],
                    value['i_shares_buy'],
                    func.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']))
            self.assertAlmostEqual(float(value['result_values']['cost_tax_buy']), float(result), 4)
        func = None
        calc = None

    def test_cost_tax_sell(self):
        """
            Test cost_tax for selling
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.cost_tax(
                    Transaction.SELL,
                    value['result_values']['amount_sell'],
                    value['i_commission_sell'],
                    value['i_shares_sell'],
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']))
            self.assertAlmostEqual(float(value['result_values']['cost_tax_sell']), float(result), 4)
        func = None
        calc = None

    def test_calculate_amount_with_tax_buy(self):
        """
            Test calculate_amount_with_tax for buying
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_amount_with_tax(
                    Transaction.BUY,
                    value['i_shares_buy'],
                    func.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']),
                    value['i_tax_buy'])
            self.assertAlmostEqual(float(value['result_values']['amount_with_tax_buy']), float(result), 4)
        func = None
        calc = None

    def test_calculate_amount_with_tax_sell(self):
        """
            Test calculate_amount_with_tax for selling 
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_amount_with_tax(
                    Transaction.SELL,
                    value['i_shares_sell'],
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_tax_sell'])
            self.assertAlmostEqual(float(value['result_values']['amount_with_tax_sell']), float(result), 4)
        func = None
        calc = None
 
    def test_calculate_profit_loss(self):
        """
            Test calculate_profit_loss
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            result = calc.calculate_profit_loss(
                    func.test_conversion_to(value['i_price_buy_orig'], value['i_exchange_rate_buy']),
                    value['i_shares_buy'],
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell']),
                    value['i_shares_sell'],
                    value['i_tax_buy'],
                    value['i_tax_sell'],
                    value['i_commission_buy'],
                    value['i_commission_sell'],
                    value['i_long_bool'])
            self.assertAlmostEqual(float(value['result_values']['profit_loss']), float(result), 4)
        func = None
        calc = None

    def test_calculate_cost_other(self):
        """
            Test calculate_cost_other
        """
        calc = CalculatorFinance()
        for value in self.test_values:
            result = calc.calculate_cost_other(
                    value['result_values']['cost_total'],
                    value['result_values']['profit_loss'])
            self.assertAlmostEqual(float(value['result_values']['cost_other']), float(result), 4)
        calc = None

    def test_calculate_shares_recommended(self):
        """
            Test calculate_shares_recommended
        """
        calc = CalculatorFinance()
        func = Functions()
        for value in self.test_values:
            print ' test0: pool=', value['i_pool']
            print 'test1: margin_of_pool=', func.test_margin_of_pool(
                        value['i_pool'],
                        value['i_margin'])
            result = calc.calculate_shares_recommended(
                    func.test_margin_of_pool(
                        value['i_pool'],
                        value['i_margin']),
                    value['i_risk_input'],
                    value['i_commission_sell'],
                    value['i_tax_sell'],
                    func.test_conversion_to(value['i_price_sell_orig'], value['i_exchange_rate_sell'])
                    )
            self.assertAlmostEqual(float(value['result_values']['shares_recommended']), float(result), 4)
        func = None
        calc = None

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
    #getcontext().prec = 28
    unittest.main(verbosity=2)

#def run(self):
#        """
#           Run the unit tests. 
#        """
#        try:
#            print("test calc_..._test.py")
#            unittest.main()
#            print("test calc_..._test.py 2")
#        except Exception as ex:
#            print("Error running unittest: ", ex)
