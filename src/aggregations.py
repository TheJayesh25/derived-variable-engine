import numpy as np

def mean_aggregation(df):
    return df.mean(axis=1)

def sum_aggregation(df):
    return df.sum(axis=1)

AGGREGATION_REGISTRY = {
    "mean": mean_aggregation,
    "sum": sum_aggregation,
}
