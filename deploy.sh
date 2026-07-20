#!/bin/bash

set -e

echo "Deploying Healthcare Analytics Monthly Refresh..."

gcloud functions deploy monthly_pipeline_refresh \
    --gen2 \
    --runtime=python312 \
    --region=us-west2 \
    --source=. \
    --entry-point=monthly_pipeline_refresh \
    --trigger-http \
    --no-allow-unauthenticated \
    --memory=2Gi \
    --timeout=1800s \
    --env-vars-file=env.cloud.yaml

echo ""
echo "Deployment complete!"
