import BAC0
from loguru import logger
import time
from env import MILTIREAD_LENGTH


class BACnetClient:

    def create(self, ip_address, port):
        try:
            self.client = BAC0.lite(ip=ip_address, port=port)
            logger.debug("READY create bacnet-client")
            # return True
        except Exception as e:
            logger.exception("FAIL create bacnet-client", e)
        # return False

    def read_single(self, device_dict):
        device_dict['STATUS_FLAGS'] = []
        signal = -1
        while signal < (len(device_dict['OBJECT_ID']) - 1):
            signal += 1
            try:
                self.pv = self.client.read(f'{device_dict["DEVICE_IP"][0]}/24 {device_dict["OBJECT_TYPE"][signal]}'
                                           f' {device_dict["OBJECT_ID"][signal]} presentValue')
                self.sf = self.client.read(f'{device_dict["DEVICE_IP"][0]}/24 {device_dict["OBJECT_TYPE"][signal]}'
                                           f' {device_dict["OBJECT_ID"][signal]} statusFlags')
                logger.debug(f'READ OK {device_dict["DEVICE_IP"][0]} {device_dict["OBJECT_TYPE"][signal]}'
                             f' {device_dict["OBJECT_ID"][signal]} presentValue: {self.pv} statusFlags: {self.sf}')
            except Exception as e:
                logger.exception(f'FAIL READ {device_dict["DEVICE_IP"][0]} {device_dict["OBJECT_TYPE"][signal]}'
                                 f' {device_dict["OBJECT_ID"][signal]}', e)
            if isinstance(self.pv, (str, int, float)):
                device_dict['PRESENT_VALUE'][signal] = self.pv
            else:
                device_dict['PRESENT_VALUE'][signal] = "Null"
            if isinstance(self.sf, list):
                device_dict['STATUS_FLAGS'].append(self.sf)
            else:
                device_dict['STATUS_FLAGS'].append(['Null', 'Null', 'Null', 'Null'])
        return device_dict

    def read_multiple(self):
        _rpm = self.rpm_maker(self.load_data)
        try:
            self.read_result = self.client.readMultiple(f'{self.device["DEVICE_IP"][0]}/24', request_dict=_rpm)
            if len(self.read_result) == len(_rpm['objects']):
                idx = -1
                for i in self.read_result:
                    print(i)
                    print(self.read_result[i][0][1])
                    idx += 1
                    #  print(self.read_result[i][0][1])
                    self.device["PRESENT_VALUE"].append(self.read_result[i][0][1])
                    #  print(self.read_result[i][1][1])
                    self.device["STATUS_FLAGS"].append(self.read_result[i][1][1])
                    logger.debug(f"{self.device['DEVICE_IP'][0]} {i[0]}: {i[1]} {self.read_result[i][0][0]}:"
                                 f" pv={self.read_result[i][0][1]} sf={self.read_result[i][1][1]}")
                # print(self.device)
                return self.device
            else:
                logger.error("FAIL MULTIPLE-READ")
                idx = -1
                for i in self.load_data['OBJECT_ID']:
                    idx += 1
                    #  print(self.read_result[i][0][1])
                    self.device["PRESENT_VALUE"].append('Null')
                    #  print(self.read_result[i][1][1])
                    self.device["STATUS_FLAGS"].append(['Null', 'Null', 'Null', 'Null'])

                return self.device

        except Exception as e:
            logger.exception("FAIL MULTIPLE-READ", e)
            return False

    def read_load(self, device_dict):
        self.pack_dict = {'PRESENT_VALUE': [], 'STATUS_FLAGS': [], 'OBJECT_NAME': []}
        self.device = device_dict
        self.device['STATUS_FLAGS'] = []
        self.device['PRESENT_VALUE'] = []
        start = time.time()
        self.len_request = MILTIREAD_LENGTH
        if MILTIREAD_LENGTH > len(self.device['OBJECT_ID']):
            self.len_request = len(self.device['OBJECT_ID'])
        elif len(self.device['OBJECT_ID']) > self.len_request:
            self.len_signals = len(self.device['OBJECT_ID'])
            self.load_data = dict()
            segments = self.len_signals // self.len_request
            self.last_segment = self.len_signals % self.len_request
            s = 0
            while s < segments:
                s += 1
                if s == 1:
                    self.slicer(s)
                    self.read_multiple()
                else:
                    self.slicer(s)
                    self.read_multiple()
            if self.last_segment > 0:
                self.slicer(0)
                self.read_multiple()
                if isinstance(self.device, dict):
                    self.insert_pv()
            cycle = (time.time() - start)
            print(f'Cycle time {cycle} sec')
            self.insert_pv()
            return self.pack_dict

    def insert_pv(self):
        self.pack_dict["OBJECT_NAME"] = self.device["OBJECT_NAME"]
        self.pack_dict["PRESENT_VALUE"] = self.device['PRESENT_VALUE']
        self.pack_dict["STATUS_FLAGS"] += self.device['STATUS_FLAGS']

    def slicer(self, s):
        if s == 1:
            self.load_data["OBJECT_TYPE"] = self.device['OBJECT_TYPE'][0:self.len_request]
            self.load_data["OBJECT_ID"] = self.device['OBJECT_ID'][0:self.len_request]
        elif s == 0:
            self.load_data["OBJECT_TYPE"] = self.device['OBJECT_TYPE'][-self.last_segment:]
            # print("last segment",self.device['OBJECT_TYPE'][-self.last_segment:])
            self.load_data["OBJECT_ID"] = self.device['OBJECT_ID'][-self.last_segment:]
        else:
            self.load_data["OBJECT_TYPE"] = self.device['OBJECT_TYPE'][self.len_request * (s - 1):self.len_request * s]
            self.load_data["OBJECT_ID"] = self.device['OBJECT_ID'][self.len_request * (s - 1):self.len_request * s]

    def rpm_maker(self, load):
        read_objects = dict()
        _rpm = {'address': self.device['DEVICE_IP'][0]}
        idx = -1
        while idx < (len(load["OBJECT_ID"]) - 1):
            idx += 1
            key_0 = load['OBJECT_TYPE'][idx]
            key_1 = load['OBJECT_ID'][idx]
            properties = ['presentValue', 'statusFlags']
            read_objects.update({f"{key_0}:{key_1}": properties})
        _rpm['objects'] = read_objects
        return _rpm

    def disconnect(self):
        self.client.disconnect()
