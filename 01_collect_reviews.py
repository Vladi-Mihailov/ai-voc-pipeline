from google_play_scraper import reviews_all
import pandas as pd
import config
import os

from translate_reviews import translate_reviews
from input_loader import load_csv_reviews
from utils import ensure_standard_columns


os.makedirs(
    config.APP_FOLDER,
    exist_ok=True
)


# ==========================================
# SENTIMENT
# ==========================================

def sentiment(score):

    if pd.isna(score):
        return None

    if score >= config.POSITIVE_MIN:
        return "Positive"

    elif score == config.NEUTRAL_SCORE:
        return "Neutral"

    else:
        return "Negative"


# ==========================================
# PLAYSTORE MODE
# ==========================================

def load_playstore_reviews():

    print("Loading Google Play reviews...")

    if config.PLATFORM == config.PLATFORM_ANDROID:

        reviews = reviews_all(
            config.APP_ID,
            lang=config.LANGUAGE,
            country=config.COUNTRY
        )

    elif config.PLATFORM == config.PLATFORM_IOS:

        raise NotImplementedError(
            "iOS review collection not implemented yet"
        )

    else:

        raise ValueError(
            f"Unknown platform: {config.PLATFORM}"
        )

    df = pd.DataFrame(reviews)

    print(f"Reviews loaded: {len(df)}")

    if df.empty:
        return df

    # ==========================================
    # DATE FIELDS
    # ==========================================

    df["at"] = pd.to_datetime(df["at"])

    df["Year-Month"] = (
        df["at"]
        .dt.strftime("%Y-%m")
    )

    # ==========================================
    # SENTIMENT
    # ==========================================

    df["sentiment"] = (
        df["score"]
        .apply(sentiment)
    )

    # ==========================================
    # CLEAN REVIEWS
    # ==========================================

    print("\nCleaning reviews...")

    initial_reviews = len(df)

    df = df[
        df["content"].notna()
    ]

    df = df.drop_duplicates(
        subset=["content"]
    )

    df = df.reset_index(
        drop=True
    )

    df["ReviewID"] = (
        df.index + 1
    )

    print(f"Initial reviews: {initial_reviews}")
    print(f"Reviews after cleaning: {len(df)}")

    # ==========================================
    # STANDARD FORMAT
    # ==========================================

    reviews_for_ai = df[
        [
            "ReviewID",
            "at",
            "Year-Month",
            "score",
            "sentiment",
            "content"
        ]
    ].copy()

    reviews_for_ai.columns = [
        "ReviewID",
        "Date",
        "YearMonth",
        "Rating",
        "Sentiment",
        "Review"
    ]

    reviews_for_ai["Language"] = config.LANGUAGE
    reviews_for_ai["Platform"] = config.PLATFORM
    reviews_for_ai["Company"] = config.COMPANY
    reviews_for_ai["AppName"] = config.APP_NAME

    return reviews_for_ai


# ==========================================
# CSV MODE
# ==========================================

def load_custom_csv_reviews():

    print("Loading CSV reviews...")

    reviews_for_ai = load_csv_reviews(
        config.INPUT_CSV_FILE
    )

    reviews_for_ai = ensure_standard_columns(
        reviews_for_ai
    )

    reviews_for_ai = reviews_for_ai[
        reviews_for_ai["Review"].notna()
    ]

    reviews_for_ai = reviews_for_ai[
        reviews_for_ai["Review"].astype(str).str.strip() != ""
    ]

    reviews_for_ai = reviews_for_ai.reset_index(
        drop=True
    )

    reviews_for_ai["ReviewID"] = (
        reviews_for_ai.index + 1
    )

    print(f"CSV reviews loaded: {len(reviews_for_ai)}")

    return reviews_for_ai


# ==========================================
# LOAD DATA
# ==========================================

print("Loading reviews...")

if config.INPUT_MODE == "PLAYSTORE":

    reviews_for_ai = load_playstore_reviews()

elif config.INPUT_MODE == "CSV":

    reviews_for_ai = load_custom_csv_reviews()

else:

    raise ValueError(
        f"Unknown INPUT_MODE: {config.INPUT_MODE}"
    )


# ==========================================
# EMPTY REVIEWS CHECK
# ==========================================

if reviews_for_ai.empty:

    print("\nNo reviews found.")
    print(
        f"Source: {config.INPUT_MODE}"
    )

    raise SystemExit(0)


# ==========================================
# ENSURE STANDARD COLUMNS
# ==========================================

reviews_for_ai = ensure_standard_columns(
    reviews_for_ai
)


# ==========================================
# TRANSLATE REVIEWS
# ==========================================

if config.TRANSLATE_REVIEWS:

    print("\nTranslating reviews...")

    reviews_for_ai = translate_reviews(
        reviews_for_ai
    )

else:

    reviews_for_ai["Review_EN"] = (
        reviews_for_ai["Review"]
    )


# ==========================================
# REORDER COLUMNS
# ==========================================

columns = [
    "ReviewID",
    "Date",
    "YearMonth",
    "Platform",
    "Company",
    "AppName",
    "Language",
    "Rating",
    "Sentiment",
    "Review",
    "Review_EN"
]

extra_columns = [
    col
    for col in reviews_for_ai.columns
    if col not in columns
]

reviews_for_ai = reviews_for_ai[
    columns + extra_columns
]


# ==========================================
# PREVIEW
# ==========================================

print("\n==============================")
print("OPENAI INPUT FILE")
print("==============================")
print(
    reviews_for_ai.head()
)

print("\nColumns:")
print(
    reviews_for_ai.columns.tolist()
)


# ==========================================
# SAVE FILES
# ==========================================

reviews_for_ai.to_csv(
    config.REVIEWS_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nFiles saved:")
print(
    config.REVIEWS_FILE
)