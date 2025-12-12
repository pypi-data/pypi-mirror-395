"""
Example demonstrating the experimental setup split.
"""

from oddball import Dataset, load

# Create train/test split with only normal samples in training
x_train, x_test, y_test = load(Dataset.COVER, setup=True, seed=42)

print("Train shape:", x_train.shape)
print("Test shape :", x_test.shape)
print(
    "Test class balance:",
    y_test.value_counts(normalize=True).rename("fraction").to_frame().T,
)
