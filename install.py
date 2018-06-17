#!/usr/bin/env  python

import os
import sys
import shutil
import subprocess
import platform
import errno
from colorama import Fore, Style


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print 'Directory not copied. Error: %s' % e
            return False


def install_package():
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])


if __name__ == "__main__":
    print Fore.YELLOW + "Welcome to Operative Framework HD" + Style.RESET_ALL
    print Fore.BLUE + "information: " + Style.RESET_ALL + "Loading dependency..."
    install_package()
    user_directory = os.path.expanduser('~') + '/'
    if not os.path.exists('backend/'):
        print Fore.RED + "error: " + Style.RESET_ALL + "directory 'backend/' not found please download fresh install."
        sys.exit()
    if os.path.exists(user_directory + '.operative_framework/'):
        print Fore.RED + "error: " + Style.RESET_ALL + "directory '" + user_directory + ".operative_framework' exist"
        user_put = raw_input(Fore.BLUE + 'interaction: ' + Style.RESET_ALL + 'removing [y or (n)] : ')
        if user_put == "" or user_put.lower() == "n" or user_put.lower() != "y":
            print "exiting..."
            sys.exit()
        shutil.rmtree(user_directory + '.operative_framework/')
    print Fore.BLUE + "information: " + Style.RESET_ALL + "Copy directory to '~/.operative_framwork'"
    copy('backend/', user_directory + '.operative_framework/backend')
    print Fore.GREEN + "success: " + Style.RESET_ALL + "Directory copy success."
    if platform.system() == "Darwin":
        if os.path.isfile('/usr/bin/operative_server'):
            os.remove('/usr/bin/operative_server')
        copy("bin/operative_server.py", "/usr/bin/operative_server")
    elif platform.system() == "Linux":
        if os.path.isfile('/usr/bin/operative_server'):
            os.remove('/usr/bin/operative_server')
        copy("bin/operative_server.py", "/usr/bin/operative_server")
    print Fore.GREEN + "success: " + Style.RESET_ALL + "Operative framework HD successfully installed"
    print Fore.BLUE + "information: " + Style.RESET_ALL + "now, you can run operative_server"
