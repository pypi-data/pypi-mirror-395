"""
Minimal application-style example for using oddball datasets.
"""

from oddball import Dataset, list_available, load, split_by_label

# List available datasets
print("Available:", ", ".join(list_available()))

# Load a dataset (raw NumPy arrays)
X, y = load(Dataset.COVER)
print(f"COVER shape: {X.shape}, anomaly rate: {y.mean():.2%}")

# Access normal/anomaly subsets
normal, anomaly = split_by_label("cover")
print(f"Normal samples: {len(normal)}, Anomaly samples: {len(anomaly)}")
