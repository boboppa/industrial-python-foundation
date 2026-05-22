import pandas as pd

df = pd.read_csv("alarms_week4.csv")

alarm_overview = df[["tag","area","priority"]]
#print(alarm_overview)

active_high_alarms = df[(df["status"] == "active") & (df["priority"] == "high")]
#print(active_high_alarms)

sorted_by_area = df.sort_values("area")
#print(sorted_by_area)

active_alarm_report = df[df["status"] == "active"].sort_values("priority")
print(active_alarm_report[["tag","area","priority"]])