
#!/bin/bash

#cd ..

helm upgrade --install network-monitor \
  ./helm/k8s-network-monitor \
  -n monitoring \
  --create-namespace

kubectl get deployments -n monitoring

kubectl get pods -n monitoring

# kubectl rollout restart deployment/network-monitor-k8s-network-monitor -n monitoring