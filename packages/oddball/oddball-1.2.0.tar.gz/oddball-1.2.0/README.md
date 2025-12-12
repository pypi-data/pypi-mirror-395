# oddball

Lightweight access to the 47 ADBench classical anomaly detection datasets.
Downloads the published `.npz` assets from the GitHub release on demand and
returns raw `(X, y)` NumPy arrays.

- Default assets: https://github.com/OliverHennhoefer/oddball/releases/tag/v1.0-datasets
- Cache: `~/.cache/oddball/<version>` (override with env vars below)

## Installation

```bash
pip install oddball
```

## Usage

```python
from oddball import Dataset, load, split_by_label, list_available

print("Available:", list_available())

X, y = load(Dataset.COVER)           # raw arrays
normal, anomaly = split_by_label("cover")  # feature slices

# Generators for batch/online experimentation
from oddball import BatchGenerator, OnlineGenerator

batch_gen = BatchGenerator(
    load_data_func=lambda: load(Dataset.COVER, as_dataframe=True),
    batch_size=32,
    anomaly_proportion=0.1,
    seed=42,
)
for x_batch, y_batch in batch_gen.generate():
    print(f"Batch: {x_batch.shape}, anomalies: {y_batch.sum()}")
    break
```

## Configuration

- `ODDBALL_DATASET_VERSION` (default: `v1.0-datasets`)
- `ODDBALL_DATASET_URL` (default: `https://github.com/OliverHennhoefer/oddball/releases/download/<version>/`)
- `ODDBALL_CACHE_DIR` (default: `~/.cache/oddball/<version>`)
- `.env` support: place the above keys in `.env` (or set `ODDBALL_DOTENV=/path/to/.env`).

## Supported datasets

All 47 ADBench classical datasets are available. Call `oddball.list_available()` to see slugs (e.g., `cover`, `fraud`, `satimage2`).
