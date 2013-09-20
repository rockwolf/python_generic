"""
See LICENSE file for copyright and license details.
"""
from datetime import datetime

""" A file with functions that can be used everywhere """

def current_date(date_format='%Y-%m-%d %H:%M:%S'):
    """ Returns the current date, formatted. """
    now = datetime.now()
    return string_to_datetime(now.strftime(date_format))

def string_to_datetime(datetime_string, datetime_format='%Y-%m-%d %H:%M:%S'):
    """ Returns a datetime from a string. """
    return datetime.strptime(datetime_string, datetime_format)

def string_to_date(date_string):
    """ Returns a datetime, formatted as a date (without timing info).  """
    date_string = date_string.split(' ')
    date_string = date_string[0]
    return string_to_datetime(date_string, '%Y-%m-%d')
    
def print_in_columns(values):
    """
        Print data values in a nice centered layout.
        Input should be a list of lists with
        column values to print.
        e.g.: [[col_1_value0, col_2_value0]
                ,[col_1_value1, col_2_value1]]
    """
    # TODO: make 30 a variable
    print('{:x^30}'.format(''.join(str(value) for value in values)))
    
def print_separator(self, linechar='-', length=80):
    """
        Print nice divider line.
    """
    print_inn_colums([[linechar*length]])

