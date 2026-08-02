import pandas as pd


def create_feature_matrix(ml_ready_table):
    X = ml_ready_table.drop(columns = ["target_critical","is_critical"])
    return X

def create_target_vector(ml_ready_table):
    y = ml_ready_table["target_critical"]
    return y

def create_feature_target_summary(X,y):
    feature_target_summary = pd.DataFrame([{
    "feature_row_count": X.shape[0],
    "feature_column_count": X.shape[1],
    "target_row_count": len(y),
    "positive_target_count": y.sum(),
    "negative_target_count": len(y) - y.sum()
    }])
    return feature_target_summary

def validate_feature_target_split(X, y):
    validation_report = pd.DataFrame([{
    "has_target_in_features": "target_critical" in X.columns,
    "has_leak_column" : "is_critical" in X.columns,
    "same_row_count": X.shape[0] == len(y)
    }])
    return validation_report

def main():
    ml_ready_table = pd.DataFrame({
    "temperature": [70.0, 78.0, 82.0, 96.0, 91.0, 65.0, 79.0, 105.0],
    "temperature_threshold": [95, 95, 90, 95, 90, 100, 100, 90],
    "rolling_mean_temperature": [70.0, 74.0, 82.0, 81.3, 86.5, 65.0, 72.0, 92.6],
    "temperature_deviation": [0.0, 4.0, 0.0, 14.7, 4.5, 0.0, 7.0, 12.4],
    "is_warning": [0, 0, 0, 0, 1, 0, 1, 0],
    "is_critical": [0, 0, 0, 1, 0, 0, 0, 1],
    "area_PM1": [1, 1, 0, 1, 0, 0, 0, 0],
    "area_PM2": [0, 0, 1, 0, 1, 0, 0, 1],
    "area_PM3": [0, 0, 0, 0, 0, 1, 1, 0],
    "equipment_Pump_A": [1, 1, 0, 1, 0, 0, 0, 0],
    "equipment_Motor_A": [0, 0, 1, 0, 1, 0, 0, 1],
    "equipment_Compressor_A": [0, 0, 0, 0, 0, 1, 1, 0],
    "criticality_high": [0, 0, 1, 0, 1, 0, 0, 1],
    "criticality_medium": [1, 1, 0, 1, 0, 0, 0, 0],
    "criticality_low": [0, 0, 0, 0, 0, 1, 1, 0],
    "target_critical": [0, 0, 0, 1, 0, 0, 0, 1]
})
    X = create_feature_matrix(ml_ready_table)
    #print(f"X is: {X.head()}")
    y = create_target_vector(ml_ready_table)
    #print(f"y is: {y}")
    feature_target_summary = create_feature_target_summary(X,y)
    print(f"summary: {feature_target_summary}")
    validation_report = validate_feature_target_split(X,y)
    print(validation_report)


if __name__ == "__main__":
    main() 