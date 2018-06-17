#!/usr/bin/env	python

import requests
import string
import random

class module_element(object):

    def __init__(self):
        self.require = [
            {"name": "link", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.export_status = False
        self.id_list = []
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'link',
            'result': "textarea",
            'description': 'Parse content of selected link'
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
        link_tpl = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        link = self.get_options('link')
        try:
            r = requests.get(link, headers=headers)
        except:
            self.export.append(link_tpl)
            return True
        content = r.content
        link_tpl.append(content)
        self.export.append(link_tpl)
        return True





