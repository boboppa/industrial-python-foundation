import pandas as pd

df = pd.read_csv("alarms_week4_dirty.csv")
#print(df.head(5))
#print(df.shape)
#print(df.isna().sum())

valid_status = ["active", "cleared"]
valid_priority = ["high", "medium", "low"]

valid_condition = (
    df["tag"].notna() & df["area"].notna() & df["status"].isin(valid_status) & df["priority"].isin(valid_priority)
)

valid_alarms = df[valid_condition]
invalid_alarms = df[~valid_condition]
#print(valid_alarms)
#print(invalid_alarms)
print("Total rows:", len(df))
print("Valid rows:", len(valid_alarms))
print("Invalid rows:", len(invalid_alarms))
