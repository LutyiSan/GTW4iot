import BAC0
from loguru import logger
import time
from env import MILTIREAD_LENGTH


class BACnetClient:
    def __init__(self):
        self.pack_dict = None
        self.read_result = None
        self.read_dict = None
        self.device_dict = dict()
        self.pv = None
        self.client = None
        self.port = None
        self.ip_address = None
        logger.add('logs/bacnet.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation='10 MB')

    def create(self, ip_address, port):
        try:
            self.client = BAC0.lite(ip=ip_address, port=port)
            logger.debug("READY create bacnet-client")
            return True
        except Exception as e:
            logger.exception("FAIL create bacnet-client", e)
            return False

    def read_single(self, device_dict):
        signal = -1
        while signal < (len(device_dict['OBJECT_ID']) - 1):
            signal += 1
            try:
                self.pv = self.client.read(f'{device_dict["DEVICE_IP"][signal]}/24 {device_dict["OBJECT_TYPE"][signal]}'
                                           f' {device_dict["OBJECT_ID"][signal]} presentValue')
                logger.debug(f'READ OK {device_dict["DEVICE_IP"][signal]} {device_dict["OBJECT_TYPE"][signal]}'
                             f' {device_dict["OBJECT_ID"][signal]} presentValue: {self.pv}')
            except Exception as e:
                logger.exception(f'FAIL READ {device_dict["DEVICE_IP"][signal]} {device_dict["OBJECT_TYPE"][signal]}'
                                 f' {device_dict["OBJECT_ID"][signal]}', e)
            if isinstance(self.pv, (str, int, float)):
                device_dict['PRESENT_VALUE'][signal] = self.pv
            else:
                device_dict['PRESENT_VALUE'][signal] = "Null"
        return device_dict

    def read_multiple(self, device_dict):
        _rpm = self.rpm_maker(device_dict)
        try:
            self.read_result = self.client.readMultiple(f'{self.read_dict["DEVICE_IP"][1]}/24', request_dict=_rpm)
            if len(self.read_result) >1:
                idx = -1
                for i in self.read_result:
                    idx += 1
                    self.read_dict["PRESENT_VALUE"][idx] = self.read_result[i][0][1]
                    logger.debug(
                        f"{device_dict['DEVICE_IP'][0]} {i[0]}: {i[1]} {self.read_result[i][0][0]}: {self.read_result[i][0][1]}")
                return self.read_dict
            else:
                idx = -1
                while idx < len(self.read_dict["OBJECT_ID"])-1:
                    idx += 1
                    self.read_dict["PRESENT_VALUE"][idx] = "fault"
                return self.read_dict
        except Exception as e:
            logger.exception("FAIL MULTIPLE-READ", e)
        return False

    def read_load(self, device_dict):
        start = time.time()
        self.len_request = MILTIREAD_LENGTH
        self.pack_dict = {"DEVICE_IP": [], "DEVICE_ID": [], "OBJECT_TYPE": [], "OBJECT_ID": [], "OBJECT_NAME": [], "PRESENT_VALUE": [], "TOPIC": []}
        if MILTIREAD_LENGTH > len(device_dict['OBJECT_ID']):
            self.len_request = len(device_dict['OBJECT_ID'])

        if len(device_dict['OBJECT_ID']) > self.len_request:
            self.len_signals = len(device_dict['OBJECT_ID'])
            self.load_data = dict()
            self.ip = device_dict['DEVICE_IP']
            self.device_id = device_dict['DEVICE_ID']
            self.typ = device_dict["OBJECT_TYPE"]
            self.id = device_dict["OBJECT_ID"]
            self.pv = device_dict["PRESENT_VALUE"]
            self.name = device_dict["OBJECT_NAME"]
            self.topic = device_dict["TOPIC"]
            segments = self.len_signals // self.len_request
            self.last_segment = self.len_signals % self.len_request
            s = 0
            while s < segments:
                s += 1
                if s == 1:
                    self.slicer(s)
                    read_result = self.read_multiple(self.load_data)
                    if isinstance(read_result, dict):
                        self.insert_pv(read_result)
                else:
                    self.slicer(s)
                    read_result = self.read_multiple(self.load_data)
                    if isinstance(read_result, dict):
                        self.insert_pv(read_result)
            if self.last_segment > 0:
                self.slicer(0)
                read_result = self.read_multiple(self.load_data)
                if isinstance(read_result, dict):
                    self.insert_pv(read_result)
            cicle = (time.time() - start)
            print (f'Cicle time {cicle} sec')
            return self.pack_dict
        elif len(device_dict['OBJECT_ID']) == self.len_request:
            return device_dict

    def insert_pv(self, read_result):
        self.pack_dict["DEVICE_IP"] += read_result['DEVICE_IP']
        self.pack_dict["DEVICE_ID"] += read_result['DEVICE_ID']
        self.pack_dict["OBJECT_TYPE"] += read_result['OBJECT_TYPE']
        self.pack_dict["OBJECT_ID"] += read_result['OBJECT_ID']
        self.pack_dict["PRESENT_VALUE"] += read_result['PRESENT_VALUE']
        self.pack_dict["OBJECT_NAME"] += read_result["OBJECT_NAME"]
        self.pack_dict["TOPIC"] += read_result["TOPIC"]

    def slicer(self, s):
        if s == 1:
            self.load_data["DEVICE_IP"] = self.ip[0:self.len_request]
            self.load_data["DEVICE_ID"] = self.device_id[0:self.len_request]
            self.load_data["OBJECT_TYPE"] = self.typ[0:self.len_request]
            self.load_data["OBJECT_ID"] = self.id[0:self.len_request]
            self.load_data["OBJECT_NAME"] = self.name[0:self.len_request]
            self.load_data["PRESENT_VALUE"] = self.pv[0:self.len_request]
            self.load_data["TOPIC"] = self.topic[0:self.len_request]
        elif s == 0:
            self.load_data["DEVICE_IP"] = self.ip[self.len_request * s:self.len_request * s + self.last_segment]
            self.load_data["DEVICE_ID"] = self.device_id[self.len_request * s:self.len_request * s + self.last_segment]
            self.load_data["OBJECT_TYPE"] = self.typ[self.len_request * s:self.len_request * s + self.last_segment]
            self.load_data["OBJECT_ID"] = self.id[self.len_request * s:self.len_request * s + self.last_segment]
            self.load_data["PRESENT_VALUE"] = self.pv[self.len_request * s:self.len_request * s + self.last_segment]
            self.load_data["OBJECT_NAME"] = self.name[self.len_request * s:self.len_request * s + self.last_segment]
            self.load_data["TOPIC"] = self.topic[self.len_request * s:self.len_request * s + self.last_segment]

        else:
            self.load_data["DEVICE_IP"] = self.ip[self.len_request * (s - 1):self.len_request * s]
            self.load_data["DEVICE_ID"] = self.device_id[self.len_request * (s - 1):self.len_request * s]
            self.load_data["OBJECT_TYPE"] = self.typ[self.len_request * (s - 1):self.len_request * s]
            self.load_data["OBJECT_ID"] = self.id[self.len_request * (s - 1):self.len_request * s]
            self.load_data["OBJECT_NAME"] = self.name[self.len_request * (s - 1):self.len_request * s]
            self.load_data["PRESENT_VALUE"] = self.pv[self.len_request * (s - 1):self.len_request * s]
            self.load_data["TOPIC"] = self.topic[self.len_request * (s - 1):self.len_request * s]

    def rpm_maker(self, device_dict):
        self.read_dict = device_dict
        read_objects = dict()
        _rpm = {'address': self.read_dict['DEVICE_IP'][0]}
        idx = -1
        while idx < (len(self.read_dict["OBJECT_ID"]) - 1):
            idx += 1
            key_0 = self.read_dict['OBJECT_TYPE'][idx]
            key_1 = self.read_dict['OBJECT_ID'][idx]
            properties = ['presentValue', 'objectName']
            read_objects.update({f"{key_0}:{key_1}": properties})
        _rpm['objects'] = read_objects
        return _rpm



    def disconnect(self):
        self.client.disconnect()