# GTW4iot
Данная программа является шлюзом BACnet - MQTT.
# Установка
1. Выполнить команду "sudo git lone https://github.com/LutyiSan/GTW4iot"
2. Перейти в папку "GTW4iot"
3. Заполнить параметры в файле "GTW4iot/gtw/env.py"
4. В папке "GTW4iot/gtw/devices" разместить файлы с конфигурациями девайсов в формате csv( Пример: device_109.csv).
5. Находясь в папке "GTW4iot", выполнить команду "sudo sh build.sh"
# Запуск
Находясь в папке GTW4iot, выполнить команду "sudo sh start.sh"
