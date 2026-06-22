from openai import OpenAI
import pandas as pd
import json
import time
import config

# ==========================================
# SETTINGS
# ==========================================




client = OpenAI(
    api_key=config.API_KEY
)

MODEL = config.MODEL_TOPICS
INPUT_FILE = config.CLUSTERS_FILE

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(INPUT_FILE)

results = []

# ==========================================
# LOOP CLUSTERS
# ==========================================

for cluster_id in sorted(df["ClusterID"].unique()):

    cluster_df = df[df["ClusterID"] == cluster_id]
    platform = cluster_df["Platform"].iloc[0]
    company = cluster_df["Company"].iloc[0]
    app_name = cluster_df["AppName"].iloc[0]

    reviews_count = len(cluster_df)

    avg_rating = round(
        cluster_df["Rating"].mean(),
        2
    )

    samples = (
        cluster_df["Review"]
        .dropna()
        .sample(
            min(30, len(cluster_df)),
            random_state=42
        )
        .tolist()
    )

    reviews_text = "\n\n".join(samples)

    prompt = f"""
You are a senior product researcher.

Analyze the customer reviews below.

Identify the single dominant customer topic inside this cluster.

Return ONLY valid JSON in exactly this format:

{{
  "cluster_name": "Topic name",
  "description": "Short description",
  "sentiment": "Positive"
}}

Rules:
- Return exactly one topic.
- Choose the dominant theme that best represents most reviews in this cluster.
- Do not return multiple topics.
- Do not return an array.
- Do not return markdown.
- Do not use code fences.
- Root element must always be an object with keys: cluster_name, description, sentiment.
- Sentiment must be only: Positive, Negative, Mixed.

Reviews:

{reviews_text}
"""

    print(f"Processing cluster {cluster_id}...")




    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
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
        response.choices[0].message.content)

        results.append({
        "Platform": platform,
        "Company": company,
        "AppName": app_name,
        "ClusterID": cluster_id,
        "Reviews": reviews_count,
        "AvgRating": avg_rating,
        "ClusterName": result["cluster_name"],
        "Description": result["description"],
        "Sentiment": result["sentiment"]
})

    except Exception as e:

     print("\n")
     print("=" * 80)
     print(f"ERROR CLUSTER {cluster_id}")
     print("=" * 80)

     print("EXCEPTION:")
     print(e)

     print("\nRAW RESPONSE:")

     print(
        response.choices[0].message.content
    )


# ==========================================
# SAVE
# ==========================================

output = pd.DataFrame(results)

output = output[
    [
        "Platform",
        "Company",
        "AppName",
        "ClusterID",
        "ClusterName",
        "Sentiment",
        "Reviews",
        "AvgRating",
        "Description"
    ]
]

output.to_csv(
    config.CLUSTER_NAMES_FILE,
    index=False,
    encoding="utf-8-sig"
)
print(output.columns.tolist())

print("\nSaved:")
print(config.CLUSTER_NAMES_FILE)
print(output)