import sqlite3
import csv

def read_csv(filename):
    res = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        for now in reader:
            res.append(now)

    return res
def valid_alarm_set(filename):
    res = read_csv(filename)
    good_status = ["active","cleared"]
    good_priority = ["low","medium","high"]
    
    valid_alarm_data = []
    for alarm in res:
        if alarm["tag"] != "" and alarm["area"] != "" and alarm["status"] != "" and alarm["status"] and alarm["status"] in good_status and alarm["priority"] in good_priority:
            valid_alarm_data.append((alarm["tag"],alarm["area"],alarm["status"],alarm["priority"]))
    

    return valid_alarm_data


#print(valid_alarm_set("alarms_day19_dirty.csv"))

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

valid_alarm_data = valid_alarm_set("alarms_day19_dirty.csv")

cursor.executemany("""
                    insert into alarms (tag, area, status, priority)
                    values (?,?,?,?)
                   """, valid_alarm_data)
conn.commit()
print("Insert into sql")
cursor.execute("""
select * from alarms               
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

print("count alarm by area")
cursor.execute("""
select area, count(*) from alarms
group by area
               """)
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

