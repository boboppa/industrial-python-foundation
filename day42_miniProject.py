import pandas as pd
import numpy as np

def parse_event_timepstamps(sensor_events):
    events_with_datetime = sensor_events.assign(
        timestamp = pd.to_datetime(sensor_events["timestamp"])
    )
    
    return events_with_datetime

def enrich_events_with_master(events_with_datetime, equipment_master):
    enriched_events = events_with_datetime.merge(equipment_master, how = "left", on = "sensor_id")
    return enriched_events

def create_unknown_sensor_report(enriched_events):
    unknown_sensor_report = enriched_events[enriched_events["area"].isna()]
    return unknown_sensor_report

def create_sorted_sensor_log(enriched_events):
    sorted_sensor_log = enriched_events.sort_values(["sensor_id","timestamp"])
    return sorted_sensor_log
def add_temperature_threshold(sorted_sensor_log, temperature_threshold_config):
    events_with_threshold = sorted_sensor_log.assign(
        temperature_threshold = sorted_sensor_log["criticality"].map(temperature_threshold_config)
    )
    return events_with_threshold

def add_dynamic_temperature_status(events_with_threshold):
    events_with_temperature_status = events_with_threshold.assign(
        is_high_temperature = events_with_threshold["temperature"] >= events_with_threshold["temperature_threshold"]
    )
    return events_with_temperature_status

def add_rolling_temperature_baseline(events_with_temperature_status, window_size):
    events_with_rolling_baseline = events_with_temperature_status.assign(
        rolling_mean_temperature = events_with_temperature_status.groupby("sensor_id")["temperature"].transform(
            lambda values: values.rolling(window_size, min_periods =1).mean()
        )       
    )
    return events_with_rolling_baseline

def add_temperature_deviation(events_with_rolling_baseline):
    events_with_deviation = events_with_rolling_baseline.assign(
        temperature_deviation = (events_with_rolling_baseline["temperature"] - events_with_rolling_baseline["rolling_mean_temperature"]).abs()
    )
    return events_with_deviation

def add_anomaly_severity(events_with_deviation, warning_deviation_threshold, critical_deviation_threshold):
    choices = ["critical", "warning"]
    conditions = [(events_with_deviation["temperature_deviation"] >= critical_deviation_threshold) | (events_with_deviation["status"] == "error") 
                  | (events_with_deviation["is_high_temperature"] == True), (events_with_deviation["status"]=="warning") | (events_with_deviation["temperature_deviation"] >= warning_deviation_threshold)]
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
    critical_event_report = events_with_severity_flags[events_with_severity_flags["is_critical"] == True]
    critical_event_report = critical_event_report[["event_id","sensor_id","area","equipment","criticality","timestamp","temperature","temperature_threshold","rolling_mean_temperature","temperature_deviation","status","anomaly_severity"]]
    return critical_event_report

def create_sensor_monitoring_summary(events_with_severity_flags): 
    sensor_monitoring_summary = events_with_severity_flags.groupby("sensor_id").agg(
        event_count = ("event_id", "count"),
        max_temperature = ("temperature", "max"),
        mean_temperature = ("temperature", "mean"),
        max_temperature_deviation=("temperature_deviation", "max"),
        mean_temperature_deviation =("temperature_deviation", "mean"),
        high_temperature_count = ("is_high_temperature","sum"),
        critical_count=("is_critical", "sum"),
        warning_count=("is_warning", "sum")
    ).reset_index()
    return sensor_monitoring_summary

def main():
    sensor_events = pd.DataFrame({
    "event_id": ["E001", "E002", "E003", "E004", "E005", "E006", "E007", "E008", "E009", "E010", "E011"],
    "sensor_id": ["S001", "S001", "S002", "S001", "S002", "S003", "S003", "S002", "S004", "S999", "S004"],
    "timestamp": [
        "2026-06-27 08:00",
        "2026-06-27 09:00",
        "2026-06-27 08:30",
        "2026-06-27 10:00",
        "2026-06-27 09:30",
        "2026-06-27 08:15",
        "2026-06-27 09:15",
        "2026-06-27 10:30",
        "2026-06-27 08:45",
        "2026-06-27 09:45",
        "2026-06-27 10:45"
    ],
    "temperature": [70.0, 78.0, 82.0, 96.0, 91.0, 65.0, 79.0, 105.0, 88.0, 80.0, 101.0],
    "status": ["ok", "ok", "ok", "error", "warning", "ok", "warning", "error", "ok", "ok", "error"]
})

    equipment_master = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004"],
    "area": ["PM1", "PM2", "PM3", "PM2"],
    "equipment": ["Pump_A", "Motor_A", "Compressor_A", "Pump_B"],
    "criticality": ["medium", "high", "low", "high"]
})

    temperature_threshold_config = {
    "high": 90,
    "medium": 95,
    "low": 100
}

    window_size = 3
    warning_deviation_threshold = 8
    critical_deviation_threshold = 15

    events_with_datetime = parse_event_timepstamps(sensor_events)
    enriched_events = enrich_events_with_master(events_with_datetime, equipment_master)
    unknown_sensor_report = create_unknown_sensor_report(enriched_events)
    sorted_sensor_log = create_sorted_sensor_log(enriched_events)
    events_with_threshold = add_temperature_threshold(sorted_sensor_log, temperature_threshold_config)
    events_with_temperature_status = add_dynamic_temperature_status(events_with_threshold)
    events_with_rolling_baseline = add_rolling_temperature_baseline(events_with_temperature_status, window_size)
    events_with_deviation = add_temperature_deviation(events_with_rolling_baseline)
    events_with_severity = add_anomaly_severity(events_with_deviation, warning_deviation_threshold, critical_deviation_threshold)
    events_with_severity_flags = add_severity_flags(events_with_severity)
    critical_event_report = create_critical_event_report(events_with_severity_flags)
    sensor_monitoring_summary = create_sensor_monitoring_summary(events_with_severity_flags)
    print(sensor_monitoring_summary)

if __name__ == "__main__":
    main()    