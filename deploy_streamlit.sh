#!/bin/bash

set -euo pipefail

PROJECT_ID="hospital-healthcare-analysis"
REGION="us-west2"
SERVICE_NAME="ai-hospital-researcher"
SECRET_NAME="github-models-token"

gcloud config set project "${PROJECT_ID}"

gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    bigquery.googleapis.com

PROJECT_NUMBER="$(
    gcloud projects describe "${PROJECT_ID}" \
        --format="value(projectNumber)"
)"

SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/bigquery.jobUser" \
    --quiet

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/bigquery.dataViewer" \
    --quiet

gcloud secrets add-iam-policy-binding "${SECRET_NAME}" \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor" \
    --quiet

gcloud run deploy "${SERVICE_NAME}" \
    --source=. \
    --region="${REGION}" \
    --allow-unauthenticated \
    --service-account="${SERVICE_ACCOUNT}" \
    --set-env-vars="GCP_PROJECT_ID=${PROJECT_ID},BIGQUERY_DATASET=healthcare_gold" \
    --set-secrets="GITHUB_TOKEN=${SECRET_NAME}:latest" \
    --memory=1Gi \
    --cpu=1 \
    --timeout=300 \
    --max-instances=3 \
    --quiet

gcloud run services describe "${SERVICE_NAME}" \
    --region="${REGION}" \
    --format="value(status.url)"
