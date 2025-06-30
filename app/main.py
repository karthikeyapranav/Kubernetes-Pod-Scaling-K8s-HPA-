# main.py
from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def read_root():
    # Simulate CPU load
    start = time.time()
    while time.time() - start < 1.5:
        pass
    return {"message": "CPU Load generated!"}
