#!/usr/bin/env  python

import subprocess
import datetime
import sys
import os
import errno
from colorama import Fore, Style
error = 0
try:
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0])
    from framework import config
except:
    error = 1
try:
    sys.path.insert(0, os.path.expanduser('~') + "/.operative_framework/")
    from framework import config
except:
    error = 2


class OperativeBinary(object):

    def __init__(self):
        self.meta = {
            'author': 'Tristan Granier',
            'description': 'launch operative framework HD flask application server.'
        }
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        if error == 1:
            self.directory = os.path.expanduser('~') + "/.operative_framework"


    @staticmethod
    def print_log(color_string, type_string, text):
        return datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] ') + color_string + str(type_string) +  Style.RESET_ALL + " " + str(text)

    def run(self):
        if not os.geteuid() == 0:
            print >> sys.stderr, "You need root permissions to do this please run sudo " + sys.argv[0] + "."
            sys.exit(1)
        print self.print_log(Fore.BLUE, 'INFO', 'Welcome to Operative Framework backend ' + str(config.OPERATIVE_FRAMEWORK_VERSION))
        if not os.path.isdir(self.directory + "/framework"):
            print self.print_log(Fore.RED, 'ERROR', "directory : '" + self.directory + "/framework' not found")
            sys.exit()
        print self.print_log(Fore.BLUE, 'INFO', 'Starting framework in background....')
        print self.print_log(Fore.GREEN, 'SUCCESS', 'framework start  at 127.0.0.1:' + config.BACKEND_PORT)
        cmd = "python " + self.directory + "/framework/app.py"
        a = subprocess.Popen(cmd, shell=True)
        stdout, stderr = a.communicate()
        if a.returncode != 0:
            print self.print_log(Fore.RED, "ERROR", "A error has been occurred with a framework")
            print self.print_log(Fore.RED, "ERROR", "Please run it manually: sudo python framework/app.py")
            sys.exit()
        return True

    def run_no_banner(self):
        print self.print_log(Fore.BLUE, 'INFO',
                             'Welcome to Operative Framework backend ' + str(config.OPERATIVE_FRAMEWORK_VERSION))
        if not os.path.isdir(self.directory + "/framework"):
            print self.print_log(Fore.RED, 'ERROR',
                                 "directory : '" + self.directory + "/framework' not found")
            sys.exit()
        print self.print_log(Fore.BLUE, 'INFO', 'Starting framework in background....')
        print self.print_log(Fore.GREEN, 'SUCCESS', 'framework start  at 127.0.0.1:' + config.BACKEND_PORT)
        cmd = "python " + self.directory + "/framework/app.py"
        a = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        return True


if __name__ == "__main__":
    OperativeBinary().run()
