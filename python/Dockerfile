# python/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install sqlite3 package
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure we're using the right broker address in the Python code
ENV KAFKA_BROKER="kafka:9092"
ENV REDIS_HOST="redis"

# Add a command to keep the container running
CMD ["tail", "-f", "/dev/null"]
