from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# INPUT SOURCE
# ==========================================

#INPUT_MODE = "PLAYSTORE"
INPUT_MODE = "CSV"
#INPUT_FILE = "input_reviews"
INPUT_FOLDER = "input_revie"
# ==========================================
# OPENAI
# ==========================================

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is not set. Create a .env file."
    )

# ==========================================
# MODELS
# ==========================================

MODEL_EMBEDDINGS = "text-embedding-3-small"
MODEL_TOPICS = "gpt-4.1-mini"

# ==========================================
# CLUSTERING
# ==========================================

DEFAULT_CLUSTERS = 15
MIN_CLUSTERS = 2
REVIEWS_PER_CLUSTER = 5

# ==========================================
# SENTIMENT
# ==========================================

POSITIVE_MIN = 4
NEUTRAL_SCORE = 3

# ==========================================
# APP
# ==========================================

current_app = pd.read_csv("current_app.csv").iloc[0]
PLATFORM = current_app["Platform"]
COMPANY = current_app["Company"]
APP_NAME = current_app["AppName"]

APP_ID = current_app["AppID"]

#STORE_ID = (
#    current_app["StoreID"]
#    if "StoreID" in current_app.index
#    else ""
#)


# ==========================================
# TRANSLATION
# ==========================================

TRANSLATE_REVIEWS = False

LANGUAGE = current_app["Language"]

COUNTRY = current_app["Country"]

# ==========================================
# PLATFORMS
# ==========================================

PLATFORM_ANDROID = "Android"
PLATFORM_IOS = "iOS"

# ==========================================
# OUTPUT
# ==========================================

OUTPUT_DIR = "output"

if INPUT_MODE == "CSV":

    APP_FOLDER = os.path.join(
        "output",
        "csv_input"
    )

else:

    APP_FOLDER = os.path.join(
        "output",
        APP_ID.replace(".", "_")
    )

# ==========================================
# GLOBAL VOC FILES
# ==========================================

VOC_ALL_COMPANIES_FILE = os.path.join(
    OUTPUT_DIR,
    "voc_all_companies.csv"
)

VOC_TOPIC_GROUPS_FILE = os.path.join(
    OUTPUT_DIR,
    "voc_topic_groups.csv"
)

VOC_TOPIC_CONSOLIDATED_FILE = os.path.join(
    OUTPUT_DIR,
    "voc_topic_consolidated.csv"
)

VOC_BUSINESS_TOPICS_FILE = os.path.join(
    OUTPUT_DIR,
    "voc_business_topics.csv"
)

VOC_TOPIC_CLUSTERS_FILE = os.path.join(
    OUTPUT_DIR,
    "topic_clusters.csv"
)

VOC_TOPIC_MAPPING_FILE = os.path.join(
    OUTPUT_DIR,
    "topic_mapping.csv"
)

VOC_BUSINESS_TOPIC_MAPPING_FILE = os.path.join(
    OUTPUT_DIR,
    "business_topic_mapping.csv"
)


# ==========================================
# FILES
# ==========================================
REVIEWS_FILE = os.path.join(APP_FOLDER, "reviews.csv")

EMBEDDINGS_FILE = os.path.join(APP_FOLDER, "embeddings.pkl")

CLUSTERS_FILE = os.path.join(APP_FOLDER, "clusters.csv")

CLUSTER_SUMMARY_FILE = os.path.join(
    APP_FOLDER,
    "cluster_summary.csv"
)

CLUSTER_NAMES_FILE = os.path.join(
    APP_FOLDER,
    "cluster_names.csv"
)

CLUSTER_SAMPLES_FILE = os.path.join(
    APP_FOLDER,
    "cluster_samples.txt"
)

FINAL_FILE = os.path.join(
    APP_FOLDER,
    "voc_final.csv"
)

REVIEWS_DETAILED_FILE = os.path.join(
    APP_FOLDER,
    "reviews_detailed.csv"
)

MONTHLY_SENTIMENT_FILE = os.path.join(
    APP_FOLDER,
    "monthly_sentiment.csv"
)

MONTHLY_KPI_FILE = os.path.join(
    APP_FOLDER,
    "monthly_kpi.csv"
)

# ==========================================
# MULTI APP
# ==========================================

APPS_FILE = "apps.csv"

