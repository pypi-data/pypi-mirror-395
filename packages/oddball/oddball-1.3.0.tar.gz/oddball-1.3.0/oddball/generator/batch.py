"""Batch generator for anomaly detection datasets."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Literal

import pandas as pd

from .base import BaseDataGenerator


class BatchGenerator(BaseDataGenerator):
    """Generate batches with configurable anomaly contamination."""

    def __init__(
        self,
        load_data_func: Callable[[], pd.DataFrame],
        batch_size: int,
        anomaly_proportion: float,
        anomaly_mode: Literal["proportional", "probabilistic"] = "proportional",
        n_batches: int | None = None,
        train_size: float = 0.5,
        seed: int | None = None,
    ) -> None:
        if batch_size <= 0:
            raise ValueError(f"batch_size must be positive, got {batch_size}")

        self.batch_size = batch_size

        super().__init__(
            load_data_func=load_data_func,
            anomaly_proportion=anomaly_proportion,
            anomaly_mode=anomaly_mode,
            n_batches=n_batches,
            train_size=train_size,
            seed=seed,
        )

        if anomaly_mode == "proportional":
            self.n_anomaly_per_batch = int(batch_size * anomaly_proportion)
            self.n_normal_per_batch = batch_size - self.n_anomaly_per_batch
            self._validate_batch_config()

    def _validate_batch_config(self) -> None:
        if self.n_normal_per_batch > self.n_normal:
            raise ValueError(
                f"Not enough normal instances ({self.n_normal}) for "
                f"{self.n_normal_per_batch} normal samples per batch"
            )
        if self.n_anomaly_per_batch > self.n_anomaly:
            raise ValueError(
                f"Not enough anomaly instances ({self.n_anomaly}) for "
                f"{self.n_anomaly_per_batch} anomaly samples per batch"
            )

    def generate(self) -> Iterator[tuple[pd.DataFrame, pd.Series]]:
        """Yield batches of (x_batch, y_batch)."""
        batch_count = 0

        def should_continue() -> bool:
            if self.anomaly_mode == "proportional":
                return self.n_batches is None or batch_count < self.n_batches
            return batch_count < self.n_batches

        while should_continue():
            if self.anomaly_mode == "proportional":
                batch_data = []
                batch_labels = []

                for _ in range(self.n_normal_per_batch):
                    instance, label = self._sample_instance(False)
                    batch_data.append(instance)
                    batch_labels.append(label)

                for _ in range(self.n_anomaly_per_batch):
                    instance, label = self._sample_instance(True)
                    batch_data.append(instance)
                    batch_labels.append(label)

                x_batch = pd.concat(batch_data, axis=0, ignore_index=True)
                y_batch = pd.Series(batch_labels, dtype=float)

                shuffle_idx = self.rng.permutation(self.batch_size)
                x_batch = x_batch.iloc[shuffle_idx].reset_index(drop=True)
                y_batch = y_batch.iloc[shuffle_idx].reset_index(drop=True)

            else:
                batch_data = []
                batch_labels = []

                for _ in range(self.batch_size):
                    is_anomaly = self._should_generate_anomaly()
                    instance, label = self._sample_instance(is_anomaly)

                    batch_data.append(instance)
                    batch_labels.append(label)

                    self._current_anomalies += label
                    self._items_generated += 1

                x_batch = pd.concat(batch_data, axis=0, ignore_index=True)
                y_batch = pd.Series(batch_labels, dtype=float)

            yield x_batch, y_batch
            batch_count += 1
