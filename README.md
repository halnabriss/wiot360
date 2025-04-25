# wiot360
Note 1: Because we need to run our project on Single node, then we need to use minikube in this installation.
Note 2: This repo is cloned to the location /home/ubuntu/wiot360


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

Flask Source code and Dockerfile can be found in app.py , and Dockerfile
I built this docker and uploaded it to my dockerhub account:
halnabriss/ip-capture-api


Prometheus Installation:
1. Install Helm
2. Add Repos:

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

3. Install Prometheus:
helm install prometheus prometheus-community/kube-prometheus-stack

4. Install MySQL Exporter for Prometheus:
helm install mysql-exporter prometheus-community/prometheus-mysql-exporter

5. Configure MySQL Exporter:
Check the values.yaml file , which includes the host, user and password for mysql server.

6. Apply Values configs:
helm upgrade mysql-exporter prometheus-community/prometheus-mysql-exporter -f values.yaml



Note 2: When we work with Kubernettes on the cloud, we can use LoadBalancer to Allow access from external internet to internal pods, but in this installation we are going to use the kubectl port-forward to redirect connections to our containers. This approach makes our container unable to read the real public IP address of the client, but instead it reads the localhost forwarder IP.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

final Checks:
1. Check Running Deployments:
ubuntu@ip-172-31-84-119:~/wiot360$ kubectl get deployment
NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
grafana                                    1/1     1            1           6m38s
ip-capture-api                             1/1     1            1           128m
mysql                                      1/1     1            1           139m
mysql-exporter-prometheus-mysql-exporter   1/1     1            1           33m
prometheus-grafana                         1/1     1            1           36m
prometheus-kube-prometheus-operator        1/1     1            1           36m
prometheus-kube-state-metrics              1/1     1            1           36m



2. Check Pods:
ubuntu@ip-172-31-84-119:~/wiot360$ kubectl get pods
NAME                                                       READY   STATUS    RESTARTS   AGE
alertmanager-prometheus-kube-prometheus-alertmanager-0     2/2     Running   0          37m
grafana-5c89444469-c8clc                                   1/1     Running   0          7m11s
ip-capture-api-685c99cdfb-pvs8d                            1/1     Running   0          129m
mysql-55fb76ff58-vvw5p                                     1/1     Running   0          140m
mysql-exporter-prometheus-mysql-exporter-bbb5d6c7f-ts8l6   1/1     Running   0          19m
prometheus-grafana-55d7d6c6f6-btsm9                        3/3     Running   0          37m
prometheus-kube-prometheus-operator-5bff5b5f5b-gfwtf       1/1     Running   0          37m
prometheus-kube-state-metrics-9d99cb4d9-r5f2f              1/1     Running   0          37m
prometheus-prometheus-kube-prometheus-prometheus-0         2/2     Running   0          37m
prometheus-prometheus-node-exporter-sjnbf                  1/1     Running   0          37m

3. Check Services
kubectl get svc
NAME                                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
alertmanager-operated                      ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   38m
grafana                                    ClusterIP   10.109.141.16    <none>        80/TCP                       8m21s
ip-capture-api                             NodePort    10.111.60.129    <none>        3000:30001/TCP               137m
kubernetes                                 ClusterIP   10.96.0.1        <none>        443/TCP                      154m
mysql                                      NodePort    10.100.208.246   <none>        3306:30306/TCP               152m
mysql-exporter-prometheus-mysql-exporter   ClusterIP   10.102.110.164   <none>        9104/TCP                     35m
prometheus-grafana                         ClusterIP   10.109.242.168   <none>        80/TCP                       38m
prometheus-kube-prometheus-alertmanager    ClusterIP   10.108.63.174    <none>        9093/TCP,8080/TCP            38m
prometheus-kube-prometheus-operator        ClusterIP   10.106.167.94    <none>        443/TCP                      38m
prometheus-kube-prometheus-prometheus      ClusterIP   10.105.29.148    <none>        9090/TCP,8080/TCP            38m
prometheus-kube-state-metrics              ClusterIP   10.108.195.87    <none>        8080/TCP                     38m
prometheus-operated                        ClusterIP   None             <none>        9090/TCP                     38m
prometheus-prometheus-node-exporter        ClusterIP   10.106.235.30    <none>        9100/TCP                     38m



4. Flask Access URL:
http://13.218.70.251:3000/

5. DB Check:
mysql -h 192.168.49.2 -P 30306 -u root -p
#use the passowrd: my-secret-pw
mysql> use ips
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> select * from ip_addresses;
+----+------------+---------------------+
| id | ip         | timestamp           |
+----+------------+---------------------+
|  1 | 10.244.0.1 | 2025-04-25 08:20:19 |
|  2 | 127.0.0.1  | 2025-04-25 08:22:00 |
|  3 | 127.0.0.1  | 2025-04-25 10:05:51 |
|  4 | 127.0.0.1  | 2025-04-25 10:15:31 |
|  5 | 127.0.0.1  | 2025-04-25 10:23:40 |
|  6 | 127.0.0.1  | 2025-04-25 10:31:04 |
+----+------------+---------------------+
6 rows in set (0.04 sec)


6. Prometheus metrics endpoint:
http://13.218.70.251:9104/metrics



