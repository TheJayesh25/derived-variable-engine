# 📊 Derived Variable Engine  
*A Config-Driven Composite & Index Builder for Analytics Workflows*

---

## 🔎 Overview

The **Derived Variable Engine** is a modular, configuration-driven transformation engine designed to build composite metrics, indices, and derived KPIs from structured datasets.

It supports:

- Multiple aggregation strategies (mean, sum, weighted mean, etc.)
- Special code handling
- Minimum valid response thresholds
- Optional governance validation (scale enforcement)
- Config-controlled fallback behavior
- Execution reporting with JSON audit logs

The architecture intentionally separates:

- **Computation logic**
- **Fallback logic**
- **Governance validation**
- **Configuration validation**

This keeps the system extensible, auditable, and production-friendly.

---

## 🧭 Navigation

- [Architecture](#-architecture)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Execution Flow](#-execution-flow)
- [Validation Layers Explained](#-validation-layers-explained)
- [Edge Case Testing](#-edge-case-testing)
- [Requirements](#-requirements)
- [License](#-license)

---

## 🏗 Architecture

```
Config (YAML)
      ↓
Config Validation (engine.py)
      ↓
Optional Governance Layer (validation.py)
      ↓
Aggregation Registry (aggregations.py)
      ↓
Fallback Registry (fallback.py)
      ↓
Output Dataset + JSON Report
```


Each layer has a clearly defined responsibility.

---

## 🚀 Features

### 📌 Aggregation Strategies

- `mean`
- `sum`
- `median`
- `min`
- `max`
- `std`
- `count_valid`
- `weighted_mean`

All aggregations are registry-based and easily extensible.

---

### 📌 Special Code Handling

Special values (e.g., `-98`, `-99`) are excluded from aggregation and handled via configurable fallback strategies.

---

### 📌 Fallback Strategies

- `nan_if_no_valid`
- `propagate_special`
- Configurable multi-special fallback values

---

### 📌 Minimum Valid Ratio

Control the proportion of valid responses required before computing a derived variable.

Example:

```yaml
min_valid_ratio: 0.5
```
---

### 📌 Optional Governance Layer

Enable strict scale validation:
```
enable_validation: true
```

Validation Checks:

- Numeric enforcement
- Scale bounds (scale_min, scale_max)
- Special code exclusion from scale validation

---

### 📌 Execution Reporting

Each run generates:

- Execution time
- Total rows processed
- Derived variables created
- Valid vs invalid row counts per variable
- JSON audit report

---

### 📂 Project Structure
```
derived-variable-engine/
│
├── src/
│   ├── main.py
│   ├── engine.py
│   ├── aggregations.py
│   ├── fallback.py
│   ├── validation.py
│
├── configs/
│   └── derived_config.yaml
│
├── data/
│   ├── sample_input.csv
│   ├── sample_input_edge_case.csv
│
├── outputs/
│   ├── derived_output.csv
│   ├── derived_output_edge_case.csv
│
├── logs/
│   └── derived_report.json
│
├── requirements.txt
├── README.md
└── License
```

---

### ⚙ Configuration

Configuration is YAML-driven.

Example:
```
enable_validation: true

derived_variables:
  - name: SATIS
    source_columns:
      - q100_1
      - q100_2
      - q100_3
      - q100_4
    aggregation: mean
    special_codes: [-98, -99]
    fallback_strategy: propagate_special
    multi_special_fallback: -98
    scale_min: 1
    scale_max: 5
    min_valid_ratio: 0.5
```

No code changes are required to:

- Add new derived variables
- Change aggregation strategy
- Modify fallback logic
- Adjust governance strictness

---

### 🔄 Execution Flow

1. Load dataset (CSV)
2. Load YAML configuration
3. Validate configuration structure
4. Optionally run governance validation
5. Apply aggregation registry
6. Apply fallback registry
7. Save derived dataset
8. Generate execution report

---

### 🛡 Validation Layers Explained
1️⃣ Configuration Validation (engine.py)

Ensures:
- No duplicate derived variables
- No overwriting existing columns
- Aggregation exists
- Source columns exist
- Weight lengths match (for weighted mean)

Stops execution if invalid.

---

### 2️⃣ Governance Validation (validation.py)

Triggered via config flag.

Ensures:
- Numeric data types
- Scale boundaries respected
- Special codes excluded from scale checks

Stops execution on scale violations.

---

### 3️⃣ Row-Level Eligibility Logic

Inside the engine:

- Counts valid responses
- Enforces min_valid_ratio
- Determines whether fallback applies

Does not stop execution — controls derived output behavior.


---

### 🧪 Edge Case Testing

Included:
- Fully valid rows
- All special code rows
- Mixed special code rows
- Threshold boundary rows
- Weighted mean edge cases
- Below-threshold cases
- Multi-special fallback cases

Edge case Test files:

- sample_input_edge_case.csv
- derived_output_edge_case.csv

---

### 📦 Requirements
```
pandas>=1.5
numpy>=1.23
PyYAML>=6.0
```

---

### 📜 License

MIT License

Copyright (c) 2026