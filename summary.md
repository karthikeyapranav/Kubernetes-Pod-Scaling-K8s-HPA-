
---

### 📄 `SUMMARY.md` (for explanation & reflection)

```markdown
# Summary: Kubernetes Horizontal Pod Autoscaler Project

## 🎯 Goal

Demonstrate Kubernetes Horizontal Pod Autoscaling (HPA) with a CPU-heavy FastAPI app, deployed on a local Minikube cluster.

---

## 🧠 How It Works

1. **FastAPI app (`main.py`)**
   - Every request runs a 1.5s CPU loop
   - Simulates heavy CPU usage

2. **Docker Image**
   - Built inside Minikube environment
   - Image is local, not pulled from Docker Hub

3. **Kubernetes Deployment**
   - Starts with 1 replica
   - Sets CPU resource requests/limits
   - Uses `imagePullPolicy: Never` to use the local image

4. **Kubernetes Service**
   - Exposes the FastAPI app via NodePort
   - Accessed using `minikube service --url`

5. **Horizontal Pod Autoscaler**
   - Monitors CPU usage
   - Scales replicas between 1 and 10
   - Threshold: 50% average CPU usage

6. **Load Testing Script**
   - Simulates multiple clients making requests
   - Triggers autoscaler by increasing CPU load

7. **Scaling Behavior**
   - As load increases, pods scale up
   - When load reduces, pods scale down automatically

---

## ⚙️ Why This Matters

- **Autoscaling ensures high availability and performance**
- Reduces costs by scaling down when idle
- Production-ready pattern used in cloud platforms like AWS EKS, GCP GKE, Azure AKS

---

## 🧪 Observations

- CPU usage increased to 268% → triggered scaling
- Pod count increased from 1 → 6 → 8
- When load script stopped, pods gradually reduced

---

## 🔚 Conclusion

This project demonstrated:
- Real-world autoscaling behavior using CPU metrics
- Efficient traffic handling using horizontal scaling
- Clean integration of Docker, FastAPI, and Kubernetes on Minikube

This forms the foundation for building robust, scalable microservices in production environments.
