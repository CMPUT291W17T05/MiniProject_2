#!/usr/bin/python3
from bsddb3 import db
from sys import argv
from sys import stdin

'''
Helper script to insert output from break into database
'''

def create_index(db_name, db_type):
    database = db.DB()
    database.open(db_name , None, db_type, db.DB_CREATE)

    for key in stdin:
        val = stdin.readline()
        database.put(bytes(key, encoding="ascii"), val)

    database.close()

db_name, db_type = argv[1:]
db_type = int(eval(db_type)) # Get the db_type

create_index(db_name, db_type)
