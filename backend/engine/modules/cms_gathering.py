#!/usr/bin/env	python
#description:Check if CMS is used (wordpress,joomla,magento)#

from colorama import Fore, Back, Style

import os
import sys
import string
import random
import requests

class module_element(object):
    def __init__(self):
        self.title = "CMS gathering : \n"
        self.require = [
            {"name": "website", "value": "", "required": "yes", "placeholder": "https://wordpress.com"}
        ]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.cms = {
            "wordpress": ['/wp-includes/', '/wp-admin/'],
            "magento": ['/frontend/default/', '/static/frontend/'],
            "joomla": ['/administrator/', '/templates/']
        }
        self.status_code = [200, 403, 301, 302]
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'cms_engine',
            'description': 'Check if cms as used from selected website.'
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
        start = 0
        website = self.get_options('website')
        if "http//" in website:
            website = website.replace('http//', 'http://')
        if website[-1:] == "/":
            website = website[:-1]
        try:
            requests.get(website)
            start = 1
        except:
            return "url schema not correct"
        if start == 1:
            tpl = []
            for line in self.cms:
                for path in self.cms[line]:
                    complet_url = website + path
                    req = requests.get(complet_url)
                    if req.status_code in self.status_code:
                        template = {
                            "cms_engine": str(line),
                            "full_link": str(complet_url),
                            "_id": self.generate_unique_id()
                        }
                        tpl.append(template)
            self.export.append(tpl)
