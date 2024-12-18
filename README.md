# **Zoner MVP - Event-Driven Backend**

Zoner is a real-time platform designed to help users optimize their circadian rhythms, manage jet lag, and adjust to new time zones. This Proof of Concept (PoC) demonstrates the backend architecture for ingesting, processing, and storing user activity data using Kafka, Python, Snowflake, and Redis.

---

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [How It Works](#how-it-works)

---

## **Project Overview**

This project implements a real-time event-driven architecture to handle user activity data, such as:
- Sleep schedules
- Meal timings
- Light exposure data

The platform ingests user activity events, processes them in real-time, and stores the data in Snowflake for further analytics and recommendations.

---

## **Architecture**

### **High-Level Architecture**
```plaintext
[User Activity Events (Producer)] --> [Kafka (Event Broker)] --> [Python Consumer] --> [Snowflake (Database)]
```

### **Components**
1. **Kafka**: A distributed message broker that ingests user activity events.
2. **Python Producer**: Simulates real-time user activity and publishes events to Kafka.
3. **Python Consumer**: Processes Kafka events and stores them in Snowflake.
4. **Snowflake**: Cloud-based data warehouse for storing and analyzing user activity data.
5. **Redis**: Caching layer for real-time recommendations (optional for this MVP).

---

## **Technologies Used**

- **Apache Kafka**: Real-time event streaming.
- **Python**: For producing and consuming Kafka events.
- **Snowflake**: Data warehouse for storing user activity data.
- **Redis**: In-memory database for caching recommendations (optional).
- **Docker Compose**: Orchestrates multi-container deployment.
- **Dotenv**: Securely manages environment variables.

---

## **Setup Instructions**

### **1. Prerequisites**
- Install Docker Desktop
- Install Python 3.x
- Create a Snowflake account and set up credentials.

### **2. Clone the Repository**
```bash
git clone https://github.com/cynthialmy/zoner-mvp.git
cd zoner-mvp
```

### **3. Set Up Environment Variables**
Create a `.env` file in the `python` directory with the following variables:

```plaintext
KAFKA_BROKER=kafka:9092
SNOWFLAKE_USER=<your_snowflake_username>
SNOWFLAKE_PASSWORD=<your_snowflake_password>
SNOWFLAKE_ACCOUNT=<your_snowflake_account_identifier>
SNOWFLAKE_DATABASE=ZONER_DB
SNOWFLAKE_SCHEMA=PUBLIC
```

### **4. Start the Services**
Use Docker Compose to start all services (Kafka, Zookeeper, Redis, and Python).

```bash
docker-compose up --build
```

### **5. Verify Kafka**
- Create the `user_activity` topic:
  ```bash
  docker-compose exec kafka kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user_activity
  ```
- Verify the topic:
  ```bash
  docker-compose exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092
  ```

### **6. Test the Data Pipeline**
- Check Python producer logs to verify events are being produced:
  ```bash
  docker-compose logs python
  ```
- Verify Snowflake:
  - Log in to Snowflake.
  - Query the `user_activity` table:
    ```sql
    SELECT * FROM ZONER_DB.PUBLIC.USER_ACTIVITY;
    ```

---

## **How It Works**

1. **Producer**:
   - The `producer.py` script generates random user activity events (e.g., sleep, meal).
   - Events are published to Kafka’s `user_activity` topic.

2. **Consumer**:
   - The `consumer.py` script reads events from Kafka.
   - Processes the data and inserts it into the Snowflake `user_activity` table.

3. **Database**:
   - Snowflake stores user activity data, which can be queried for analysis or used to generate recommendations.
