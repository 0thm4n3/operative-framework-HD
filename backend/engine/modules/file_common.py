#!/usr/bin/env	python
#description:	Read/Search common file#

from colorama import Fore,Back,Style

import os, sys
import requests
import string
import random

class module_element(object):
    def __init__(self):
        self.title = "Common file : \n"
        self.require = [{"name":"website","placeholder":"https://google.com","value":"","required":"yes"}]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.common_file = ['/robots.txt']
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'URL',
            'description': 'Read/Search common file on selected website.'
        }

    def get_options(self, name):
        for argument in self.require:
            if argument['name'] == name:
                return argument['value']

    def generate_unique_id(self, size=6, chars=string.ascii_uppercase + string.digits):
        start = 0
        unique_id = ""
        while start == 0:
            unique_id = ''.join(random.choice(chars) for _ in range(size))
            if unique_id not in self.id_list:
                self.id_list.append(unique_id)
                start = 1
        return unique_id

    def main(self):
        already_check = []
        print Fore.YELLOW + "* check if url is stable" + Style.RESET_ALL
        website = self.get_options('website')
        action = 0
        if "http//" in website:
            website = website.replace('http//', 'http://')
            if website[-1:] == "/":
                website = website[:-1]
            elif "http" not in website or "https" not in website:
                website = "http://"+website
        elif "http://" not in website and "https://" not in website:
            website = "http://" + website
        try:
            requests.get(website)
            action = 1
            print Fore.GREEN + "* website / url is stable" + Style.RESET_ALL
        except:
            print Fore.RED + "* website / url not found" + Style.RESET_ALL
        for line in self.common_file:
            tpl = []
            complet_url = website + line
            req = requests.get(complet_url)
            if req.status_code == 200:
                source = req.content
                source = source.split('\n')
                for line in source:
                    if line.strip() != "":
                        already_check.append(complet_url)
                        if complet_url not in tpl:
                            tpl.append({"URL": complet_url, "_id": self.generate_unique_id()})
            self.export.append(tpl)




