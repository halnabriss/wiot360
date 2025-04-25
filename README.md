# wiot360

To run your Kubernetes project using Minikube, follow these steps:

1. Start Minikube
Start Minikube on your machine.

minikube start

2. Create Persistent Volume Claim (PVC) for MySQL

kubectl apply -f mysql-pvc.yaml

3. Create MySQL Deployment

kubectl apply -f mysql-deployment.yaml


4. Create MySQL Service
Now, expose MySQL with the service defined in mysql-service.yaml. This will allow other pods in the cluster to access MySQL.

kubectl apply -f mysql-service.yaml


5. Create Flask API Deployment
kubectl apply -f flask-deployment.yaml

6. Create Flask API Service
kubectl apply -f flask-service.yaml

7. Expose Flask API to the External World
kubectl port-forward --address 0.0.0.0 svc/ip-capture-api 3306:3306

8. Access Flask API
To access your Flask app from outside the cluster, use Minikube’s tunnel feature. In a new terminal window, run:
http://13.218.70.251:3000/
