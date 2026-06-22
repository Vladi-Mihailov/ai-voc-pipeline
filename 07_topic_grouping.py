import pandas as pd
import numpy as np
from openai import OpenAI
from sklearn.cluster import AgglomerativeClustering
from tqdm import tqdm
import config

# ==========================================
# SETTINGS
# ==========================================

INPUT_FILE = config.VOC_ALL_COMPANIES_FILE

client = OpenAI(
    api_key=config.API_KEY
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(INPUT_FILE)

topics = (
    df[
        ["ClusterName", "Description"]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

print(f"Unique topics: {len(topics)}")

# ==========================================
# EMBEDDINGS
# ==========================================

embeddings = []

for text in tqdm(
    topics["Description"],
    desc="Generating embeddings"
):

    response = client.embeddings.create(
        model=config.MODEL_EMBEDDINGS,
        input=str(text)
    )

    embeddings.append(
        response.data[0].embedding
    )

X = np.array(embeddings)

print("\nEmbedding matrix:")
print(X.shape)

# ==========================================
# CLUSTERING
# ==========================================

clustering = AgglomerativeClustering(
    n_clusters=None,
    metric="cosine",
    linkage="average",
    distance_threshold=0.35
)

topics["MetaClusterID"] = clustering.fit_predict(X)

print(
    f"\nMeta clusters: "
    f"{topics['MetaClusterID'].nunique()}"
)

# ==========================================
# SAVE
# ==========================================

output = topics[
    [
        "MetaClusterID",
        "ClusterName",
        "Description"
    ]
]

output.to_csv(
    config.VOC_TOPIC_CLUSTERS_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print(config.VOC_TOPIC_CLUSTERS_FILE)

# ==========================================
# PREVIEW
# ==========================================

print("\n" + "=" * 80)
print("SAMPLE CLUSTERS")
print("=" * 80)

for cluster_id in sorted(
    output["MetaClusterID"].unique()
)[:20]:

    cluster_topics = output[
        output["MetaClusterID"] == cluster_id
    ]

    print(f"\nMetaCluster {cluster_id}")
    print("-" * 50)

    for topic in cluster_topics[
        "ClusterName"
    ].tolist():

        print(topic)

print(
    f"Meta clusters: "
    f"{topics['MetaClusterID'].nunique()}"
)