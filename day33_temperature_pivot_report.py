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
            df["status"].isin(valid_status)
            )
    
def get_valid_readings(df):
    valid_readings = df[get_valid_condition(df)]
    return valid_readings

def get_invalid_readings(df):
    invalid_readings = df[~get_valid_condition(df)]
    return invalid_readings
    
def create_area_equipment_temperature_matrix (valid_readings):
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


def create_matrix_alerts(sorted_matrix, threshold):
    matrix_alerts = sorted_matrix[sorted_matrix["total_mean_temp"] >= threshold]
    return matrix_alerts

def create_summary_report(df, valid_readings, invalid_readings):
    new_col = [{"metric":"Total rows", "count":len(df)},
               {"metric":"Valid rows", "count":len(valid_readings)},
               {"metric":"Invalid rows","count":len(invalid_readings)}]
    summary_report = pd.DataFrame(new_col)
    return summary_report

def export_reports (valid_readings, invalid_readings, temp_matrix, sorted_matrix, matrix_alerts, summary_report):
    valid_readings.to_csv("day33_valid_readings.csv", index = False)
    invalid_readings.to_csv("day33_invalid_readings.csv", index = False)
    temp_matrix.to_csv("day33_temperature_matrix.csv", index = False)
    sorted_matrix.to_csv("day33_sorted_temperature_matrix.csv", index = False)
    matrix_alerts.to_csv("day33_matrix_alerts.csv", index = False)
    summary_report.to_csv("day33_summary_report.csv", index = False)
    
    
def main():
    df = read_temperature_data("temperature_pivot_dirty.csv")
    valid_readings = get_valid_readings(df)
    invalid_readings = get_invalid_readings(df)
    #print(valid_readings)
    #print(invalid_readings)
    temp_matrix = create_area_equipment_temperature_matrix(valid_readings)
    sorted_matrix = create_sorted_temperature_matrix(temp_matrix)
    #print(temp_matrix)
    #print(sorted_matrix)
    threshold = 130
    matrix_alerts = create_matrix_alerts(sorted_matrix, threshold)
    #print(matrix_alerts)
    summary_report = create_summary_report(df, valid_readings, invalid_readings)
    #print(summary_report)
    export_reports(valid_readings, invalid_readings, temp_matrix, sorted_matrix, matrix_alerts, summary_report)
if __name__ == "__main__":
    main()
 