#!/usr/bin/env	python

import subprocess
import json
import string
import random

class module_element(object):

    def __init__(self):
        self.require = [
            {"name": "software", "value": "", "required": "yes"}
        ]
        self.export = []
        self.export_file = ""
        self.id_list = []
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'software',
            'result': "rows",
            'export_primary': 'Title',
            'description': 'Search exploit from selected software'
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
        software = self.get_options('software')
        process = subprocess.Popen(['searchsploit', '-w', '-o', '-j', str(software)], stdout=subprocess.PIPE)
        read_t = process.stdout.read()
        if read_t != "":
            json_t = json.loads(read_t)
            if json_t['RESULTS_EXPLOIT'] != None:
                if len(json_t['RESULTS_EXPLOIT']) > 0:
                    for exploit in json_t['RESULTS_EXPLOIT']:
                        exploit_tpl.append({
                            'Title': exploit['Title'],
                            'Link': exploit['URL'],
                            '_id': self.generate_unique_id()
                        })
                    self.export.append(exploit_tpl)
                else:
                    exploit_tpl.append({
                        'information': "No exploit found",
                        '_id': self.generate_unique_id()
                    })
                    self.export.append(exploit_tpl)




