"""
    See LICENSE file for copyright and license details.    
"""
class MessageHandler:
    """
        A general class to handle messages
    """

    def __init__(self):
        """
            Init of MessageHandler class
        """
    
    def confirmation(self, stract):
        """
            Show confirmation dialog
        """
        answer = input('{} [y|n] '.format(stract) \
            ).strip().lower()
        if answer == 'y':
            return True
        else:
            print('Aborted.')
            return False
    
    def get_input(self, label):
        """
            Ask for user input and return it as a string.
        """
        return input(label).strip().lower()

    def print_action(self, stract, dictstr):
        """
            Print message about straction
            for each item in the dictstr dictionary
        """
        for s in dictstr.keys():
            print('{0} {1}.'.format(stract, s))

class ErrorHandler(MessageHandler):
    """
        A class to handle error messages,
        it inherits from MessageHandler
    """

    def __init__(self):
        """
            Init of ErrorHandler class
        """
        print('ErrorHandling loaded...')
