# 🚀 Kubernetes Pod Autoscaling: FastAPI + Horizontal Pod Autoscaler (HPA)

[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.20%2B-326CE5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Minikube](https://img.shields.io/badge/Minikube-1.25%2B-blue.svg?logo=kubernetes&logoColor=white)](https://minikube.sigs.k8s.io/docs/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10%2B-0db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This project provides a practical, hands-on demonstration of deploying a web application on Kubernetes and configuring **Horizontal Pod Autoscaling (HPA)**. It showcases how your application can automatically scale its resources up or down based on real-time demand, ensuring optimal performance and cost efficiency.

We'll use a lightweight **FastAPI** application that simulates CPU load, deployed on a local Kubernetes cluster (Minikube), to observe HPA in action as traffic increases.

---

## 🎯 Project Objective

The primary goal of this project is to:

* **Deploy a simple FastAPI web application** within a Kubernetes environment using Minikube.
* **Configure and observe Horizontal Pod Autoscaling (HPA)**, demonstrating how Kubernetes automatically scales the number of application pods based on their CPU utilization. This ensures your application handles varying loads efficiently without manual intervention.

---

## 💡 How Horizontal Pod Autoscaling (HPA) Works

HPA in Kubernetes automatically adjusts the number of pod replicas in a Deployment or ReplicaSet based on observed CPU utilization (or other select metrics).

* **Monitoring:** HPA continuously monitors the specified metrics (e.g., CPU, memory) for the pods in a target workload.
* **Thresholds:** You define target thresholds for these metrics (e.g., 50% CPU utilization).
* **Scaling Decision:**
    * If the average metric value across all pods exceeds the target, HPA will **increase** the number of pod replicas (scale out).
    * If the average metric value falls below the target, HPA will **decrease** the number of pod replicas (scale in).
* **Metrics Server:** For CPU and memory-based autoscaling, Kubernetes relies on the `metrics-server` to collect resource usage data from nodes and pods.

This project specifically targets **CPU-based autoscaling**, where our FastAPI app intentionally consumes CPU to trigger the scaling events.

---

## 🛠 Setup & Run Instructions

Follow these steps to deploy the application, configure HPA, and observe autoscaling.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Minikube:** A tool that runs a single-node Kubernetes cluster on your local machine.
    * [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
* **Kubectl:** The Kubernetes command-line tool for interacting with your cluster.
    * [Install Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* **Docker:** Used by Minikube to build and manage container images.
* **Python 3.8+:** For running the `load_test.py` script.

### Step-by-Step Guide

1.  **Start Minikube and Set Docker Environment:**
    First, start your Minikube cluster. Then, configure your local Docker daemon to use Minikube's Docker environment. This ensures that any Docker images you build locally are available within the Minikube cluster.

    ```bash
    minikube start
    # For Linux/macOS:
    eval $(minikube -p minikube docker-env)
    # For Windows (PowerShell):
    minikube -p minikube docker-env | Invoke-Expression
    ```

2.  **Build Docker Image inside Minikube:**
    Navigate to the project's root directory (`Kubernetes-Pod-Scaling-K8s-HPA-/`). Build the Docker image for your FastAPI application. Since you set the Docker environment to Minikube, this image will be built directly into Minikube's Docker daemon, making it accessible to Kubernetes.

    ```bash
    docker build -t fastapi-cpu-app ./app
    ```
    *(You should see output indicating the image is being built)*

3.  **Apply Kubernetes Resources:**
    Now, deploy your application and configure HPA using the provided Kubernetes YAML files.

    ```bash
    # Deploy the FastAPI application as a Kubernetes Deployment
    kubectl apply -f k8s/deployment.yaml

    # Create a Kubernetes Service to expose the FastAPI app
    kubectl apply -f k8s/service.yaml

    # Enable the Kubernetes Metrics Server (essential for HPA to get CPU/memory metrics)
    minikube addons enable metrics-server

    # Apply the Horizontal Pod Autoscaler configuration
    kubectl apply -f k8s/hpa.yaml
    ```
    *You should see confirmations like `deployment.apps/fastapi-cpu-app-deployment created`, `service/fastapi-service created`, `metrics-server enabled`, and `horizontalpodautoscaler.autoscaling/fastapi-hpa created`.*

---

## 🚀 Run the Application & Trigger Autoscaling

1.  **Get the Service URL:**
    Find out the URL through which you can access your FastAPI application deployed in Minikube.
    ```bash
    minikube service fastapi-service --url
    ```
    *This will output a URL like `http://192.168.49.2:30000`.*

2.  **Access the Application:**
    Open the URL obtained in the previous step in your web browser. You should see a simple JSON response:
    ```json
    {"message": "CPU Load generated!"}
    ```
    This confirms your app is running. Note that accessing this endpoint *generates* CPU load on the pod.

3.  **Trigger Autoscaling with a Load Test:**
    To see HPA in action, we need to generate significant traffic to increase the CPU usage of the pods.
    Open a **new terminal window** and run the provided load testing script:

    ```bash
    python load_test.py
    ```
    *This script sends a high volume of requests to your FastAPI service, continuously stressing its CPU.*

4.  **Monitor Scaling in Real-Time:**
    In **another new terminal window** (keep the load test running), you can observe the HPA and pod scaling status:

    ```bash
    # Watch the Horizontal Pod Autoscaler status
    kubectl get hpa -w

    # Watch the current pods in your deployment
    kubectl get pods -w
    ```
    * You will initially see `fastapi-hpa` showing `1/10` (1 replica, targeting up to 10).
    * As the load test runs, you'll observe the `TARGETS` (CPU utilization) increasing.
    * Soon after, Kubernetes will automatically create new pods, scaling your application from the initial `1` replica up to the configured maximum of `10` pods to handle the increased CPU load. You'll see new pods appearing in the `kubectl get pods -w` output.
    * Once the load test finishes (or if you stop it), after a brief cool-down period, you'll see the HPA scale down the pods back to the minimum replica count (1 in `k8s/deployment.yaml`).

---

## 📦 Folder Structure

k8s-autoscale-project/
├── app/                        # Contains the FastAPI application and its Dockerfile
│   ├── main.py                 # FastAPI app: responds with a message and generates CPU load
│   └── Dockerfile              # Dockerfile to containerize the FastAPI app
├── k8s/                        # Kubernetes manifest files
│   ├── deployment.yaml         # Defines the Kubernetes Deployment for the FastAPI app
│   ├── service.yaml            # Defines the Kubernetes Service to expose the app
│   └── hpa.yaml                # Defines the Horizontal Pod Autoscaler configuration
├── load_test.py                # Python script to simulate high traffic and trigger autoscaling
├── README.md                   # This comprehensive project documentation
└── SUMMARY.md                  # A brief overview of the project

---

## ✅ Features Demonstrated

This project effectively showcases several key Kubernetes and cloud-native concepts:

* **Dockerized FastAPI Application:** A simple Python web application packaged into a Docker image for consistent deployment.
* **Kubernetes Deployment:** Correctly deploying an application using Kubernetes Deployment resources.
* **Kubernetes Service:** Exposing the deployed application within the cluster and to external traffic via a Service.
* **CPU-Based Horizontal Pod Autoscaling:** Practical implementation and demonstration of HPA, scaling pods from a minimum of 1 up to a maximum of 10 replicas based on CPU utilization.
* **Metrics Server Integration:** Understanding the necessity and enabling the `metrics-server` for HPA to collect performance metrics.
* **Real Traffic Simulation:** Using a Python script to simulate realistic load and observe the autoscaling mechanism respond dynamically.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

* The Kubernetes and Minikube communities for robust container orchestration tools.
* The FastAPI team for an excellent web framework.
* Everyone contributing to open-source software that makes projects like this possible.
