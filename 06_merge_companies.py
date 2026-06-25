import pandas as pd
import os
import config
from utils import ensure_standard_columns

all_data = []

for folder in os.listdir(config.OUTPUT_DIR):

    folder_path = os.path.join(
        config.OUTPUT_DIR,
        folder
    )

    if not os.path.isdir(folder_path):
        continue

    file_path = os.path.join(
        folder_path,
        "cluster_names.csv"
    )

    if not os.path.exists(file_path):
        continue

    df = pd.read_csv(file_path)
    df = ensure_standard_columns(df)
    all_data.append(df)

# ==========================================
# MERGE
# ==========================================

output = pd.concat(
    all_data,
    ignore_index=True
)

# ==========================================
# SAVE
# ==========================================

output.to_csv(
    config.VOC_ALL_COMPANIES_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print(config.VOC_ALL_COMPANIES_FILE)

print(output.head())