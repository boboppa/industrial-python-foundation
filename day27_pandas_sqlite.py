import sqlite3
import pandas as pd

conn = sqlite3.connect("industrial_alarms.db")


df = pd.read_sql_query("""
    select * from alarms
                      """,conn)

#print(df.head())
#print(df.shape)

#ex 2
area_report = pd.read_sql_query("""
    select area, count(*) as count from alarms
    group by area
                                """,conn)

#print(area_report)

#ex 3
active_area_report = pd.read_sql_query("""
    select area, count(*) as count from alarms
    where status = 'active'
    group by area
                                       """,conn)

#print(active_area_report)

#ex 4
area_report.to_csv("sqlite_area_report.csv", index= False)
active_area_report.to_csv("sqlite_active_area_report.csv", index= False)

#ex 5

pandas_area_report = df.groupby("area").size().reset_index(name='count')

print(area_report)
print(pandas_area_report)