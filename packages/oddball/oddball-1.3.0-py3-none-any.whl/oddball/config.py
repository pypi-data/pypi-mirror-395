"""
Configuration helpers for oddball.

Values can be provided via environment variables or a ``.env`` file. A
``.env`` file path can be overridden with ``ODDBALL_DOTENV``; otherwise the
current working directory's ``.env`` is used if present.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urljoin

DATASET_VERSION_ENV = "ODDBALL_DATASET_VERSION"
DATASET_URL_ENV = "ODDBALL_DATASET_URL"
CACHE_DIR_ENV = "ODDBALL_CACHE_DIR"
DOTENV_ENV = "ODDBALL_DOTENV"

DEFAULT_DATASET_VERSION = "v1.0-datasets"
DEFAULT_BASE_URL = "https://github.com/OliverHennhoefer/oddball/releases/download/"
DEFAULT_CACHE_ROOT = Path.home() / ".cache" / "oddball"


@dataclass(frozen=True)
class Settings:
    dataset_version: str
    dataset_url: str
    cache_root: Path


def _read_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    env: dict[str, str] = {}
    try:
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue
            key, val = stripped.split("=", 1)
            env[key.strip()] = val.strip().strip("'").strip('"')
    except OSError:
        return {}
    return env


def load_settings() -> Settings:
    dotenv_path = Path(os.environ.get(DOTENV_ENV, Path.cwd() / ".env"))
    dotenv_values = _read_dotenv(dotenv_path)

    def get(key: str, default: str) -> str:
        if key in os.environ:
            return os.environ[key]
        if key in dotenv_values:
            return dotenv_values[key]
        return default

    version = get(DATASET_VERSION_ENV, DEFAULT_DATASET_VERSION)
    default_base = urljoin(DEFAULT_BASE_URL, quote(version, safe="") + "/")
    dataset_url = get(DATASET_URL_ENV, default_base)
    if not dataset_url.endswith("/"):
        dataset_url += "/"

    cache_root = Path(get(CACHE_DIR_ENV, str(DEFAULT_CACHE_ROOT)))

    return Settings(
        dataset_version=version,
        dataset_url=dataset_url,
        cache_root=cache_root,
    )
