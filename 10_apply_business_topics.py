# 10_apply_business_topics_v2.py

import pandas as pd
import config
from pathlib import Path


# ==========================================
# SETTINGS
# ==========================================

output_dir = Path("output")

OUTPUT_FILE = config.VOC_BUSINESS_TOPICS_FILE

# ==========================================
# LOAD COMPANY FILES
# ==========================================

all_clusters = []
all_cluster_names = []

for company_dir in output_dir.iterdir():

    if not company_dir.is_dir():
        continue

    clusters_file = company_dir / "clusters.csv"
    names_file = company_dir / "cluster_names.csv"

    if clusters_file.exists():

        df = pd.read_csv(clusters_file)
        df["SourceFolder"] = company_dir.name

        all_clusters.append(df)

        print(f"Loaded clusters: {clusters_file} | rows: {len(df)}")

    if names_file.exists():

        df = pd.read_csv(names_file)
        df["SourceFolder"] = company_dir.name

        all_cluster_names.append(df)

        print(f"Loaded cluster_names: {names_file} | rows: {len(df)}")

# ==========================================
# CONCAT
# ==========================================

clusters = pd.concat(
    all_clusters,
    ignore_index=True
)

cluster_names = pd.concat(
    all_cluster_names,
    ignore_index=True
)

print("\n==============================")
print("INPUT CHECK")
print("==============================")

print("Clusters rows:")
print(len(clusters))

print("Cluster names rows:")
print(len(cluster_names))

print("\nClusters columns:")
print(clusters.columns.tolist())

print("\nCluster names columns:")
print(cluster_names.columns.tolist())

# ==========================================
# CLEAN CLUSTERS
# ==========================================

clusters = clusters.drop(
    columns=["embedding"],
    errors="ignore"
)

# ==========================================
# KEEP REQUIRED COLUMNS
# ==========================================

cluster_names = cluster_names[
    [
        "SourceFolder",
        "Company",
        "AppName",
        "ClusterID",
        "ClusterName"
    ]
].drop_duplicates()

# ==========================================
# CHECK DUPLICATES: CLUSTER NAMES
# ==========================================

print("\n==============================")
print("CLUSTER_NAMES CHECK")
print("==============================")

cluster_name_key = [
    "SourceFolder",
    "Company",
    "AppName",
    "ClusterID"
]

duplicates = cluster_names[
    cluster_names.duplicated(
        subset=cluster_name_key,
        keep=False
    )
]

print("Duplicated cluster_names rows:")
print(len(duplicates))

if len(duplicates) > 0:

    print(
        duplicates
        .sort_values(cluster_name_key)
        .head(50)
    )

# ==========================================
# ADD CLUSTER NAME
# ==========================================

print("\n==============================")
print("JOIN #1: clusters + cluster_names")
print("==============================")

rows_before = len(clusters)

voc = clusters.merge(
    cluster_names,
    on=[
        "SourceFolder",
        "Company",
        "AppName",
        "ClusterID"
    ],
    how="left"
)

rows_after = len(voc)

print("Rows before:")
print(rows_before)

print("Rows after:")
print(rows_after)

print("Missing ClusterName:")
print(voc["ClusterName"].isna().sum())

# ==========================================
# LOAD VOC TAXONOMY
# ==========================================

topic_clusters = pd.read_csv(
    config.VOC_TOPIC_CLUSTERS_FILE
)

topic_mapping = pd.read_csv(
    config.VOC_TOPIC_MAPPING_FILE
)

business_mapping = pd.read_csv(
    config.VOC_BUSINESS_TOPIC_MAPPING_FILE
)

# ==========================================
# DEBUG TOPIC CLUSTERS
# ==========================================

print("\n==============================")
print("TOPIC CLUSTERS CHECK")
print("==============================")

print("Rows:")
print(len(topic_clusters))

print("\nColumns:")
print(topic_clusters.columns.tolist())

print("\nUnique ClusterName:")
print(
    topic_clusters["ClusterName"]
    .nunique()
)

print("\nDuplicated ClusterName:")

duplicates = topic_clusters[
    topic_clusters.duplicated(
        subset=["ClusterName"],
        keep=False
    )
]

print(len(duplicates))

if len(duplicates) > 0:

    print(
        duplicates
        .sort_values("ClusterName")
        .head(100)
    )

# ==========================================
# CLEAN TOPIC CLUSTERS
# ==========================================

topic_clusters_clean = topic_clusters[
    [
        "ClusterName",
        "MetaClusterID"
    ]
].drop_duplicates()

topic_clusters_clean = topic_clusters_clean.drop_duplicates(
    subset=["ClusterName"],
    keep="first"
)

print("\nTopic clusters rows after clean:")
print(len(topic_clusters_clean))

# ==========================================
# ADD META CLUSTER
# ==========================================

print("\n==============================")
print("JOIN #2: voc + topic_clusters")
print("==============================")

rows_before = len(voc)

voc = voc.merge(
    topic_clusters_clean,
    on="ClusterName",
    how="left"
)

rows_after = len(voc)

print("Rows before:")
print(rows_before)

print("Rows after:")
print(rows_after)

print("Missing MetaClusterID:")
print(voc["MetaClusterID"].isna().sum())

# ==========================================
# CHECK TOPIC MAPPING
# ==========================================

print("\n==============================")
print("TOPIC MAPPING CHECK")
print("==============================")

print("Rows:")
print(len(topic_mapping))

print("Columns:")
print(topic_mapping.columns.tolist())

duplicates = topic_mapping[
    topic_mapping.duplicated(
        subset=["MetaClusterID"],
        keep=False
    )
]

print("Duplicated MetaClusterID rows:")
print(len(duplicates))

if len(duplicates) > 0:

    print(
        duplicates
        .sort_values("MetaClusterID")
        .head(50)
    )

topic_mapping_clean = topic_mapping[
    [
        "MetaClusterID",
        "MetaTopic"
    ]
].drop_duplicates()

topic_mapping_clean = topic_mapping_clean.drop_duplicates(
    subset=["MetaClusterID"],
    keep="first"
)

# ==========================================
# ADD META TOPIC
# ==========================================

print("\n==============================")
print("JOIN #3: voc + topic_mapping")
print("==============================")

rows_before = len(voc)

voc = voc.merge(
    topic_mapping_clean,
    on="MetaClusterID",
    how="left"
)

rows_after = len(voc)

print("Rows before:")
print(rows_before)

print("Rows after:")
print(rows_after)

print("Missing MetaTopic:")
print(voc["MetaTopic"].isna().sum())

# ==========================================
# CHECK BUSINESS MAPPING
# ==========================================

print("\n==============================")
print("BUSINESS MAPPING CHECK")
print("==============================")

print("Rows:")
print(len(business_mapping))

print("Columns:")
print(business_mapping.columns.tolist())

duplicates = business_mapping[
    business_mapping.duplicated(
        subset=["meta_topic"],
        keep=False
    )
]

print("Duplicated meta_topic rows:")
print(len(duplicates))

if len(duplicates) > 0:

    print(
        duplicates
        .sort_values("meta_topic")
        .head(50)
    )

business_mapping_clean = business_mapping[
    [
        "meta_topic",
        "business_topic"
    ]
].drop_duplicates()

business_mapping_clean = business_mapping_clean.drop_duplicates(
    subset=["meta_topic"],
    keep="first"
)

# ==========================================
# ADD BUSINESS TOPIC
# ==========================================

print("\n==============================")
print("JOIN #4: voc + business_mapping")
print("==============================")

rows_before = len(voc)

voc = voc.merge(
    business_mapping_clean,
    left_on="MetaTopic",
    right_on="meta_topic",
    how="left"
)

rows_after = len(voc)

print("Rows before:")
print(rows_before)

print("Rows after:")
print(rows_after)

# ==========================================
# CLEAN
# ==========================================

voc = voc.drop(
    columns=[
        "meta_topic",
        "SourceFolder"
    ],
    errors="ignore"
)

voc = voc.rename(
    columns={
        "business_topic": "BusinessTopic"
    }
)

# ==========================================
# FINAL CHECK
# ==========================================

print("\n==============================")
print("FINAL CHECK")
print("==============================")

print("Input review rows:")
print(len(clusters))

print("Output rows:")
print(len(voc))

if len(voc) == len(clusters):

    print("OK: Output rows match input review rows.")

else:

    print("WARNING: Output rows != input review rows.")

print("\nUnique ReviewID only:")
print(
    voc["ReviewID"]
    .nunique()
)

print("\nUnique Source-level reviews:")
print(
    voc[
        [
            "Company",
            "AppName",
            "ReviewID"
        ]
    ]
    .drop_duplicates()
    .shape[0]
)

print("\nRows per Company/App/ReviewID:")

print(
    voc.groupby(
        [
            "Company",
            "AppName",
            "ReviewID"
        ]
    )
    .size()
    .value_counts()
    .sort_index()
)

print("\nMissing values:")

check_cols = [
    "ClusterName",
    "MetaClusterID",
    "MetaTopic",
    "BusinessTopic"
]

print(
    voc[
        check_cols
    ]
    .isna()
    .sum()
)

# ==========================================
# REORDER
# ==========================================

columns = [
    "ReviewID",
    "Date",
    "YearMonth",
    "Platform",
    "Company",
    "AppName",
    "Language",
    "Rating",
    "Sentiment",
    "Review",
    "ClusterID",
    "ClusterName",
    "MetaClusterID",
    "MetaTopic",
    "BusinessTopic"
]

columns = [
    c
    for c in columns
    if c in voc.columns
]

voc = voc[columns]

# ==========================================
# SAVE
# ==========================================

voc.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# INFO
# ==========================================

print("\nSaved:")
print(OUTPUT_FILE)

print("\nRows:")
print(len(voc))

print("\nColumns:")
print(voc.columns.tolist())

print("\nBusiness Topics:")
print(
    voc["BusinessTopic"]
    .value_counts(
        dropna=False
    )
    .head(20)
)

print("\nSample:")
print(
    voc.head(10)
)