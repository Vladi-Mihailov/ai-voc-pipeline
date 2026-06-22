from google_play_scraper import reviews_all
import pandas as pd
import config
import os

os.makedirs(
    config.APP_FOLDER,
    exist_ok=True
)

# ==========================================
# LOAD
# ==========================================

print("Loading reviews...")

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

# ==========================================
# EMPTY REVIEWS CHECK
# ==========================================

if df.empty:

    print("\nNo reviews found.")
    print(
        f"App: {config.COMPANY} | {config.APP_NAME}"
    )

    raise SystemExit(0)

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

def sentiment(score):

    if score >= config.POSITIVE_MIN:
        return "Positive"

    elif score == config.NEUTRAL_SCORE:
        return "Neutral"

    else:
        return "Negative"

df["sentiment"] = (
    df["score"]
    .apply(sentiment)
)

# ==========================================
# OVERALL SUMMARY
# ==========================================

review_counts = (
    df["sentiment"]
    .value_counts()
)

review_pct = (
    df["sentiment"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

summary = pd.DataFrame({
    "Reviews": review_counts,
    "%": review_pct
})

summary = summary.reindex(
    [
        "Positive",
        "Neutral",
        "Negative"
    ]
)

print("\n==============================")
print("OVERALL SENTIMENT")
print("==============================")
print(summary)

# ==========================================
# MONTHLY SENTIMENT
# ==========================================

monthly_sentiment = (
    df.groupby(
        [
            "Year-Month",
            "sentiment"
        ]
    )
    .size()
    .reset_index(name="Reviews")
)

print("\n==============================")
print("MONTHLY SENTIMENT")
print("==============================")
print(
    monthly_sentiment.head(30)
)

# ==========================================
# MONTHLY KPI
# ==========================================

monthly_kpi = (
    df.groupby("Year-Month")
      .agg(
          Reviews=("score", "count"),
          Avg_Rating=("score", "mean")
      )
      .reset_index()
)

monthly_kpi["Avg_Rating"] = (
    monthly_kpi["Avg_Rating"]
    .round(2)
)

print("\n==============================")
print("MONTHLY KPI")
print("==============================")
print(
    monthly_kpi.tail(24)
)

# ==========================================
# CLEAN REVIEWS
# ==========================================

print("\nCleaning reviews...")

initial_reviews = len(df)

# remove empty reviews
df = df[
    df["content"].notna()
]

# remove duplicates
df = df.drop_duplicates(
    subset=["content"]
)

# reset index
df = df.reset_index(
    drop=True
)

# add ReviewID
df["ReviewID"] = (
    df.index + 1
)

print(
    f"Initial reviews: {initial_reviews}"
)

print(
    f"Reviews after cleaning: {len(df)}"
)

# ==========================================
# OPENAI INPUT FILE
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

reviews_for_ai["Language"] = (
    config.LANGUAGE
)

reviews_for_ai["Platform"] = (
    config.PLATFORM
)

reviews_for_ai["Company"] = (
    config.COMPANY
)

reviews_for_ai["AppName"] = (
    config.APP_NAME
)

reviews_for_ai = reviews_for_ai[
    [
        "ReviewID",
        "Date",
        "YearMonth",
        "Platform",
        "Company",
        "AppName",
        "Language",
        "Rating",
        "Sentiment",
        "Review"
    ]
]

print("\n==============================")
print("OPENAI INPUT FILE")
print("==============================")
print(
    reviews_for_ai.head()
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