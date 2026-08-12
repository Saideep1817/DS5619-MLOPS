"""
The "after" version — YOUR file to complete.

Fill in the three functions marked with # TODO. Everything else (CLI wiring,
imports) is already done for you. Do not hardcode any path, format string, or
threshold value anywhere in this file — if you find yourself typing a literal
number or file path outside of a default/example, it belongs in the config
file instead.

Run with:
    python src/pipeline.py --config config/pipeline.yaml
"""
import argparse
import csv
import json

import yaml

REQUIRED_KEYS = ["input_path", "input_format", "high_value_threshold", "output_path"]


def load_config(path):
    """Load a YAML config file and validate required keys are present.

    Must raise ValueError naming the specific missing key if REQUIRED_KEYS
    are not all present. Do not let this fail with a bare KeyError later.
    """
    with open(path,'r') as file :
        data = yaml.safe_load(file)
        for key in REQUIRED_KEYS :
            if key not in data :
                raise ValueError(f"{key} not present in the yaml file")
    return data
    raise NotImplementedError("load_config is not implemented yet")


def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    if fmt not in ("csv","json") :
        raise ValueError(f"Unsupported format:{fmt}")
    with open(path,'r') as file :
        if fmt == "csv":
            reader = csv.DictReader(file)
            data = list(reader)
        elif fmt == "json" :
            data = json.load(file)
    if not isinstance(data,list) :
        raise ValueError("Data is not a list")
    for i in data :
        if not isinstance(i,dict) :
            raise ValueError("Data is not a list of dict")
        if "amount" not in i or "is_fraud" not in i :
            raise ValueError("Data is not a list of dict with amount and is_fraud")
    filtered_data = [{'amount':tx['amount'] , 'is_fraud' : tx['is_fraud']} for tx in data]
    return filtered_data
    raise NotImplementedError("load_transactions is not implemented yet")


def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    data = load_transactions(config['input_path'],config['input_format'])
    n = len(data)
    total_amount = sum(float(r["amount"]) for r in data)
    n_fraud = sum(1 for r in data if str(r["is_fraud"]).lower() == "true")
    n_high_value = sum(1 for r in data if float(r["amount"]) > config['high_value_threshold'])
    report = {
        "n_transactions": n,
        "total_amount": round(total_amount, 2),
        "fraud_rate": round(n_fraud / n, 4) if n else 0.0,
        "n_high_value": n_high_value,
        "high_value_threshold": config['high_value_threshold'],
    }
    with open(config['output_path'], "w") as f:
        json.dump(report, f, indent=2)
    return report
    raise NotImplementedError("run_pipeline is not implemented yet")


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
