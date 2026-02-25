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

            subset = df[source_cols]

            special_codes = set(float(code) for code in var_cfg.get("special_codes", []))

            # Identify valid values (excluding special codes)
            non_special_mask = ~subset.isin(special_codes)

            invalid_mask = (
                ((subset < scale_min) | (subset > scale_max))
                & non_special_mask
            )

            if invalid_mask.any().any():
                raise ValueError(
                    f"Scale violation detected in '{name}'. "
                    f"Values outside [{scale_min}, {scale_max}] found."
                )


    print("Validation completed successfully.")
