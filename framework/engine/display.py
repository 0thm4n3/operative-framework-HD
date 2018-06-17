#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import glob
import os
import string
import random
from threading import Thread
from pymongo import MongoClient
from engine import config


def work(random_id, module_class, database):
    module_class.main()
    collection = database.running_modules
    collection.update({"task_id": random_id}, {'$set': {"results": module_class.export}})