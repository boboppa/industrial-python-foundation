import pandas as pd
import numpy as np
def classify_metric(metric_value): 
    if metric_value >= 0.8:
        return "high"
    elif metric_value >= 0.5:
        return "medium"
    else:
        return "low"

def create_metric_status_report(model_report):
    status_report = pd.DataFrame([{
        "accuracy_status" : classify_metric(model_report["accuracy"].iloc[0]),
        "precision_status": classify_metric(model_report["precision"].iloc[0]),
        "recall_status": classify_metric(model_report["recall"].iloc[0]),
        "f1_status": classify_metric(model_report["f1_score"].iloc[0])
    }])
    return status_report

def has_serious_model_risk(model_report):
    if (model_report["false_negative"].iloc[0] > 0) | (model_report["recall"].iloc[0] < 0.5):
        return True
    else:
        return False
    
def validate_metric_columns(model_report):
    columns_names = ["accuracy","precision","recall","f1_score"]
    check_errors = all([name in model_report.columns for name in columns_names])
    return check_errors

def has_any_error_count(model_report):
    check_error = (model_report[["false_negative","false_positive"]] > 0).any().any()
    
    return check_error
    
def create_error_summary(model_report):
    summary = pd.DataFrame([{
        "total_errors" : model_report["false_positive"].iloc[0] + model_report["false_negative"].iloc[0],
        "has_errors" :  (model_report["false_positive"].iloc[0] + model_report["false_negative"].iloc[0]) > 0
    }])
    return summary

def find_low_metrics_with_loop(model_report):
    metric_names = ["accuracy", "precision", "recall", "f1_score"]
    low_metrics = []
    for name in metric_names:
        if model_report[name].iloc[0] < 0.6:
            low_metrics.append(name)
    return low_metrics

def find_existing_colums(model_report):
    requested_columns = [
        "accuracy",
        "recall",
        "roc_auc",
        "false_negative"
    ]
    
    exist_list = [col for col in requested_columns if col in model_report.columns]
    return exist_list

def check_metrics_above_minimum(model_report):
    check = model_report[["accuracy","precision","recall","f1_score"]] >= 0.5
    check = check.all().all()
    return check
    
def main():
    model_report = pd.DataFrame([{
        "accuracy": 0.91,
        "precision": 0.76,
        "recall": 0.48,
        "f1_score": 0.59,
        "false_positive": 3,
        "false_negative": 4
    }])
    
    status_report = create_metric_status_report(model_report)
    #print(status_report)
    print(check_metrics_above_minimum(model_report))
    
    
if __name__ == "__main__":
    main() 