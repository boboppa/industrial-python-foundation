import pandas as pd

def read_alarm_data(filename):
    df = pd.read_csv(filename)
    return df

def get_valid_alarms(df):
    valid_status = ["active", "cleared"]
    valid_priority =  ["high","medium","low"]
    valid_condition = (
        df["tag"].notna() & 
        df["area"].notna() &
        df["status"].isin(valid_status) &
        df["priority"].isin(valid_priority)
    )
    
    return df[valid_condition] 
    
def get_invalid_alarms(df):
    valid_status = ["active", "cleared"]
    valid_priority =  ["high","medium","low"]
    valid_condition = (
        df["tag"].notna() & 
        df["area"].notna() &
        df["status"].isin(valid_status) &
        df["priority"].isin(valid_priority)
    )
    
    return df[~valid_condition] 

def create_area_report(valid_alarms):
    area_rp = valid_alarms.groupby("area").size().reset_index(name="count")
    return area_rp

def create_priority_report(valid_alarms):
    priority_rp = valid_alarms.groupby("priority").size().reset_index(name="count")
    return priority_rp

def create_active_area_report(valid_alarms):
    active_area_rp = valid_alarms[valid_alarms["status"]=="active"].groupby("area").size().reset_index(name="count")
    return active_area_rp

def create_area_priority_report(valid_alarms):
    area_prio_rp = valid_alarms.groupby(["area","priority"]).size().reset_index(name="count")
    return area_prio_rp

def create_summary_report(df, valid_alarms, invalid_alarms):
    new_col = [{"metric":"Total rows", "count" : len(df)},
           {"metric":"Valid rows", "count" : len(valid_alarms)},
           {"metric":"Invalid rows", "count" : len(invalid_alarms)}]
    summary = pd.DataFrame(new_col)
    return summary
    
def export_reports(df,valid_alarms, invalid_alarms):
    get_valid_alarms(df).to_csv("week4_valid_alarms.csv",index = False)
    get_invalid_alarms(df).to_csv("week4_invalid_alarms.csv", index = False)
    create_area_report(valid_alarms).to_csv("week4_area_report.csv", index = False)
    create_priority_report(valid_alarms).to_csv("week4_priority_report.csv",index = False)
    create_active_area_report(valid_alarms).to_csv("week4_active_area_report.csv", index = False)
    create_area_priority_report(valid_alarms).to_csv("week4_area_priority_report.csv", index = False)
    create_summary_report(df,valid_alarms,invalid_alarms).to_csv("week4_summary_report.csv", index = False)
    
def main():
    df = read_alarm_data("alarms_week4_dirty.csv")

    valid_alarms = get_valid_alarms(df)
    invalid_alarms = get_invalid_alarms(df)

    #area_report = create_area_report(valid_alarms)
    #priority_report = create_priority_report(valid_alarms)
    #active_area_report = create_active_area_report(valid_alarms)
    #area_priority_report = create_area_priority_report(valid_alarms)
    summary_report = create_summary_report(df, valid_alarms, invalid_alarms)

    export_reports(
        df,
        valid_alarms,
        invalid_alarms
    )

    print(summary_report)
    print("Mini project completed")


if __name__ == "__main__":
    main()
    