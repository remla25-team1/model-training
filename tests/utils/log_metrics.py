import json
import os

def log_metric(name, value, message=None, precision=3,  category=None, json_path="metrics.json"):
    if isinstance(value, float):
        value = round(value, precision)

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            metrics = json.load(f)
    else:
        metrics = {}

    metrics[name] = {
        "value": value,
        "message": message or "",
        "category": category
    }

    with open(json_path, "w") as f:
        json.dump(metrics, f, indent=2)
