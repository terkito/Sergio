#!/bin/bash

export PROJECT_ID="YOUR-PROJECT-ID"

echo "🟥 BUILDING AND PUSHING STREAMLIT FRONTEND TO ARTIFACT REGISTRY..."
export FRONTEND_TAG="us-central1-docker.pkg.dev/$PROJECT_ID/fixmycar/frontend-cloud-sql:latest"
cd frontend
docker build --platform linux/amd64 -t $FRONTEND_TAG .
docker push $FRONTEND_TAG

echo "☕ BUILDING AND PUSHING JAVA BACKEND TO ARTIFACT REGISTRY..."
cd ../backend
export BACKEND_TAG="us-central1-docker.pkg.dev/$PROJECT_ID/fixmycar/backend-cloud-sql:latest"
docker build --platform linux/amd64 -t $BACKEND_TAG .
docker push $BACKEND_TAG

echo "✅ Container build and push complete."
