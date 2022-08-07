# Здесь нужно выбрать вариант отправки собранных из BACnet данных
GTW_MODE = "bacnet-mqtt"  # или "bacnet-mqtt-sqlite3", "bacnet-mqtt-timescaledb"

# Параметры сетевого интерфейса хоста с которого опрашиваются девайсы
HOST_IP = "10.168.253.150"
HOST_PORT = 47808

# Список csv-файлов с конфигурациями объектов девайсов, вписанные девайсы будут опрашиваться
DEVICE_CSV = ['gtw/devices/device_105.csv']

# Максимальное Количество точек для мультичтения
MILTIREAD_LENGTH = 50 #  Минимум 3, Максимум заисит от того сколько может отдать девайс по превысив APDU

# MQTT параметры
USER_NAME = 'admin'
USE_PASSWD = 'admin'
BROKER = "46.8.210.67"
BROKER_PORT = 15675
TOPIC = "zavidovo"

# Параметры базы данных sqlite3
DB_NAME = "gtw/database/devices.db"

# Параметры Timescale DB

TSDB_USER = "postgres"
TSDB_PASS = "Postgres2!"
TSDB_HOST = "tsdb.4iot.pro"
TSDB_PORT = 1532
TSDB_DB = "postgres"
