#08_topic_consolidation.py

import pandas as pd
import json
from openai import OpenAI
import config

# ==========================================
# SETTINGS
# ==========================================

#INPUT_FILE = config.VOC_TOPIC_CLUSTERS_FILE
INPUT_FILE = config.VOC_TOPIC_MAPPING_FILE
OUTPUT_FILE = config.VOC_BUSINESS_TOPIC_MAPPING_FILE

client = OpenAI(
    api_key=config.API_KEY
)

# ==========================================
# LOAD
# ==========================================

df = pd.read_csv(INPUT_FILE)

topics = (
    df["MetaTopic"]
    .dropna()
    .unique()
    .tolist()
)

print(
    f"Meta topics: {len(topics)}"
)

# ==========================================
# GPT CONSOLIDATION
# ==========================================

topics_text = "\n".join(
    f"- {topic}"
    for topic in topics
)

prompt = f"""
You are a senior Voice of Customer analyst.

Below is a list of customer feedback topics.

Your task:

Group similar topics into broader business themes.

Examples:

Customer Support Quality
Customer Support Challenges
Customer Support Effectiveness

→ Customer Support

Deposit Requirements
Deposit And Withdrawal
Payment Support Options

→ Deposits & Withdrawals

Rules:

- Create 15-30 business topics.
- Use short business-friendly names.
- Keep important distinctions:
  * Customer Support
  * Verification
  * Deposits & Withdrawals
  * Platform Performance
  * Trust & Security
  * Fraud Allegations
  * Pricing & Fees
  * Localization
  * Geographic Restrictions
  * User Experience
- Return JSON only.

Format:

{{
  "mappings": [
    {{
      "meta_topic": "Customer Support Quality",
      "business_topic": "Customer Support"
    }}
  ]
}}

Topics:

{topics_text}
"""

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

result = json.loads(
    response.choices[0].message.content
)

output = pd.DataFrame(
    result["mappings"]
)

# ==========================================
# SAVE
# ==========================================

output.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print(OUTPUT_FILE)

print("\nBusiness topics:")
print(
    output["business_topic"]
    .value_counts()
)