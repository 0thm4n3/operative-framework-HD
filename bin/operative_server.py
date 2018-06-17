#!/usr/bin/env  python

import subprocess
import datetime
import sys
import os
sys.path.insert(0, os.path.expanduser('~') + '/.operative_framework/')
from colorama import Fore, Style
from backend import config


def print_log(color_string, type_string, text):
    return datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] ') + color_string + str(type_string) +  Style.RESET_ALL + " " + str(text)


def main():
    print print_log(Fore.BLUE, 'INFO', 'Welcome to Operative Framework backend ' + str(config.OPERATIVE_FRAMEWORK_VERSION))
    user_directory = str(os.path.expanduser('~'))
    if not os.path.isdir(user_directory + "/.operative_framework/backend/"):
        print print_log(Fore.RED, 'ERROR', "directory : '" + user_directory + "/.operative_framework/backend/' not found")
        sys.exit()
    print print_log(Fore.BLUE, 'INFO', 'Starting backend in background....')
    print print_log(Fore.GREEN, 'SUCCESS', 'backend start  at 127.0.0.1:' + config.BACKEND_PORT)
    cmd = "python " + user_directory + "/.operative_framework/backend/app.py"
    a = subprocess.Popen(cmd, shell=True)
    stdout, stderr = a.communicate()
    if a.returncode != 0:
        print print_log(Fore.RED, "ERROR", "A error has been occurred with a backend or frontend")
        print print_log(Fore.RED, "ERROR", "Please run it manually: sudo python backend/app.py")
        print print_log(Fore.RED, "ERROR", "Please run it manually: npm run build --prefix 'frontend/'")
        sys.exit()


if __name__ == "__main__":
    main()
