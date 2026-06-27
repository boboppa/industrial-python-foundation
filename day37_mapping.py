import pandas as pd


def enrich_readings_with_master(sensor_readings, equipment_master):
    enriched_readings =  pd.merge(
        sensor_readings,
        equipment_master,
        on="sensor_id",
        how = "left"
    )
    return enriched_readings

def add_temperature_threshold(enriched_readings, threshold_config):
    readings_with_threshold = enriched_readings.assign(
        temperature_threshold = enriched_readings["criticality"].map(threshold_config)
    )
    return readings_with_threshold

def create_missing_threshold_report(readings_with_threshold):
    missing_threshold_config = readings_with_threshold[readings_with_threshold["temperature_threshold"].isna()]
    missing_threshold_config = missing_threshold_config[["sensor_id","area","equipment","criticality","temperature","temperature_threshold"]]
    return missing_threshold_config


def add_dynamic_temperature_status(readings_with_threshold):
    
    readings_with_dynamic_status = readings_with_threshold.assign(
        is_high_temperature = readings_with_threshold["temperature"] >= readings_with_threshold["temperature_threshold"]
    )
    return readings_with_dynamic_status

def create_dynamic_high_temperature_report(readings_with_dynamic_status):
    dynamic_high_temperature_report = readings_with_dynamic_status[readings_with_dynamic_status["is_high_temperature"]]
    dynamic_high_temperature_report = dynamic_high_temperature_report[["sensor_id","area","equipment","criticality","temperature","temperature_threshold","status"]]
    return dynamic_high_temperature_report

def create_area_temperature_report(readings_with_dynamic_status):
    area_temperatur_report = readings_with_dynamic_status.groupby("area")["temperature"].agg(["min","max","mean"])
    area_temperatur_report = area_temperatur_report.rename(columns= {
        "min": "min_temperature",
        "max" : "max_temperature",
        "mean" : "mean_temperature"
    }).reset_index()
    return area_temperatur_report



def main():
    sensor_readings = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004", "S005", "S006", "S999"],
    "temperature": [72.0, 88.5, 91.0, 65.0, 96.0, 84.0, 80.0],
    "status": ["ok", "ok", "warning", "ok", "error", "warning", "ok"]
})
    equipment_master = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004", "S005", "S006"],
    "area": ["PM1", "PM1", "PM2", "PM2", "PM3", "PM3"],
    "equipment": ["Pump_A", "Pump_A", "Motor_A", "Pump_B", "Motor_C", "Compressor_A"],
    "criticality": ["medium", "high", "high", "low", "high", "very_high"]
})
    threshold_config = {
    "high": 85,
    "medium": 90,
    "low": 95
}
    
    enriched_readings = enrich_readings_with_master(sensor_readings, equipment_master)
    readings_with_threshold = add_temperature_threshold(enriched_readings, threshold_config)
    missing_threshold_config = create_missing_threshold_report(readings_with_threshold)
    readings_with_dynamic_status = add_dynamic_temperature_status(readings_with_threshold)
    dynamic_high_temperature_report = create_dynamic_high_temperature_report(readings_with_dynamic_status)
    area_temperature_report = create_area_temperature_report(readings_with_dynamic_status)
    print(dynamic_high_temperature_report)
    
if __name__ == "__main__":
    main()  