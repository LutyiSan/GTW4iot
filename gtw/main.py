from loguru import logger
from csv_to_dict import get_device_dict
from BACnet import BACnetClient
from mqtt import MyMQTT
from timescale_db import TSDB
from sql_db import MySQL
import multiprocessing
from env import *


def time_control(period, func):
    run_time = multiprocessing.Process(target=func)
    run_time.start()
    # Wait for 10 seconds or until process finishes
    run_time.join(period)
    # If thread is still active
    if run_time.is_alive():
        #print("running... before changed values...")
        # Terminate - may not work if process is stuck for good
        run_time.terminate()
        # OR Kill - will work for sure, no chance for process to finish nicely however
        # p.kill()
        run_time.join()


class GTW:
    def __init__(self):
        if GTW_MODE == "bacnet-mqtt-timescaledb":
            self.tsdb_create_state = self.ts = TSDB()
        elif GTW_MODE == "bacnet-mqtt-sqlite3":
            self.sql = MySQL()
        self.mqttclient = MyMQTT()
        self.mqtt_create_state = self.mqttclient.create(USER_NAME, USE_PASSWD)




    def run_bacnet(self):
        self.bacnet = BACnetClient()
        for i in DEVICE_CSV:
            time_control(5,self.bacnet.create(HOST_IP, HOST_PORT))
            self.device = get_device_dict(i)  # Получаем словарь из csv девайса
            if self.device:
                if GTW_MODE == "bacnet-mqtt-timescaledb" and self.tsdb_create_state:
                    self.tsdb_create_table_state = self.ts.create_table(
                            f'{self.device["TOPIC"][1]}')  # Создаем таблицу девайса в Timescale DB
                elif GTW_MODE == "bacnet-mqtt-sqlite3":
                    if self.sql.connect(DB_NAME):
                        self.sql.create_table(f'{self.device["TOPIC"][1]}')  # Создаем таблицу девайса в SQLITE3
                    # Опрашиваем девайс
                if MILTIREAD_LENGTH > 1:
                    self.reading_data = self.bacnet.read_load(self.device)
                    self.bacnet.disconnect()
                else:
                    self.reading_data = self.bacnet.read_single(self.device)
                    self.bacnet.disconnect()
                if self.mqtt_create_state:
                    self.sent_data()
                else:
                    logger.error(f"MQTT Client not created")

                if GTW_MODE == "bacnet-mqtt-timescaledb" and self.tsdb_create_state:
                        # Сохраняем полученые данные в Timescale DB
                    self.ts.put_data(f'{self.device["TOPIC"][1]}', self.reading_data)
                elif GTW_MODE == "bacnet-mqtt-sqlite3":
                        # Сохраняем полученые данные в Timescale DB
                    self.sql.put_data(f'{self.device["TOPIC"][1]}', self.reading_data)
            else:
                logger.info(f"FAIL read csv {i}")
                self.bacnet.disconnect()



    def sent_data(self):
        sent_data = dict.fromkeys(self.reading_data['OBJECT_NAME'])
        idx = -1
        for i in sent_data:
            idx += 1
            sent_data[i] = self.reading_data['PRESENT_VALUE'][idx]
        if self.mqttclient.connect(BROKER, BROKER_PORT):
            self.mqttclient.send(f'{TOPIC}/{self.device["TOPIC"][1]}', sent_data)


def run():
    gtw = GTW()
    while True:
        gtw.run_bacnet()


if __name__ == '__main__':
    run()
