FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and modules
COPY main.py .
COPY trading_engine.py .
COPY tax_optimizer.py .
COPY goal_tracker.py .
COPY coinbase_integration.py .

# Create data directory
RUN mkdir -p /data

EXPOSE 8080

# Run with minimal resources
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1", "--threads", "2"]
