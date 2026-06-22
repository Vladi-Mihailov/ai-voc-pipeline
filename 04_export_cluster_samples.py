import pandas as pd
import config

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(config.CLUSTERS_FILE)

# ==========================================
# EXPORT SAMPLES
# ==========================================

with open(
    config.CLUSTER_SAMPLES_FILE,
    "w",
    encoding="utf-8"
) as f:

    for cluster in sorted(df["ClusterID"].unique()):

        cluster_df = df[df["ClusterID"] == cluster]

        avg_rating = round(
            cluster_df["Rating"].mean(),
            2
        )

        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write(
            f"CLUSTER {cluster} | "
            f"Reviews={len(cluster_df)} | "
            f"AvgRating={avg_rating}\n"
        )
        f.write("=" * 80 + "\n\n")

        samples = cluster_df.sample(
            min(20, len(cluster_df)),
            random_state=42
        )

        for review in samples["Review"]:

            f.write("-" * 40 + "\n")
            f.write(str(review) + "\n")

print(f"Saved: {config.CLUSTER_SAMPLES_FILE}")