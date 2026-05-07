# TN 2026 Election Intelligence Platform (Google Cloud Edition)

Production-style Streamlit dashboard for Tamil Nadu election analytics with dynamic Kaggle dataset ingestion and Google Cloud service integrations:
- Cloud Run (deployment)
- BigQuery (analytics)
- Firestore (real-time activity)
- Cloud SQL Postgres (persistence)
- Vertex AI Gemini (AI insights)

## Project Structure

- `app.py` - Main Streamlit dashboard
- `src/config.py` - Configuration from secrets/env
- `src/services/bigquery_service.py` - Constituency result query
- `src/services/firestore_service.py` - Activity feed query
- `src/services/gemini_service.py` - Gemini-based insights
- `src/services/kaggle_service.py` - KaggleHub dynamic dataset loader/normalizer
- `src/services/database.py` - Cloud SQL SQLAlchemy engine
- `src/services/realtime.py` - Firestore activity write helper

## Quickstart (2 mins)

1. `pip install -r requirements-google.txt`
2. `cp .streamlit/secrets.toml.example .streamlit/secrets.toml`  # Add keys
3. Set dataset source in `.env` or `.streamlit/secrets.toml`:
   - `KAGGLE_DATASET_REF` or `KAGGLE_DATASET_LINK`
   - Optional `KAGGLE_FILE_PATH`
4. `python fetch_data.py`  # Pull dynamic Kaggle data
5. `streamlit run app.py`

The dashboard uses Kaggle dataset data paths only (no sample/static dataset fallback in app flow).

## BigQuery Table Contract

Expected columns in `results` table:
- `constituency_name` (STRING)
- `leading_party` (STRING)
- `vote_share` (FLOAT)
- `lat` (FLOAT)
- `lon` (FLOAT)

## Production

`./deploy.sh`  # Cloud Run live URL

Tech: Google Cloud services + Kaggle dataset ingestion
Data: Kaggle dynamic dataset (configurable via env/secrets)

## Deploy to Cloud Run (Manual)

1. Set project:
   - `gcloud config set project YOUR_PROJECT_ID`
2. Enable APIs:
   - `gcloud services enable run.googleapis.com bigquery.googleapis.com firestore.googleapis.com sqladmin.googleapis.com aiplatform.googleapis.com`
3. Deploy:
   - `gcloud run deploy tn-election --source . --allow-unauthenticated --region us-central1`
4. Add runtime environment variables/secrets in Cloud Run for all keys from `.env.example`.

## Demo Checklist

- [ ] Kaggle data auto-fetch
- [ ] Vertex AI insights live
- [ ] BigQuery queries working
- [ ] Firestore real-time feed
- [ ] Glassmorphism UI + animations
- [ ] Cloud Run URL ready
- [ ] Metric callout for pitch (example: "DMK 108 seats, +12% swing detected")

## Notes

- `VERTEX_API_KEY` is used for Gemini insight generation.
- For production, use Secret Manager for API keys and DB passwords.
- `src/services/realtime.py` can be used by a Cloud Function trigger to push activity updates.
- Use `KAGGLE_DATASET_LINK` when you want to pass a Kaggle dataset URL; the app resolves it to `<owner>/<dataset>` automatically.
