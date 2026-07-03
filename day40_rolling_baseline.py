import pandas as pd


def parse_event_timestamps(sensor_events):
    events_with_datetime = sensor_events.assign(
        timestamp = pd.to_datetime(sensor_events["timestamp"])
    )
    return events_with_datetime

def create_sorted_sensor_log(events_with_datetime):
    sorted_sensor_log = events_with_datetime.sort_values(["sensor_id","timestamp"])
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
        temperature_deviation =(events_with_rolling_baseline["temperature"] - events_with_rolling_baseline["rolling_mean_temperature"]).abs()
    )
    return events_with_deviation

def add_anomaly_flag(events_with_deviation, deviation_threshold):
    events_with_anomaly_flag = events_with_deviation.assign(
        is_temperature_anomaly  = events_with_deviation["temperature_deviation"] >= deviation_threshold
    )
    return events_with_anomaly_flag

def create_temperature_anomaly_report(events_with_anomaly_flag):
    temperature_anomaly_report = events_with_anomaly_flag[events_with_anomaly_flag["is_temperature_anomaly"]]
    temperature_anomaly_report = temperature_anomaly_report[["event_id","sensor_id","timestamp","temperature","rolling_mean_temperature","temperature_deviation","status"]]
    return temperature_anomaly_report

def create_sensor_deviation_summary(events_with_anomaly_flag):
    sensor_deviation_summary = events_with_anomaly_flag.groupby("sensor_id").agg(max_temperature_deviation=("temperature_deviation","max"),
        mean_temperature_deviation  = ("temperature_deviation","mean"),
        anomaly_count = ("is_temperature_anomaly","sum")
    ).reset_index()
    
    return sensor_deviation_summary
    
    
def main():
    sensor_events = pd.DataFrame({
        "event_id": ["E001", "E002", "E003", "E004", "E005", "E006", "E007", "E008", "E009"],
        "sensor_id": ["S001", "S001", "S001", "S001", "S002", "S002", "S002", "S002", "S003"],
        "timestamp": [
            "2026-06-27 08:00",
            "2026-06-27 09:00",
            "2026-06-27 10:00",
            "2026-06-27 11:00",
            "2026-06-27 08:30",
            "2026-06-27 09:30",
            "2026-06-27 10:30",
            "2026-06-27 11:30",
            "2026-06-27 08:15"
        ],
        "temperature": [70.0, 72.0, 74.0, 95.0, 80.0, 82.0, 83.0, 105.0, 65.0],
        "status": ["ok", "ok", "ok", "error", "ok", "ok", "warning", "error", "ok"]
    })
    
    events_with_datetime = parse_event_timestamps(sensor_events)
    sorted_sensor_log = create_sorted_sensor_log(events_with_datetime)
    window_size = 3
    events_with_rolling_baseline = add_rolling_temperature_baseline(sorted_sensor_log, window_size)
    events_with_deviation = add_temperature_deviation(events_with_rolling_baseline)
    deviation_threshold = 10
    events_with_anomaly_flag = add_anomaly_flag(events_with_deviation, deviation_threshold)
    temperature_anomaly_report = create_temperature_anomaly_report(events_with_anomaly_flag)
    sensor_deviation_summary = create_sensor_deviation_summary(events_with_anomaly_flag)
    print(sensor_deviation_summary)
    
if __name__ == "__main__":
    main() 