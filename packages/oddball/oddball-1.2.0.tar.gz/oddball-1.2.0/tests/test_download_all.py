from pathlib import Path
import os

import pytest

from oddball import clear_cache, get_cache_location, list_available, load
from oddball.data.registry import DATASET_FILES


@pytest.fixture(scope="session")
def cache_env(tmp_path_factory):
    cache_root = tmp_path_factory.mktemp("cache")
    previous = os.environ.get("ODDBALL_CACHE_DIR")
    os.environ["ODDBALL_CACHE_DIR"] = str(cache_root)
    clear_cache(all_versions=True)
    yield cache_root
    clear_cache(all_versions=True)
    if previous is None:
        os.environ.pop("ODDBALL_CACHE_DIR", None)
    else:
        os.environ["ODDBALL_CACHE_DIR"] = previous


@pytest.mark.parametrize("dataset_name", list_available())
def test_dataset_downloads(cache_env, dataset_name):  # noqa: ARG001
    X, y = load(dataset_name)
    assert X.shape[0] == y.shape[0] > 0


def test_all_assets_cached(cache_env):  # noqa: ARG001
    cache_dir = Path(get_cache_location())
    for filename in DATASET_FILES.values():
        assert (cache_dir / filename).exists(), f"{filename} missing from cache"
