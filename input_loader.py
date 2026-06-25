import pandas as pd
from utils import ensure_standard_columns


def load_csv_reviews(file_path):

    df = pd.read_csv(file_path)

    if "Comment" in df.columns:
        df = df.rename(
            columns={
                "Comment": "Review"
            }
        )

    df = ensure_standard_columns(df)

    return df