import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://<your-minikube-ip>:<nodeport>/"

# Replace with your real values
URL = "http://127.0.0.1:55833"  # or use the tunnel URL if preferred

def hit_server():
    while True:
        try:
            response = requests.get(URL)
            print(response.json())
        except:
            print("Request failed")
        time.sleep(0.1)

# Use many threads to increase load
with ThreadPoolExecutor(max_workers=30) as executor:
    for _ in range(30):
        executor.submit(hit_server)
