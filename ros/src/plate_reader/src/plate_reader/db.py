#!/usr/bin/env python

import os
import time

import numpy as np
from pymongo import MongoClient

os.environ['MONGO_URI'] = 'mongodb://172.20.10.11:27017'
os.environ['PARKING_TABLE'] = 'Parking'

class Db:
    MONGO_URI = os.environ['MONGO_URI']
    PARKING_TABLE = os.environ['PARKING_TABLE']

    def __init__(self, uri=MONGO_URI, db='lattice'):
        self._db = MongoClient(uri)[db]

    def add_plate(self, plate_sequence):
        """Add plate to database, overwritting timeOut if exists, otherwise record timeIn"""
        if self._db[self.PARKING_TABLE].find_one({'plate': plate_sequence}):
            self._db[self.PARKING_TABLE].update_one({'plate': plate_sequence}, {'$set': {'lastSeen': int(time.time())}})
        else:
            self._db[self.PARKING_TABLE].insert_one({'plate': plate_sequence,
                                                'timeIn': int(time.time())})
