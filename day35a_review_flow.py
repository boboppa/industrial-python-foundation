import pandas as pd

data = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004", "S005"],
    "area": ["PM1", "PM1", "PM2", "PM2", "PM3"],
    "equipment": ["Pump_A", "Pump_A", "Motor_A", "Motor_B", "Pump_C"],
    "temperature": [70.0, 88.0, 91.0, 60.0, 95.0],
    "status": ["ok", "ok", "warning", "ok", "error"]
})

def classify_temperature(temperature, threshold):
    if temperature >= threshold + 5 :
        return "critical"
    if temperature >= threshold:
        return "high"
    if temperature < threshold:
        return "normal"
    
def create_readings_with_status(valid_readings, threshold):
    readings_with_status = valid_readings.assign(
        temperature_margin=valid_readings["temperature"] - threshold,
        temperature_status=valid_readings["temperature"].apply(
            lambda temperature: classify_temperature(temperature, threshold)
        )
    )
    return readings_with_status

def create_temperature_alerts(readings_with_status):
    alerts = readings_with_status[readings_with_status["temperature_status"].isin(["high","critical"])]
    return alerts

def create_temperature_matrix (valid_readings):
    matrix = valid_readings.pivot_table(
        index = "area",
        columns = "equipment",
        values = "temperature",
        aggfunc = "mean",
        fill_value = 0
    )
    temp_matrix = matrix.reset_index()
    return temp_matrix
    
def create_sorted_temperature_matrix(temp_matrix):
    new_temp_matrix = temp_matrix.copy()
    new_temp_matrix["total_mean_temp"] = new_temp_matrix.drop(columns=["area"]).sum(axis=1)
    sorted_matrix = new_temp_matrix.sort_values("total_mean_temp", ascending = False)
    return sorted_matrix

def main():
    threshold = 85
    valid_readings = data
    readings_with_status = create_readings_with_status(valid_readings,threshold)
    alerts = create_temperature_alerts(readings_with_status)
    temp_matrix = create_temperature_matrix(valid_readings)
    sorted_matrix  = create_sorted_temperature_matrix(temp_matrix)
    print(alerts)
    print(sorted_matrix)
    
if __name__ == "__main__":
    main()