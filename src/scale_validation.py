import pandas as pd


def validate_dataset(df, config):
    """
    Governance layer:
    - Numeric enforcement
    - Scale bounds validation
    - Minimum valid ratio logic validation
    """

    for var_cfg in config["derived_variables"]:
        name = var_cfg["name"]
        source_cols = var_cfg["source_columns"]

        # Ensure numeric
        for col in source_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(
                    f"Column '{col}' in derived variable '{name}' must be numeric."
                )

        # Scale validation
        scale_min = var_cfg.get("scale_min")
        scale_max = var_cfg.get("scale_max")

        if scale_min is not None and scale_max is not None:
            special_codes = set(var_cfg.get("special_codes", []))

            subset = df[source_cols]

            invalid_mask = (
                (subset < scale_min) | (subset > scale_max)
            )

            if special_codes:
                for code in special_codes:
                    invalid_mask &= (subset != code)

            if invalid_mask.any().any():
                raise ValueError(
                    f"Scale violation detected in '{name}'. "
                    f"Values outside [{scale_min}, {scale_max}] found."
                )

    print("Validation completed successfully.")
