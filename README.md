# Kubernetes-Pod-Scaling-K8s-HPA-
Implemented a scalable K8s deployment with Horizontal Pod Autoscaling


# Kubernetes HPA Project – FastAPI + Horizontal Pod Autoscaler

## 📌 Objective

Deploy a FastAPI app on Kubernetes using Minikube and configure **Horizontal Pod Autoscaling (HPA)** to scale pods based on CPU usage.

---

## 🛠 Setup Instructions

### 1. Start Minikube and Set Docker Env

```bash
minikube start
minikube -p minikube docker-env | Invoke-Expression  # (for PowerShell)
2. Build Docker Image inside Minikube
bash
Copy
Edit
docker build -t fastapi-cpu-app ./app
3. Apply Kubernetes Resources
bash
Copy
Edit
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube addons enable metrics-server
kubectl apply -f k8s/hpa.yaml
🚀 Run the Application
Get the service URL
bash
Copy
Edit
minikube service fastapi-service --url
Open the URL in a browser. You should see:

json
Copy
Edit
{"message": "CPU Load generated!"}
💣 Trigger Autoscaling
Load Testing Script
bash
Copy
Edit
python load_test.py
✅ The script sends many requests to create CPU load.

📈 Monitor Scaling in Real-Time
bash
Copy
Edit
kubectl get hpa -w
kubectl get pods
You’ll observe pods scale from 1 up to 10 based on traffic.

📦 Folder Structure
css
Copy
Edit
k8s-autoscale-project/
├── app/
│   ├── main.py
│   └── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
├── load_test.py
├── README.md
└── SUMMARY.md
✅ Features Demonstrated
FastAPI app dockerized

Kubernetes deployment and service

CPU-based HPA scaling (1 to 10 replicas)

Metrics-server enabled in Minikube

Real traffic simulation for autoscaling test