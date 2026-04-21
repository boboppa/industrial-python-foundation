alarms = [
    {"tag": "P101", "severity": "high", "message": "Pump overload"},
    {"tag": "T202", "severity": "medium", "message": "Temperature high"},
    {"tag": "V303", "severity": "high", "message": "Valve feedback error"},
    {"tag": "M404", "severity": "low", "message": "Motor vibration"},
]

def print_all_tags(alarms):
    for alarm in alarms:
        print(alarm["tag"])
        
print_all_tags(alarms)

def count_high_alarms(alarms):
    count = 0
    for alarm in alarms:
        if alarm["severity"] == "high":
            count += 1
    return count

print(count_high_alarms(alarms))

def print_high_alarms_tags(alarms):
    for alarm in alarms:
        if alarm["severity"] == "high":
            print(alarm["tag"])

print_high_alarms_tags(alarms)