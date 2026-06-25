## Google Play Mode

The pipeline automatically collects customer reviews from Google Play.

### Required configuration

Populate `apps.csv` with the applications to analyze.

Minimum required fields:

```csv
Platform,Company,AppName,AppID,Language,Country
Android,Exness,Exness,com.exness.android.pa,ar,ae
Android,XM,XM,com.xm.webapp,ar,ae
```

Multiple applications can be specified in the same file.

---

### Configuration

Set the input mode in `config.py`:

```python
INPUT_MODE = "PLAYSTORE"
```

---

### Run

```bash
python 00_run_pipeline.py
```

The pipeline will automatically:

- Download reviews from Google Play
- Clean and deduplicate reviews
- Translate reviews to English (optional)
- Generate embeddings
- Cluster customer feedback
- Generate Meta Topics
- Generate Business Topics
- Produce the final VOC dataset

---

### Output

```
output/voc_business_topics.csv
```

The output contains review-level data for all processed applications.



## CSV Mode

The pipeline supports customer feedback in CSV format.

### Minimum required fields

Only one text column is required.

Option 1:

```csv
Review
The app is slow.
Customer support is excellent.
```

Option 2:

```csv
Comment
The app is slow.
Customer support is excellent.
```

---

### Recommended fields

```csv
Date,Review
2026-06-01,The app is slow.
2026-06-02,Withdrawal takes too long.
```

The pipeline will automatically derive the reporting month from the date.

---

### Full supported format

```csv
ReviewID,Date,YearMonth,Platform,Company,AppName,Language,Rating,Sentiment,Review,Review_EN
1,2026-06-01,2026-06,Survey,My Company,Customer Survey,en,5,Positive,Great service!,Great service!
2,2026-06-02,2026-06,Survey,My Company,Customer Survey,en,1,Negative,Withdrawal is delayed.,Withdrawal is delayed.
```

All columns are optional except the review text.

If a column is missing, the pipeline automatically fills default values where possible.

For example:

- ReviewID → generated automatically
- YearMonth → derived from Date (when available)
- Platform → "Custom"
- Company → "Unknown"
- AppName → "Unknown"
- Language → "en"
- Review_EN → copied from Review (or translated if translation is enabled)