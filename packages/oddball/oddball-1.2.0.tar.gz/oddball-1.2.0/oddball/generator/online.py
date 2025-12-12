"""Online generator for streaming anomaly detection datasets."""

from __future__ import annotations

from collections.abc import Callable, Iterator

import pandas as pd

from .base import BaseDataGenerator


class OnlineGenerator(BaseDataGenerator):
    """Generate single instances with probabilistic anomaly control."""

    def __init__(
        self,
        load_data_func: Callable[[], pd.DataFrame],
        anomaly_proportion: float,
        n_instances: int,
        train_size: float = 0.5,
        seed: int | None = None,
    ) -> None:
        super().__init__(
            load_data_func=load_data_func,
            anomaly_proportion=anomaly_proportion,
            anomaly_mode="probabilistic",
            n_batches=n_instances,
            train_size=train_size,
            seed=seed,
        )

    def generate(
        self, n_instances: int | None = None
    ) -> Iterator[tuple[pd.DataFrame, int]]:
        """Yield streaming instances with labels."""
        if n_instances is None:
            n_instances = self.n_batches

        if n_instances > self.n_batches:
            raise ValueError(
                f"Requested {n_instances} instances exceeds configured "
                f"n_instances={self.n_batches}"
            )

        instance_count = 0

        while instance_count < n_instances:
            is_anomaly = self._should_generate_anomaly()
            instance, label = self._sample_instance(is_anomaly)

            self._current_anomalies += label
            self._items_generated += 1

            yield instance, label
            instance_count += 1
