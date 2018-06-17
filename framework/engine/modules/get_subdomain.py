#!/usr/bin/env	python
import os
import sys
import string
import random
import re
import json
import subprocess


class module_element(object):
    def __init__(self):
        self.require = [
            {"name": "website", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False
        self.export_category = "opened_services"
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'domain',
            'description': 'Enumerate possible domain name'
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
        domain_tpl = []
        domain_cheked = []
        website = self.get_options('website')
        website = website.split("//")[-1].split("/")[0].split('?')[0]
        if "www." in website:
            website = website.split('www.')[1]
        res = subprocess.Popen(['/usr/bin/python', 'external_tool/subdomain/execute.py', '-d', website], stdout=subprocess.PIPE)
        output = res.stdout.read()
        test_out = json.loads(output)
        for element in test_out:
            if element['domain'] not in domain_cheked:
                domain_tpl.append({
                    '_id': self.generate_unique_id(),
                    'subdomain': element['domain']
                })
        self.export.append(domain_tpl)


