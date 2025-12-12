"""Utilities for creating train/test anomaly detection setups."""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split


def create_setup(
    df: pd.DataFrame, seed: int | None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """
    Create an experimental train/test split from a dataset.

    This setup creates a scenario for anomaly detection where:
    - The training set contains only normal samples (Class 0).
    - The test set contains a mix of normal and anomaly samples.

    Args:
        df: The input DataFrame with a "Class" column.
        seed: Random seed for data splitting.

    Returns:
        A tuple (x_train, x_test, y_test).
    """
    normal = df[df["Class"] == 0]
    n_train = len(normal) // 2
    n_test = min(1000, n_train // 3)
    n_test_outlier = n_test // 10
    n_test_normal = n_test - n_test_outlier

    x_train_full, test_set_normal_pool = train_test_split(
        normal, train_size=n_train, random_state=seed
    )
    x_train = x_train_full.drop(columns=["Class"])

    actual_n_test_normal = min(n_test_normal, len(test_set_normal_pool))
    test_normal = test_set_normal_pool.sample(n=actual_n_test_normal, random_state=seed)

    outliers_available = df[df["Class"] == 1]
    actual_n_test_outlier = min(n_test_outlier, len(outliers_available))
    test_outliers = outliers_available.sample(
        n=actual_n_test_outlier, random_state=seed
    )

    test_set = pd.concat([test_normal, test_outliers], ignore_index=True)

    x_test = test_set.drop(columns=["Class"])
    y_test = test_set["Class"]

    return x_train, x_test, y_test
