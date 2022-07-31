import sqlite3 as sql
from datetime import datetime

input = {"DEVICE_IP": ["10.10.10.10", "10.10.10.10", "10.10.10.10"],
         "DEVICE_ID": [10, 10, 10],
         "OBJECT_TYPE": ["analogValue", "binaryValue", "binaryOutput"],
         "OBJECT_ID": [1, 2, 3],
         "OBJECT_NAME": ["TE-1", "START:", "ALARM"],
         "PRESENT_VALUE": ["22.5", "inactive", "active"],
         "TOPIC": ["sch_1", "sch_1", "sch_1"]}


class MySQL:
    def __init__(self):
        self.sql = sql
        self.cursor = None
        self.conn = None

    def connect(self, db):
        self.conn = self.sql.connect(db)
        self.cursor = self.conn.cursor()

    def create_table(self, table):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}(DEVICE_IP TEXT,DEVICE_ID INT, OBJECT_TYPE TEXT, 
        OBJECT_ID INT, OBJECT_NAME TEXT, TOPIC TEXT, PRESENT_VALUE TEXT, TIMESTAMP TEXT);""")
        self.conn.commit()

    def put_data(self, table, input_data):

        count = len(input_data['OBJECT_ID'])
        idx = -1
        while idx < (count - 1):
            timestamp = str(datetime.now())
            idx += 1
            self.cursor.execute(
                f"""INSERT INTO {table} VALUES('{input_data["DEVICE_IP"][idx]}', {input_data["DEVICE_ID"][idx]}, '{input_data["OBJECT_TYPE"][idx]}', {input_data["OBJECT_ID"][idx]}, '{input_data["OBJECT_NAME"][idx]}','{input_data["TOPIC"][idx]}', '{input_data["PRESENT_VALUE"][idx]}','{timestamp}' );""")
        self.conn.commit()

    def get_data_all_device(self, table):
        self.cursor.execute(f"""SELECT * FROM {table};""")
        result = self.cursor.fetchall()
        # print(result)
        # for i in result:
        # print(i)
        return result

    def get_data_one_signal(self, table, name):
        self.cursor.execute(
            f"""SELECT OBJECT_NAME, PRESENT_VALUE, TIMESTAMP FROM {table} WHERE OBJECT_NAME = '{name}';""")
        result = self.cursor.fetchall()
        # print(result)
        for i in result:
            print(i)
        return result
