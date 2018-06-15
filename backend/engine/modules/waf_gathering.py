#!/usr/bin/env	python
#description:WAF information gathering : need wafw00f#

from colorama import Fore,Back,Style

import os,sys
import urllib
import subprocess
import re,string
import random

class module_element(object):

    def __init__(self):
        self.title = "Web Application Firewall gathering : \n"
        self.require = [
            {"name": "website", "value": "", "required": "yes"}
        ]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'firewall',
            'description': 'Retrieve possible firewall from selected website'
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
        firewall_tpl = []
        website = str(self.get_options("website"))
        if "://" in website:
            website = website.split('://')[1]
        try:
            response = subprocess.check_output(["wafw00f", str(website)])
            if "is behind a" in response:
                regex = re.compile("is behind a(.*)")
                result = regex.findall(response)
                firewall_tpl.append({
                    'firewall': result[0].strip(),
                    '_id': self.generate_unique_id()
                })
            else:
                firewall_tpl.append({
                    'firewall': 'no firewall found',
                    '_id': self.generate_unique_id()
                })
            self.export.append(firewall_tpl)
        except OSError as e:
            firewall_tpl.append({
                'error': 'error has occured',
                '_id': self.generate_unique_id()
            })
            self.export.append(firewall_tpl)
            if e.errno == os.errno.ENOENT:
                print e
            else:
                # Something else went wrong while trying to run `wget`
                raise


