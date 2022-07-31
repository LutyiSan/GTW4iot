# Параметры сетевого интерфейса хоста с которого опрашиваются девайсы
HOST_IP = "10.168.253.150"
HOST_PORT = 47808

# Список csv-файлов с конфигурациями объектов девасов, вписаные девайсы будут опрашиваться
DEVICE_CSV = ['device_101.csv','device_102.csv','device_103.csv','device_104.csv','device_105.csv','device_106.csv','device_107.csv','device_108.csv','device_109.csv','device_110.csv','device_111.csv','device_112.csv','device_113.csv']
#DEVICE_CSV = ["device_113.csv"]

# Максимальное Количество точек для мультичтения
MILTIREAD_LENGTH = 50

# MQTT параметры
USER_NAME = 'admin'
USE_PASSWD = 'admin'
BROKER = "46.8.210.67"
BROKER_PORT = 15675
TOPIC = "zavidovo"