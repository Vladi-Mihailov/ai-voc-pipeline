from deep_translator import GoogleTranslator
import pandas as pd


def translate_reviews(df):
    """
    Adds Review_EN column.
    Translates only non-English reviews.
    """

    translator = GoogleTranslator(
        source="auto",
        target="en"
    )

    translation_map = {}

    unique_reviews = df["Review"].dropna().unique()

    print(f"Translating {len(unique_reviews)} unique reviews...")

    for i, review in enumerate(unique_reviews, start=1):
        try:
            translation_map[review] = translator.translate(review)
        except Exception:
            translation_map[review] = review

        if i % 100 == 0:
            print(f"{i}/{len(unique_reviews)}")

    df["Review_EN"] = df["Review"].map(translation_map)

    return df