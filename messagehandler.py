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
class MessageHandler:
    """ A general class to handle messages """

    def __init__(self):
        """ Init of MessageHandler class """
    
    def confirmation(self, stract):
        """ Show confirmation dialog """
        answer = \
            raw_input(
                'Are you sure you want to %s? [y|n] ' % stract \
            ).strip().lower()
        if answer != 'y':
            print('Aborted.')
            return -1
        elif answer == 'y':
            return 0

    def print_action(self, stract, dictstr):
        """ Print message about straction for each item in the lstObj list """
        for s in dictstr.keys():
            print('{0} {1}.'.format(stract, s))

class ErrorHandler(MessageHandler):
    """ A class to handle error messages, it inherits from MessageHandler """

    def __init__(self):
        """ Init of ErrorHandler class """
        print('ErrorHandling loaded...')
