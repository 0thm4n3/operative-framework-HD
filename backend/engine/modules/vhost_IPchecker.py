#!/usr/bin/env	python
#description:Reverse IP domain check (BING)#

from bs4 import BeautifulSoup

import os
import sys
import urllib
import requests
import string
import random


class module_element(object):

    def __init__(self):
        self.title = "Reverse ip gathering (BING) : \n"
        self.require = [
            {"name": "ip_address", "value": "", "required": "yes"}
        ]
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'ip_address',
            'result': "rows",
            'export_primary': 'virtual host',
            'description': 'Find possible virtual host on selected ip address.'
        }
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False

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
        bing_tpl = []
        error = 0
        server = "www.bing.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        server_ip = self.get_options('ip_address')
        url = "http://"+server+"/search?q=ip%3a"+str(server_ip)
        try:
            req = requests.get(url, headers=headers)
            html = req.content
        except:
            error = 1
        if error == 0:
            soup = BeautifulSoup(html, "html.parser",from_encoding="utf-8")
            parsing = soup.findAll('cite')
            for link in parsing:
                website = link.text.encode('ascii', 'ignore')
                if " " in website:
                    website = website.split(' ')[0]
                if "/" in website:
                    website = website.split('/')[0]
                if "	" in website:
                    website = website.split('	')[0]
                if not website in self.export and "." in website:
                    bing_tpl.append({
                        'virtual host': website,
                        '_id': self.generate_unique_id()
                    })
            self.export.append(bing_tpl)


