#!/usr/bin/env bash

set -e

# ==============================================================================
# k8s-network-monitor - Kubernetes Deployment Script
#
# Deploys or upgrades the k8s-network-monitor application using the Helm chart
# stored in this repository.
#
# Workflow:
#   1. Install or upgrade the Helm release.
#   2. Wait for the Kubernetes Deployment rollout to complete.
#   3. Display the resulting Deployment, Pods, and Services.
#
# Usage:
#   ./scripts/deploy_app.sh
# ==============================================================================


# -------------------------------------------------------------------
# This script must be run from the repository root.
# We verify that expected repo files/directories are present.
# -------------------------------------------------------------------

if [[ ! -f "Dockerfile" || ! -d "helm/k8s-network-monitor" || ! -d ".git" ]]; then
  echo "ERROR: This script must be run from the k8s-network-monitor repository root."
  echo
  echo "Example:"
  echo "  cd ~/k8s-network-monitor"
  echo "  ./scripts/deploy_app.sh"
  exit 1
fi


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

RELEASE_NAME="network-monitor"
NAMESPACE="monitoring"
CHART_PATH="./helm/k8s-network-monitor"
DEPLOYMENT_NAME="network-monitor-k8s-network-monitor"


# ------------------------------------------------------------------------------
# Deployment
# ------------------------------------------------------------------------------

echo
echo "======================================================================"
echo " Deploying k8s-network-monitor"
echo "======================================================================"
echo "Helm release : ${RELEASE_NAME}"
echo "Namespace    : ${NAMESPACE}"
echo "Helm chart   : ${CHART_PATH}"
echo "======================================================================"
echo


echo "[1/4] Installing/upgrading Helm release..."

helm upgrade --install "${RELEASE_NAME}" \
  "${CHART_PATH}" \
  --namespace "${NAMESPACE}" \
  --create-namespace

echo
echo "Helm deployment completed successfully."


# ------------------------------------------------------------------------------
# Wait for Kubernetes rollout
# ------------------------------------------------------------------------------

echo
echo "[2/4] Waiting for Deployment rollout..."

kubectl rollout status \
  deployment/"${DEPLOYMENT_NAME}" \
  --namespace "${NAMESPACE}" \
  --timeout=120s


# ------------------------------------------------------------------------------
# Display deployed resources
# ------------------------------------------------------------------------------

echo
echo "[3/4] Deployment status:"
echo

kubectl get deployments \
  --namespace "${NAMESPACE}" \
  -o wide


echo
echo "[4/4] Pod and Service status:"
echo

kubectl get pods \
  --namespace "${NAMESPACE}" \
  -o wide

echo

kubectl get services \
  --namespace "${NAMESPACE}"


# ------------------------------------------------------------------------------
# Deployment complete
# ------------------------------------------------------------------------------

echo
echo "======================================================================"
echo " k8s-network-monitor deployment completed successfully"
echo "======================================================================"
echo