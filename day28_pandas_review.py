import pandas as pd

#ex 1
df = pd.read_csv("alarms_week4_dirty.csv")

#print(df.head(5))
#print(df.shape)
#print(df.isna().sum())

#ex 2
valid_status = ["active","cleared"]
valid_prio =  ["high","medium","low"]
valid_condition = (df["tag"].notna() & df["area"].notna() & df["status"].isin(valid_status) & df["priority"].isin(valid_prio))
valid_alarm = df[valid_condition]
invalid_alarm = df[~valid_condition]

new_col = [{"metric":"Total rows", "count" : len(df)},
           {"metric":"Valid rows", "count" : len(valid_alarm)},
           {"metric":"Invalid rows", "count" : len(invalid_alarm)}]
summary = pd.DataFrame(new_col)
#print(summary)

#ex 3
area_report = valid_alarm.groupby("area").size().reset_index(name = "count")
print(area_report)
priority_report = valid_alarm.groupby("priority").size().reset_index(name= "count")
print(priority_report)
active_area_report = valid_alarm[valid_alarm["status"]=="active"].groupby("area").size().reset_index(name="count")
print(active_area_report)

#ex 4
valid_alarm.to_csv("day28_valid_alarms.csv", index = False)
area_report.to_csv("day28_area_report.csv", index = False)
priority_report.to_csv("day28_priority_report.csv", index = False)
active_area_report.to_csv("day28_active_area_report.csv", index = False)

#ex 5

area_priority_report = valid_alarm.groupby(["area","priority"]).size().reset_index(name="count")
area_priority_report.to_csv("day28_area_priority_report.csv",index=False)