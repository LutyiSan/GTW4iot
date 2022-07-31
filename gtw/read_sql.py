import sqlite3 as sql

db = "devices.db"
table = "device_device_108"

conn = sql.connect(db)
cursor = conn.cursor()
res = cursor.execute(f"""SELECT OBJECT_NAME, PRESENT_VALUE, TIMESTAMP FROM {table};""")
for i in res:
    print(f'name: {i[0]}: value: {i[1]} time: {i[2]}')