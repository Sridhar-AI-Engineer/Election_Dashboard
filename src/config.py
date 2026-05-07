import os

try:
    import streamlit as st
except Exception:
    st = None


def _get_secret(key: str, default: str = "") -> str:
    if st is not None:
        try:
            value = st.secrets.get(key)
            if value:
                return str(value)
        except Exception:
            pass
    return os.getenv(key, default)


GCP_PROJECT_ID = _get_secret("GCP_PROJECT_ID", "tn-election-2026")
BIGQUERY_DATASET = _get_secret("BIGQUERY_DATASET", "tn_elections")
BIGQUERY_TABLE = _get_secret("BIGQUERY_TABLE", "results")
GEMINI_API_KEY = _get_secret("VERTEX_API_KEY", "")
GEMINI_MODEL = _get_secret("GEMINI_MODEL", "gemini-1.5-pro")
FIRESTORE_ACTIVITY_COLLECTION = _get_secret("FIRESTORE_ACTIVITY_COLLECTION", "activity_logs")
CLOUD_SQL_INSTANCE = _get_secret("CLOUD_SQL_INSTANCE", "")
DB_USER = _get_secret("DB_USER", "")
DB_PASSWORD = _get_secret("DB_PASSWORD", "")
DB_NAME = _get_secret("DB_NAME", "")
KAGGLE_DATASET_REF = _get_secret("KAGGLE_DATASET_REF", "nuhmanpk/tamil-nadu-assembly-election-results-2026")
KAGGLE_DATASET_LINK = _get_secret("KAGGLE_DATASET_LINK", "")
KAGGLE_FILE_PATH = _get_secret("KAGGLE_FILE_PATH", "")
