#!/usr/bin/env	python
#description:Linkedin employee search module#

from colorama import Fore,Back,Style
from bs4 import BeautifulSoup

import os,sys
import string
import random
import requests

class module_element(object):
    def __init__(self):
        self.require = [
            {"name": "enterprise", "value": "", "required": "yes"},
            {"name": "limit_search", "value": "10", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'enterprise',
            'result': "rows",
            'export_primary': 'employee',
            'description': 'Search possible employees list on Linkedin.com'
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
        enterprise = self.get_options("enterprise")
        counter = ""
        result_tpl = []
        url = "https://" + server + "/search?num=" + limit + "&start=0&hl=en&q=site:linkedin.com/in+" + enterprise
        request = requests.get(url)
        status_code = request.status_code
        if status_code == 200:
            html = BeautifulSoup(request.text, "html.parser")
            results = html.find_all('div', {'class': 'g'})
            try:
                for i, result in enumerate(results):
                    employee = result.find('h3', {'class': 'r'}).getText()
                    if "| LinkedIn" or "on LinkedIn" or "LinkedIn" in employee:
                        employee = employee.replace('| LinkedIn', '')
                        employee = employee.replace('LinkedIn', '')
                        employee = employee.replace('on LinkedIn', '')
                    if result.find('cite') != None:
                        profile = result.find('cite').getText()
                        result_tpl.append(
                            {'employee': employee.encode('utf-8'), 'full_link': profile.encode('utf-8'), '_id': self.generate_unique_id()}
                        )
                        counter = i
                self.export.append(result_tpl)
            except:
                error = 1
            if counter == "":
                print Fore.RED + "Nothing on linkedin." + Style.RESET_ALL
        else:
            print Fore.RED + "Can't get response" + Style.RESET_ALL
