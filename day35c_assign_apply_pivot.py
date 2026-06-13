import pandas as pd

valid_readings = pd.DataFrame({
    "sensor_id": ["S001", "S002", "S003", "S004", "S005", "S006"],
    "area": ["PM1", "PM1", "PM2", "PM2", "PM3", "PM3"],
    "equipment": ["Pump_A", "Pump_A", "Motor_A", "Pump_B", "Pump_C", "Motor_C"],
    "temperature": [70.0, 88.0, 91.0, 60.0, 95.0, 82.0],
    "status": ["ok", "ok", "warning", "ok", "error", "ok"]
})

def add_temperature_margin(valid_readings, threshold):
    temp_margin = valid_readings.assign(
        temperature_margin = valid_readings["temperature"] - threshold
        )
    return temp_margin

def classify_temp(temperature, threshold):
    if temperature >= threshold + 5:
        return "critical"
    if temperature >= threshold:
        return "high"
    if temperature < threshold:
        return "normal"
    
def add_temperature_status(temp_margin, threshold):
    temp_status = temp_margin.assign(
        temperature_status = temp_margin["temperature"].apply(
        lambda temperature : classify_temp(temperature, threshold)
    ))
    
    return temp_status

def create_temperature_alerts(temp_status):
    alerts = temp_status[temp_status["temperature_status"].isin(["high", "critical"])]
    return alerts
    
def create_temperature_matrix(temp_status):
    matrix = temp_status.pivot_table(
        index = "area",
        columns = "equipment",
        values = "temperature",
        aggfunc = "mean",
        fill_value = 0,
    ).reset_index()
    return matrix
    
def main():
    threshold = 85
    temp_margin = add_temperature_margin(valid_readings, threshold)
    temp_status = add_temperature_status(temp_margin, threshold)
    alerts = create_temperature_alerts(temp_status)
    matrix = create_temperature_matrix(temp_status)
    print(matrix)
    
if __name__ == "__main__":
    main()