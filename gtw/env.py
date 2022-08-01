# Здесь нужно выбрать вариант отправки собранных из BACnet данных
GTW_MODE = "bacnet-mqtt"  # или "bacnet-mqtt-sqlite3", "bacnet-mqtt-timescaledb"

# Параметры сетевого интерфейса хоста с которого опрашиваются девайсы
HOST_IP = "127.0.01"
HOST_PORT = 47808

# Список csv-файлов с конфигурациями объектов девайсов, вписанные девайсы будут опрашиваться
DEVICE_CSV = ['gtw/devices/device_101.csv', 'gtw/devices/device_102.csv', 'gtw/devices/device_103.csv',
              'gtw/devices/device_104.csv', 'gtw/devices/device_105.csv', 'gtw/devices/device_106.csv',
              'gtw/devices/device_107.csv', 'gtw/devices/device_108.csv', 'gtw/devices/device_109.csv',
              'gtw/devices/device_110.csv', 'gtw/devices/device_111.csv', 'gtw/devices/device_112.csv',
              'gtw/devices/device_113.csv']

# Максимальное Количество точек для мультичтения
MILTIREAD_LENGTH = 50

# MQTT параметры
USER_NAME = 'name'
USE_PASSWD = 'pass'
BROKER = "my.mqtt.com"
BROKER_PORT = 15675
TOPIC = "zavidovo"

# Параметры базы данных sqlite3
DB_NAME = "database/devices.db"

# Параметры Timescale DB

TSDB_USER = "name"
TSDB_PASS = "pass"
TSDB_HOST = "tsdb.my.com"
TSDB_PORT = 1532
TSDB_DB = "database"
