from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import time

# ==========================================
# SETTINGS
# ==========================================

import config

client = OpenAI(
    api_key=config.API_KEY
)

MODEL = config.MODEL_EMBEDDINGS
INPUT_FILE = config.REVIEWS_FILE

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(INPUT_FILE)

print(f"Reviews loaded: {len(df)}")
print(df.columns.tolist())

# ==========================================
# GENERATE EMBEDDINGS (BATCH MODE)
# ==========================================

BATCH_SIZE = 100

reviews = df["Review"].fillna("").tolist()

embeddings = []

for i in tqdm(
    range(0, len(reviews), BATCH_SIZE),
    desc="Generating embeddings"
):

    batch = reviews[i:i + BATCH_SIZE]

    try:

        response = client.embeddings.create(
            model=MODEL,
            input=batch,
            dimensions=1536
        )

        batch_embeddings = [
            item.embedding
            for item in response.data
        ]

        embeddings.extend(batch_embeddings)

    except Exception as e:

        print("ERROR:", e)

        embeddings.extend(
            [None] * len(batch)
        )

        time.sleep(5)

# ==========================================
# SAVE
# ==========================================

df["embedding"] = embeddings

#df.to_pickle("capital_embeddings.pkl")
df.to_pickle(config.EMBEDDINGS_FILE)

print("\nSaved:")
print(config.EMBEDDINGS_FILE)