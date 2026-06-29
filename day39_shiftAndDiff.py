import pandas as pd

def parse_event_timestamps(sensor_events):
    events_with_datetime = sensor_events.assign(
        timestamp = pd.to_datetime(sensor_events["timestamp"])
    )
    return events_with_datetime

def create_sorted_sensor_log(events_with_datetime):
    sorted_sensor_log = events_with_datetime.sort_values(["sensor_id","timestamp"])
    return sorted_sensor_log

def add_temperature_change_features(sorted_sensor_log):
    events_with_change_features = sorted_sensor_log.assign(
        previous_temperature = sorted_sensor_log.groupby("sensor_id")["temperature"].shift(1),
        temperature_change = sorted_sensor_log.groupby("sensor_id")["temperature"].diff()
    )
    return events_with_change_features

def create_first_event_report(events_with_change_features):
    first_event_report = events_with_change_features[events_with_change_features["previous_temperature"].isna()]
    return first_event_report

def create_rapid_temperature_increase_report(events_with_change_features, change_threshold):
    rapid_temperature_increase_report = events_with_change_features[events_with_change_features["temperature_change"] >= change_threshold]
    return rapid_temperature_increase_report

def create_sensor_change_summary(events_with_change_features):
    sensor_change_summary = events_with_change_features.groupby("sensor_id")["temperature_change"].agg(["min","max","mean"])
    sensor_change_summary = sensor_change_summary.rename(columns = {
        "min" : "min_temperature_change",
        "max" : "max_temperature_change",
        "mean": "mean_temperature_change"
    }).reset_index()
    return sensor_change_summary

def main():
    sensor_events = pd.DataFrame({
    "event_id": ["E001", "E002", "E003", "E004", "E005", "E006", "E007", "E008"],
    "sensor_id": ["S001", "S001", "S002", "S001", "S002", "S003", "S003", "S002"],
    "timestamp": [
        "2026-06-27 08:00",
        "2026-06-27 09:00",
        "2026-06-27 08:30",
        "2026-06-27 10:00",
        "2026-06-27 09:30",
        "2026-06-27 08:15",
        "2026-06-27 09:15",
        "2026-06-27 10:30"
    ],
    "temperature": [70.0, 76.0, 82.0, 90.0, 91.0, 65.0, 79.0, 96.0],
    "status": ["ok", "ok", "ok", "warning", "warning", "ok", "ok", "error"]
})
    
    events_with_datetime = parse_event_timestamps(sensor_events)
    sorted_sensor_log = create_sorted_sensor_log(events_with_datetime)
    events_with_change_features = add_temperature_change_features(sorted_sensor_log)
    first_event_report = create_first_event_report(events_with_change_features)
    change_threshold = 10
    rapid_temperature_increase_report = create_rapid_temperature_increase_report(events_with_change_features, change_threshold)
    sensor_change_summary = create_sensor_change_summary(events_with_change_features)
    print(sensor_change_summary) 
if __name__ == "__main__":
    main()  