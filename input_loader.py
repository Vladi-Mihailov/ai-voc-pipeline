from pathlib import Path

import pandas as pd

from utils import ensure_standard_columns
import config


def load_csv_reviews():

    input_folder = Path(config.INPUT_FOLDER)

    if not input_folder.exists():

        raise FileNotFoundError(
            f"Input folder not found: {input_folder}"
        )

    files = []

    files.extend(
        sorted(input_folder.glob("*.xlsx"))
    )

    files.extend(
        sorted(input_folder.glob("*.xls"))
    )

    files.extend(
        sorted(input_folder.glob("*.csv"))
    )

    if len(files) == 0:

        raise FileNotFoundError(
            f"No CSV or Excel files found in {input_folder}"
        )

    print("\nLoading input files...\n")

    dfs = []

    total_reviews = 0

    for file in files:

        if file.suffix.lower() == ".csv":

            df = pd.read_csv(file)

        else:

            df = pd.read_excel(file)

        # Support Comment column
        if "Comment" in df.columns and "Review" not in df.columns:

            df = df.rename(
                columns={
                    "Comment": "Review"
                }
            )

        df["SourceFile"] = file.name

        df = ensure_standard_columns(df)

        dfs.append(df)

        total_reviews += len(df)

        print(
            f"✓ {file.name:<35} {len(df):>8,} reviews"
        )

    print("-" * 55)

    print(
        f"Total files: {len(files)}"
    )

    print(
        f"Total reviews: {total_reviews:,}"
    )

    reviews = pd.concat(
        dfs,
        ignore_index=True
    )

    print(
        f"Combined reviews: {len(reviews):,}\n"
    )

    return reviews