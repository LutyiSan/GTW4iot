import sqlite3 as sql
from loguru import logger
from datetime import datetime
from env import *

class MySQL:
    def __init__(self):
        self.sql = sql


    def connect(self, db):
        try:
            self.conn = self.sql.connect(db)
            self.cursor = self.conn.cursor()
            logger.debug("READY connect to sqlite3")
        except Exception as e:
            logger.exception("FAIL connect to sqlite3\n", e)

    def create_table(self, table):
        try:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}(DEVICE_IP TEXT,DEVICE_ID INT, OBJECT_TYPE TEXT, 
                                OBJECT_ID INT, OBJECT_NAME TEXT, TOPIC TEXT, PRESENT_VALUE TEXT, TIMESTAMP TEXT);""")
            self.conn.commit()
            logger.debug(F"READY (or ALREADY EXISTS) create table {table} in sqlite3")
        except Exception as e:
            logger.exception(f"FAIL create table {table} in sqlite3\n", e)

    def put_data(self, table, input_data):
        try:
            count = len(input_data['OBJECT_ID'])
            idx = -1
            while idx < (count - 1):
                timestamp = str(datetime.now())
                idx += 1
                self.cursor.execute(
                    f"""INSERT INTO {table} VALUES('{input_data["DEVICE_IP"][idx]}', {input_data["DEVICE_ID"][idx]}, '{input_data["OBJECT_TYPE"][idx]}', {input_data["OBJECT_ID"][idx]}, '{input_data["OBJECT_NAME"][idx]}','{input_data["TOPIC"][idx]}', '{input_data["PRESENT_VALUE"][idx]}','{timestamp}' );""")
            self.conn.commit()
            logger.debug(f"READY insert data to {table} in sqlite3")
        except Exception as e:
            logger.exception(f"FAIL insert data to {table} in sqlite3\n", e)
