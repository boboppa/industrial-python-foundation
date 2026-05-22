import pandas as pd

df = pd.read_csv("alarms_week4.csv")
#print(df.head(5))
#print(df.shape)
#df.info()

active_alarms = df[df["status"] == "active"]
#print(df["tag"])
#print(active_alarms)

count_alarm_by_area = df["area"].value_counts()
count_alarm_by_prio = df["priority"].value_counts()
print(count_alarm_by_area)
print(count_alarm_by_prio)
