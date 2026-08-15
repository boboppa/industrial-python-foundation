import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


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


def split_train_test_sets(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size = 0.25,
        random_state = 42
    )
    return X_train, X_test, y_train, y_test

def create_train_test_summary (X_train, X_test, y_train, y_test):
    train_test_summary = pd.DataFrame([{
        "train_row_count" : X_train.shape[0],
        "test_row_count" : X_test.shape[0],
        "train_target_positive_count" : y_train.sum(),
        "test_target_positive_count" : y_test.sum(),
        "total_row_count" : X_train.shape[0] + X_test.shape[0]
    }])
    return train_test_summary

def validate_train_test_split(X, y, X_train, X_test, y_train, y_test): 
    validation_train_test_report = pd.DataFrame([{
        "same_total_row_count" : len(X_train) + len(X_test) == len(X),
        "train_feature_target_match" : len(X_train) == len(y_train),
        "test_feature_target_match" : len(X_test) == len(y_test),
        "no_target_in_train_features" : "target_critical" not in X_train.columns,
        "no_leak_column_in_train_features" : "is_critical" not in X_train.columns
    }])
    return validation_train_test_report

def train_classification_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def create_model_predictions(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred

def create_prediction_report(y_test, y_pred):
    prediction_report = pd.DataFrame({
        "actual_critical" : y_test.values,
        "predicted_critical" : y_pred
    }) 
    return prediction_report

def validate_prediction_output(y_test, y_pred):
    validate_pred_rp = pd.DataFrame([{
        "same_prediction_count" : len(y_test) == len(y_pred),   
        "prediction_values_valid" : ((y_pred == 0) | (y_pred == 1)).all()
    }])
    return validate_pred_rp


def calculate_model_accuracy(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

def create_accuracy_report(y_test, y_pred):
    accuracy_report = pd.DataFrame([{
        "correct_prediction_count" : (y_test.values == y_pred).sum(),
        "total_prediction_count" : len(y_test),
        "accuracy" : accuracy_score(y_test,y_pred)
    }])
    return accuracy_report

def add_prediction_correctness(prediction_report):
    prediction_correctness = prediction_report.assign(
        is_correct = prediction_report["actual_critical"] == prediction_report["predicted_critical"]
    )
    return prediction_correctness

def validate_accuracy_report(accuracy_report):
    accuracy_validation_report = pd.DataFrame([{
        "accuracy_in_valid_range" : 0 <= accuracy_report["accuracy"].iloc[0] <= 1,
        "has_correct_count" : "correct_prediction_count" in accuracy_report.columns,
        "has_total_count" : "total_prediction_count" in accuracy_report.columns
    }])
    return accuracy_validation_report

def create_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred, labels=[0,1])
    return cm

def create_confusion_matrix_report(cm, y_test, y_pred):
    confusion_matrix_report = pd.DataFrame([{
        "true_negative" : cm[0,0],
        "false_positive" : cm[0,1],
        "false_negative" : cm[1,0],
        "true_positive" : cm[1,1]
    }])
    return confusion_matrix_report

def add_prediction_error_type(prediction_report):
    prediction_report_with_error_type = prediction_report.assign(
        prediction_type =  
    )
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

    X_train, X_test, y_train, y_test = split_train_test_sets(X, y)
    print(X_train)
    print(X_test)
    print(y_train)
    print(y_test)

    train_test_summary = create_train_test_summary(X_train, X_test, y_train, y_test)
    print(train_test_summary)

    validation_train_test_report = validate_train_test_split(X, y, X_train, X_test, y_train, y_test)
    print(validation_train_test_report)
    
    
    
    model =train_classification_model(X_train, y_train)
    y_pred = create_model_predictions(model, X_test)
    prediction_report = create_prediction_report(y_test, y_pred)
    validate_pred_rp = validate_prediction_output(y_test, y_pred)
    print(prediction_report)
    print(validate_pred_rp)


    accuracy = calculate_model_accuracy(y_test, y_pred)
    print(accuracy)
    accuracy_report = create_accuracy_report(y_test, y_pred)
    print(accuracy_report)
    prediction_correctness = add_prediction_correctness(prediction_report)
    print(prediction_correctness)

    accuracy_validation_report = validate_accuracy_report(accuracy_report)
    print(accuracy_validation_report)

    cm = create_confusion_matrix(y_test, y_pred)
    print(cm)
    confusion_matrix_report = create_confusion_matrix_report(cm, y_test, y_pred)
    print(confusion_matrix_report)
if __name__ == "__main__":
    main() 