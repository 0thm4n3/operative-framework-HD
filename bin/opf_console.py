#!/usr/bin/env  python

import datetime
import sys
import os
import time
from colorama import Fore, Style
error = 0
try:
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0])
    from framework import config
    from framework.external_tool import integrated
    from bin import opf_client, opf_server
except:
    error = 1
try:
    sys.path.insert(0, os.path.expanduser('~') + "/.operative_framework/")
    from framework import config
    from framework.external_tool import integrated
    from bin import opf_client, opf_server
except:
    error = 2


class OperativeBinary(object):

    def __init__(self):
        self.meta = {
            'author': 'Tristan Granier',
            'description': 'Manage operative framework HD'
        }
        self.status = {
            'client': 'stopped',
            'server': 'stopped'
        }
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        if error == 1:
            self.directory = os.path.expanduser('~') + "/.operative_framework"
        self.print_banner()
        self.run()

    @staticmethod
    def print_log(color_string, type_string, text):
        return datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] ') + color_string + str(type_string) + Style.RESET_ALL + " " + str(text)

    @staticmethod
    def print_help():
        print "help" + Fore.YELLOW + ":" + Style.RESET_ALL + Fore.GREEN + "   show this bullet" + Style.RESET_ALL
        print "status" + Fore.YELLOW + ":" + Style.RESET_ALL + Fore.GREEN + " print current status" + Style.RESET_ALL
        print "config" + Fore.YELLOW + ":" + Style.RESET_ALL + Fore.GREEN + " show current config" + Style.RESET_ALL
        print "tools" + Fore.YELLOW + ":" + Style.RESET_ALL + Fore.GREEN + " View external tools " + Style.RESET_ALL
        print "run_client" + Fore.YELLOW + ":" + Style.RESET_ALL + Fore.GREEN + " Run operative framework client " + Style.RESET_ALL
        print "run_server" + Fore.YELLOW + ":" + Style.RESET_ALL + Fore.GREEN + " Run operative framework server " + Style.RESET_ALL

    @staticmethod
    def print_config():
        config_vars = dir(config)
        for config_var in config_vars:
            if "__" not in config_var:
                print config_var + Fore.YELLOW + ": " + Style.RESET_ALL + Fore.GREEN + str(getattr(config, config_var)) + Style.RESET_ALL

    @staticmethod
    def print_tools():
        integrated.ExternalTools().listing()

    def print_status(self):
        print "client" + Fore.YELLOW + "    :   " + Style.RESET_ALL + str(self.status['client']).upper()
        print "server" + Fore.YELLOW + "    :   " + Style.RESET_ALL + str(self.status['server']).upper()

    def start_client(self):
        print self.print_log(Fore.YELLOW, 'WARNING', 'BEWARE YOU DON\'T HAVE LOG WHEN YOUR START WITH THIS BIN')
        print self.print_log(Fore.YELLOW, 'WARNING', 'START WITH opf_client.py FOR VIEW LOGS.')
        try:
            opf_client.OperativeBinary().run_no_banner()
            self.status['client'] = 'STARTED'
        except:
            print self.print_log(Fore.RED, 'ERROR', 'A error as been found please check log or run client with binary (opf_client.py).')
            return False
        print self.print_log(Fore.BLUE, 'INFORM', 'WAITING BROWSER OPENING...')
        time.sleep(5)
        return True

    def start_server(self):
        print self.print_log(Fore.YELLOW, 'WARNING', 'BEWARE YOU DON\'T HAVE LOG WHEN YOUR START WITH THIS BIN')
        print self.print_log(Fore.YELLOW, 'WARNING', 'START WITH opf_server.py FOR VIEW LOGS.')
        try:
            opf_server.OperativeBinary().run_no_banner()
            self.status['server'] = 'STARTED'
        except:
            print self.print_log(Fore.RED, 'ERROR', 'A error as been found please check log or run server with binary (opf_server.py).')
            return False
        return True

    @staticmethod
    def print_banner():
        print Fore.YELLOW + """
                               __  _                                    
  ____  ____  ___  _________ _/ /_(__   _____                           
 / __ \/ __ \/ _ \/ ___/ __ `/ __/ | | / / _ \                          
/ /_/ / /_/ /  __/ /  / /_/ / /_/ /| |/ /  __/                          
\____/ .___/\___/_/   \__,_/\__/_/ |___/\___/""" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + """
    ____                                             __      __  ______ 
   / ___________ _____ ___  ___ _      ______  _____/ /__   / / / / __ \\
  / /_/ ___/ __ `/ __ `__ \/ _ | | /| / / __ \/ ___/ //_/  / /_/ / / / /
 / __/ /  / /_/ / / / / / /  __| |/ |/ / /_/ / /  / ,<    / __  / /_/ / 
/_/ /_/   \__,_/_/ /_/ /_/\___/|__/|__/\____/_/  /_/|_|  /_/ /_/_____/  
                                                                        
""" + Style.RESET_ALL

    def run(self):
        if not os.geteuid() == 0:
            print >> sys.stderr, "You need root permissions to do this please run sudo " + sys.argv[0] + "."
            sys.exit(1)
        action = 0
        while action == 0:
            try:
                user_put = raw_input(Fore.YELLOW + str(sys.argv[0]) + Style.RESET_ALL + " ("+Fore.LIGHTBLUE_EX+"client:" + Style.RESET_ALL + self.status['client'] + "/"+Fore.LIGHTBLUE_EX+"server:" + Style.RESET_ALL + self.status['server'] + ") $ ")
            except:
                print "\nbye..."
                sys.exit()
            if ":" in user_put:
                user_put = user_put.split(':')[1]
            if user_put == "help":
                self.print_help()
            if user_put == "config":
                self.print_config()
            if user_put == "tools":
                self.print_tools()
            if user_put == "run_client":
                self.start_client()
            if user_put == "run_server":
                self.start_server()
            if user_put == "status":
                self.print_status()


if __name__ == "__main__":
    OperativeBinary()
