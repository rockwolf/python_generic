#! /usr/local/bin/python
"""
    See LICENSE file for copyright and license details.					
"""

from decimal import Decimal

class Table():
    """
       Tables.
    """
    FINANCE = 't_finance'
    INVESTMENT = 't_investment'
    MARKET = 't_market'
    STOCK_NAME = 't_stock_name'
    ACCOUNT = 't_account'
    CURRENCY = 't_currency'
    CURRENCY_EXCHANGE = 't_currency_exchange'
    FORMULA = 't_formula'
    PARAMETER = 't_parameter'
    TRADE = 't_trade'
    RATE = 't_rate'
    DRAWDOWN = 't_drawdown'
    MARGIN = 't_margin'
    MARGIN_TYPE = 't_margin_type'
    POOL = 't_pool'
    
class View():
    """
        Views.
    """
    FINANCE = 'v_finance'
    INVESTMENT = 'v_investment'
    MARKET = 'v_market'
    STOCK_NAME = 'v_stock_name'
    ACCOUNT = 'v_account'
    CURRENCY = 'v_currency'
    CURRENCY_EXCHANGE = 'v_currency_exchange'
    FORMULA = 'v_formula'
    PARAMETER = 'v_parameter'
    TRADE = 'v_trade'
    RATE = 'v_rate'
    DRAWDOWN = 'v_drawdown'
    MARGIN = 'v_margin'
    MARGIN_TYPE = 'v_margin_type'
    POOL = 'v_pool'
    REP_CHECK_TOTAL = 'v_rep_check_total'
    ACCOUNT_NAME = 'v_account_name'

class Error():
    """
        Error messages.
    """
    GET_MARKET_DESCRIPTION = "Error in get_marketdescription: "
    GET_CATEGORIES = "Error in get_categories: "
    GET_ACCOUNTS = "Error in get_accounts: "
    GET_MARKETS = "Error in get_markets: "
    GET_STOCK_NAMES = "Error in get_stocknames: "
    GET_STOCK_DESCRIPTION = "Error in get_stockdescription: "
    GET_STOCK_INFO = "Error in get_stockinfo: "
    GET_CURRENCIES = "Error in get_currencies: "
    EXPORT_RECORDS = "Error in export_records: "
    SUBCATEGORY_ID_FROM_SUBCATEGORY = "Error retrieving subcategory_id: "
    ACCOUNT_ID_FROM_ACCOUNT = "Error retrieving account_id: "
    WRITE_TO_DATABASE_MAIN = "Error in write_to_database from main controller: "
    WRITE_TO_DATABASE = "Error in write_to_database: "
    WRITE_TO_DATABASE_SESSION = "Error creating session in write_to_database: "
    WRITE_TO_DATABASE_CORE = "Error creating session in write_to_database from core_module: "
    INSERT_DATABASE = "Error in write_statement_list_insert: "
    UPDATE_DATABASE = "Error in write_statement_list_update: "
    DELETE_DATABASE = "Error in write_statement_list_delete: "
    GET_INPUT_FIELDS = "Error in get_input_fields: "
    CREATE_STATEMENTS_TABLE_FINANCE = "Error in create_statements_TABLE_FINANCE: "
    CREATE_STATEMENTS_TABLE_STOCK = "Error in create_statements_TABLE_STOCK: "
    CREATE_STATEMENTS_TABLE_TRADE = "Error in create_statements_TABLE_TRADE: "
    CREATE_STATEMENTS_TABLE_INVESTMENT = "Error in create_statements_TABLE_INVESTMENT: "
    CREATE_STATEMENTS_TABLE_RATE = "Error in create_statements_TABLE_RATE: "
    CREATE_STATEMENTS_TABLE_CURRENCY_EXCHANGE = "Error in create_statements_TABLE_CURRENCY_EXCHANGE: "
    INVADE_ALREADY_STARTED = "Error in invade_already_started: "
    NEW_DRAWDOWN_RECORD = "Error in new_drawdown_record: "
    GET_SPECIFIC_FINANCE_RECORD = "Error in get_specific_finance_record: "

class InputIndex():
    """
        Index for the input list, for easy recognition.
    """
    DATE = 0
    ACCOUNT_FROM = 1
    ACCOUNT_TO = 2
    AMOUNT = 3
    COMMENT = 4
    STOCK = 5
    STOCK_DESCRIPTION = 6
    MARKET = 7
    MARKET_DESCRIPTION = 8
    QUANTITY = 9
    PRICE = 10
    COMMISSION = 11
    TAX = 12
    RISK = 13
    CURRENCY_FROM = 14
    CURRENCY_TO = 15
    EXCHANGE_RATE = 16
    MANUAL_COMMISSION = 17
    DATE_EXPIRATION = 18
    POOL = 19
    PERIODIC_FLAG = 20
    PERIODIC_START = 21
    PERIODIC_END = 22
    SIZE = 22 #size of the enum
    
class Message():
    """
       Messages to print to stdout.
    """
    EXEC_ALL = "Executing statements all at once..."
    PREPARING = "Preparing statements..."
    DONE = "Done."
    
class Export():
    """
        Export types.
    """
    LEDGER = "ledger"
    CSV = "csv"
    
class Statement():
    """
        Statement types.
    """
    INSERT = 0
    UPDATE = 1
    DELETE = 2
    
class Transaction():
    """
        Transaction types.
    """
    BUY = 0
    SELL = 1
    
TRADING_ACCOUNTS = ['whsi00']
INVESTMENT = ['stock', 'fund', 'bond']
#TODO: credit the giver? How to add to NEGATIVES?
NEGATIVES = ['income', 'capital_gain', 'profit', 'liabilities']
    
DEFAULT_DATE = "1900-01-01"
DEFAULT_DECIMAL = Decimal(0.0)
DEFAULT_INT = 0
TRADING_ACCOUNT_ID = 6
