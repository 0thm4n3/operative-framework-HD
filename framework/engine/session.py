#!/usr/bin/env  python


import os
import pickle

class Sess(object):

    def __init__(self, session_name):
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        print self.directory
        self.session_name = session_name

    def exist(self):
        if not os.path.exists(self.directory + "/engine/history/" + self.session_name + ".ofk"):
            return False
        return True

    def generate(self, session_object):
        if os.path.exists(self.directory + "/engine/history/" + self.session_name + ".ofk"):
            return False
        serialize_object = pickle.dumps(session_object)
        file_sess = open(self.directory + "/engine/history/" + self.session_name + ".ofk", 'w+')
        file_sess.write(serialize_object)
        file_sess.close()
        return True

    def load_session(self):
        if not os.path.exists(self.directory + "/engine/history/" + self.session_name + ".ofk"):
            return False

        file_sess = open(self.directory + "/engine/history/" + self.session_name + ".ofk").read()
        serialized_object = pickle.loads(file_sess)
        return serialized_object

    def delete_session(self):
        if not os.path.exists(self.directory + "/engine/history/" + self.session_name + ".ofk"):
            return False
        os.remove(self.directory + "/engine/history/" + self.session_name + ".ofk")
        return True
