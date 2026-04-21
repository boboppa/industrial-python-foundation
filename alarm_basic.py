alarms = [
    {"tag": "P101", "severity": "high"},
    {"tag": "T202", "severity": "medium"},
    {"tag": "V303", "severity": "high"},
    {"tag": "M404", "severity": "low"}
]
high_count = 0
for alarm in alarms:
    if alarm["severity"] == "high":
        high_count += 1
print(high_count)

