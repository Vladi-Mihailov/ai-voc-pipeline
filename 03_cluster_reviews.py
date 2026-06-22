import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import config

# ==========================================
# SETTINGS
# ==========================================

N_CLUSTERS = config.DEFAULT_CLUSTERS

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_pickle(config.EMBEDDINGS_FILE)

print(f"Reviews loaded: {len(df)}")
print(df.columns.tolist())

# ==========================================
# ADAPTIVE CLUSTERS
# ==========================================

if len(df) < 5:

    print("\nToo few reviews for clustering.")
    print("Skipping app.")

    raise SystemExit(0)

if len(df) < N_CLUSTERS:

    N_CLUSTERS = max(
        config.MIN_CLUSTERS,
        len(df) // config.REVIEWS_PER_CLUSTER
    )

print(f"\nReviews: {len(df)}")
print(f"Clusters: {N_CLUSTERS}")

# ==========================================
# PREPARE EMBEDDINGS
# ==========================================

embeddings = np.vstack(df["embedding"].values)

print("Embedding matrix shape:")
print(embeddings.shape)

# ==========================================
# KMEANS
# ==========================================

print(f"\nRunning KMeans ({N_CLUSTERS} clusters)...")

kmeans = KMeans(
    n_clusters=N_CLUSTERS,
    random_state=42,
    n_init=10
)

df["ClusterID"] = kmeans.fit_predict(
    embeddings
)

# ==========================================
# CLUSTER SIZES
# ==========================================

cluster_summary = (
    df.groupby("ClusterID")
      .agg(
          Reviews=("ReviewID", "count"),
          Avg_Rating=("Rating", "mean")
      )
      .reset_index()
      .sort_values(
          "Reviews",
          ascending=False
      )
)

cluster_summary["Avg_Rating"] = (
    cluster_summary["Avg_Rating"]
    .round(2)
)

print("\n==============================")
print("CLUSTER SUMMARY")
print("==============================")
print(cluster_summary)

# ==========================================
# SAVE
# ==========================================

df.to_csv(
    config.CLUSTERS_FILE,
    index=False,
    encoding="utf-8-sig"
)

cluster_summary.to_csv(
    config.CLUSTER_SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print(config.CLUSTERS_FILE)
print(config.CLUSTER_SUMMARY_FILE)