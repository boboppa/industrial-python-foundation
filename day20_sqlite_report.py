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
    ("ALM008", "tank", "active", "high"),
    ("ALM009", "pump", "active", "high"),
    ("ALM010", "conveyor", "cleared", "medium")
    
]

cursor.executemany("""
                insert into alarms (tag, area, status, priority)
                values (?,?,?,?)
                   """, datanew)

conn.commit()
print("ex 1")
cursor.execute("""
select area,count(*) from alarms 
group by area;          
""")

rows = cursor.fetchall()

#for row in rows:
    #print(row)
    
report_area = []

for row in rows:
    report_area.append({
        "area" : row [0], 
        "count" : row[1]
    })
print(report_area)

print("ex2")

cursor.execute("""
select area, count(*)  from alarms 
where status = "active"
group by area          
""")

rows = cursor.fetchall()
report_area2 = []
for row in rows:
    report_area2.append({
        "area" : row[0],
        "active_count" : row [1]
    })
print(report_area2)


print("ex 3")
cursor.execute("""
select priority, count(*)  from alarms 
group by priority          
""")

rows = cursor.fetchall()
report_area3 = []
for row in rows:
    report_area3.append({
        "priority" : row[0],
        "count" : row [1]
    })
print(report_area3)

conn.close()


