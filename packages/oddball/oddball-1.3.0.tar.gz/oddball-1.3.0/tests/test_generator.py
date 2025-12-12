import io

import pandas as pd
import numpy as np
import pytest

from oddball import BatchGenerator, Dataset, OnlineGenerator, clear_cache, load
from oddball.data.loader import DatasetManager


@pytest.fixture(autouse=True)
def reset_cache():
    clear_cache(all_versions=True)
    yield
    clear_cache(all_versions=True)


@pytest.fixture
def sample_npz_bytes():
    def factory(n_rows: int = 200, n_features: int = 4) -> bytes:
        rng = np.random.default_rng(123)
        X = rng.normal(size=(n_rows, n_features)).astype(np.float32)
        y = np.zeros(n_rows, dtype=np.int64)
        y[: max(1, n_rows // 5)] = 1
        rng.shuffle(y)
        buf = io.BytesIO()
        np.savez(buf, X=X, y=y)
        return buf.getvalue()

    return factory


@pytest.fixture
def mock_download(monkeypatch, sample_npz_bytes):
    payload = sample_npz_bytes()

    def fake_download(self, filename: str) -> bytes:  # noqa: ARG001
        return payload

    monkeypatch.setattr(DatasetManager, "_download", fake_download)
    return payload


def test_load_as_dataframe(mock_download):  # noqa: ARG001
    df = load(Dataset.COVER, as_dataframe=True)
    assert isinstance(df, pd.DataFrame)
    assert "Class" in df.columns
    assert df.shape[0] > 0


def test_batch_generator_proportional(monkeypatch, mock_download):  # noqa: ARG001
    # Force deterministic RNG
    seed = 7
    gen = BatchGenerator(
        load_data_func=lambda: load(Dataset.COVER, as_dataframe=True),
        batch_size=20,
        anomaly_proportion=0.2,
        anomaly_mode="proportional",
        n_batches=2,
        seed=seed,
    )

    batches = list(gen.generate())
    assert len(batches) == 2

    for x_batch, y_batch in batches:
        assert x_batch.shape[0] == 20
        assert y_batch.sum() == 4  # 20% anomalies per batch
        assert set(y_batch.unique()) <= {0, 1}

    # Training data should contain only normal samples
    df = load(Dataset.COVER, as_dataframe=True)
    train_idx = gen.get_training_data().index
    assert train_idx.isin(df.index).all()
    assert df.loc[train_idx, "Class"].eq(0).all()


def test_online_generator_probabilistic(mock_download):  # noqa: ARG001
    n_instances = 50
    anomaly_proportion = 0.1
    gen = OnlineGenerator(
        load_data_func=lambda: load(Dataset.COVER, as_dataframe=True),
        anomaly_proportion=anomaly_proportion,
        n_instances=n_instances,
        seed=42,
    )

    items = list(gen.generate())
    assert len(items) == n_instances

    _, labels = zip(*items)
    labels = list(labels)

    assert sum(labels) == int(n_instances * anomaly_proportion)
    assert set(labels) <= {0, 1}
