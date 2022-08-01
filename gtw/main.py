from loguru import logger
from csv_to_dict import get_device_dict
from BACnet import BACnetClient
from mqtt import MyMQTT
from timescale_db import TSDB
from sql_db import MySQL
from env import *


class GTW:
    def __init__(self):
        if GTW_MODE == "bacnet-mqtt":
            self.mqttclient = MyMQTT()
            self.mqttclient.create(USER_NAME, USE_PASSWD)
        elif GTW_MODE == "bacnet-mqtt-timescaledb":
            self.mqttclient = MyMQTT()
            self.mqttclient.create(USER_NAME, USE_PASSWD)
            self.ts = TSDB()
        elif GTW_MODE == "bacnet-mqtt-sqlite3":
            self.mqttclient = MyMQTT()
            self.mqttclient.create(USER_NAME, USE_PASSWD)
            self.sql = MySQL()

    def run_bacnet(self):
        self.bacnet = BACnetClient()
        for i in DEVICE_CSV:
            state = self.bacnet.create(HOST_IP, HOST_PORT)
            if state:
                #  Получаем словарь из csv девайса
                self.device = get_device_dict(i)

                if self.device:
                    if GTW_MODE == "bacnet-mqtt-timescaledb":
                        #  Создаем таблицу девайса в Timescale DB
                        self.ts.create_table(f'{self.device["TOPIC"][1]}')
                    elif GTW_MODE == "bacnet-mqtt-sqlite3":
                        #  Создаем таблицу девайса в SQLITE3
                        self.sql.connect(DB_NAME)
                        self.sql.create_table(f'{self.device["TOPIC"][1]}')

                    # Опрашиваем девайс
                    self.reading_data = self.bacnet.read_load(self.device)
                    self.bacnet.disconnect()

                    # Отправляем полученые данные в MQTT
                    self.sent_data()

                    if GTW_MODE == "bacnet-mqtt-timescaledb":
                        # Сохраняем полученые данные в Timescale DB
                        self.ts.put_data(f'{self.device["TOPIC"][1]}', self.reading_data)
                    elif GTW_MODE == "bacnet-mqtt-sqlite3":
                        # Сохраняем полученые данные в Timescale DB
                        self.sql.put_data(f'{self.device["TOPIC"][1]}', self.reading_data)

                else:
                    logger.info(f"FAIL read csv {i}")

            else:
                logger.info("Please inspect parameters in env.py")
                # return False

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
