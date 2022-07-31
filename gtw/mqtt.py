import paho.mqtt.client as mqttc
import json
from loguru import logger


class MyMQTT:

    #def __init__(self):
        #logger.add('logs/mqtt.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation='10 MB')

    def create(self, user_name, user_passwd):
        try:
            self.client = mqttc.Client(userdata=None, protocol=mqttc.MQTTv311, transport="websockets")
            self.client.ws_set_options(path="/ws", headers=None)
            self.client.username_pw_set(username=user_name, password=user_passwd)
            logger.debug("READY create mqtt-client")
        except Exception as e:
            logger.exception("FAIL create mqtt-client", e)

    def connect(self, broker, port):
        try:
            self.client.connect(broker, port=port, keepalive=60, bind_address="")
            logger.debug("READY connect mqtt-client to broker")
            return True
        except Exception as e:
            logger.exception("FAIL connect mqtt-client to broker", e)
            return False

    def send(self, topic, send_data):
        try:
            send_json = json.dumps(send_data)
            self.client.publish(topic, payload=send_json, qos=1, retain=True)
            logger.debug(f"SUCCESSFUL sent data {topic}")
            #logger.info(send_json)
        except Exception as e:
            logger.exception("FAIL sent data", e)


