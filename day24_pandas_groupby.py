import pandas as pd

df = pd.read_csv("alarms_week4.csv")

area_count = df["area"].value_counts()
#print(area_count)

area_report  = df.groupby("area").size().reset_index(name="count")
#print(area_report)

active_area_report = df[df["status"] == "active"]["area"].value_counts().reset_index(name="count")
print(active_area_report)

area_priority_report = df.groupby(["area", "priority"]).size().reset_index(name="count")
#print(area_priority_report)