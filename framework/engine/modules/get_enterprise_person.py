#!/usr/bin/env	python

from colorama import Fore,Back,Style
from bs4 import BeautifulSoup

import os
import sys
import string
import random
import requests

class module_element(object):
    def __init__(self):
        self.require = [
            {"name": "person", "value": "", "required": "yes"},
            {"name": "limit_search", "value": "10", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'person',
            'result': "rows",
            'export_primary': 'person',
            'description': 'Search possible enterprise for selected person'
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
        server = "encrypted.google.com"
        limit = self.get_options("limit_search")
        person = self.get_options("person")
        counter = ""
        result_tpl = []
        url = "https://" + server + "/search?num=" + limit + "&start=0&hl=en&q="+str(person)+" site:linkedin.com"
        request = requests.get(url)
        status_code = request.status_code
        if status_code == 200:
            html = BeautifulSoup(request.text, "html.parser")
            results = html.find_all('div', {'class': 'g'})
            try:
                for i, result in enumerate(results):
                    subtext = result.find('div', class_="slp")
                    if subtext != None:
                        empl = subtext.getText()
                        result_tpl.append(
                                {
                                    '_id': self.generate_unique_id(),
                                    'work': empl
                                }
                            )
                        counter = i
                self.export.append(result_tpl)
            except:
                error = 1
            if counter == "":
                return True
        else:
            return False
