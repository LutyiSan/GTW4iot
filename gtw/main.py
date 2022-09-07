from loguru import logger
import time
from csv_to_dict import csv_to_dict
from BACnet import BACnetClient
from mqtt import MyMQTT
from TimeOut import timeout
from env import *


def sign_sf(sf):
    if sf is not None and len(sf) == 4:
        if sf[0] and sf[0] != 'Null':
            sf[0] = 'in-alarm'
        if sf[1] and sf[1] != 'Null':
            sf[1] = 'fault'
        if sf[2] and sf[2] != 'Null':
            sf[2] = 'overridden'
        if sf[3] and sf[3] != 'Null':
            sf[3] = 'is-not-service'
        return sf
    else:
        return [None, None, None, None]


def get_devices():
    devices = []
    if len(DEVICE_CSV) > 0:
        for dev in DEVICE_CSV:
            device = csv_to_dict(dev, ';')
            if device:
                devices.append(device)
    if len(devices) > 0:
        return devices
    else:
        return False


class GTW:
    def run_bacnet(self,device_list):
        self.poll_devices = device_list
        if self.poll_devices:
            self.bacnet = BACnetClient()
            for device in self.poll_devices:
                bc_state = self.bacnet.create(HOST_IP, device['PORT'][0])
                if bc_state:
                    if MILTIREAD_LENGTH > 1:
                        logger.debug(f"READING from device {device['DEVICE_IP'][0]} : {device['PORT'][0]}")
                        self.reading_data = self.bacnet.read_load(device)
                    else:
                        self.reading_data = self.bacnet.read_single(device)
                    self.mqttclient = MyMQTT()
                    self.mqtt_create_state = self.mqttclient.create(USER_NAME, USE_PASSWD)
                    if self.mqtt_create_state:
                        self.sent_data(device)
                    else:
                        logger.error(f"FAIL MQTT Client created")
                else:
                    logger.error(f"FAIL BACnet Client not created")
                time.sleep(1)
        else:
            logger.info(f"FAIL read from env.DEVICE_LIST")

    def sent_data(self, device):
        sent_data = dict.fromkeys(self.reading_data['OBJECT_NAME'])
        idx = -1
        for i in sent_data:
            idx += 1
            sfs = sign_sf(self.reading_data['STATUS_FLAGS'][idx])
            sent_data[i] = [self.reading_data['PRESENT_VALUE'][idx], sfs]
        if self.mqttclient.connect(BROKER, BROKER_PORT):
            self.mqttclient.send(f'{TOPIC}/{device["TOPIC"][0]}', sent_data)


def run():
    gtw = GTW()
    device_list = get_devices()
    while True:
        gtw.run_bacnet(device_list)


if __name__ == '__main__':
    while True:
        timeout(run, 600)