from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from pathlib import Path
import os

from src.config import FIRESTORE_ACTIVITY_COLLECTION, GCP_PROJECT_ID


@lru_cache(maxsize=1)
def _get_client():
	adc_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
	if adc_path and not Path(adc_path).exists():
		raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS points to a missing file")
	if not adc_path:
		raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS is not set for local Firestore usage")

	try:
		from google.cloud import firestore
	except Exception as exc:
		raise RuntimeError("google-cloud-firestore is not installed") from exc
	return firestore.Client(project=GCP_PROJECT_ID)


def fetch_activity_logs(limit: int = 20) -> list[dict]:
	from google.cloud import firestore

	docs = (
		_get_client()
		.collection(FIRESTORE_ACTIVITY_COLLECTION)
		.order_by("timestamp", direction=firestore.Query.DESCENDING)
		.limit(int(limit))
		.stream()
	)

	results: list[dict] = []
	for doc in docs:
		payload = doc.to_dict() or {}
		timestamp = payload.get("timestamp")
		if hasattr(timestamp, "isoformat"):
			timestamp = timestamp.isoformat()
		results.append(
			{
				"id": doc.id,
				"timestamp": timestamp,
				"message": str(payload.get("message", "")),
				"event": str(payload.get("event", payload.get("message", ""))),
			}
		)
	return results


def publish_activity(message: str, event: str | None = None) -> None:
	from google.cloud import firestore

	clean_message = str(message or "").strip()
	if not clean_message:
		return

	_get_client().collection(FIRESTORE_ACTIVITY_COLLECTION).add(
		{
			"timestamp": firestore.SERVER_TIMESTAMP,
			"message": clean_message,
			"event": str(event or clean_message),
			"created_at": datetime.utcnow().isoformat(),
		}
	)
