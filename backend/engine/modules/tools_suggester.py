#!/usr/bin/env	python

import os
import sys
import requests
import string
import random


class module_element(object):

    def __init__(self):
        self.require = [
            {"name": "website", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.export_status = False
        self.status_code = [200, 403]
        self.tools = [
            {"tools": "wpscan", "type": "wordpress", "url": "https://github.com/wpscanteam/wpscan"},
            {"tools": "joomscan", "type": "joomla", "url": "https://sourceforge.net/projects/joomscan/"},
            {"tools": "drupscan", "type": "drupal", "url": "https://github.com/tibillys/drupscan"},
            {"tools": "SPIPScan", "type": "spip", "url": "https://github.com/PaulSec/SPIPScan"},
            {"tools": "Magescan", "type": "magento", "url": "https://github.com/steverobbins/magescan"}
        ]
        self.directory = [
            {"file": "/wp-includes/", "type": "wordpress", "intext": ""},
            {"file": "/wp-admin/", "type": "wordpress", "intext": ""},
            {"file": "/readme.html", "type": "wordpress", "intext": "WordPress"},
            {"file": "/CHANGELOG.txt", "type": "drupal", "intext": "drupal"},
            {"file": "/administrator/", "type": "joomla", "intext": "Joomla"},
            {"file": "/robots.txt", "type": "spip", "intext": "SPIP"},
            {"file": "/frontend/default/", "type": "magento", "intext": ""},
            {"file": "/static/frontend/", "type": "magento", "intext": ""}
        ]
        self.id_list = []
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'tools',
            'description': 'Find possible tools for exploitation of target.'
        }

    def generate_unique_id(self, size=6, chars=string.ascii_uppercase + string.digits):
        start = 0
        unique_id = ""
        while start == 0:
            unique_id = ''.join(random.choice(chars) for _ in range(size))
            if unique_id not in self.id_list:
                self.id_list.append(unique_id)
                start = 1
        return unique_id

    def get_options(self, name):
        for argument in self.require:
            if argument['name'] == name:
                return argument['value']

    def main(self):
        current = ""
        export = []
        exported_tools = []
        website = self.get_options('website')
        if website[-1] == "/":
            website = website[:-1]
        if "http" not in website or "https" not in website:
            website = "http://"+website
        for element in self.directory:
            complet = website + element['file']
            req = requests.get(complet)
            if req.status_code in self.status_code:
                if element["intext"] != "":
                    if element["intext"].upper() in req.content.upper():
                        current = element["type"]
                    else:
                        current = ""
                else:
                    current = element["type"]
            if current != "":
                for tool in self.tools:
                    if tool["type"].upper() == current.upper():
                        if not tool["tools"] in exported_tools:
                            exported_tools.append(tool["tools"])
                            export.append({
                                "tools": tool["tools"],
                                "url": tool["url"],
                                "_id": self.generate_unique_id()
                            })
        self.export.append(export)
