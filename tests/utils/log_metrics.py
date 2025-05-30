def log_metric(name, value, message=None, precision=3, category=None, json_path="metrics.json"):
    import os, json
    from pathlib import Path

    json_path = os.path.abspath(json_path)

    if isinstance(value, float):
        value = round(value, precision)
    elif isinstance(value, bool):
        value = str(value).lower()  

    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
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
