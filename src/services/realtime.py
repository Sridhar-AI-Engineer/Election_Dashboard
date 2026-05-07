from google.cloud import firestore

from src.config import GCP_PROJECT_ID


def publish_lead_change(constituency_id: str, leading_party: str, vote_share: float) -> None:
    client = firestore.Client(project=GCP_PROJECT_ID)
    client.collection("activity_logs").add(
        {
            "timestamp": firestore.SERVER_TIMESTAMP,
            "message": f"{constituency_id}: lead changed to {leading_party} ({vote_share:.2f}%)",
        }
    )
