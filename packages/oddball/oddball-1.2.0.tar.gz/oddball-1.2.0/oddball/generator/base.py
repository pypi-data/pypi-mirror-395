"""Base functionality for generating anomaly-contaminated data."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from typing import Any, Literal

import numpy as np
import pandas as pd


class BaseDataGenerator(ABC):
    """Abstract base for generators with anomaly contamination control."""

    def __init__(
        self,
        load_data_func: Callable[[], pd.DataFrame],
        anomaly_proportion: float,
        anomaly_mode: Literal["proportional", "probabilistic"] = "proportional",
        n_batches: int | None = None,
        train_size: float = 0.5,
        seed: int | None = None,
    ) -> None:
        self.load_data_func = load_data_func
        self.anomaly_proportion = anomaly_proportion
        self.anomaly_mode = anomaly_mode
        self.n_batches = n_batches
        self.train_size = train_size
        self.seed = seed

        self.rng = np.random.default_rng(seed)

        self._validate_config()
        self._prepare_data()

        if anomaly_mode == "probabilistic":
            self._init_probabilistic_tracking()

    def _validate_config(self) -> None:
        if not 0 <= self.anomaly_proportion <= 1:
            raise ValueError(
                f"anomaly_proportion must be between 0 and 1, "
                f"got {self.anomaly_proportion}"
            )

        if not 0 < self.train_size < 1:
            raise ValueError(
                f"train_size must be between 0 and 1, got {self.train_size}"
            )

        if self.anomaly_mode not in ["proportional", "probabilistic"]:
            raise ValueError(
                f"anomaly_mode must be 'proportional' or 'probabilistic', "
                f"got {self.anomaly_mode}"
            )

        if self.anomaly_mode == "probabilistic" and self.n_batches is None:
            raise ValueError(
                "n_batches must be specified when anomaly_mode='probabilistic'"
            )

        if self.n_batches is not None and self.n_batches <= 0:
            raise ValueError(f"n_batches must be positive, got {self.n_batches}")

    def _prepare_data(self) -> None:
        df = self.load_data_func()
        if "Class" not in df.columns:
            raise ValueError("Expected 'Class' column in data")

        normal_mask = df["Class"] == 0
        df_normal = df[normal_mask]
        df_anomaly = df[~normal_mask]

        if len(df_normal) == 0:
            raise ValueError("No normal instances found in dataset")
        if len(df_anomaly) == 0:
            raise ValueError("No anomalous instances found in dataset")

        n_train = int(len(df_normal) * self.train_size)
        if n_train == 0:
            raise ValueError("train_size too small to select any training samples")

        train_idx = self.rng.choice(len(df_normal), size=n_train, replace=False)
        test_normal_mask = np.ones(len(df_normal), dtype=bool)
        test_normal_mask[train_idx] = False

        self.x_train = df_normal.iloc[train_idx].drop(columns=["Class"])
        self.x_normal = (
            df_normal.iloc[test_normal_mask]
            .drop(columns=["Class"])
            .reset_index(drop=True)
        )
        self.x_anomaly = df_anomaly.drop(columns=["Class"]).reset_index(drop=True)

        self.n_normal = len(self.x_normal)
        self.n_anomaly = len(self.x_anomaly)

    def _init_probabilistic_tracking(self) -> None:
        total_instances = (
            self.n_batches * self.batch_size
            if hasattr(self, "batch_size")
            else self.n_batches
        )
        self._target_anomalies = int(total_instances * self.anomaly_proportion)
        self._current_anomalies = 0
        self._items_generated = 0

    def get_training_data(self) -> pd.DataFrame:
        """Return training data consisting of normal instances only."""
        return self.x_train

    def reset(self) -> None:
        """Reset RNG and tracking state."""
        self.rng = np.random.default_rng(self.seed)
        if self.anomaly_mode == "probabilistic":
            self._current_anomalies = 0
            self._items_generated = 0

    def _should_generate_anomaly(self) -> bool:
        if self.anomaly_mode == "probabilistic":
            if hasattr(self, "batch_size"):
                total_instances = self.n_batches * self.batch_size
            else:
                total_instances = self.n_batches

            remaining_items = total_instances - self._items_generated
            remaining_anomalies = self._target_anomalies - self._current_anomalies

            if remaining_items <= 0 or remaining_anomalies <= 0:
                return False
            if remaining_anomalies >= remaining_items:
                return True

            return self.rng.random() < (remaining_anomalies / remaining_items)

        return self.rng.random() < self.anomaly_proportion

    def _sample_instance(self, is_anomaly: bool) -> tuple[pd.DataFrame, float]:
        if is_anomaly:
            idx = self.rng.integers(0, self.n_anomaly)
            instance = self.x_anomaly.iloc[[idx]].reset_index(drop=True)
            label = 1.0
        else:
            idx = self.rng.integers(0, self.n_normal)
            instance = self.x_normal.iloc[[idx]].reset_index(drop=True)
            label = 0.0

        return instance, label

    @abstractmethod
    def generate(self, **kwargs) -> Iterator[Any]:
        """Yield generated items."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"n_normal={self.n_normal}, "
            f"n_anomaly={self.n_anomaly}, "
            f"anomaly_proportion={self.anomaly_proportion}, "
            f"anomaly_mode='{self.anomaly_mode}')"
        )
