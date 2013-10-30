#!/usr/local/bin/python
"""
    See LICENSE file for copyright and license details.	
"""
from decimal import Decimal

class Align():
    RIGHT = '{: <0}'
    LEFT = '{: >0}'
    CENTER = '{: ^30}'

class Transaction():
    """
        Transaction types.
    """
    BUY = 0
    SELL = 1
 
DEFAULT_DATE = "1900-01-01"
DEFAULT_DECIMAL = Decimal('0.0')
