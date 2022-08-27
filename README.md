# bacnet4iot
Данная программа является шлюзом BACnet - MQTT.
# Установка
1. Выполнить команду "sudo git lone https://github.com/LutyiSan/bacnet4iot"
2. Перейти в папку "bacnet4iot"
3. Заполнить параметры в файле "bacnet4iot/gtw/env.py"
4. В папке "bacnet4iot/gtw/devices" разместить файлы с конфигурациями девайсов в формате csv( Пример: device_109.csv).

# Запуск без Docker
1. Находясь в папке bacnet4iot, выполнить команду "sudo sh build.sh". !! Только при первом запуске !!
2. Находясь в папке bacnet4iot, выполнить команду "sudo sh start.sh"

# Запуск с Docker
1. Находясь в папке bacnet4iot, выполнить команду "sudo docker-compose up".
