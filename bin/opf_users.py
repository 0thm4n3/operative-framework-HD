#!/usr/bin/env  python

import sys
import os
import datetime
from colorama import Fore, Style
from pymongo import MongoClient, errors
import hashlib
import random
import string
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0])
from framework import config


class OperativeBinary(object):

    def __init__(self):
        self.meta = {
            'author': 'Tristan Granier',
            'description': 'Manage operative framework users'
        }
        self.client = MongoClient('mongodb://' + str(config.MONGODB_USER) + ':' + str(config.MONGODB_PASS) + '@' + str(
            config.MONGODB_HOST) + ':' + str(config.MONGODB_PORT) + '/tracking?authSource=operative_framework')
        if not self.random_query():
            sys.exit('Please configure/start correctly MongoDB database with --auth.')
        self.database = self.client.operative_framework
        self.run()

    @staticmethod
    def print_log(color_string, type_string, text):
        return datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] ') + color_string + str(type_string) + Style.RESET_ALL + " " + str(text)

    def random_query(self):
        try:
            self.client.server_info()
        except errors.ServerSelectionTimeoutError as err:
            return False
        return True

    def random_tasks(self, size=6, chars=string.ascii_uppercase + string.digits, auth_token="", module_name="", project_id="alone", subject="", module_output="alone", module_export_primary=""):
        if auth_token != "":
            collection = self.database.users
            current_user = collection.find({'auth_token': auth_token})
            if current_user.count() < 1:
                return False
            current_user = list(current_user)
            app_id = current_user[0]['app_id']
            current_user = current_user[0]['username']
            collection = self.database.running_modules
            start = 0
            task = ""
            while start == 0:
                task = ''.join(random.choice(chars) for _ in range(size))
                if collection.find({'task_id': task, 'username': current_user}).count() < 1:
                    collection.insert({'task_id': task, 'username': current_user, 'results': "", 'status': 'pending', 'module_name': module_name, 'project_id': project_id, 'app_id': app_id, 'project_subject': subject, 'created_at': self.get_date(), 'error_msg': "", 'module_output': module_output, 'module_export_primary': module_export_primary})
                    start = 1
            return task
        return False

    def register_user(self, username, password):
        collection = self.database.users
        u_name = username
        u_password = hashlib.sha512(password.encode()).hexdigest()
        if collection.find({'username': u_name}).count() > 0:
            return False
        auth_token = self.random_tasks(12)
        app_id = self.random_letter(size=8, prefix="APP_")
        collection.insert({'username': u_name, 'password': u_password, 'auth_token': auth_token, 'app_id': app_id,
                           'user_right': "Administrator"})
        return True

    def register_add_user(self, username, password, app_id):
        collection = self.database.users
        u_name = username
        u_password = hashlib.sha512(password.encode()).hexdigest()
        if collection.find({'username': u_name, 'app_id': app_id}).count() > 0:
            return False
        auth_token = self.random_tasks(12)
        collection.insert({'username': u_name, 'password': u_password, 'auth_token': auth_token, 'app_id': app_id,
                           'user_right': "Administrator"})
        return True

    def create_user(self, user_put):
        arguments = user_put.split(' ')
        if len(arguments) < 3:
            print self.print_log(Fore.RED, 'ERROR', 'please use \':create USERNAME PASSWORD\'')
        else:
            username = arguments[1]
            password = arguments[2]
            if not self.register_user(username, password):
                print self.print_log(Fore.RED, 'ERROR', 'User already found please use another username')
            else:
                print self.print_log(Fore.GREEN, 'SUCCESS', 'User as successfully added !')
        return False

    def random_letter(self, size=6, chars=string.ascii_uppercase + string.digits, prefix=""):
        collection = self.database.users
        start = 0
        auth_token = ""
        while start == 0:
            auth_token = prefix + ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'app_id': auth_token}).count() < 1:
                start = 1
        return auth_token

    @staticmethod
    def print_menu():
        print Fore.GREEN + ":help" + Style.RESET_ALL + "    show this bullet"
        print Fore.GREEN + ":list" + Style.RESET_ALL + "    list user registered"
        print Fore.GREEN + ":create <username> <password>" + Style.RESET_ALL + "    create new user with new app_id"
        print Fore.GREEN + ":add <username> <password> <app_id>" + Style.RESET_ALL + "    add user to app_id"
        print Fore.GREEN + ":delete <username> <app_id>" + Style.RESET_ALL + "    delete user from app_id"

    def list_users(self):
        collection = self.database.users
        list_users = collection.find({}, {'_id': False, 'password': False, 'auth_token': False})
        if list_users.count() < 1:
            print self.print_log(Fore.RED, 'ERROR', 'No users found please use :create USERNAME PASSWORD in this shell.')
        else:
            for users in list_users:
                print Fore.GREEN + "username: " + Style.RESET_ALL + users['username'] + Fore.GREEN + " right: " + Style.RESET_ALL + users['user_right'] + Fore.GREEN + " app_id: " + Style.RESET_ALL + users['app_id']

    def add_user(self, user_put):
        arguments = user_put.split(' ')
        if len(arguments) < 4:
            print self.print_log(Fore.RED, 'ERROR', 'please use \':add USERNAME PASSWORD APP_ID\'')
        else:
            username = arguments[1]
            password = arguments[2]
            app_id = arguments[3]
            if not self.register_add_user(username, password, app_id):
                print self.print_log(Fore.RED, 'ERROR', 'User already found please use another username')
            else:
                print self.print_log(Fore.GREEN, 'SUCCESS', 'User as successfully added to app_id: \'' + app_id + '\'!')
        return False

    def remove_selected_user(self, username, app_id):
        collection = self.database.users
        if collection.find({'username': username, 'app_id': app_id}).count() < 1:
            return False
        collection.remove({'username': username, 'app_id': app_id})
        return True

    def remove_user(self, user_put):
        arguments = user_put.split(' ')
        if len(arguments) < 3:
            print self.print_log(Fore.RED, 'ERROR', 'please use \':delete USERNAME APP_ID\'')
        else:
            username = arguments[1]
            app_id = arguments[2]
            if not self.remove_selected_user(username, app_id):
                print self.print_log(Fore.RED, 'ERROR', 'User not found for this app_id')
            else:
                print self.print_log(Fore.GREEN, 'SUCCESS', 'User as successfully deleted from app_id: \'' + app_id + '\'!')
        return False

    def run(self):
        self.print_menu()
        action = 0
        while action == 0:
            try:
                user_put = raw_input(Fore.YELLOW + str(sys.argv[0]) + Style.RESET_ALL + " > ")
            except:
                print "\nbye..."
                sys.exit()
            if ":" in user_put:
                user_put = user_put.split(':')[1]
            if "create" in user_put:
                self.create_user(user_put)
            elif "list" in user_put:
                self.list_users()
            elif "add" in user_put:
                self.add_user(user_put)
            elif "delete" in user_put:
                self.remove_user(user_put)


if __name__ == "__main__":
    OperativeBinary()
