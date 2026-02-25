import os
import json
import time
from datetime import datetime
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
    start_time = time.time()

    df = pd.read_csv(os.path.join(DATA_DIR, "sample_input.csv"))

    with open(os.path.join(PROJECT_ROOT, "configs", "derived_config.yaml")) as f:
        config = yaml.safe_load(f)

    df, reports = apply_derived_variables(df, config)

    # Save output
    output_path = os.path.join(OUTPUT_DIR, "derived_output.csv")
    df.to_csv(output_path, index=False)

    # Execution summary
    end_time = time.time()
    execution_time = round(end_time - start_time, 4)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "rows_processed": len(df),
        "derived_variables_created": len(config["derived_variables"]),
        "execution_time_seconds": execution_time,
        "details": reports
    }

    # Save report
    report_path = os.path.join(LOG_DIR, "derived_report.json")
    with open(report_path, "w") as f:
        json.dump(summary, f, indent=2)

    # Console summary
    print("\n=== Derived Variable Engine Summary ===")
    print(f"Rows processed: {len(df)}")
    print(f"Derived variables created: {len(config['derived_variables'])}")
    print(f"Execution time: {execution_time} seconds")
    print(f"Output saved to: {output_path}")
    print(f"Report saved to: {report_path}")
    print("========================================\n")


if __name__ == "__main__":
    run()
