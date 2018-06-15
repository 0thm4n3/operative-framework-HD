#!/usr/bin/env	python
#description:Search archive of website domain (archive.org)#

from colorama import Fore,Back,Style

import os, sys
import json
import datetime
import requests
import random
import string


class module_element(object):
    def __init__(self):
        self.title = "Archive.org Gathering : \n"
        self.require = [
            {"name": "website", "value": "", "required": "yes"},
            {"name": "from_date", "value": "2010", "required": "no"},
            {"name": "to_date", "value": "2017", "required": "no"},
            {"name": "limit", "value": "100", "required": "no"}
        ]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'date',
            'description': 'Retrieve archived url information from selected website'
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
        export_tpl = []
        error = 0
        domain_name = str(self.get_options('website'))
        from_date = str(self.get_options('from_date'))
        to_date = str(self.get_options('to_date'))
        limit_result = str(self.get_options('limit'))
        if domain_name[-1] == '/':
            domain_name = domain_name[:-1]
        if "://" in domain_name:
            domain_name = domain_name.split('://')[1]
        url = "http://web.archive.org/cdx/search/cdx?url="+domain_name+"&matchType=domain&limit="+limit_result+"&output=json&from="+from_date+"&to="+to_date
        try:
            req = requests.get(url)
            json_data = json.loads(req.text)
            if len(json_data) == 0:
                export_tpl.append({
                    'information': 'no result in archive'
                })
                self.export.append(export_tpl)
                error = 1
        except:
            return False
        if error == 0:
            try:
                result = [ x for x in json_data if x[2] != 'original']
                result.sort(key=lambda x: x[1])
                for line in result:
                    timestamp = line[1]
                    website = line[2]
                    total_link = "https://web.archive.org/web/" + str(timestamp) + "/" + str(website)
                    string_date = str(timestamp[:4]) + "/" + str(timestamp[4:6]) + "/" + str(timestamp[6:8])
                    export_tpl.append({
                        'date': string_date,
                        'website': website,
                        'archive_link': total_link,
                        '_id': self.generate_unique_id()
                    })
                self.export.append(export_tpl)
            except:
                return False