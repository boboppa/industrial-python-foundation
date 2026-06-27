import pandas as pd

def enrich_readings_with_master(sensor_readings, equipment_master):
    enriched_readings = pd.merge(
        sensor_readings,
        equipment_master,
        on="sensor_id",
        how="left"
    )
    return enriched_readings

def create_unknown_sensor_report(enriched_readings):
    unknown_sensor_report = enriched_readings[enriched_readings["area"].isna()]
    return unknown_sensor_report            

def add_temperature_status(enriched_readings, threshold):
    readings_with_temperature_status = enriched_readings.assign(
        is_high_temperature = enriched_readings["temperature"] >= threshold

    )
    return readings_with_temperature_status
    
def create_high_temperature_report(readings_with_temperature_status):
    high_temperature_report = readings_with_temperature_status[readings_with_temperature_status["is_high_temperature"] == True]
    high_temperature_report = high_temperature_report[["sensor_id", "area", "equipment", "criticality", "temperature", "status"]]
    return high_temperature_report

def create_area_temperature_report(readings_with_temperature_status):
    area_temperature_report = readings_with_temperature_status.groupby("area")["temperature"].agg(["min", "max","mean"])
    area_temperature_report = area_temperature_report.rename(columns= {
        "min": "min_temperature",
        "max" : "max_temperature",
        "mean" : "mean_temperature"
    }).reset_index()  
    return area_temperature_report 

def main():
    sensor_readings = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004", "S005", "S999"],
    "temperature": [72.0, 88.5, 91.0, 65.0, 96.0, 80.0],
    "status": ["ok", "ok", "warning", "ok", "error", "ok"]
})
    equipment_master = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004", "S005"],
    "area": ["PM1", "PM1", "PM2", "PM2", "PM3"],
    "equipment": ["Pump_A", "Pump_A", "Motor_A", "Pump_B", "Motor_C"],
    "criticality": ["medium", "high", "high", "low", "high"]
})
    threshold = 85
    enriched_readings = enrich_readings_with_master(sensor_readings, equipment_master)
    unknown_sensor_report = create_unknown_sensor_report(enriched_readings)
    readings_with_temperature_status = add_temperature_status(enriched_readings, threshold)
    high_temperature_report = create_high_temperature_report(readings_with_temperature_status)
    area_temperature_report = create_area_temperature_report(readings_with_temperature_status)
    print(area_temperature_report)
    
if __name__ == "__main__":
    main()  