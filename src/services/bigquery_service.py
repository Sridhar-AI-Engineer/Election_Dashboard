from __future__ import annotations

from functools import lru_cache

import pandas as pd

from src.config import BIGQUERY_DATASET, BIGQUERY_TABLE, GCP_PROJECT_ID


@lru_cache(maxsize=1)
def _get_client():
	try:
		from google.cloud import bigquery
	except Exception as exc:
		raise RuntimeError("google-cloud-bigquery is not installed") from exc
	return bigquery.Client(project=GCP_PROJECT_ID)


def _table_ref() -> str:
	return f"`{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}`"


def fetch_constituencies(limit: int = 5000) -> list[dict]:
	from google.cloud import bigquery

	query = f"""
		SELECT
			CAST(constituency_name AS STRING) AS constituency_name,
			CAST(leading_party AS STRING) AS leading_party,
			COALESCE(SAFE_CAST(vote_share AS FLOAT64), 0.0) AS vote_share,
			COALESCE(SAFE_CAST(turnout_pct AS FLOAT64), SAFE_CAST(vote_share AS FLOAT64), 0.0) AS turnout_pct,
			SAFE_CAST(lat AS FLOAT64) AS lat,
			SAFE_CAST(lon AS FLOAT64) AS lon
		FROM {_table_ref()}
		ORDER BY constituency_name ASC
		LIMIT @limit
	"""
	job_config = bigquery.QueryJobConfig(
		query_parameters=[bigquery.ScalarQueryParameter("limit", "INT64", int(limit))]
	)
	rows = _get_client().query(query, job_config=job_config).result()
	return [dict(row.items()) for row in rows]


def fetch_constituencies_df(limit: int | None = None) -> pd.DataFrame:
	from google.cloud import bigquery

	query = f"""
		SELECT
			CAST(constituency_name AS STRING) AS constituency_name,
			CAST(leading_party AS STRING) AS leading_party,
			COALESCE(SAFE_CAST(vote_share AS FLOAT64), 0.0) AS vote_share,
			COALESCE(SAFE_CAST(turnout_pct AS FLOAT64), SAFE_CAST(vote_share AS FLOAT64), 0.0) AS turnout_pct,
			SAFE_CAST(lat AS FLOAT64) AS lat,
			SAFE_CAST(lon AS FLOAT64) AS lon,
			CAST(COALESCE(status, 'leading') AS STRING) AS status
		FROM {_table_ref()}
		ORDER BY constituency_name ASC
	"""
	if limit is not None:
		query += "\nLIMIT @limit"
		job_config = bigquery.QueryJobConfig(
			query_parameters=[bigquery.ScalarQueryParameter("limit", "INT64", int(limit))]
		)
		return _get_client().query(query, job_config=job_config).to_dataframe()
	return _get_client().query(query).to_dataframe()


def fetch_party_table() -> list[dict]:
	query = f"""
		SELECT
			CAST(leading_party AS STRING) AS party,
			CAST(leading_party AS STRING) AS party_name,
			COUNT(1) AS won,
			0 AS leading,
			COUNT(1) AS total
		FROM {_table_ref()}
		GROUP BY leading_party
		ORDER BY won DESC, party_name ASC
	"""
	rows = _get_client().query(query).result()
	return [dict(row.items()) for row in rows]


def fetch_top_cards(top_n: int = 7) -> list[dict]:
	from google.cloud import bigquery

	query = f"""
		SELECT
			CAST(leading_party AS STRING) AS party,
			CAST(leading_party AS STRING) AS party_name,
			COUNT(1) AS won
		FROM {_table_ref()}
		GROUP BY leading_party
		ORDER BY won DESC, party_name ASC
		LIMIT @top_n
	"""
	job_config = bigquery.QueryJobConfig(
		query_parameters=[bigquery.ScalarQueryParameter("top_n", "INT64", int(top_n))]
	)
	rows = _get_client().query(query, job_config=job_config).result()
	return [dict(row.items()) for row in rows]


def fetch_total_ac() -> int:
	query = f"""
		SELECT COUNT(1) AS total_ac
		FROM {_table_ref()}
	"""
	rows = list(_get_client().query(query).result())
	return int(rows[0]["total_ac"]) if rows else 0
