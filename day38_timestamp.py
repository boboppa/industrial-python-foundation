import pandas as pd

def parse_event_timestamps(sensor_events):
    events_with_datetime = sensor_events.assign(
        timestamp = pd.to_datetime(sensor_events["timestamp"])
    )
    return events_with_datetime

def add_event_hour(events_with_datetime):
    events_with_hour = events_with_datetime.assign(
        hour = events_with_datetime["timestamp"].dt.hour
    )
    return events_with_hour

def create_night_event_report(events_with_hour):
    night_events_report = events_with_hour[(events_with_hour["hour"] >= 22)  | (events_with_hour["hour"] < 6) ]
    return night_events_report

def create_high_temperature_event_report(events_with_hour, threshold):
    high_temperature_event_report = events_with_hour[events_with_hour["temperature"] >= threshold]
    return high_temperature_event_report

def create_sorted_event_log(events_with_hour):
    sorted_event_log = events_with_hour.sort_values("timestamp")
    return sorted_event_log

def create_hourly_temperature_report(events_with_hour):
    hourly_temperature_report = events_with_hour.groupby("hour")["temperature"].agg(["min","max","mean"])
    hourly_temperature_report = hourly_temperature_report.rename(columns = {
        "min" : "min_temperature",
        "max" : "max_temperature",
        "mean": "mean_temperature"
    }).reset_index()
    return hourly_temperature_report
    
    

def main():
    sensor_events = pd.DataFrame({
    "event_id": ["E001", "E002", "E003", "E004", "E005", "E006", "E007"],
    "sensor_id": ["S001", "S002", "S003", "S001", "S002", "S003", "S004"],
    "timestamp": [
        "2026-06-27 06:15",
        "2026-06-27 08:30",
        "2026-06-27 11:45",
        "2026-06-27 14:10",
        "2026-06-27 18:20",
        "2026-06-27 22:05",
        "2026-06-27 23:40"
    ],
    "temperature": [68.0, 82.5, 91.0, 88.0, 95.0, 77.0, 101.0],
    "status": ["ok", "ok", "warning", "warning", "error", "ok", "error"]
})
    events_with_datetime = parse_event_timestamps(sensor_events)
    events_with_hour = add_event_hour(events_with_datetime)
    night_events_report = create_night_event_report(events_with_hour)
    threshold = 90
    high_temperature_event_report = create_high_temperature_event_report(events_with_hour, threshold)
    sorted_event_log = create_sorted_event_log(events_with_hour)
    hourly_temperature_report = create_hourly_temperature_report(events_with_hour)
    print(hourly_temperature_report)
    
    
if __name__ == "__main__":
    main()  