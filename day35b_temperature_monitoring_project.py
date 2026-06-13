import pandas as pd

def read_temperature_data(filename):
    df = pd.read_csv(filename)
    return df

def get_valid_condition(df):
    valid_status = ["ok", "warning", "error"]
    return (df["sensor_id"].notna() &
            df["area"].notna() &
            df["equipment"].notna() &
            df["temperature"].notna() &
            (df["temperature"] >= 0) &
            (df["temperature"] <= 120) &
            df["status"].isin(valid_status))
    
def get_valid_readings(df):
    valid_readings =  df[get_valid_condition(df)]
    return valid_readings
def get_invalid_readings(df):
    invalid_readings = df[~ get_valid_condition(df)]
    return invalid_readings

def create_enriched_readings(valid_readings, threshold):
    enriched_readings = valid_readings.assign(
        temperature_margin = valid_readings["temperature"] - threshold,
        is_high_temperature = valid_readings["temperature"] >=threshold
    )
    return enriched_readings

def classify_temperature(temperature, threshold):
    if temperature >= threshold + 5:
        return "critical"
    if temperature >= threshold:
        return "high"
    if temperature < threshold:
        return "normal"
     
def add_temperature_status (enriched_readings, threshold):
    
    readings_with_status = enriched_readings.assign(
    temperature_status = enriched_readings["temperature"].apply(
        lambda temperature: classify_temperature(temperature, threshold)
    ))
    return readings_with_status

def create_temperature_alerts(reading_with_status):
    alerts = reading_with_status[reading_with_status["temperature_status"].isin(["high","critical"])]
    return alerts

def create_temperature_status_report(readings_with_status):
    temperature_status_report = readings_with_status.groupby("temperature_status").size().reset_index(name="count")
    return temperature_status_report

def create_temperature_matrix(readings_with_status):
    temp_matrix = readings_with_status.pivot_table(
        index = "area",
        columns = "equipment",
        values = "temperature",
        aggfunc = "mean",
        fill_value = 0,
    ).reset_index()
    
    return temp_matrix

def create_sorted_temperature_matrix(temp_matrix):
    new_temp_matrix = temp_matrix.copy()
    new_temp_matrix["total_mean_temp"] = new_temp_matrix.drop(columns=["area"]).sum(axis=1)
    sorted_matrix = new_temp_matrix.sort_values("total_mean_temp", ascending=False)
    return sorted_matrix

def create_summary_report(df, valid_readings, invalid_readings, alerts):
    new_col = [{"metric":"Total rows","count":len(df)},
               {"metric":"Valid rows","count":len(valid_readings)},
               {"metric":"Invalid rows","count":len(invalid_readings)},
               {"metric":"Alerts rows","count":len(alerts)}
               ]
    summary = pd.DataFrame(new_col)
    return summary

def export_reports(valid_readings, invalid_readings, enriched_readings, readings_with_status, alerts, temperature_status_report, temp_matrix, sorted_matrix,summary):
    valid_readings.to_csv("day35b_valid_readings.csv",index = False)
    invalid_readings.to_csv("day35b_invalid_readings.csv",index = False)
    enriched_readings.to_csv("day35b_enriched_readings.csv",index = False)
    readings_with_status.to_csv("day35b_readings_with_status.csv",index = False)
    alerts.to_csv("day35b_temperature_alerts.csv",index = False)
    temperature_status_report.to_csv("day35b_temperature_status_report.csv",index = False)
    temp_matrix.to_csv("day35b_temperature_matrix.csv",index = False)
    sorted_matrix.to_csv("day35b_sorted_temperature_matrix.csv",index = False)
    summary.to_csv("day35b_summary_report.csv",index = False)
    
def main():
    df = read_temperature_data("temperature_monitoring_dirty.csv")
    valid_readings = get_valid_readings(df)
    invalid_readings = get_invalid_readings(df)
    threshold = 85
    enriched_readings = create_enriched_readings(valid_readings,threshold)
    readings_with_status = add_temperature_status(enriched_readings, threshold)
    alerts = create_temperature_alerts(readings_with_status)
    temperature_status_report = create_temperature_status_report(readings_with_status)
    temp_matrix = create_temperature_matrix(readings_with_status)
    sorted_matrix = create_sorted_temperature_matrix(temp_matrix)
    summary = create_summary_report(df,valid_readings, invalid_readings,alerts)
    export_reports(valid_readings, invalid_readings, enriched_readings, readings_with_status, alerts, temperature_status_report, temp_matrix, sorted_matrix,summary)
    print(sorted_matrix)
    print(temp_matrix)
if __name__ == "__main__":
    main()
    
