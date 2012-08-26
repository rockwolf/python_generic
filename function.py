"""
This file is part of Lisa.

Lisa is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lisa is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with Lisa. If not, see <http://www.gnu.org/licenses/>.
"""
from datetime import datetime

""" A file with functions that can be used everywhere """

def current_date(date_format='%Y-%m-%d %H:%M:%S'):
    """ Returns the current date, formatted. """
    now = datetime.now()
    return now.strftime(date_format)
