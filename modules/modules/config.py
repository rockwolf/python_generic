#! /usr/local/bin/python
"""
    See LICENSE file for copyright and license details.
"""

import configparser

class ConfigParser():
    """ Class that contains values from the config file. """

    def __init__(self):
        """ Initialise config class. """ 
        self.myconf = 'config/calculator_finance.rc'
        self.dbhost = ''
        self.dbname = ''
        self.dbuser = ''
        self.dbpass = ''
        self.config()
 
    def config(self):
        """ Retrieve config file values """
        config = configparser.RawConfigParser()
        config.read(self.myconf)
        
        self.dbhost = config.get('database', 'host')[1:-1]
        self.dbname = config.get('database', 'name')[1:-1]
        self.dbuser = config.get('database', 'user')[1:-1]
        self.dbpass = config.get('database', 'password')[1:-1]
        self.importdir = config.get('data', 'importdir')[1:-1]
        self.exportdir = config.get('data', 'exportdir')[1:-1]
