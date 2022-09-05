from loguru import logger

PREFIX = "devices/"


def csv_to_dict(csv_file, csv_delimiter):
    with open(f"{PREFIX}{csv_file}", 'r') as fl:
        csv_txt = fl.read().splitlines()
    cols = csv_txt[0].split(csv_delimiter)
    result_dict = dict.fromkeys(cols)
    for col in cols:
        result_dict[col] = []
    idx = 0
    rows = len(csv_txt) - 1
    while idx < rows:
        idx += 1
        row = csv_txt[idx].split(csv_delimiter)
        c = -1
        for col in cols:
            c += 1
            if row[c].isdigit():
                row[c] = int(row[c])
            result_dict[col].append(row[c])
    validator = Validator()
    if validator.check_csv_data(result_dict):
        return result_dict
    else:
        return False


class Validator:
    state = []

    def check_csv_data(self, check_data):
        self.check_ip(check_data['DEVICE_IP'][0])
      #  self.check_port(check_data['PORT'][0])
        self.check_id(check_data['DEVICE_ID'])
        self.check_object_type(check_data['OBJECT_TYPE'])
        self.check_id(check_data['OBJECT_ID'])
        self.check_name(check_data['OBJECT_NAME'])
        self.check_topic(check_data['TOPIC'])

        if False in self.state:
            return False
        else:
            return True

    def check_ip(self, check_data):
        if Validator.validate_ip(check_data):
            self.state.append(True)
        else:
            logger.error("column 'device_ip' must be like  10.21.102.47")
            self.state.append(False)

    def check_port(self, check_data):
        if Validator.validate_digit(check_data, 1, 65535):
            self.state.append(True)
        else:
            logger.error("column 'port' must be a digit 0-65535")
            self.state.append(False)

    def check_object_type(self, check_data):
        for ot in check_data:
            if Validator.validate_in_enum(['analogInput', 'analogOutput', 'analogValue',
                                           'binaryInput', 'binaryOutput', 'binaryValue',
                                           'multiStateInput', 'multiStateOutput', 'multiStateValue', 'di'], ot):
                self.state.append(True)
            else:
                logger.error("column OBJECT_TYPE must be a analogInput, analogOutput, analogValue,binaryInput,"
                             " binaryOutput, binaryValue,multiStateInput, multiStateOutput, multiStateValue")
                self.state.append(False)

    def check_id(self, check_data):
        for di in check_data:
            if Validator.validate_digit(di, 1, 4194303):
                self.state.append(True)
            else:
                logger.error("column ID must be a digit 0-4194303")
                self.state.append(False)

    def check_name(self, check_data):
        for nm in check_data:
            if isinstance(nm, str):
                self.state.append(True)
            else:
                logger.error("column 'name' must be a string")
                self.state.append(False)

    def check_topic(self, check_data):

        if isinstance(check_data[0], str):
            self.state.append(True)
        else:
            logger.error("column 'topic' must be a string")
            self.state.append(False)

    @staticmethod
    def validate_ip(ip):
        a = ip.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    @staticmethod
    def validate_digit(value, start, stop):
        if isinstance(value, (int, float)):
            if start <= value <= stop:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def validate_in_enum(enum, input_data):
        if input_data in enum:
            return True
        else:
            return False


