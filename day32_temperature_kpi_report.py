import pandas as pd

def read_temperature_data(filename):
    df = pd.read_csv(filename)
    return df

def get_valid_condition(df):
    valid_condition = ["ok", "warning", "error"]
    return (df["sensor_id"].notna() &
            df["area"].notna() &
            df["equipment"].notna() &
            df["temperature"].notna() &
            (df["temperature"] >= 0) &
            (df["temperature"] <= 120) &
            df["status"].isin(valid_condition)
    )
    
def get_valid_readings(df):
    valid_readings = df[get_valid_condition(df)]
    return valid_readings

def get_invalid_readings(df):
    invalid_readings = df[~get_valid_condition(df)]
    return invalid_readings

def create_area_temperature_kpi(valid_readings):
    area_temp_kpi = valid_readings.groupby("area")["temperature"].agg(["min","max","mean"]).reset_index()
    area_temp_kpi = area_temp_kpi.rename(columns= {
        "min": "min_temperature",
        "max" : "max_temperature",
        "mean" : "mean_temperature"
    })
    area_temp_kpi = area_temp_kpi.sort_values("max_temperature", ascending = False)
    return area_temp_kpi

def create_area_equipment_temperature_kpi(valid_readings):
    area_equipment_kpi = valid_readings.groupby(["area","equipment"])["temperature"].agg(["min","max","mean"]).reset_index()
    area_equipment_kpi = area_equipment_kpi.rename(columns={
        "min": "min_temperature",
        "max" : "max_temperature",
        "mean" : "mean_temperature"
    })
    area_equipment_kpi = area_equipment_kpi.sort_values("max_temperature", ascending = False)
    return area_equipment_kpi

def create_high_temperature_alerts(area_equipment_kpi, threshold):
    alert = area_equipment_kpi[area_equipment_kpi["max_temperature"] >= threshold].reset_index()
    high_temperature_alerts = alert[["area","equipment","max_temperature"]]
    return high_temperature_alerts
def create_status_report(valid_readings):
    status_report = valid_readings.groupby("status").size().reset_index(name="count")
    return status_report

def create_summary_report(df,valid_readings, invalid_radings):
    new_col = [{"metric": "Total rows", "count": len(df)},
                {"metric":"Valid_rows", "count" : len(valid_readings)},
                {"metric":"Invalid_rows","count" :  len(invalid_radings)}
                ]
    summary = pd.DataFrame(new_col)
    return summary
    
def export_reports(valid_readings, invalid_readings, area_temp_kpi, area_equipment_kpi, high_temperature_alerts, status_report, summary):
    valid_readings.to_csv("day32_valid_readings.csv", index = False)
    invalid_readings.to_csv("day32_invalid_readings.csv", index = False)
    area_temp_kpi.to_csv("day32_area_temperature_kpi.csv", index = False)
    area_equipment_kpi.to_csv("day32_area_equipment_temperature.csv",index = False)
    high_temperature_alerts.to_csv("day32_high_temperature_alerts.csv", index = False)
    status_report.to_csv("day32_status_report.csv", index = False)
    summary.to_csv("summary_report.csv", index = False)
    

def main():
    df = read_temperature_data("temperature_kpi_dirty.csv")
    valid_readings = get_valid_readings(df)
    invalid_readings = get_invalid_readings(df)
    print(valid_readings)
    #print(invalid_readings)
    area_temp_kpi = create_area_temperature_kpi(valid_readings)
    #print(area_temp_kpi)
    area_equipment_kpi = create_area_equipment_temperature_kpi(valid_readings)
    #print(area_equipment_kpi)
    threshold = 85
    high_temperature_alerts = create_high_temperature_alerts(area_equipment_kpi, threshold)
    print(high_temperature_alerts)
    status_report = create_status_report(valid_readings)
    #print(status_report)
    summary = create_summary_report(df, valid_readings, invalid_readings)
    print(summary)
    export_reports(valid_readings, invalid_readings, area_temp_kpi, area_equipment_kpi, high_temperature_alerts, status_report, summary )


if __name__ == "__main__":
    main()
    