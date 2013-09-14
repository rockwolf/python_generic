#! /usr/local/bin/python
"""
See LICENSE file for copyright and license details.
"""

from sqlalchemy import Table, MetaData, \
        Column, Integer, or_, and_
from sqlalchemy.types import VARCHAR
#from sqlalchemy.sql import exisst
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from decimal import Decimal
from datetime import datetime

from modules_generic.function import *
from modules_generic.function_sqlalchemy import row_to_dict
from modules_generic.messagehandler import *
from modules_generic.calculator_finance import *
from modules.constant import *
from modules.function import *
from meta import engine, Base
from database.mappings import *
from database.mappings_views import *

class DatabaseAccess():
    """
    Connecting to the database.
    """

    def __init__(self, config):
        """
        Initialize object.
        """
        try:
            self.config = config
            self.Session = sessionmaker(bind=engine)
            self.metadata = Base.metadata
            #self.map_tables()
            #self.map_views()
            self.tables = [x for x in self.metadata.tables.keys() if is_a_table(x) ]
        except Exception as ex:
            print("Error in initialisation of DatabaseAccess: ", ex)
 
    def get_account_list(self):
        """
        Get the account_names in a list.
        """
        values = []
        try:
            session = self.Session()
            query = session.query(T_ACCOUNT)
            for instance in query:
                values.append(instance.name)
        except Exception as ex:
            print(Error.GET_ACCOUNT_LIST, ex)
        finally:
            session.rollback()
            session = None
        return values

    def get_markets(self):
        """
        Get the market codes.
        """
        values = []
        try:
            session = self.Session()
            query = session.query(T_MARKET).filter(
                    T_MARKET.active == 1)
            for instance in query:
                values.append(instance.code)
        except Exception as ex:
            print(Error.GET_MARKETS, ex)
        finally:
            session.rollback()
            session = None
        return values
 
    def get_stock_names(self, code):
        """
        Get the stock names.
        """
        values = []
        try:
            session = self.Session()
            query = session.query(T_STOCK_NAME).join(
                T_MARKET,
                T_STOCK_NAME.market_id == T_MARKET.market_id
            ).filter(
                T_MARKET.code == code,
                T_STOCK_NAME.active == 1
            )
            for instance in query:
                values.append(instance.name)
        except Exception as ex:
            print("Error in get_stock_names: ", ex)
        finally:
            session.rollback()
            session = None
        return values

    def get_market_description(self, market):
        """
        Get the market description.
        """
        value = ''
        try:
            session = self.Session()
            query = session.query(T_MARKET).filter(T_MARKET.code == market)
            for instance in query:
                value = instance.name
                break
        except Exception as ex:
            print(Error.GET_MARKET_DESCRIPTION, ex)
        finally:
            session.rollback()
            session = None
        return value

    def get_stock_description(self, stock):
        """
        Get the stock description.
        """
        value = ''
        try:
            session = self.Session()
            query = session.query(T_STOCK_NAME).filter(T_STOCK_NAME.name == stock)
            for instance in query:
                value = instance.description
                break
        except Exception as ex:
            print("Error in get_stock_description: ", ex)
        finally:
            session.rollback()
            session = None
        return value

    def get_stockinfo(self, sname):
        """
        Get extra stock info.
        """
        values = []
        try:
            session = self.Session()
            query = session.query(
                T_STOCK_NAME.name.label("stock_name"),
                T_MARKET.name.label("marketname"),
                T_MARKET.country
            ).join(
                T_MARKET,
                T_STOCK_NAME.market_id == T_MARKET.market_id
            ).filter(
                T_STOCK_NAME.name == sname
            )
            for instance in query:
                values.append(instance.stock_name)
                values.append(instance.marketname)
                values.append(instance.country)
        except Exception as ex:
            print(Error.GET_STOCK_INFO, ex)
        finally:
            session.rollback()
            session = None
        return values
     
    def get_currencies(self):
        """
        Get the currency codes.
        """
        values = []
        try:
            session = self.Session()
            query = session.query(T_CURRENCY)
            for instance in query:
                values.append(instance.code)
        except Exception as ex:
            print(Error.GET_CURRENCIES, ex)
        finally:
            session.rollback()
            session = None
        return values
    
    def account_id_from_account_name(self, account_name, from_account = True):
        """
        Get the account_id from an account.
        """
        result = -1
        session = self.Session()
        try:
            date_created = current_date()
            date_modified = current_date()
            # Get account id, based on account name
            # but first check if the account already exists
            # in T_ACCOUNT. If not, add it to the t_account table.
            obj = session.query(T_ACCOUNT).filter_by(name=account).first() is not None
            if not obj:
                if from_account:
                    description_list = self.gui.get_account_from().split(':')
                    description = description_list[len(descpription_list)-1]
                else:
                    description = self.gui.get_account_to().split(':')
                    description = description_list[len(descpription_list)-1]
                session.add(T_ACCOUNT(account, description, date_created, date_modified))
                session.commit()
                for instance in session.query(func.max(T_ACCOUNT.account_id).label('account_id')):
                    result = instance.account_id
            else:
                for instance in session.query(T_ACCOUNT).filter_by(name=account):
                    result = str(instance.account_id)
        except Exception as ex:
            print(Error.ACCOUNT_ID_FROM_ACCOUNT, ex)
        finally:
            session.rollback()
            session = None
        return result

    def stock_name_id_from_stock_name(self, stock_name, market_id):
        """
        Get the stock_name_id from T_STOCK_NAME.
        """
        result = -1
        session = self.Session()
        try:
            date_created = current_date()
            date_modified = current_date()
            # Get stock_name_id, based on stock_name
            # but first check if the stock_name already exists
            # in T_STOCK_NAME. If not, add it to the table.
            obj = session.query(T_STOCK_NAME).filter_by(name=stock_name, market_id=market_id).first() is not None
            if not obj:
                session.add(T_STOCK_NAME(stock_name, market_id, self.gui.get_stock_description(), date_created, date_modified))
                session.commit()
                for instance in session.query(func.max(T_STOCK_NAME.stock_name_id).label('stock_name_id')):
                    result = instance.stock_name_id
            else:
                for instance in session.query(T_STOCK_NAME).filter_by(name=stock_name, market_id=market_id):
                    result = str(instance.stock_name_id)
        except Exception as ex:
            print("Error retrieving stock_name_id: ", ex)
        finally:
            session.rollback()
            session = None
        return result

    def market_id_from_market(self, code):
        """
        Get the market_id from T_MARKET.
        """
        result = -1
        session = self.Session()
        try:
            date_created = current_date()
            date_modified = current_date()
            obj = session.query(T_MARKET).filter_by(code=code).first() is not None
            if not obj:
                # NOTE: this code means that when new market records have been added
                # during normal usage, a new uninstall/install/import will not be able
                # to fill in the name and country of the market.
                # For now, assume no new ones are added. If there are, add them to the
                # init_tables script!
                #TODO: add extra field in gui for the country code and country name
                # + add this to the input_fields. This way, we can also add new markets.
                # But: perhaps this makes the input too complex and a new button with a dialog window
                # behind it is needed?
                session.add(T_MARKET(None, code, 'TBD', '??', 1, date_created, date_modified))
                session.commit()
                for instance in session.query(func.max(T_MARKET.market_id).label('market_id')):
                    result = instance.market_id
            else:
                for instance in session.query(T_MARKET).filter_by(code=code):
                    result = str(instance.market_id)
        except Exception as ex:
            print("Error retrieving market_id: ", ex)
        finally:
            session.rollback()
            session = None
        return result

    def account_name_from_account_id(self, account_id):
        """
         Get the account_name for a given account_id from the T_ACCOUNT table.
        """
        result = ''
        session = self.Session()
        try:
            for instance in session.query(V_ACCOUNT_NAME).filter_by(account_id=account_id):
                result = instance.name
        except Exception as ex:
            print("Error retrieving accountname from account_id: ", ex)
        finally:
            session.rollback()
            session = None
        return result

    def currency_id_from_currency(self, currency):
        """
        Get the currency_id from a currency string (e.g.'USD').
        """
        result = -1
        session = self.Session()
        try:
            first_obj = session.query(T_CURRENCY).filter_by(code=currency).first()
            if first_obj is not None:
                result = str(first_obj.currency_id)
            else:
                raise Exception("Error: currency {0} not found! -1 used as a currency_id.".format(currency))
        except Exception as ex:
            print(Error.ACCOUNT_ID_FROM_ACCOUNT, ex)
        finally:
            session.rollback()
            session = None
        return result

    def get_parameter_value(self, parameter_id):
        """
        Function to get the value that belongs to the given parameter.
        """
        result = ''
        session = self.Session()
        try:
            for instance in session.query(T_PARAMETER).filter_by(
                    parameter_id=parameter_id):
                result = instance.value
        except Exception as ex:
            print("Error retrieving parameter value: ", ex)
        finally:
            session.rollback()
            session = None
        return result

    def get_record(self, row):
        """
        Gets a dictionary with the fields of a return record from the
        database.
        """
        result = {}
        try:
            result = row_to_dict(row)
        except Exception as ex:
            print("Error in get_record: ", ex)
        return result

    def get_pool(self):
        """
        Gets the pool available for trading.
        """
        result = DEFAULT_DECIMAL
        session = self.Session()
        try:
            first_obj = session.query(func.sum(T_FINANCE.amount).label('total')
                    ).filter_by(account_id=TRADING_ACCOUNT_ID).first()
            if first_obj.total is not None:
                result = Decimal(first_obj.total)
        except Exception as ex:
            print("Error in get_pool: ", ex)
        finally:
            session.rollback()
            session = None
        return result

    def get_specific_finance_record(self, date, account_id, category_id,
            subcategory_id, amount, comment, stock_name_id, shares, price,
            tax, commission):
        """
        Looks for a finance record with the given parameters.
        """
        try:
            session = self.Session()
            result = session.query(T_FINANCE).filter_by(
                            date=date,
                            account_id=account_id,
                            category_id=category_id,
                            subcategory_id=subcategory_id,
                            amount=amount,
                            comment=comment,
                            stock_name_id=stock_name_id,
                            shares=shares,
                            price=price,
                            tax=tax,
                            commission=commission,
                            active=1
                            ).first()
        except Exception as ex:
            print(Error.GET_SPECIFIC_FINANCE_RECORD, ex)
            session.rollback()
            result = None
        finally:
            session = None
            return result
        return result
