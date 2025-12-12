"""
Minimal demo of batch and online generators.
"""

from oddball import BatchGenerator, Dataset, OnlineGenerator, load


def load_df():
    return load(Dataset.COVER, as_dataframe=True)


# Proportional batch generator: fixed anomalies per batch
batch_prop = BatchGenerator(
    load_data_func=load_df,
    batch_size=20,
    anomaly_proportion=0.1,
    anomaly_mode="proportional",
    n_batches=5,
    seed=1,
)
for i, (x_batch, y_batch) in enumerate(batch_prop.generate(), start=1):
    print(
        f"Batch (proportional) {i}: shape={x_batch.shape}, anomalies={int(y_batch.sum())}"
    )

# Probabilistic batch generator: global proportion across batches
batch_prob = BatchGenerator(
    load_data_func=load_df,
    batch_size=20,
    anomaly_proportion=0.1,
    anomaly_mode="probabilistic",
    n_batches=5,
    seed=1,
)
for i, (x_batch, y_batch) in enumerate(batch_prob.generate(), start=1):
    print(
        f"Batch (probabilistic) {i}: shape={x_batch.shape}, anomalies={int(y_batch.sum())}"
    )

# Online generator: single instances with exact global proportion
online_gen = OnlineGenerator(
    load_data_func=load_df,
    anomaly_proportion=0.05,
    n_instances=40,
    seed=1,
)
labels = [label for _, label in online_gen.generate()]
print(f"Online: {len(labels)} items, anomalies={sum(labels)}")
