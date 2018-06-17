#!/usr/bin/env  python

import subprocess
import datetime
import sys
import os
sys.path.insert(0, '../')
from colorama import Fore, Style
from framework import config


def print_log(color_string, type_string, text):
    return datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] ') + color_string + str(type_string) +  Style.RESET_ALL + " " + str(text)


def main():
    print print_log(Fore.BLUE, 'INFO', 'Welcome to Operative Framework backend ' + str(config.OPERATIVE_FRAMEWORK_VERSION))
    if not os.path.isdir("../framework"):
        print print_log(Fore.RED, 'ERROR', "directory : '../framework' not found")
        sys.exit()
    print print_log(Fore.BLUE, 'INFO', 'Starting framework in background....')
    print print_log(Fore.GREEN, 'SUCCESS', 'framework start  at 127.0.0.1:' + config.BACKEND_PORT)
    cmd = "python ../framework/app.py"
    a = subprocess.Popen(cmd, shell=True)
    stdout, stderr = a.communicate()
    if a.returncode != 0:
        print print_log(Fore.RED, "ERROR", "A error has been occurred with a framework")
        print print_log(Fore.RED, "ERROR", "Please run it manually: sudo python framework/app.py")
        sys.exit()


if __name__ == "__main__":
    main()
