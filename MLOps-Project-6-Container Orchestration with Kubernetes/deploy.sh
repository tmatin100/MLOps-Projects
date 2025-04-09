#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Kubernetes deployment..."

# Function to check if a resource is ready
check_resource_ready() {
    local resource_type=$1
    local resource_name=$2
    local namespace=${3:-default}
    local timeout=300  # 5 minutes timeout
    local interval=10  # Check every 10 seconds
    local elapsed=0

    echo "Waiting for $resource_type/$resource_name to be ready..."
    while [ $elapsed -lt $timeout ]; do
        if kubectl get $resource_type $resource_name -n $namespace -o jsonpath='{.status.conditions[?(@.type=="Available")].status}' 2>/dev/null | grep -q "True"; then
            echo "✅ $resource_type/$resource_name is ready!"
            return 0
        fi
        sleep $interval
        elapsed=$((elapsed + interval))
    done
    echo "❌ Timeout waiting for $resource_type/$resource_name to be ready"
    return 1
}

# Create namespace if it doesn't exist
echo "📁 Creating namespace if it doesn't exist..."
kubectl create namespace ai-compose --dry-run=client -o yaml | kubectl apply -f -

# Apply ConfigMap
echo "📝 Applying ConfigMap..."
kubectl apply -f configmap.yaml -n ai-compose

# Apply PersistentVolume and PersistentVolumeClaim
echo "💾 Applying PersistentVolume and PersistentVolumeClaim..."
kubectl apply -f model-pv.yaml -n ai-compose

# Apply Model deployment and service
echo "🤖 Deploying Model service..."
kubectl apply -f model-deployment.yaml -n ai-compose
check_resource_ready "deployment" "model" "ai-compose"

# Apply Backend deployment and service
echo "⚙️ Deploying Backend service..."
kubectl apply -f backend-deployment.yaml -n ai-compose
check_resource_ready "deployment" "backend" "ai-compose"

# Apply Frontend deployment and service
echo "🎨 Deploying Frontend service..."
kubectl apply -f frontend-deployment.yaml -n ai-compose
check_resource_ready "deployment" "frontend" "ai-compose"

# Get the external IP for the frontend service
echo "🌐 Getting Frontend service external IP..."
echo "Waiting for LoadBalancer to get external IP..."
sleep 30  # Give some time for the LoadBalancer to provision

FRONTEND_IP=$(kubectl get service frontend -n ai-compose -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ -z "$FRONTEND_IP" ]; then
    echo "⚠️ Could not get external IP for frontend service"
    echo "You can check the status with: kubectl get service frontend -n ai-compose"
else
    echo "✅ Frontend service is accessible at: http://$FRONTEND_IP:3000"
fi

# Print deployment status
echo "📊 Deployment Status:"
kubectl get pods -n ai-compose -o wide
kubectl get services -n ai-compose

echo "✨ Deployment completed! You can monitor the pods with:"
echo "kubectl get pods -n ai-compose -w" 