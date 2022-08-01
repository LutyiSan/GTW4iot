# Параметры сетевого интерфейса хоста с которого опрашиваются девайсы
HOST_IP = "10.168.253.150"
HOST_PORT = 47808

# Список csv-файлов с конфигурациями объектов девасов, вписаные девайсы будут опрашиваться
DEVICE_CSV = ['gtw/devices/device_101.csv', 'gtw/devices/device_102.csv', 'gtw/devices/device_103.csv',
              'gtw/devices/device_104.csv', 'gtw/devices/device_105.csv', 'gtw/devices/device_106.csv',
              'gtw/devices/device_107.csv', 'gtw/devices/device_108.csv', 'gtw/devices/device_109.csv',
              'gtw/devices/device_110.csv', 'gtw/devices/device_111.csv', 'gtw/devices/device_112.csv',
              'gtw/devices/device_113.csv']

# Максимальное Количество точек для мультичтения
MILTIREAD_LENGTH = 50

# MQTT параметры
USER_NAME = 'admin'
USE_PASSWD = 'admin'
BROKER = "46.8.210.67"
BROKER_PORT = 15675
TOPIC = "zavidovo"

# Параметры базы данных sqlite
DB_ENABLE = False
DB_NAME = "database/devices.db"

# Параметры Timescale DB
TSDB_ENABLE = False
CONNECTION = "postgres://postgres:Postgres2!@tsdb.4iot.pro:1532/postgres"
TSDB_USER = "postgres"
TSDB_PASS = "Postgres2!"
TSDB_HOST = "tsdb.4iot.pro"
TSDB_PORT = 1532
TSDB_DB = "postgres"
