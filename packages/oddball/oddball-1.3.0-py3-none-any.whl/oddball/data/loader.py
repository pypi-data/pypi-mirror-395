"""
Dataset loading utilities for oddball.

This module handles on-demand downloads of GitHub release assets and returns the
raw ``X`` and ``y`` arrays stored in each ``.npz`` without further processing.
"""

from __future__ import annotations

import io
import shutil
from collections import OrderedDict
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

from oddball.config import load_settings
from oddball.enums import Dataset

from .registry import DATASET_FILES
from .setup import create_setup


class DatasetManager:
    """Manage dataset download, caching, and loading."""

    def __init__(self) -> None:
        self._settings = load_settings()
        self._cache_dir: Path | None = None
        self._memory_cache: OrderedDict[str, bytes] = OrderedDict()
        self.max_cache_size = 16
        self.suffix = ".npz"

    @property
    def settings(self):
        # Reload settings to pick up environment/.env changes between calls.
        self._settings = load_settings()
        return self._settings

    @property
    def version(self) -> str:
        return self.settings.dataset_version

    @property
    def base_url(self) -> str:
        return self.settings.dataset_url

    @property
    def cache_dir(self) -> Path:
        """Return the on-disk cache directory, creating it if missing."""
        target = self.settings.cache_root / self.version
        if self._cache_dir is None or self._cache_dir != target:
            self._cache_dir = target
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        return self._cache_dir

    def load(
        self,
        dataset: Dataset | str,
        *,
        setup: bool = False,
        as_dataframe: bool = False,
        seed: int | None = None,
    ) -> (
        tuple[np.ndarray, np.ndarray]
        | tuple[pd.DataFrame, pd.DataFrame, pd.Series]
        | pd.DataFrame
    ):
        """Load a dataset and return arrays, a DataFrame, or a setup split.

        When ``setup`` is ``True``, a DataFrame-based train/test split is
        returned where the training data only contains normal samples (Class 0)
        and the test set is a mix of normal and anomalous samples.
        When ``as_dataframe`` is ``True``, the full dataset is returned as a
        DataFrame with generated column names and a ``Class`` column.
        """
        name = self._normalize_name(dataset)
        filename = self._get_filename(name)

        npz_bytes = self._download(filename)
        buffer = io.BytesIO(npz_bytes)
        npz = np.load(buffer)

        if not setup and not as_dataframe:
            return npz["X"].astype(np.float64), npz["y"].astype(np.float64)

        column_names = [f"V{i + 1}" for i in range(npz["X"].shape[1])]
        df = pd.DataFrame(npz["X"].astype(np.float64), columns=column_names)
        df["Class"] = npz["y"].astype(np.float64)

        if not setup and as_dataframe:
            return df

        return create_setup(df, seed)

    def split_by_label(
        self, dataset: Dataset | str, *, as_numpy: bool = False
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return (normal, anomaly) slices of the feature matrix."""
        X, y = self.load(dataset)
        normal = X[y == 0]
        anomaly = X[y != 0]

        if as_numpy:
            return normal, anomaly

        # Return views as numpy arrays by default to avoid silent copies
        return normal, anomaly

    def list_available(self) -> list[str]:
        """Return a sorted list of available dataset names."""
        return sorted(DATASET_FILES.keys())

    def clear_cache(
        self, dataset: str | None = None, *, all_versions: bool = False
    ) -> None:
        """Clear cached datasets from memory and disk."""
        if all_versions:
            cache_root = self.cache_dir.parent
            if cache_root.exists():
                try:
                    shutil.rmtree(cache_root)
                except PermissionError:
                    pass
            self._memory_cache.clear()
            return

        if dataset:
            filename = self._get_filename(dataset)
            self._memory_cache.pop(filename, None)
            cache_path = self.cache_dir / filename
            if cache_path.exists():
                try:
                    cache_path.unlink()
                except PermissionError:
                    pass
            return

        if self.cache_dir.exists():
            try:
                shutil.rmtree(self.cache_dir)
            except PermissionError:
                pass
        self._memory_cache.clear()

    def get_cache_location(self) -> str:
        """Return the current cache directory path as a string."""
        return str(self.cache_dir)

    def _download(self, filename: str) -> bytes:
        if filename in self._memory_cache:
            self._memory_cache.move_to_end(filename)
            return self._memory_cache[filename]

        cache_path = self.cache_dir / filename
        if cache_path.exists():
            try:
                data = cache_path.read_bytes()
            except PermissionError:
                data = None
            else:
                self._add_to_memory_cache(filename, data)
                return data

        self._cleanup_old_versions()

        url = urljoin(self.base_url, filename)
        req = Request(url, headers={"User-Agent": "oddball-datasets/0.1"})
        try:
            with urlopen(req) as response:  # noqa: S310 - controlled URL
                data = response.read()
        except URLError as exc:  # pragma: no cover - network failure path
            raise URLError(
                f"Failed to download dataset asset {filename}: {exc}"
            ) from exc

        self._add_to_memory_cache(filename, data)
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(data)
        except PermissionError:
            # Skip disk caching when permissions are restricted
            pass

        return data

    def _cleanup_old_versions(self) -> None:
        cache_root = self.cache_dir.parent
        if not cache_root.exists():
            return

        for child in cache_root.iterdir():
            if not child.is_dir() or child.name == self.version:
                continue
            try:
                shutil.rmtree(child)
            except PermissionError:
                pass

    def _add_to_memory_cache(self, filename: str, data: bytes) -> None:
        self._memory_cache[filename] = data
        self._memory_cache.move_to_end(filename)
        if len(self._memory_cache) > self.max_cache_size:
            self._memory_cache.popitem(last=False)

    def _get_filename(self, dataset: Dataset | str) -> str:
        name = self._normalize_name(dataset)
        if name not in DATASET_FILES:
            available = ", ".join(sorted(DATASET_FILES))
            raise ValueError(
                f"Unknown dataset '{name}'. Available datasets: {available}"
            )
        return DATASET_FILES[name]

    @staticmethod
    def _normalize_name(dataset: Dataset | str) -> str:
        if isinstance(dataset, Dataset):
            return dataset.value
        name = str(dataset).strip().lower()
        for char, replacement in {".": "_", "-": "_", " ": "_"}.items():
            name = name.replace(char, replacement)
        name = "_".join(part for part in name.split("_") if part)
        alias = {
            "satimage_2": "satimage2",
            "satimage2": "satimage2",
            "page_blocks": "pageblocks",
            "pageblocks": "pageblocks",
            "internet_ads": "internetads",
            "internetads": "internetads",
            "spam_base": "spambase",
            "spambase": "spambase",
            "breast_wisconsin": "breastw",
            "breastw": "breastw",
            "magicgamma": "magic_gamma",
        }
        name = alias.get(name, name)
        return name


_manager = DatasetManager()


def load(
    dataset: Dataset | str,
    *,
    setup: bool = False,
    as_dataframe: bool = False,
    seed: int | None = None,
) -> (
    tuple[np.ndarray, np.ndarray]
    | tuple[pd.DataFrame, pd.DataFrame, pd.Series]
    | pd.DataFrame
):
    """Public wrapper for :meth:`DatasetManager.load`."""
    return _manager.load(dataset, setup=setup, as_dataframe=as_dataframe, seed=seed)


def split_by_label(
    dataset: Dataset | str, *, as_numpy: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """Public wrapper for :meth:`DatasetManager.split_by_label`."""
    return _manager.split_by_label(dataset, as_numpy=as_numpy)


def list_available() -> list[str]:
    """Return the datasets that can be loaded."""
    return _manager.list_available()


def clear_cache(dataset: str | None = None, *, all_versions: bool = False) -> None:
    """Clear cached datasets from disk and memory."""
    _manager.clear_cache(dataset, all_versions=all_versions)


def get_cache_location() -> str:
    """Return the cache directory path."""
    return _manager.get_cache_location()
