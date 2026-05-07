#!/bin/bash
set -e

echo "🚀 Deploying to Cloud Run..."

if [ -z "$PROJECT_ID" ]; then
  echo "❌ Please set PROJECT_ID first"
  exit 1
fi

IMAGE="gcr.io/${PROJECT_ID}/tn-election"
SERVICE="tn-election-intel"

# Build & Push
docker build -t "$IMAGE" .
docker push "$IMAGE"

# Deploy
gcloud run deploy "$SERVICE" \
  --image "$IMAGE" \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars VERTEX_API_KEY=${VERTEX_KEY},GCP_PROJECT_ID=${PROJECT_ID},BIGQUERY_DATASET=${BIGQUERY_DATASET:-tn_elections},BIGQUERY_TABLE=${BIGQUERY_TABLE:-results},FIRESTORE_ACTIVITY_COLLECTION=${FIRESTORE_ACTIVITY_COLLECTION:-activity_logs},CLOUD_SQL_INSTANCE=${CLOUD_SQL_INSTANCE},DB_USER=${DB_USER},DB_PASSWORD=${DB_PASSWORD},DB_NAME=${DB_NAME} \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10

echo "✅ Live: $(gcloud run services describe ${SERVICE} --region us-central1 --format='value(status.url)')"
