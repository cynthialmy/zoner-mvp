FROM confluentinc/cp-kafka:latest

# Set environment variables for Kafka
ENV KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
ENV KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
ENV KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1

# Expose Kafka CLI tools path
WORKDIR /opt/kafka
ENV PATH="/opt/kafka/bin:$PATH"
