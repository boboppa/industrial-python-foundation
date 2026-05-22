import csv
import sqlite3

def read_csv(filename):
    res = []
    
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            res.append(row)
        
    return res

#print(read_csv("alarms_week3_dirty.csv"))

def get_valid_alarm_data(filename):
    data = read_csv(filename)
    good_status = ["active","cleared"]
    good_prio = ["low", "medium", "high"]
    
    res = []
    for alarm in data:
        if alarm["tag"] != "" and alarm["area"] != "" and alarm["status"] in good_status and alarm["priority"] in good_prio: 
            res.append((alarm["tag"],
                        alarm["area"],
                        alarm["status"],
                        alarm["priority"]))
    
    return res

#print(get_valid_alarm_data("alarms_week3_dirty.csv"))
def setup_database(db_name, alarm_data):

    conn = sqlite3.connect(db_name)
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
    cursor.executemany("""
                       insert into alarms (tag, area, status, priority)
                       values (?,?,?,?)
                       """, alarm_data)
    conn.commit()
    return conn


def get_area_report(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
                   select area, count(*) from alarms
                   group by area
                   """)
    rows = cursor.fetchall()
    report = []
    for row in rows:
        report.append({
            "area" : row[0],
            "count": row[1]
        })
    return report

def get_active_area_report(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
                   select area, count(*) from alarms
                   where status = 'active'
                   group by area
                   """)
    rows = cursor.fetchall()
    report = []
    for row in rows: 
        report.append({
            "area" : row[0],
            "active_count" : row[1]
        })
    return report

def get_priority_report(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
                   select priority, count(*) from alarms
                   group by priority
                   """)
    rows = cursor.fetchall()
    report = []
    for row in rows: 
        report.append({
            "priority" : row[0],
            "count" : row[1]
        })
    return report


alarm_data = get_valid_alarm_data("alarms_week3_dirty.csv")
conn = setup_database("industrial_alarms.db", alarm_data)

print("Area report")
print(get_area_report(conn))

print("Active area report")
print(get_active_area_report(conn))

print("Priority report")
print(get_priority_report(conn))

conn.close()


    