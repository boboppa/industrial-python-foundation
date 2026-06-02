import pandas as pd


def read_sensor_data(filename):
    df = pd.read_csv(filename)
    return df

def get_valid_condition(df):
    valid_status = ["ok","warning","error"]
    
    return (df["sensor_id"].notna() &
            df["area"].notna() &
            df["value"].notna() &
            df["unit"].notna() &
            df["status"].isin(valid_status))
    
def get_valid_sensors(df):
    valid_condition = get_valid_condition(df)
    valid_sensors = df[valid_condition]
    return valid_sensors

def get_invalid_sensors(df):
    valid_condition = get_valid_condition(df)
    invalid_sensors = df[~valid_condition]
    return invalid_sensors

def create_area_report(valid_sensors):
    area_report = valid_sensors.groupby("area").size().reset_index(name="count")
    return area_report

def create_status_report(valid_sensors):
    status_report = valid_sensors.groupby("status").size().reset_index(name="count")
    return status_report

def create_area_status_report(valid_sensors):
    area_status_report = valid_sensors.groupby(["area","status"]).size().reset_index(name="count")
    return area_status_report

def create_summary_report(df, valid_sensors, invalid_sensors):
    new_col = [{"metric":"Total rows", "count" : len(df)},
           {"metric":"Valid rows", "count" : len(valid_sensors)},
           {"metric":"Invalid rows", "count" : len(invalid_sensors)}]
    summary_report = pd.DataFrame(new_col)
    return summary_report

def export_reports(valid_sensors, invalid_sensors, area_report, status_report, area_status_report, summary_report):
    valid_sensors.to_csv("week4_valid_alarms.csv", index=False)
    invalid_sensors.to_csv("week4_invalid_alarms.csv", index=False)
    area_report.to_csv("area_report.csv", index=False)
    status_report.to_csv("week4_priority_report.csv", index=False)
    area_status_report.to_csv("week4_area_priority_report.csv", index=False)
    summary_report.to_csv("week4_summary_report.csv", index=False)
        
        
def main():
    df = read_sensor_data("sensor_readings_dirty.csv")
    
    valid_sensors = get_valid_sensors(df)
    invalid_sensors = get_invalid_sensors(df)
    area_report = create_area_report(valid_sensors)
    status_report = create_status_report(valid_sensors)
    area_status_report = create_area_status_report(valid_sensors)
    summary_report = create_summary_report (df,valid_sensors, invalid_sensors)
    export_reports(valid_sensors, invalid_sensors, area_report, status_report, area_status_report, summary_report)
    print(summary_report)
    
if __name__ == "__main__":
    main()