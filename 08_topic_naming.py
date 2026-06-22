# 08_topic_naming.py


import pandas as pd
import json
from openai import OpenAI
import config

# ==========================================
# SETTINGS
# ==========================================

INPUT_FILE = config.VOC_TOPIC_CLUSTERS_FILE
OUTPUT_FILE = config.VOC_TOPIC_MAPPING_FILE

client = OpenAI(
    api_key=config.API_KEY
)

# ==========================================
# LOAD
# ==========================================

df = pd.read_csv(INPUT_FILE)

results = []

# ==========================================
# LOOP META CLUSTERS
# ==========================================

for cluster_id in sorted(df["MetaClusterID"].unique()):

    cluster_df = df[
        df["MetaClusterID"] == cluster_id
    ]

    topics = (
        cluster_df["ClusterName"]
        .dropna()
        .unique()
        .tolist()
    )

    topics_text = "\n".join(
        f"- {x}"
        for x in topics
    )

    prompt = f"""
You are a senior VOC analyst.

Below are customer feedback topics that belong
to the same semantic group.

Create ONE short business-friendly topic name.

Rules:
- Maximum 4 words.
- Use title case.
- Be specific.
- Do not use generic names like:
  "General Feedback"
  "Various Issues"
  "Customer Experience"
- Return only JSON.

Format:

{{
  "topic": "Customer Support"
}}

Topics:

{topics_text}
"""

    print(
        f"Processing MetaCluster {cluster_id}..."
    )

    response = client.chat.completions.create(
        model=config.MODEL_TOPICS,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    try:

        result = json.loads(
            response.choices[0].message.content
        )

        results.append({
            "MetaClusterID": cluster_id,
            "MetaTopic": result["topic"]
        })

    except Exception as e:

        print(
            f"Error MetaCluster {cluster_id}"
        )

        print(e)

# ==========================================
# SAVE
# ==========================================

output = pd.DataFrame(results)

output.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print(OUTPUT_FILE)

print(output.head())