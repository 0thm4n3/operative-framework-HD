#!/usr/bin/env	python
#description:	Whois information for domain#

from colorama import Fore,Back,Style

import os, sys
import pythonwhois
import urllib
import string
import random

class module_element(object):
    def __init__(self):
        self.title = "Whois domain gathering : \n"
        self.require = [
            {"name": "website", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'index',
            'description': 'Retrieve whois information from selected target'
        }

    def generate_unique_id(self, size=6, chars=string.ascii_uppercase + string.digits):
        start = 0
        unique_id = ""
        while start == 0:
            unique_id = ''.join(random.choice(chars) for _ in range(size))
            if unique_id not in self.id_list:
                self.id_list.append(unique_id)
                start = 1
        return unique_id

    def get_options(self, name):
        for argument in self.require:
            if argument['name'] == name:
                return argument['value']

    def main(self):
        whois_tpl = []
        detail = None
        website = self.get_options('website')
        if "://" in website:
            website = website.split('://')[1]
        try:
            whois_information = pythonwhois.get_whois(website)
            detail = whois_information['contacts']
        except:
            whois_tpl.append({
                'error': "A error as occurred"
            })
            self.export.append(whois_tpl)
            return False
        if detail != None:
            for element in detail:
                if detail[element] != None:
                    if len(detail[element]) > 0:
                        for winfo in detail[element]:
                            whois_tpl.append({
                                'index': str(winfo),
                                'value': str(detail[element][winfo]),
                                '_id': self.generate_unique_id()
                            })
        else:
            whois_tpl.append({
                'error': "A error as occurred"
            })
        self.export.append(whois_tpl)
