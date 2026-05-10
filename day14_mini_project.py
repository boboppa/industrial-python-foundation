import csv

def read_csv(filename):
    res = []
    
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        
        for new in reader:
            res.append(new)
            
    return res

def get_valid_alarms(filename):
    data = read_csv(filename)
    sev_gut = ["HIGH","LOW","MEDIUM"]
    stat_gut = ["ACTIVE", "CLEARED"]
    res = []

    for alarm in data:
        if alarm["tag"] != "" and alarm["area"] != "" and alarm["severity"] in sev_gut and alarm["status"] in stat_gut :
            res.append(alarm)
    return res
    
#print(get_valid_alarms("alarms_dirty.csv"))

def valid_area_report(filename):
    data = get_valid_alarms(filename)
    summary = {}
    
    for alarm in data:
        area = alarm["area"]
        
        if area not in summary:
            summary[area] = 0
        summary[area] += 1
        
    res = []
    for new in summary:
        res.append({
            "area" : new,
            "count" : summary[new]
        })
    res.sort(key=lambda item:item["count"], reverse=True)        
    return res


#print(valid_area_report("alarms_dirty.csv"))

def write_csv(filename, fieldnames, data):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file,fieldnames = fieldnames)
        
        writer.writeheader()
        writer.writerows(data)
    
report = valid_area_report("alarms_dirty.csv")
write_csv("valid_area_report.csv",["area", "count"], report)
