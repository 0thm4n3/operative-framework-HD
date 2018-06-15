#!/usr/bin/env	python
#description:SSL/TLS information gathering (sslyze)#

from colorama import Fore,Back,Style

import os,sys
import urllib
import string
import random
import subprocess

class module_element(object):
    def __init__(self):
        self.title = "SSL/TLS gathering : \n"
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
            'description': 'Retrieve TLS/SSL information from selected website with SSLyze'
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
        ssl_tpl = []
        domain = self.get_options('website')
        if "://" in domain:
            domain = domain.split("://")[1]
        if domain[:-1] == "/":
            domain = domain[-1]
        try:
            response = subprocess.check_output(["sslyze", "--regular", domain])
            if response != "":
                explode = response.split('\n')
                for line in explode:
                    ssl_tpl.append({
                        'element': line,
                        '_id': self.generate_unique_id()
                    })
                self.export.append(ssl_tpl)
            else:
                return False
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print e
            else:
                # Something else went wrong while trying to run `sslyze`
                raise


