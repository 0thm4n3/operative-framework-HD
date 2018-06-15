#!/usr/bin/env	python

import os
import sys
import urllib
import string
import random

class module_element(object):

    def __init__(self):
        self.title = "Domain gathering : \n"
        self.require = [
            {"name": "enterprise", "value": "", "required": "yes"}
        ]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'enterprise',
            'result': "rows",
            'export_primary': 'domain',
            'description': 'Find possible domain for selected enterprise'
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
        domain_export = []
        domain_list = []
        load_name = self.get_options("enterprise")
        start_with = ["www.", "http://", "https://"]
        end_with = [
            ".com",
            ".fr",
            ".org",
            ".de",
            ".eu",
            ".io",
            ".info"
        ]
        list_enterprise = []
        list_enterprise.append(load_name)
        if " " in load_name:
            list_enterprise.append(load_name.replace(' ', '-'))
            list_enterprise.append(load_name.replace(' ', ''))
        for enterprise in list_enterprise:
            for line in start_with:
                for end_line in end_with:
                    domain = line + str(enterprise) + end_line
                    try:
                        return_code = urllib.urlopen(domain).getcode()
                        return_code = str(return_code)
                        if return_code != "404":
                            domain_list.append(domain)
                    except:
                        error = 1
        if len(domain_list) > 0:
            for domain in domain_list:
                domain_export.append({
                    "domain": domain,
                    "_id": self.generate_unique_id()
                })
            self.export.append(domain_export)
        else:
            error = 1


