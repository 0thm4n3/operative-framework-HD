#!/usr/bin/env  python

from pymongo import MongoClient
from colorama import Fore, Back, Style


def modules_list():
    t_modules = {
        "modules": [
            {
                "name": "Linkedin search2",
                "type": "personal",
                "module": "engine.modules.linkedin_search"
            }
        ]
    }
    return t_modules


def cmd_modules_insert():
    client = MongoClient('localhost', 27017)
    database = client.operative_framework
    collection = database.modules
    for module in modules_list()['modules']:
        if collection.find({"name": module['name']}).count() < 1:
            collection.insert(module)
            print "[+] : " + Fore.GREEN + module['name'] + Style.RESET_ALL
        else:
            print "[-] : " + Fore.RED + module['name'] + Style.RESET_ALL

