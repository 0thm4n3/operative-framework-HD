#!/usr/bin/env	python
import os
import sys
import string
import random
import re
import requests

class module_element(object):
    def __init__(self):
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
            'export_primary': 'person',
            'description': 'Search possible email address on selected page'
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
        email_tpl = []
        email_checked = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        website = self.get_options('website')
        loaded = 0
        if not "://" in website:
            website = "http://" + website
        try:
            req = requests.get(website, headers=headers)
            html = req.content
            loaded = 1
        except:
            return False

        emails = re.findall(r'[\w\.-]+@[\w\.-]+', html)
        if len(emails) > 0:
            for email in emails:
                if email not in email_checked:
                    email_tpl.append({
                        '_id': self.generate_unique_id(),
                        'email': str(email)
                    })
                    email_checked.append(email)
            self.export.append(email_tpl)

