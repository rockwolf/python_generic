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

""" 
    A file with SQLAlchemy specific functions that can be used everywhere
"""

def row_to_dict(row):
    """
        This function iterates over column/value pairs and returns a
        dictionary with the results.
    """
    result = {}
    for column in row.__table__.columns:
        result[column.name] = getattr(row, column.name)
    return result
