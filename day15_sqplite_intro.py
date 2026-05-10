import sqlite3

conn  = sqlite3.connect("industrial_alarms.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS alarms")
cursor.execute("""
               create TABLE IF NOT EXISTS alarms(
                   
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   tag TEXT,
                   area TEXT,
                   status TEXT,
                   priority TEXT
               )
               """)

cursor.execute("""
               INSERT INTO alarms (tag, area, status, priority)
               VALUES(?, ?, ?, ?)
               """, ("ALM001","boiler", "active", "high"))

cursor.execute("""
               INSERT INTO alarms (tag, area, status, priority)
               VALUES(?, ?, ?, ?)
               """, ("ALM002","pump", "cleared", "low"))

cursor.execute("""
               INSERT INTO alarms (tag, area, status, priority)
               VALUES(?, ?, ?, ?)
               """, ("ALM003","boiler", "active", "medium"))

cursor.execute("""
               INSERT INTO alarms (tag, area, status, priority)
               VALUES(?, ?, ?, ?)
               """, ("ALM004","conveyor", "active", "high"))

conn.commit()

cursor.execute("SELECT * FROM alarms")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()