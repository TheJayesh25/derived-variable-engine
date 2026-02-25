import numpy as np

def nan_if_no_valid(result_series, valid_mask, original_df, special_codes, config):
    # If no valid values exist → NaN
    result_series[~valid_mask] = np.nan
    return result_series


def propagate_special(result_series, valid_mask, original_df, special_codes, config):
    multi_special_fallback = config.get("multi_special_fallback", -98)

    for idx in result_series.index[~valid_mask]:
        row_vals = original_df.loc[idx].values
        specials = [v for v in row_vals if v in special_codes]

        if len(set(specials)) == 1:
            result_series.loc[idx] = specials[0]
        elif len(specials) > 1:
            result_series.loc[idx] = multi_special_fallback
        else:
            result_series.loc[idx] = np.nan

    return result_series


FALLBACK_REGISTRY = {
    "nan_if_no_valid": nan_if_no_valid,
    "propagate_special": propagate_special,
}
