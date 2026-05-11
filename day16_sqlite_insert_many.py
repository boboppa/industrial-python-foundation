import sqlite3

conn = sqlite3.connect("industrial_alarms.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS alarms")

cursor.execute("""
               create table alarms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT,
                    area TEXT,
                    status TEXT,
                    priority TEXT
               )
               """)


alarm_data = [
    ('ALM001', 'boiler', 'active', 'high'),
    ('ALM002', 'pump', 'cleared', 'low'),
    ('ALM003', 'boiler', 'active', 'medium'),
    ('ALM004', 'conveyor', 'active', 'high'),
    ('ALM005', 'pump', 'active', 'medium'),
    ('ALM006', 'tank', 'cleared', 'low'),

]


cursor.executemany("""
                   insert into alarms (tag, area, status, priority)
                   values (?, ? , ? , ?)
                   """, alarm_data)


conn.commit()

cursor.execute("select * from alarms")
rows = cursor.fetchall()

for row in rows: 
    print(row)
    
conn.close() 