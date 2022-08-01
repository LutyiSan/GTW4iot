import psycopg2 as ts
from loguru import logger
from env import *
from datetime import datetime

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
                                                   time TIMESTAMPTZ NOT NULL,
                                                   device_id INTEGER,
                                                   object_name TEXT,
                                                   present_value TEXT
                                                   );""")
                self.conn.commit()
                logger.debug("TABLE Created")
        except Exception as e:
            logger.exception("FAIL Create table", e)

    def put_data(self, table, input_data):
        data = []
        lid= len(input_data["OBJECT_NAME"])
        idx = -1
        while idx < (lid - 1):
            idx += 1
            single_data = []
            tst = datetime.now()
            single_data.append(tst)
            single_data.append(input_data["DEVICE_ID"][idx])
            single_data.append(input_data["OBJECT_NAME"][idx])
            single_data.append(input_data["PRESENT_VALUE"][idx])
            data.append(tuple(single_data))
        print(data)
        try:
            with ts.connect(self.CONNECTION) as self.conn:
                self.cursor = self.conn.cursor()
                query = f"""INSERT INTO {table}(time, device_id, object_name, present_value) VALUES (%s, %s, %s, %s);"""
                self.cursor.executemany(query, data)
                self.conn.commit()
            logger.debug("DATA INSERTED into table")
        except Exception as e:
            logger.exception("FAIL INSERT DATA", e)

    def get_data(self, table):
        with ts.connect(self.CONNECTION) as self.conn:
            self.cursor = self.conn.cursor()
           # self.query_get_data = f"""SELECT * FROM {table}"""
            self.cursor.execute(f"""SELECT * FROM device_109; """)
            for i in self.cursor.fetchall():
                print(i)