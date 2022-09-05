# Параметры сетевого интерфейса хоста с которого опрашиваются девайсы
HOST_IP = "192.168.1.67"
HOST_PORT = 47808

# Список csv-файлов с конфигурациями объектов девайсов, вписанные девайсы будут опрашиваться
DEVICE_CSV = ['device_sim_bacnet.csv']

# Максимальное Количество точек для мультичтения
MILTIREAD_LENGTH = 29  # Минимум 3, Максимум заисит от того сколько может отдать девайс по превысив APDU
#  Если =1, то будет происходить чтение сигналов по одному

# MQTT параметры
USER_NAME = 'user'
USE_PASSWD = 'user'
BROKER = "mq.4iot.pro"
BROKER_PORT = 15675
TOPIC = "zavidovo"

# Здесь нужно выбрать вариант отправки, собранных из BACnet, данных
# GTW_MODE = "bacnet-mqtt"  # или "bacnet-mqtt-sqlite3", "bacnet-mqtt-timescaledb"
# Параметры базы данных sqlite3######
# DB_NAME = "gtw/database/devices.db"#

# Параметры Timescale DB#

# TSDB_USER = "postgres"#
# TSDB_PASS = "PostgresPass"#
# TSDB_HOST = "10.10.10.10"#
# TSDB_PORT = 1532#
# TSDB_DB = "postgres"#
##########################
