#!/usr/bin/env python
"""
See LICENSE file for copyright and license details.
"""

"""
A file with financial calculations
"""

from constant import * 
from decimal import Decimal, getcontext
from math import floor

class CalculatorFinance:
    """
        CalculatorFinance class with financial calculations.
    """
    
    def __init__(self):
        """
            Initialisation.
        """
        #TODO: since we are in python,
        # add an rc file with connection data
        # and retrieve all the below values
        # from the databas.
        getcontext().prec = 28

        ## Market definitions ##
        # binb00
        self.markets_euronext_brussels = [
            "ebr"
         ]

        self.markets_euronext_other = [
            "ams"
            ,"etr"
            ,"epa"
            ,"other"
            ,"eli"
            ,"lse"
            ,"ise"
            ,"mil"
            ,"bma"
            ,"vse"
            ,"other"
        ]

        self.markets_us = [
            "nyse"
            ,"nasdaq"
            ,"otc bb & pinksheets"
            ,"amex"
            ,"other us"
        ]

        self.markets_options_euronext = [
            "options ams"
            ,"options ebr"
        ]

        binb00_commissions = [
              {"2500":  [7.25, 9.75, 12.75, 12.75, 19.75, 29.75]}
            , {"5000":  [9.75, 9.25, 12.75, 12.75, 19.75, 29.75]}
            , {"25000": [13.75, 13.75, 16.75, 16.75, 24.75, 29.75]}
            , {"50000": [19.75, 19.75, 22.75, 22.75, 29.75, 59.75]}
            , {"50000+":[19.75, 19.75, 19.75, 19.72, 29.75, 29.75]}
            #TODO: expand for options?
        ]

        # whsi00
        self.markets_cfd_share = [
            "cfd BE"
            ,"cfd FR"
            ,"cfd DE"
            ,"cfd UK"
            ,"cfd DK"
            ,"cfd FI"
            ,"cfd IT"
            ,"cfd NL"
            ,"cfd NO"
            ,"cfd PT"
            ,"cfd SE"
            ,"cfd CH"
            ,"cfd ES"
            ,"cfd other share"
        ]

        self.markets_cfd_dev1 = [
            "cfd AU"
            ,"cfd AT"
        ]

        self.markets_cfd_dev2 = [
            "cfd PL"
            ,"cfd CN"
            ,"cfd SG"
        ]

        self.markets_cfd_non_share = [
            "cfd .gold"
            ,"cfd .silver"
            ,"cfd oil"
            ,"cfd index"
            ,"cfd other non-share"
        ]

        self.markets_cfd_us = [
            "cfd US"
        ]

        self.markets = self.markets_euronext_brussels + self.markets_euronext_other + self.markets_us + self.markets_options_euronext + self.markets_cfd_dev1 + self.markets_cfd_dev2 + self.markets_cfd_non_share + self.markets_cfd_us

    ## Helper functions ##
    def is_euronext_brussels(self, market):
        """
            Market elem of markets_euronext_brussels?
        """
        return market in self.markets_euronext_brussels

    def is_euronext_other(self, market):
        """
            Market elem of markets_euronext_other?
        """
        return market in self.markets_euronext_other

    def is_us(self, market):
        """
            Market elem of markets_us?
        """
        return market in self.markets_us

    def is_euro_exchange(self, market):
        """
            Market elem of <TBD>?
        """
        return market == "dummy"

    def is_canada_exchange(self, market):
        """
            Market elem of <TBD>?
        """
        return market == "dummy"

    def is_swiss_scandinavian_exchange(self, market):
        """
            Market elem of <TBD>?
        """
        return market == "dummy"

    def is_non_share_cfd(self, market):
        """
            Market elem markets_cfd_non_share?
        """
        return market in self.markets_cfd_non_share

    def is_share_cfd(self, market):
        """
            Market elem markets_cfd_share?
        """
        return market in self.markets_cfd_share

    def is_share_cfd_dev1(self, market):
        """
            Market elem markets_cfd_dev1?
        """
        return market in self.markets_cfd_dev1

    def is_share_cfd_dev2(self, market):
        """
            Market elem markets_cfd_dev2?
        """
        return market in self.markets_cfd_dev2

    def is_share_cfd_us(self, market):
        """
            Market elem markets_cfd_us?
        """
        return market in self.markets_cfd_us

    def is_options_euronext(self, market):
        """
            Market elem markets_options_euronext?
        """
        return market in self.markets_options_euronext

    def calculate_percentage_of(self, value, from_value):
        """
           Calculate what percentage value is from from_value.
        """
        return value / from_value * Decimal('100.0')

    ## Financial calculations ##
    def calculate_stoploss(self, price, shares, tax, commission, i_risk, i_pool, long_bool):
        """
            Calculates the stoploss.
            Note:
            Long
            ----
            amount selling at stoploss - amount at buying = initial risk of pool
            (S.Pb + S.Pb.T + C) - (S.Psl - S.Psl.T - C) -  = R/100 * pool
            
            Short
            -----
            amount selling - amount buying at stoploss = initial risk of pool
            (S.Psl + S.Psl.T + C) - (S.Ps - S.Ps.T - C) = R/100 * pool
        """
        if long_bool:
            var_T = shares * price * (Decimal('1.0') + tax / Decimal('100.0')) - (i_risk / Decimal('100.0') * i_pool) + Decimal('2.0') * commission
            var_N = shares * (Decimal('1.0') - tax / Decimal('100.0'))
            result = var_T / var_N
        else:
            var_T = (i_risk / Decimal('100.0') * i_pool) + shares * price * (Decimal('1.0') - tax / Decimal('100.0')) - Decimal('2.0') * commission
            var_N = shares * (Decimal('1.0') + tax / Decimal('100.0'))
            result = var_T / var_N
        return  result
            
    def calculate_risk_input(self, i_pool, i_risk):
        """
            Calculates the risk based on total pool and input.
            Consider this the theoretical risk we want to take.
        """
        return i_risk/Decimal('100.0') * i_pool

    def calculate_risk_initial(self, price, shares, tax, commission, stoploss, long_bool):
        """
            Calculates the initial risk.
            This is the risk we will take if our stoploss is reached.
            This should be equal to the risk_input if everything was
            correctly calculated.
            Note:
            Calculated using:
            
            long:
            S.Pb + S.Pb.T + C - (S.Psl - S.Psl.T - C)
            
            short:
            S.Ps + S.Psl.T + C - (S.Ps - S.Ps.T - C)
        """
        if long_bool:
            result = shares * price * (Decimal('1.0') + tax / Decimal('100.0')) - shares * stoploss * (Decimal('1.0') - tax / Decimal('100.0')) + Decimal('2.0') * commission
        else:
            result = shares * stoploss * (Decimal('1.0') + tax / Decimal('100.0')) - shares * price * (Decimal('1.0') - tax / Decimal('100.0')) + Decimal('2.0') * commission

        return abs(result)

    def calculate_risk_actual(self, price_buy, shares_buy, tax_buy, commission_buy, price_sell, shares_sell, tax_sell, commission_sell, stoploss, risk_initial, profit_loss, long_bool):
        """
            Calculates the risk we actually took,
            based on the data in TABLE_TRADE.
            Note:
            Calculation based on:
            
            risk_actual = S.Pb + S.Pb.T + Cb - (S.Ps - S.Ps.T - Cs)
            
            Note:
            -----
            It's the same for long and short.
        """
        if ((profit_loss < DEFAULT_DECIMAL) and (abs(profit_loss) < risk_initial)) or (profit_loss >= DEFAULT_DECIMAL):
            result = risk_initial
        else:
            result = shares_buy * price_buy * (Decimal('1.0') + tax_buy / Decimal('100.0')) - shares_sell * price_sell * (Decimal('1.0') - tax_buy / Decimal('100.0')) + commission_buy + commission_sell
        return abs(result)

    def calculate_r_multiple(self, profit_loss, risk_initial):
        """ 
            Function to calculate R-multiple.
        """
        return profit_loss / risk_initial


    def calculate_cost_total(self, tax_buy, commission_buy, tax_sell, commission_sell):
        """
            Returns the total costs associated with the given trade.
        """
        #TODO: fix this: tax * amount_buy_simple!
        return tax_buy / Decimal('100.0') + commission_buy + tax_sell / Decimal('100.0') + commission_sell

    def calculate_amount_simple(self, price, shares):
        """
            Calculates the amount without tax and commission.
        """
        return price * shares
        
    def calculate_amount(self, price, shares, transactionid, tax, commission):
        """
            Calculates the amount, including tax and commission.
        """
        # NOTE:
        # AMT = SP + SPT + C (buy)
        # AMT = SP - SPT - C (sell)
        if transactionid == Transaction.BUY:
            return shares * price + shares * price * tax + commission
        else:
            return shares * price - shares * price * tax - commission

    def cost_transaction(self, transactionid, price, shares, tax, commission):
        """
            Cost of transaction (tax and commission)
            price * shares * tax + commission
        """
        return (price * shares * tax) + commission
        
    def cost_tax(self, transactionid, amount, commission, shares, price):
        """
            shares * price * tax_percentage for buy or sell
        """
        if transactionid == Transaction.SELL:
            result = - amount - commission + shares * price
        else:
            result = amount - shares * price - commission
        return result

    def calculate_amount_with_tax(self, transactionid, shares, price, tax):
        """
            Calculates the amount (buy/sell) with tax included, but not the commission.
            Note:
            Calculation based on:
            buy
            ----
            profit_loss = S.P + S.P.T
            
            sell 
            -----
            profit_loss = S.P - S.P.T
        """
        if transactionid == Transaction.SELL:
            result = shares * price * (Decimal('1.0') + tax / Decimal('100.0'))
        else:
            result = shares * price * (Decimal('1.0') - tax / Decimal('100.0'))
        return result

    def calculate_profit_loss(self, price_buy, shares_buy, price_sell, shares_sell, tax_buy, tax_sell, commission_buy, commission_sell, long_bool):
        """
            Calculates the profit_loss.
            Note:
            Calculation based on:
            long
            ----
            profit_loss =  S.Ps - S.Ps.T - C - (S.Pb + S.Pb.T + C)
            
            short
            -----
            profit_loss = S.Ps - S.Ps.T - C - (S.Pb + S.Pb.T + C) 

        """
        return shares_sell * price_sell * (1 - tax_sell / Decimal('100.0')) - shares_buy * price_buy * (1 - tax_buy / Decimal('100.0')) - (commission_buy + commission_sell)

    def calculate_cost_other(self, cost_total, profit_loss):
        """
            Calculates others costs based on the difference that remains.
        """
        diff_cost_profit = cost_total - profit_loss
        if diff_cost_profit > DEFAULT_DECIMAL:
            result = diff_cost_profit
        else:
            result = DEFAULT_DECIMAL
        return result

    def calculate_shares_recommended(self, pool, risk, commission, tax, price):
        """
            Calculate the recommended amount of shares you can buy.
        """
        var_T = pool - (tax / Decimal('100.0') * pool) - commission
        var_N = price
        return  floor(var_T / var_N)

    def calculate_price(self, transactionid, amount, shares, tax, commission):
        """
            Calculates the price when buying or selling
        """
        if transactionid == Transaction.SELL:
            var_T = amount + commission
            var_N = (Decimal('1.0') - tax / Decimal('100.0')) * Decimal(str(shares))
        else:
            var_T = amount - commission
            var_N = (Decimal('1.0') + tax / Decimal('100.0')) * Decimal(str(shares))
        return var_T / var_N

## Commission calculations ##
    def calculate_commission(self, account, market, commodity, price, shares):
        """
            Calculate the correct commission.
        """
        result = DEFAULT_DECIMAL
        if account.lower() == "binb00":
            result = get_binb00_commission(market, price, shares)
        elif account.lower() == "whsi00":
            result = self.get_whsi00_commission(market, commodity, price, shares)
        return result

    def get_binb00_commission(self, market, price, shares):
        """
            Get the correct commission for binb00.
        """
        amount_simple = self.calculate_amount_simple(price, shares)
        return get_bin00_commission_value(amount_simple, market)

    def get_binb00_commission_index(self, market):
        """
            Gets the index needed to get the correct value
            from binb00_commissions.
        """
        if is_euronext_brussels(market):
            result = 0
        elif is_euronext_other(market):
            result = 1
        elif is_euro_exchange(market):
            result = 2
        elif is_us(market):
            result = 3
        elif is_canada_exchange(market):
            result = 4
        elif is_swiss_scandinavian_exchange(market):
            result = 5
            #TODO: expand for options
        else:
            #TODO: raise exception, now it will take the last value
            result = -1
        return result

    def get_binb00_commission_value(self, amount_simple, market):
        """
            Gets the binb00 commission for the given threshhold value.
        """
        index = self.get_binb00_commission_index(market)
        if amount_simple <= Decimal('2500.0'):
            result = self.binb00_commissions["2500"][index]
        elif (amount_simple > Decimal('2500.0')) and (amount_simple <= Decimal('5000.0')):
            result = self.binb00_commissions["5000"][index]
        elif (amount_simple > Decimal('5000.0')) and (amount_simple <= Decimal('25000.0')):
            result = self.binb00_commissions["25000"][index]
        elif (amount_simple > Decimal('25000.0')) and (amount_simple <= Decimal('50000.0')):
            result = self.binb00_commissions["50000"][index]
        elif (amount_simple > Decimal('5000.0')):
            result = self.binb00_commissions["50000+"][index]
            #TODO: expand for options?
        else:
            result = DEFAULT_DECIMAL
        return result

    def get_whsi00_commission(self, market, commodity, price, shares):
        """
            Get the correct commission for whsi00.
        """
        if self.is_non_share_cfd(market):
            result = Decimal('3.0')
        elif self.is_share_cfd(market):
            result = Decimal('4.50') + self.calculate_percentage_of(Decimal('0.054'), amount_simple)
        elif self.is_share_cfd_dev1(market):
            result = Decimal('4.50') + self.calculate_percentage_of(Decimal('0.09'), amount_simple)
        elif self.is_share_cfd_dev2(market):
            result = Decimal('4.50') + self.calculate_percentage_of(Decimal('0.19'), amount_simple)
        elif self.is_share_cfd_us(market):
            result = Decimal('4.50') + Decimal('0.023') * Decimal(str(shares))
        else:
            result = DEFAULT_DECIMAL
        return result
