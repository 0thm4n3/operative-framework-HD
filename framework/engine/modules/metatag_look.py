#!/usr/bin/env	python
#description:	get meta name,content#

from colorama import Fore,Back,Style
from bs4 import BeautifulSoup

import os, sys
import requests
import string
import random

class module_element(object):

    def __init__(self):
        self.title = "Meta tags Retriever : \n"
        self.require = [
            {"name": "link", "value": "", "required": "yes"}
        ]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'link',
            'result': "rows",
            'export_primary': 'name',
            'description': 'Retrieve metatag from selected url'
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
        metatag_tpl = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
            }
        website = self.get_options('link')
        loaded = 0
        if not "://" in website:
            website = "http://" + website
        try:
            req = requests.get(website, headers=headers)
            html = req.content
            loaded = 1
        except:
            return False
        if loaded == 1:
            soup = BeautifulSoup(html, "html.parser",from_encoding="utf-8")
            for tag in soup.findAll('meta'):
                try:
                    content = "empty" if tag['content'] == "" else tag['content']
                    metatag_tpl.append({
                        'name': str(tag['name']),
                        'value': str(content),
                        '_id': self.generate_unique_id()
                    })
                except:
                    nots = 1
            self.export.append(metatag_tpl)


