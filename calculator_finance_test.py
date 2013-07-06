#!/usr/env/python
"""
See LICENSE file for copyright and license details.
"""

"""
Unit test for calculator_finance.py
"""
import calculator_finance
import unittest
from decimal import Decimal, getcontext
from function import *
from modules.constant import *

class TestValues(unittest.TestCase):
    """
        Test the calculations with an example.
    """
    test_values = [] 
    # Profit - long
    ## buy 99 devg at 25, sell at 30
    test_values.append({
        'i_date_buy':string_to_date("2013-06-12"),
        'i_date_sell':string_to_date("2013-06-12"),
        'i_account_from':'assets:current_assets:binb00', #Note: Get account_id from T_ACCOUNT for final insert
        'i_account_to':'assets:stock:ebr.devg',
        'i_amount_buy':Decimal(2488.44),
        'i_amount_sell':Decimal(2955.33),
        'i_comment':'test comment',
        'i_stock_name':'devg',
        'i_stock_description':'Devgen N.V.',
        'i_market_name':'ebr',
        'i_market_description':'Europe Brussels',
        'i_shares_buy':Decimal(99.0),
        'i_shares_sell':Decimal(99.0),
        'i_price_buy':Decimal(25.0),
        'i_price_sell':Decimal(30.0),
        'i_commission_buy':Decimal(7.25),
        'i_commission_sell':Decimal(7.25),
        'i_tax_buy':Decimal(0.0025),
        'i_tax_sell':Decimal(0.0025),
        'i_risk_input':Decimal(0.02),
        'i_currency_from':'EUR', #Note: Get currency_id from T_CURRENCY for final insert
        'i_currency_to':'EUR', #Note: Get currency_id from T_CURRENCY for final insert
        'i_exchange_rate':Decimal(1.0),
        'i_automatic_flag':0,
        'i_date_expiration':string_to_date("2014-01-01"),
        'i_periodic':0,
        'i_periodic_start':string_to_date("1900-01-01"),
        'i_periodic_end':string_to_date("1900-01-01"),
        'i_pool':Decimal(50000),
        'result_values': {
            'stoploss': Decimal(7.28)
            ,'risk_input': Decimal(0.002)
            ,'risk_initial': Decimal(2500)
            ,'risk_actual': Decimal(1754.28)
            ,'r_multiple': Decimal(0.28)
            ,'cost_total': Decimal(28.12)
            ,'amount_buy_simple':Decimal(2475.0)
            ,'amount_sell_simple':Decimal(2970.0)
            ,'amount_buy':Decimal(2488.44)
            ,'amount_sell':Decimal(2955.33)
            ,'cost_transaction_buy': Decimal(13.44)
            ,'cost_transaction_sell': Decimal(14.68)
            ,'cost_tax_buy': Decimal(4.21)
            ,'cost_tax_sell': Decimal(5.05)
            ,'amount_with_tax_buy': Decimal(2481.19)
            ,'amount_with_tax_sell': Decimal(2977.42)
            ,'profit_loss': Decimal(494.11)
            ,'cost_other': Decimal(0.0)
            ,'shares_recommended': Decimal(99.0)
            ,'price_buy':Decimal(25.0)
            ,'price_sell':Decimal(30.0)
            ,'commission_buy':Decimal(7.25)
            ,'commission_sell':Decimal(7.25)
        } 
    })
    
    def test_calculate_percentage_of(self):
        """
            Test calculate_percentage_of
        """
        result = calculator_finance.calculate_percentage_of(
                Decimal(25.45),
                Decimal(100.0))
        self.assertAlmostEqual(float(25.45), float(result), 4)

    def test_calculate_stoploss(self):
        """
            Test calculate_stoploss
        """
        for value in self.test_values:
            result = calculator_finance.calculate_stoploss(
                    value['i_price_buy'],
                    value['i_shares_buy'],
                    value['i_tax_buy'],
                    value['i_commission_buy'],
                    value['i_risk_input'],
                    value['i_pool'])
            self.assertAlmostEqual(float(value['result_values']['stoploss']), float(result), 4)

    def test_calculate_risk_input(self):
        """
            Test calculate_risk_input
        """
        for value in self.test_values:
            result = calculator_finance.calculate_risk_input(
                    value['i_pool'],
                    value['i_risk_input'])
            self.assertAlmostEqual(float(value['result_values']['risk_input']), float(result), 4)

    def calculate_risk_initial(self):
        """
            Test calculate_risk_initial
        """
        for value in self.test_values:
            result = calculator_finance.calculate_risk_initial(
                    value['i_price_buy'],
                    value['i_shares'],
                    value['result_values']['stoploss'])
            self.assertAlmostEqual(float(value['result_values']['risk_initial']), float(result), 4)
                    

    def calculate_risk_actual(self):
        """
            Test calculate_risk_actual
        """
        for value in self.test_values:
            result = calculator_finance.calculate_risk_actual(
                    value['result_values']['price_buy'],
                    value['result_values']['shares_buy'],
                    value['i_price_sell'],
                    value['i_shares_sell'],
                    value['result_values']['stoploss'],
                    value['result_values']['risk_initial'])
            self.assertAlmostEqual(float(value['result_values']['risk_actual']), float(result), 4)

    def calculate_r_multiple(self):
        """
            Test calculate_r_multiple
        """
        for value in self.test_values:
            result = calculator_finance.calculate_r_multiple(
                    value['result_values']['i_price_buy'],
                    value['i_price_sell'],
                    value['result_values']['stoploss'])
            self.assertAlmostEqual(float(value['result_values']['r_multiple']), float(result), 4)

    def calculate_cost_total(self):
        """
            Test calculate_cost_total
        """
        for value in self.test_values:
            result = calculator_finance.calculate_cost_total(
                    value['result_values']['tax_buy'],
                    value['result_values']['commission_buy'],
                    value['i_tax_sell'],
                    value['i_commission_sell'])
            self.assertAlmostEqual(float(value['result_values']['cost_total']), float(result), 4)

    def test_calculate_amount_buy_simple(self):
        """
            Test calculate_amount_simpel for buying
        """
        for value in self.test_values:
            result = calculator_finance.calculate_amount_simple(
                    value['i_price_buy'],
                    value['i_shares_buy'])
            self.assertAlmostEqual(float(value['result_values']['amount_buy_simple']), float(result), 4)

    def test_calculate_amount_sell_simple(self):
        """
            Test calculate_amount_simpel for selling
        """
        for value in self.test_values:
            result = calculator_finance.calculate_amount_simple(
                    value['i_price_sell'],
                    value['i_shares_sell'])
            self.assertAlmostEqual(float(value['result_values']['amount_sell_simple']), float(result), 4)
    
    def test_calculate_amount_buy(self):
        """
            Test calculate_amount for buying
        """
        # AMT = SP + SPT + C
        #     = SP * (1 + T) + C
        #     = 99 * 25.0 * (1 + 0.0025) + 7.25
        #     = 2488.4375
        for value in self.test_values:
            result = calculator_finance.calculate_amount(
                    value['i_price_buy'],
                    value['i_shares_buy'],
                    Transaction.BUY,
                    value['i_tax_buy'],
                    value['i_commission_buy'])
            self.assertAlmostEqual(float(value['result_values']['amount_buy']), float(result), 4)
                    
    def test_calculate_amount_sell(self):
        """
            Test calculate_amount for selling
        """
        # AMT = SP - SPT - C
        #     = SP * (1 - T) - C
        #     = 99 * 30.0 * (1 - 0.0025) - 7.25
        #     = 2955.3250
        for value in self.test_values:
            result = calculator_finance.calculate_amount(
                    value['i_price_sell'],
                    value['i_shares_sell'],
                    Transaction.SELL,
                    value['i_tax_sell'],
                    value['i_commission_sell'])
            self.assertAlmostEqual(float(value['result_values']['amount_sell']), float(result), 4)
    
    def test_cost_transaction_buy(self):
        """
            Test cost_transaction for buying
        """
        for value in self.test_values:
            result = calculator_finance.cost_transaction(
                    Transaction.BUY,
                    value['i_price_buy'],
                    value['i_shares_buy'],
                    value['i_tax_buy'],
                    value['i_tax_sell'])
            self.assertAlmostEqual(float(value['result_values']['cost_transaction_buy']), float(result), 4)

    def test_cost_transaction_sell(self):
        """
            Test cost_transaction for selling
        """
        for value in self.test_values:
            result = calculator_finance.cost_transaction(
                    Transaction.SELL,
                    value['i_price_sell'],
                    value['i_shares_sell'],
                    value['i_tax_sell'],
                    value['i_tax_sell'])
            self.assertAlmostEqual(float(value['result_values']['cost_transaction_sell']), float(result), 4)

    def test_cost_tax_buy(self):
        """
            Test cost_tax for buying
        """
        for value in self.test_values:
            result = calculator_finance.cost_tax(
                    Transaction.BUY,
                    value['i_amount_buy'],
                    value['i_commission_buy'],
                    value['i_shares_buy'],
                    value['i_price_buy'])
            self.assertAlmostEqual(float(value['result_values']['cost_tax_buy']), float(result), 4)

    def test_cost_tax_sell(self):
        """
            Test cost_tax for selling
        """
        for value in self.test_values:
            result = calculator_finance.cost_tax(
                    Transaction.SELL,
                    value['i_amount_sell'],
                    value['i_commission_sell'],
                    value['i_shares_sell'],
                    value['i_price_sell'])
            self.assertAlmostEqual(float(value['result_values']['cost_tax_sell']), float(result), 4)

    def test_calculate_amount_with_tax_buy(self):
        """
            Test calculate_amount_with_tax for buying
        """
        for value in self.test_values:
            result = calculator_finance.calculate_amount_with_tax(
                    value['i_tax_buy'],
                    value['i_shares_buy'],
                    value['i_price_buy'])
            self.assertAlmostEqual(float(value['result_values']['amount_with_tax_buy']), float(result), 4)

    def test_calculate_amount_with_tax_sell(self):
        """
            Test calculate_amount_with_tax for selling
        """
        for value in self.test_values:
            result = calculator_finance.calculate_amount_with_tax(
                    value['i_tax_sell'],
                    value['i_shares_sell'],
                    value['i_price_sell'])
            self.assertAlmostEqual(float(value['result_values']['amount_with_tax_sell']), float(result), 4)


    def test_calculate_profit_loss(self):
        """
            Test calculate_profit_loss
        """
        for value in self.test_values:
            result = calculator_finance.calculate_profit_loss(
                    value['result_values']['amount_sell_simple'],
                    value['result_values']['amount_buy_simple'],
                    value['result_values']['cost_total'])
            self.assertAlmostEqual(float(value['result_values']['profit_loss']), float(result), 4)

    def test_calculate_cost_other(self):
        """
            Test calculate_cost_other
        """
        for value in self.test_values:
            result = calculator_finance.calculate_cost_other(
                    value['result_values']['cost_total'],
                    value['result_values']['profit_loss'])
            self.assertAlmostEqual(float(value['result_values']['cost_other']), float(result), 4)

    def test_calculate_shares_recommended(self):
        """
            Test calculate_shares_recommended
        """
        for value in self.test_values:
            result = calculator_finance.calculate_shares_recommended()
            self.assertAlmostEqual(float(value['result_values']['cost_other']), float(result), 4)

    def test_calculate_price_buy(self):
        """
            Test calculate_price at buying.
        """
        for value in self.test_values:
            result = calculator_finance.calculate_price(
                    Transaction.BUY,
                    value['i_amount_buy'],
                    value['i_shares_buy'],
                    value['i_tax_buy'],
                    value['i_commission_buy'])
            self.assertAlmostEqual(float(value['result_values']['price_buy']), float(result), 4)

    def test_calculate_price_sell(self):
        """
            Test calculate_price at selling.
        """
        for value in self.test_values:
            result = calculator_finance.calculate_price(
                    Transaction.SELL,
                    value['i_amount_sell'],
                    value['i_shares_sell'],
                    value['i_tax_sell'],
                    value['i_commission_sell'])
            self.assertAlmostEqual(float(value['result_values']['price_sell']), float(result), 4)

    def test_calculate_commission_buy(self):
        """
            Test calculate_commission for buying
        """
        for value in self.test_values:
            result = calculator_finance.calculate_commission(
                    value['i_account_to'],
                    value['i_market_name'],
                    value['i_stock_name'],
                    value['i_price_buy'],
                    value['i_shares_buy'])
            self.assertAlmostEqual(float(value['result_values']['commission_buy']), float(result), 4)

    def test_calculate_commission_sell(self):
        """
            Test calculate_commission for selling
        """
        for value in self.test_values:
            result = calculator_finance.calculate_commission(
                    value['i_account_to'],
                    value['i_market_name'],
                    value['i_stock_name'],
                    value['i_price_sell'],
                    value['i_shares_sell'])
            self.assertAlmostEqual(float(value['result_values']['commission_sell']), float(result), 4)

if __name__ == "__main__":
    getcontext().prec = 6
    unittest.main()   
