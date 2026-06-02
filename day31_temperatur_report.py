import pandas as pd

def read_temperature_data(filename):
    df = pd.read_csv(filename)
    return df

def get_valid_condition(df):
    valid_status = ["ok", "warning", "error"]
    return (df["sensor_id"].notna() 
           & df["area"].notna()
           & df["temperature"].notna()
           & (df["temperature"] >= 0)
           & (df["temperature"] <= 120)
           & df["status"].isin(valid_status))

  
def get_valid_temperatures(df):
    valid_temperatures = df[get_valid_condition(df)]
    return valid_temperatures

def get_invalid_temperatures(df):
    invalid_temperatures = df[~get_valid_condition(df)]
    return invalid_temperatures

def create_area_report(valid_temperatures):
    area_rp = valid_temperatures.groupby("area").size().reset_index(name= "count")
    return area_rp
    
def create_status_report(valid_temperatures):
    status_rp = valid_temperatures.groupby("status").size().reset_index(name= "count")
    return status_rp

def create_area_status_report(valid_temperatures):
    area_status_rp = valid_temperatures.groupby(["area","status"]).size().reset_index(name="count")
    return area_status_rp

def create_temperature_stats(valid_temperatures):
    new_col = [{"stats":"min","value":valid_temperatures["temperature"].min()},
                         {"stats":"max","value":valid_temperatures["temperature"].max()},
                         {"stats":"mean","value":valid_temperatures["temperature"].mean()}
    ]
    temperature_stats = pd.DataFrame(new_col)
    return temperature_stats

def create_summary_report(df, valid_temperatures, invalid_temperatures):
    new_col = [{"metric":"Total rows", "count" : len(df)},
           {"metric":"Valid rows", "count" : len(valid_temperatures)},
           {"metric":"Invalid rows", "count" : len(invalid_temperatures)}]
    summary_report = pd.DataFrame(new_col)
    return summary_report

def export_reports(valid_temperatures, invalid_temperatures, area_rp, status_rp, area_status_rp,temperature_stats, summary_report):
    valid_temperatures.to_csv("week4_valid_alarms.csv", index=False)
    invalid_temperatures.to_csv("week4_invalid_alarms.csv", index=False)
    area_rp.to_csv("area_report.csv", index=False)
    status_rp.to_csv("week4_priority_report.csv", index=False)
    area_status_rp.to_csv("week4_area_priority_report.csv", index=False)
    temperature_stats.to_csv("day30_temp_stats.csv", index = False)
    summary_report.to_csv("week4_summary_report.csv", index=False)

def main():
    df = read_temperature_data("temperature_readings_dirty.csv")
    
    valid_temperatures = get_valid_temperatures(df)
    invalid_temperatures = get_invalid_temperatures(df)
    
    area_rp = create_area_report(valid_temperatures)
    status_rp = create_status_report(valid_temperatures)
    area_status_rp = create_area_status_report(valid_temperatures)
    temperature_stats = create_temperature_stats(valid_temperatures)
    summary_report = create_summary_report(df, valid_temperatures, invalid_temperatures)
    export_reports(valid_temperatures, invalid_temperatures, area_rp, status_rp, area_status_rp,temperature_stats, summary_report) 
    print(summary_report)

if __name__ == "__main__":
    main()
    