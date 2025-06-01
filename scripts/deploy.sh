#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting deployment process...${NC}"

# Check if required tools are installed
command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker is required but not installed.${NC}" >&2; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo -e "${RED}❌ kubectl is required but not installed.${NC}" >&2; exit 1; }

# Set variables
ENVIRONMENT=${1:-staging}
IMAGE_TAG=${2:-latest}
NAMESPACE="crm-shop-${ENVIRONMENT}"

echo -e "${YELLOW}📦 Environment: ${ENVIRONMENT}${NC}"
echo -e "${YELLOW}🏷️  Image tag: ${IMAGE_TAG}${NC}"

# Create namespace if it doesn't exist
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Apply secrets
echo -e "${YELLOW}🔐 Applying secrets...${NC}"
kubectl apply -f k8s/secrets.yml -n ${NAMESPACE}

# Apply database
echo -e "${YELLOW}🗄️  Deploying database...${NC}"
kubectl apply -f k8s/postgres.yml -n ${NAMESPACE}

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=postgres -n ${NAMESPACE} --timeout=300s

# Apply Redis
echo -e "${YELLOW}📦 Deploying Redis...${NC}"
kubectl apply -f k8s/redis.yml -n ${NAMESPACE}

# Update deployment with new image
echo -e "${YELLOW}🔄 Updating deployment...${NC}"
sed "s|your-registry/crm-shop:latest|your-registry/crm-shop:${IMAGE_TAG}|g" k8s/deployment.yml | kubectl apply -f - -n ${NAMESPACE}

# Wait for deployment to be ready
echo -e "${YELLOW}⏳ Waiting for deployment to be ready...${NC}"
kubectl rollout status deployment/crm-shop-web -n ${NAMESPACE} --timeout=300s

# Run migrations
echo -e "${YELLOW}🔄 Running database migrations...${NC}"
kubectl exec -n ${NAMESPACE} deployment/crm-shop-web -- python manage.py migrate

# Collect static files
echo -e "${YELLOW}📁 Collecting static files...${NC}"
kubectl exec -n ${NAMESPACE} deployment/crm-shop-web -- python manage.py collectstatic --noinput

# Get service URL
SERVICE_URL=$(kubectl get service crm-shop-service -n ${NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Service URL: http://${SERVICE_URL}${NC}"

# Run health check
echo -e "${YELLOW}🏥 Running health check...${NC}"
if curl -f "http://${SERVICE_URL}/health/" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check passed!${NC}"
else
    echo -e "${RED}❌ Health check failed!${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Deployment process completed!${NC}"
