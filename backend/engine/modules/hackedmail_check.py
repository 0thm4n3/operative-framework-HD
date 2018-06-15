#!/usr/bin/env	python
#description:Check if email as been hacked#

from colorama import Fore, Back, Style

import os
import sys
import urllib
import requests
import string
import random
import json


class module_element(object):
    def __init__(self):
        self.require = [
            {"name": "email", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.export_status = False
        self.id_list = []
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'email',
            'result': "rows",
            'export_primary': 'breach',
            'description': 'Check if email as been hacked'
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
        user_email = self.get_options('email')
        breach_tpl = []
        headers = {
            'pragma': 'no-cache',
            'cookie': '__cfduid=d6fd3dd2ab8eaa1a149a9d5e8a32399371526371246; _ga=GA1.2.96217395.1526830169; ai_user=B+I+z|2018-05-20T15:29:29.713Z; _gid=GA1.2.737580366.1528234839; _gat=1; ai_session=d56ON|1528234840669.4|1528234840669.4',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'accept': '*/*',
            'cache-control': 'no-cache',
            'authority': 'haveibeenpwned.com',
            'x-requested-with': 'XMLHttpRequest',
            'request-id': '|DOlN6.aX8lY',
            'referer': 'https://haveibeenpwned.com/',
        }

        response = requests.get('https://haveibeenpwned.com/api/v2/unifiedsearch/' + str(user_email),
                                headers=headers)
        content = response.text
        data_json = json.loads(content)
        if len(data_json['Breaches']) > 0:
            for breach in data_json['Breaches']:
                breach_tpl.append({
                    '_id': self.generate_unique_id(),
                    'breach': 'hacked on ' + breach['Title'],
                    'breachDate': breach['BreachDate']
                })
            self.export.append(breach_tpl)
