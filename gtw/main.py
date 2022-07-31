from loguru import logger
from csv_to_dict import get_device_dict
from BACnet import BACnetClient
from mqtt import MyMQTT
from DATABASE import MySQL
from env import *


class GTW:

    def __init__(self):
        self.sql = MySQL()
        self.sql.connect("devices.db")

    def create_mqtt(self):
        self.mqttclient = MyMQTT()
        self.mqttclient.create(USER_NAME, USE_PASSWD)

    def run_bacnet(self):
        self.bacnet = BACnetClient()
        for i in DEVICE_CSV:
            state = self.bacnet.create(HOST_IP, HOST_PORT)
            if state:
                #  Получаем словарь из csv девайса
                self.device = get_device_dict(i)
                if DB_ENABLE:
                    #  Создаем таблицу девайса в БД
                    self.crate_table(f'{self.device["TOPIC"][1]}')

                # Опрашиваем девайс
                self.reading_data = self.bacnet.read_load(self.device)
                self.bacnet.disconnect()
                if DB_ENABLE:
                    # Сохраняем полученые данные в БД

                    self.sql.put_data(f'{self.device["TOPIC"][1]}', self.reading_data)

                # Отправляем полученые данные в MQTT
                self.sent_data()
            else:
                logger.info("Please inspect parameters in env.py")

    def sent_data(self):
        sent_data = dict.fromkeys(self.reading_data['OBJECT_NAME'])
        idx = -1
        for i in sent_data:
            idx += 1
            sent_data[i] = self.reading_data['PRESENT_VALUE'][idx]
            self.mqttclient.connect(BROKER, BROKER_PORT)
            self.mqttclient.send(f'{TOPIC}/{self.device["TOPIC"][1]}', sent_data)

    def crate_table(self, table):
        self.sql.connect(DB_NAME)
        self.sql.create_table(table)

    def insert_data_to_table(self, table, input_data):
        self.sql.connect("devices.db")
        self.sql.put_data(table, input_data)


def run():
    gtw = GTW()
    gtw.create_mqtt()
    while True:
        gtw.run_bacnet()


if __name__ == '__main__':
    run()

