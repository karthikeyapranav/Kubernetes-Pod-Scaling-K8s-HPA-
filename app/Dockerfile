# Use a light Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install FastAPI + Uvicorn
RUN pip install fastapi uvicorn

# Copy app code
COPY main.py .

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
