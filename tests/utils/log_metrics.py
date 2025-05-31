def log_metric(name, value, message=None, precision=3, category=None, json_path="metrics.json"):
    import json
    import os

    if isinstance(value, float):
        value = round(value, precision)
    elif isinstance(value, bool):
        value = "True" if value else "False"

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                metrics = json.load(f)
            except json.JSONDecodeError:
                metrics = {}
    else:
        metrics = {}

    metrics[name] = {
        "value": value,
        "message": message or "",
        "category": category
    }

    with open(json_path, "w") as f:
        json.dump(metrics, f, indent=2)
