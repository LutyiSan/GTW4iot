import psycopg2 as ts
from loguru import logger
from env import *
from datetime import datetime
import json

class TSDB:
    def __init__(self):
        self.CONNECTION = f"postgres://{TSDB_USER}:{TSDB_PASS}@{TSDB_HOST}:{TSDB_PORT}/{TSDB_DB}"
        self.query_get_data = None
        self.query_put_data = None
        self.query_create_table = None
        self.cursor = None

    def create_table(self, table):
        try:
            with ts.connect(self.CONNECTION) as self.conn:
                self.cursor = self.conn.cursor()
                self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
                                                   time TIMESTAMP NOT NULL,
                                                   device_data JSON
                                                   );""")
                self.conn.commit()
            logger.debug(f"READY (or ALREADY EXISTS) {table} in Timescale DB")
        except Exception as e:
            logger.exception(f"FAIL Create table {table} in Timescale DB\n", e)

    def put_data(self, table, input_data):
        try:
            input_data.pop('DEVICE_IP', None)
            input_data.pop('OBJECT_TYPE', None)
            input_data.pop('OBJECT_ID', None)
            input_data.pop('TOPIC', None)
            qdata = []
            jdata = json.dumps(input_data)
            with ts.connect(self.CONNECTION) as self.conn:
                self.cursor = self.conn.cursor()
                query = f"""INSERT INTO {table}(time, device_data) VALUES (%s, %s);"""
                timestamp = datetime.now()
                qdata.append(timestamp)
                qdata.append(jdata)
                self.cursor.execute(query, qdata)
                self.conn.commit()
            logger.debug(f"READY insert data to {table} in Timescale DB")
        except Exception as e:
            logger.exception(f"FAIL insert data to {table} in Timescale DB\n", e)




