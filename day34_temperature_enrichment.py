import pandas as pd

def read_temperature_data(filename):
    df = pd.read_csv(filename)
    return df

def get_valid_condition(df):
    valid_status = ["ok","warning","error"]
    return (df["sensor_id"].notna() &
            df["area"].notna() &
            df["equipment"].notna() &
            df["temperature"].notna() &
            (df["temperature"] >= 0) &
            (df["temperature"] <= 120) &
            df["status"].isin(valid_status))
    
def get_valid_readings(df):
    valid_readings = df[get_valid_condition(df)]
    return valid_readings

def get_invalid_readings(df):
    invalid_readings = df[~get_valid_condition(df)]
    return invalid_readings

def create_enriched_readings(valid_readings, threshold):
    enriched_readings = valid_readings.assign(temperature_margin = valid_readings["temperature"] - threshold,
                                              is_high_temperature = valid_readings["temperature"] >= threshold)
    return enriched_readings

def classify_temperature(temperature, threshold):
    if temperature >= threshold + 5:
        return "critical"
    if temperature >= threshold:
        return "high"
    if temperature < threshold:
        return "normal"
    
def add_temperature_status(enriched_readings,threshold):
    result = enriched_readings.assign(
        temperature_status = enriched_readings["temperature"].apply(
            lambda temperature: classify_temperature(temperature, threshold)
        )
    )
    return result

def create_temperature_alerts (result):
    alerts = result[(result["temperature_status"] == "high") | (result["temperature_status"] == "critical")]
    return alerts

def create_temperature_status_report(result):
    temp_status_rp = result.groupby("temperature_status").size().reset_index(name="count")
    return temp_status_rp

def create_summary_report(df,valid_readings, invalid_readings, alerts):
    new_col = [{"metric":"Total rows", "count":len(df)},
               {"metric":"Valid rows", "count":len(valid_readings)},
               {"metric":"Invalid rows", "count":len(invalid_readings)},
               {"metric":"Alerts rows", "count":len(alerts)}
               ]
    
    summary = pd.DataFrame(new_col)
    return summary

def export_reports (valid_readings, invalid_readings, enriched_readings, result, alerts, temp_status_rp, summary ):
    valid_readings.to_csv("day34_valid_readings.csv",index= False)
    invalid_readings.to_csv("day34_invalid_readings.csv",index= False)
    enriched_readings.to_csv("day34_enriched_readings.csv", index = False)
    result.to_csv("day34_reading_with_status.csv", index = False)
    alerts.to_csv("day34_temperature_alerts.csv", index= False)
    temp_status_rp.to_csv("day34_temperature_status_report.csv", index= False)
    summary.to_csv("summary_report.csv",index=False)

    
def main():
    df = read_temperature_data("temperature_enrichment_dirty.csv")
    valid_readings = get_valid_readings(df)
    invalid_readings = get_invalid_readings(df)
    #print(valid_readings)
    threshold = 85
    enriched_readings = create_enriched_readings(valid_readings, threshold)
    #print(enriched_readings)
    result = add_temperature_status(enriched_readings, threshold)
    alerts = create_temperature_alerts(result)
    temp_status_rp = create_temperature_status_report(result)
    summary = create_summary_report(df, valid_readings, invalid_readings, alerts)
    export_reports(valid_readings, invalid_readings, enriched_readings, result, alerts, temp_status_rp, summary )

if __name__ == "__main__":
    main()