import os
import json
import pandas as pd
import yaml
from engine import apply_derived_variables


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def run():
    df = pd.read_csv(os.path.join(DATA_DIR, "sample_input.csv"))

    with open(os.path.join(PROJECT_ROOT, "configs", "derived_config.yaml")) as f:
        config = yaml.safe_load(f)

    df, reports = apply_derived_variables(df, config)

    df.to_csv(os.path.join(OUTPUT_DIR, "derived_output.csv"), index=False)

    with open(os.path.join(LOG_DIR, "derived_report.json"), "w") as f:
        json.dump(reports, f, indent=2)

    print("Derived variables created successfully.")


if __name__ == "__main__":
    run()
