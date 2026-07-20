import pandas as pd
import numpy as np


def parse_event_timestamps(sensor_events):
    events_with_datetime = sensor_events.assign(
        timestamp = pd.to_datetime(sensor_events["timestamp"])
    )
    return events_with_datetime

def create_sorted_sensor_log(events_with_datetime):
    sorted_sensor_log =  events_with_datetime.sort_values(["sensor_id","timestamp"])
    return sorted_sensor_log

def add_rolling_temperature_baseline(sorted_sensor_log, window_size):
    events_with_rolling_baseline = sorted_sensor_log.assign(
        rolling_mean_temperature = sorted_sensor_log.groupby("sensor_id")["temperature"].transform(
        lambda values: values.rolling(window_size, min_periods =1).mean()
    )
    )
    return events_with_rolling_baseline

def add_temperature_deviation(events_with_rolling_baseline):
    events_with_deviation = events_with_rolling_baseline.assign(
        temperature_deviation = (events_with_rolling_baseline["temperature"] - events_with_rolling_baseline ["rolling_mean_temperature"]).abs()
    )
    return events_with_deviation


def add_anomaly_severity(events_with_deviation, warning_deviation_threshold, critical_deviation_threshold):
    choices = ["critical", "warning"]
    conditions = [(events_with_deviation["temperature_deviation"] >= critical_deviation_threshold) | (events_with_deviation["status"] == "error"),
                  (events_with_deviation["temperature_deviation"] >= warning_deviation_threshold)]
    events_with_severity = events_with_deviation.assign(
        anomaly_severity = np.select(conditions, choices, default="normal")
    )
    return events_with_severity

def add_severity_flags(events_with_severity):
    events_with_severity_flags = events_with_severity.assign(
        is_critical = events_with_severity["anomaly_severity"] == "critical",
        is_warning = events_with_severity["anomaly_severity"] == "warning"
    )
    return events_with_severity_flags

def create_critical_event_report(events_with_severity_flags):
    critical_event_report = events_with_severity_flags[events_with_severity_flags["is_critical"]]
    critical_event_report = critical_event_report[["event_id","sensor_id","timestamp","temperature", "rolling_mean_temperature","temperature_deviation","status","anomaly_severity"]]
    return critical_event_report    

def create_sensor_severity_summary(events_with_severity_flags):
    sensor_severity_summary = events_with_severity_flags.groupby("sensor_id").agg(
    max_temperature_deviation=("temperature_deviation", "max"),
    mean_temperature_deviation =("temperature_deviation", "mean"),
    critical_count=("is_critical", "sum"),
    warning_count=("is_warning", "sum")
).reset_index()
    return sensor_severity_summary

def main():
    sensor_events = pd.DataFrame({
    "event_id": ["E001", "E002", "E003", "E004", "E005", "E006", "E007", "E008", "E009", "E010"],
    "sensor_id": ["S001", "S001", "S001", "S001", "S002", "S002", "S002", "S002", "S003", "S003"],
    "timestamp": [
        "2026-06-27 08:00",
        "2026-06-27 09:00",
        "2026-06-27 10:00",
        "2026-06-27 11:00",
        "2026-06-27 08:30",
        "2026-06-27 09:30",
        "2026-06-27 10:30",
        "2026-06-27 11:30",
        "2026-06-27 08:15",
        "2026-06-27 09:15"
    ],
    "temperature": [70.0, 72.0, 74.0, 95.0, 80.0, 82.0, 83.0, 105.0, 65.0, 92.0],
    "status": ["ok", "ok", "ok", "error", "ok", "ok", "warning", "error", "ok", "warning"]
})
    
    window_size = 3
    warning_deviation_threshold = 8
    critical_deviation_threshold = 15

    events_with_datetime = parse_event_timestamps(sensor_events)    
    sorted_sensor_log = create_sorted_sensor_log(events_with_datetime)
    events_with_rolling_baseline = add_rolling_temperature_baseline(sorted_sensor_log, window_size)
    events_with_deviation  = add_temperature_deviation(events_with_rolling_baseline)
    events_with_severity = add_anomaly_severity(events_with_deviation, warning_deviation_threshold, critical_deviation_threshold)
    events_with_severity_flags = add_severity_flags(events_with_severity)
    critical_event_report = create_critical_event_report(events_with_severity_flags)
    sensor_severity_summary = create_sensor_severity_summary(events_with_severity_flags)
    print(sensor_severity_summary)
    
if __name__ == "__main__":
    main()    