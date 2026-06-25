import pandas as pd

def ensure_column(df, column, default_value=None):
    if column not in df.columns:
        df[column] = default_value
    return df


def ensure_standard_columns(df):
    required_columns = {
        "ReviewID": None,
        "Date": None,
        "YearMonth": None,
        "Platform": "Custom",
        "Company": "Unknown",
        "AppName": "Unknown",
        "Language": "en",
        "Rating": None,
        "Sentiment": None,
        "Review": "",
        "Review_EN": "",
    }

    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default

    if "Review_EN" in df.columns:
        df["Review_EN"] = df["Review_EN"].fillna(df["Review"])
    else:
        df["Review_EN"] = df["Review"]

    return df

from pathlib import Path
import config


def get_processing_folders():

    if config.INPUT_MODE == "CSV":
        return [Path(config.APP_FOLDER)]

    return [
        folder
        for folder in Path("output").iterdir()
        if folder.is_dir()
    ]