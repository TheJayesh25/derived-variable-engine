import numpy as np


def mean_aggregation(df):
    return df.mean(axis=1)


def sum_aggregation(df):
    return df.sum(axis=1)


def median_aggregation(df):
    return df.median(axis=1)


def min_aggregation(df):
    return df.min(axis=1)


def max_aggregation(df):
    return df.max(axis=1)


def std_aggregation(df):
    return df.std(axis=1)


def count_valid_aggregation(df):
    return df.notna().sum(axis=1)


def weighted_mean_aggregation(df, weights=None):
    if weights is None:
        raise ValueError("weighted_mean requires 'weights' parameter")

    weights_array = np.array(weights)

    def row_weighted_mean(row):
        mask = ~np.isnan(row)
        if not mask.any():
            return np.nan
        return np.average(row[mask], weights=weights_array[mask])

    return df.apply(row_weighted_mean, axis=1)


AGGREGATION_REGISTRY = {
    "mean": mean_aggregation,
    "sum": sum_aggregation,
    "median": median_aggregation,
    "min": min_aggregation,
    "max": max_aggregation,
    "std": std_aggregation,
    "count_valid": count_valid_aggregation,
    "weighted_mean": weighted_mean_aggregation,
}
