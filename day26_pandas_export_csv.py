import pandas as pd

df = pd.read_csv("alarms_week4_dirty.csv")

valid_status = ["active", "cleared"]
valid_priority = ["high", "medium", "low"]

valid_condition = (
    df["tag"].notna() & df["area"].notna() & df["status"].isin(valid_status) & df["priority"].isin(valid_priority)
)

valid_alarms = df[valid_condition]
invalid_alarms = df[~valid_condition]
valid_alarms.to_csv("valid_alarms_week4.csv", index=False)

#ex 2
area_report = valid_alarms.groupby("area").size().reset_index(name="count")
area_report.to_csv("area_report_week4.csv", index=False)

#ex 3
priority_report = valid_alarms["priority"].value_counts().reset_index(name="count")
priority_report.to_csv("priority_report_week4.csv", index=False)

#ex 4
new_table = [
    {"metric": "total_rows", "count": len(df)},
    {"metric": "valid_rows", "count": len(valid_alarms)},
    {"metric": "invalid_rows", "count": len(invalid_alarms)}
]
summary_report = pd.DataFrame(new_table)
summary_report.to_csv("validation_summary_week4.csv", index=False)
