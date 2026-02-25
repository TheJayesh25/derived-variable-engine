import pandas as pd
import numpy as np
from aggregations import AGGREGATION_REGISTRY
from fallback import FALLBACK_REGISTRY


def apply_derived_variables(df, config):
    reports = []

    for var_cfg in config["derived_variables"]:
        name = var_cfg["name"]
        source_cols = var_cfg["source_columns"]
        aggregation = var_cfg["aggregation"]
        special_codes = set(var_cfg.get("special_codes", []))
        fallback_strategy = var_cfg.get("fallback_strategy", "nan_if_no_valid")

        # Validate
        missing = [c for c in source_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing source columns for {name}: {missing}")

        original_subset = df[source_cols].copy()

        # Replace special codes with NaN for aggregation
        working_df = original_subset.replace(list(special_codes), np.nan)

        # Determine valid rows
        valid_mask = working_df.notna().any(axis=1)

        # Aggregate
        agg_func = AGGREGATION_REGISTRY.get(aggregation)
        if not agg_func:
            raise ValueError(f"Unsupported aggregation: {aggregation}")

        if aggregation == "weighted_mean":
            weights = var_cfg.get("weights")
            if not weights:
                raise ValueError(f"Weights required for weighted_mean in {name}")
            result = agg_func(working_df, weights=weights)
        else:
            result = agg_func(working_df)


        # Apply fallback
        fallback_func = FALLBACK_REGISTRY.get(fallback_strategy)
        if fallback_func:
            result = fallback_func(result, valid_mask, original_subset, special_codes, var_cfg)

        df[name] = result

        # Reporting
        reports.append({
            "derived_variable": name,
            "aggregation": aggregation,
            "rows_total": len(df),
            "rows_with_valid": int(valid_mask.sum()),
            "rows_without_valid": int((~valid_mask).sum())
        })

    return df, reports
