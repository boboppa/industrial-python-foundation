import sqlite3

conn = sqlite3.connect("industrial_alarms.db")
cursor = conn.cursor()

cursor.execute("drop table if exists alarms")

cursor.execute("""
            create table alarms (
               id integer primary key autoincrement,
               tag text,
               area text,
               status text,
               priority text
            )
            """)

alarms = [
    ("ALM001", "boiler", "active", "high"),
    ("ALM002", "pump", "cleared", "low"),
    ("ALM003", "boiler", "active", "medium"),
    ("ALM004", "conveyor", "active", "high"),
    ("ALM005", "pump", "active", "medium"),
    ("ALM006", "tank", "cleared", "low")
]

cursor.executemany("""
                    insert into alarms (tag, area, status, priority)
                    values (?,?,?,?)
                   """, alarms)
conn.commit()

print("Ex 1")
cursor.execute("""
                   select * from alarms
                   where status = 'active'
                   """)


rows = cursor.fetchall()

for row in rows:
    print(row)


print("ex 2")
cursor.execute("""
                select * from alarms
                where area = 'boiler'
               """)
rows = cursor.fetchall()
for row in rows:
    print(row)


print("ex 3")
cursor.execute("""
                select * from alarms
                where status = 'active' and priority = 'high'
               """)
rows = cursor.fetchall()
for row in rows:
    print(row)
    
conn.close()