"""
See LICENSE file for copyright and license details.
"""

"""
A file with financial calculations
"""

from modules.constant import * 
from decimal import Decimal
from math import floor
#from database import DatabaseAccess
#from modules.config import ConfigParser

## Market definitions ##
# binb00
markets_euronext_brussels = [
    "ebr"
 ]

markets_euronext_other = [
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

markets_us = [
    "nyse"
    ,"nasdaq"
    ,"otc bb & pinksheets"
    ,"amex"
    ,"other us"
]

markets_options_euronext = [
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
markets_cfd_share = [
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

markets_cfd_dev1 = [
    "cfd AU"
    ,"cfd AT"
]

markets_cfd_dev2 = [
    "cfd PL"
    ,"cfd CN"
    ,"cfd SG"
]

markets_cfd_non_share = [
    "cfd .gold"
    ,"cfd .silver"
    ,"cfd oil"
    ,"cfd index"
    ,"cfd other non-share"
]

markets_cfd_us = [
    "cfd US"
]

markets = markets_euronext_brussels + markets_euronext_other + markets_us + markets_options_euronext + markets_cfd_dev1 + markets_cfd_dev2 + markets_cfd_non_share + markets_cfd_us

## Helper functions ##
def is_euronext_brussels(market):
    """
        Market elem of markets_euronext_brussels?
    """
    return market in markets_euronext_brussels

def is_euronext_other(market):
    """
        Market elem of markets_euronext_other?
    """
    return market in markets_euronext_other

def is_us(market):
    """
        Market elem of markets_us?
    """
    return market in markets_us

def is_euro_exchange(market):
    """
        Market elem of <TBD>?
    """
    return market == "dummy"

def is_canada_exchange(market):
    """
        Market elem of <TBD>?
    """
    return market == "dummy"

def is_swiss_scandinavian_exchange(market):
    """
        Market elem of <TBD>?
    """
    return market == "dummy"

def is_non_share_cfd(market):
    """
        Market elem markets_cfd_non_share?
    """
    return market in markets_cfd_non_share

def is_share_cfd(market):
    """
        Market elem markets_cfd_share?
    """
    return market in markets_cfd_share

def is_share_cfd_dev1(market):
    """
        Market elem markets_cfd_dev1?
    """
    return market in markets_cfd_dev1

def is_share_cfd_dev2(market):
    """
        Market elem markets_cfd_dev2?
    """
    return market in markets_cfd_dev2

def is_share_cfd_us(market):
    """
        Market elem markets_cfd_us?
    """
    return market in markets_cfd_us

def is_options_euronext(market):
    """
        Market elem markets_options_euronext?
    """
    return market in markets_options_euronext

def calculate_percentage_of(value, from_value):
    """
       Calculate what percentage value is from from_value.
    """
    return value / from_value * Decimal(100.0)

## Financial calculations ##
def calculate_stoploss(price_buy, shares_buy, tax_buy, commission_buy, i_risk, pool_at_start):
    """
        Calculates the stoploss.
    """
    var_T = ((i_risk * price_buy) - calculate_amount_simple(price_buy, shares_buy)) - commission_buy
    var_N = shares_buy * (tax_buy - Decimal(1.0))
    return  var_T / var_N
        
def calculate_risk_input(i_pool, i_risk):
    """
        Calculates the risk based on total pool and input.
        Consider this the theoretical risk we want to take.
    """
    return i_risk/Decimal(100.0) * i_pool

def calculate_risk_initial(price_buy, shares_buy, stoploss):
    """
        Calculates the initial risk.
        This is the risk we will take if our stoploss is reached.
        This should be equal to the risk_input if everything was
        correctly calculated.
    """
    return (price_buy * shares_buy) - (stoploss * shares_buy)

def calculate_risk_actual(price_buy, shares_buy, price_sell, shares_sell, stoploss, risk_initial):
    """
        Calculates the risk we actually took,
        based on the data in TABLE_TRADE.
    """
    if price_sell < stoploss:
        result = (price_buy * shares_buy) - (price_sell * shares_sell)
    else:
        result = risk_initial
    return result

def calculate_r_multiple(price_buy, price_sell, stoploss):
    """ 
        Function to calculate R-multiple.
    """
    var_T = price_sell - price_buy
    var_N = price_buy - stoploss
    return var_T / var_N

def calculate_cost_total(tax_buy, commission_buy, tax_sell, commission_sell):
    """
        Returns the total costs associated with the given trade.
    """
    return tax_buy + commission_buy + tax_sell + commission_sell

def calculate_amount_simple(price, shares):
    """
        Calculates the amount without tax and commission.
    """
    return price * shares
    
def calculate_amount(price, shares, transactionid, tax, commission):
    """
        Calculates the amount, including tax and commission.
    """
    # NOTE:
    # AMT = SP + SPT + C (buy)
    # AMT = SP - SPT - C (buy)
    if transactionid == Transaction.BUY:
        return shares * price + shares * price * tax + commission
    else:
        return shares * price - shares * price * tax - commission

def cost_transaction(transactionid, price, shares, tax, commission):
    """
        Cost of transaction (tax and commission)
    """
    if transactionid == Transaction.SELL:
        result = (price * shares * (Decimal(1.0) - tax)) - commission
    else:
        result = (price * shares * (Decimal(1.0) + tax)) + commission
    return result
    
def cost_tax(transactionid, amount, commission, shares, price):
    """
        shares * price * tax_percentage for buy or sell
    """
    if transactionid == Transaction.SELL:
        result = -amount - commission + shares * price
    else:
        result = amount - shares * price - commission
    return result

def calculate_amount_with_tax(tax, shares, price):
    """
        Calculates the amount (buy/sell) with tax included, but not the commission.
    """
    return shares * price * ( Decimal(1.0) + tax)

def calculate_profit_loss(amount_sell_simple, amount_buy_simple, total_cost):
    """
        Calculates the profit_loss.
    """
    return amount_sell_simple - amount_buy_simple - total_cost

def calculate_cost_other(cost_total, profit_loss):
    """
        Calculates others costs based on the difference that remains.
    """
    diff_cost_profit = cost_total - profit_loss
    if diff_cost_profit > DEFAULT_DECIMAL:
        result = diff_cost_profit
    else:
        result = DEFAULT_DECIMAL
    return result

def calculate_shares_recommended(pool, risk, commission, tax, price):
    """
        Calculate the recommended amount of shares you can buy.
    """
    var_T = pool * risk
    var_N = price * (1 + tax)
    return  floor(var_T / var_N)

def calculate_price(transactionid, amount, shares, tax, commission):
    """
        Calculates the price when buying or selling
    """
    if transactionid == Transaction.SELL:
        var_T = amount + commission
        var_N = (Decimal(1.0) - tax) * shares
    else:
        var_T = amount - commission
        var_N = (Decimal(1.0) + tax) * shares
    return var_T / var_N

## Commission calculations ##
def calculate_commission(account, market, commodity, price, shares):
    """
        Calculate the correct commission.
    """
    result = DEFAULT_DECIMAL
    if account.lower() == "binb00":
        result = get_binb00_commission(market, price, shares)
    elif account.lower() == "whsi00":
        result = get_whsi00_commission(market, commodity, price, shares)
    return result

def get_binb00_commission(market, price, shares):
    """
        Get the correct commission for binb00.
    """
    amount_simple = self.calculate_amount_simple(price, shares)
    return get_bin00_commission_value(amount_simple, market)

def get_binb00_commission_index(market):
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

def get_binb00_commission_value(amount_simple, market):
    """
        Gets the binb00 commission for the given threshhold value.
    """
    index = get_binb00_commission_index(market)
    if amount_simple <= Decimal(2500.0):
        result = binb00_commissions["2500"][index]
    elif (amount_simple > Decimal(2500.0)) and (amount_simple <= Decimal(5000.0)):
        result = binb00_commissions["5000"][index]
    elif (amount_simple > Decimal(5000.0)) and (amount_simple <= Decimal(25000.0)):
        result = binb00_commissions["25000"][index]
    elif (amount_simple > Decimal(25000.0)) and (amount_simple <= Decimal(50000.0)):
        result = binb00_commissions["50000"][index]
    elif (amount_simple > Decimal(5000.0)):
        result = binb00_commissions["50000+"][index]
        #TODO: expand for options?
    else:
        result = DEFAULT_DECIMAL
    return result

def get_whsi00_commission(market, commodity, price, shares):
    """
        Get the correct commission for whsi00.
    """
    if is_non_share_cfd(market):
        result = Decimal(3.0)
    elif is_share_cfd(market):
        result = Decimal(4.50) + calculate_percentage_of(Decimal(0.054), amount_simple)
    elif is_share_cfd_dev1(market):
        result = Decimal(4.50) + calculate_percentage_of(Decimal(0.09), amount_simple)
    elif is_share_cfd_dev2(market):
        result = Decimal(4.50) + calculate_percentage_of(Decimal(0.19), amount_simple)
    elif is_share_cfd_us(market):
        result = Decimal(4.50) + Decimal(0.023) * shares
    else:
        result = DEFAULT_DECIMAL
    return result
