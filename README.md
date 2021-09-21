



helm install -n shopify-image -f image-kube-charts/test-values.yaml shopify image-kube-charts --create-namespace


minikube service --url shopify