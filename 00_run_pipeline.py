import pandas as pd
import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# Сlean Temp Files
# ==========================================

def cleanup_company_files(app_id):

    app_folder = os.path.join(
        "output",
        app_id.replace(".", "_")
    )

    files_to_delete = [
        "embeddings.pkl",
        "cluster_samples.txt",
        "cluster_summary.csv"
    ]

    for file_name in files_to_delete:

        file_path = os.path.join(
            app_folder,
            file_name
        )

        if os.path.exists(file_path):

            os.remove(file_path)

            print(
                f"Deleted temp file: {file_path}"
            )






COMPANY_PIPELINE = [
    "01_collect_reviews.py",
    "02_generate_embeddings.py",
    "03_cluster_reviews.py",
    "04_export_cluster_samples.py",
    "05_cluster_naming.py"
]

GLOBAL_PIPELINE = [
    "06_merge_companies.py",
    "07_topic_grouping.py",
    "08_topic_naming.py",
    "09_topic_consolidation.py",
    "10_apply_business_topics.py"
]

# ==========================================
# PROCESS ALL APPS
# ==========================================

apps = pd.read_csv("apps.csv")

pipeline_start = time.time()

for _, app in apps.iterrows():
    company_start = time.time()

    pd.DataFrame([app]).to_csv(
        "current_app.csv",
        index=False
    )

    print("\n" + "=" * 80)
    print(
        f"PROCESSING: {app['Company']} | {app['AppName']}"
    )
    print("=" * 80)

    company_failed = False

    for script in COMPANY_PIPELINE:

        print(f"\nRunning: {script}")

        result = subprocess.run(
            [sys.executable, script],
            cwd=BASE_DIR,
            text=True
        )

        if result.returncode != 0:

            print(
                f"\nFAILED: {app['Company']} | {app['AppName']}"
            )

            print(
                f"Error in: {script}"
            )

            company_failed = True
            break

    if not company_failed:

        cleanup_company_files(
            app["AppID"]
        )

    company_time = round(
        time.time() - company_start,
        1
    )

    print(
        f"\nCompleted: {app['Company']} | "
        f"{app['AppName']} "
        f"({company_time} sec)"
    )

    if company_failed:
        continue

# ==========================================
# GLOBAL VOC PIPELINE
# ==========================================

print("\n" + "=" * 80)
print("RUNNING GLOBAL VOC PIPELINE")
print("=" * 80)

for script in GLOBAL_PIPELINE:

    print(f"\nRunning: {script}")

    result = subprocess.run(
        [sys.executable, script],
        cwd=BASE_DIR,
        text=True
    )

    if result.returncode != 0:

        print(
            f"\nPipeline stopped. Error in: {script}"
        )

        sys.exit(result.returncode)

print("\n" + "=" * 80)
print("VOC PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 80)