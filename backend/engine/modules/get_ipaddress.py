#!/usr/bin/env	python

import socket
import string
import random

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
            'export_primary': 'ip_address',
            'description': 'Find ip address for selected website'
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
        exploit_tpl = []
        website = self.get_options('website')
        domain = website.split("//")[-1].split("/")[0].split('?')[0]
        ip_address = socket.gethostbyname(domain)
        exploit_tpl.append({
            'ip_address': str(ip_address),
            '_id': self.generate_unique_id()
        })
        self.export.append(exploit_tpl)




