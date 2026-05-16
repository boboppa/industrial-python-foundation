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

datanew = [
    ("ALM001", "boiler", "active", "high"),
    ("ALM002", "pump", "cleared", "low"),
    ("ALM003", "boiler", "active", "medium"),
    ("ALM004", "conveyor", "active", "high"),
    ("ALM005", "pump", "active", "medium"),
    ("ALM006", "tank", "cleared", "low"),
    ("ALM007", "boiler", "cleared", "low"),
    ("ALM008", "tank", "active", "high")

]

cursor.executemany("""
                insert into alarms (tag, area, status, priority)
                values (?,?,?,?)
                   """, datanew)

conn.commit()
print("order by area")
cursor.execute("""
select * from alarms
order by area asc               
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

print("count status active")
cursor.execute("""
select count(*) from alarms
where status = 'active'
               """)

rows = cursor.fetchall()
for row in rows:
    print(row)

print("count alarm by area")
cursor.execute("""
select area, count(*) from alarms
group by area
order by area 
               """)
rows = cursor.fetchall()
for row in rows:
    print(row)

print("count alarm active by area ex 4")
cursor.execute("""
select area, count(*) from alarms
               where status ='active'
group by area
order by area 
               """)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()

