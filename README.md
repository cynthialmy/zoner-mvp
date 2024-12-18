# zoner-mvp

This project represents an **MVP real-time data processing pipeline** with a focus on event-driven architecture. It integrates **Kafka** for message streaming, **Redis** for caching, **SQLite** for persistence, and **Python** for processing. Here’s an explanation and critique of the individual components, along with suggestions for improvement.

---

## **Project Overview**

### **Components**
1. **Kafka**: Acts as the message broker, enabling real-time event streaming.
   - **Producer**: Simulates user activity events and sends them to Kafka.
   - **Consumer**: Processes messages from Kafka and stores them in SQLite.

2. **Redis**: Serves as an in-memory cache for pre-aggregated query results, reducing load on SQLite.

3. **SQLite**: Lightweight database used to persist raw user activity data for historical analysis.

4. **Docker Compose**: Manages the deployment of all services in a containerized environment.

5. **Python**: Used for:
   - Producing events (producer.py).
   - Consuming events and persisting them to SQLite (consumer.py).
   - Aggregating data and caching results in Redis (cache_manager.py).

---

## **Explanation of Key Code and Configurations**

### **Kafka**
#### **Dockerfile**
- Uses `confluentinc/cp-kafka:latest` or `bitnami/kafka:latest` images.
- Provides environment variables for Kafka broker configuration:
  - `KAFKA_ZOOKEEPER_CONNECT`: Links Kafka to Zookeeper.
  - `KAFKA_ADVERTISED_LISTENERS`: Exposes the broker for external communication.

#### **Producer**
- Simulates user activity with randomized data (`user_id`, `activity`, `timestamp`).
- Sends messages to Kafka with the `user_activity` topic.

#### **Consumer**
- Reads messages from Kafka, parses them, and writes them into SQLite.
- Ensures a durable storage layer for raw event data.

### **Redis**
- Provides real-time caching for aggregated activity summaries.
- Uses `cache_manager.py` to periodically update the cache with aggregated data from SQLite.

### **SQLite**
- Lightweight relational database.
- Stores raw `user_activity` data with a simple schema (`user_id`, `activity`, `timestamp`).

### **Docker Compose**
- Orchestrates the services: Zookeeper, Kafka, Redis, and Python-based services.
- Volume mounts ensure data persistence and easy code updates during development.

## Setup

```bash
docker compose up
```

## Run

```bash
docker compose exec python python consumer.py
```

## Stop

```bash
docker compose down
```
