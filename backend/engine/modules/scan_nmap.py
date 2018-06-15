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
            {"name": "ip_address", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'ip_address',
            'result': "rows",
            'export_primary': 'port',
            'description': 'Scan open port from target ip address'
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
        port_tpl = []
        u_ipAddress = self.get_options('ip_address')
        

