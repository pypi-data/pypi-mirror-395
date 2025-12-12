# py-kafka-sdk

A simple Python SDK for Apache Kafka, providing:
- Asynchronous producer abstraction
- Multi-threaded consumer utilities
- Batch and single-message consumption

## Requirements
- Python 3.8+
- [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
- A running Kafka broker (see Docker Compose example below)

## Installation

Install dependencies:
```sh
pip install -r requirements.txt
```

## Environment Variables

Configure using a `.env` file or environment variables:

```
KAFKA_BROKERS=localhost:9092
KAFKA_TOPICS=test-topic
KAFKA_GROUP_ID=test-group
```

## Running Kafka Locally (Docker Compose)

See the included `docker-compose.yml` file.

Start Kafka:
```sh
docker-compose up -d
```

## Usage

### Producer Example
See `examples/producer_example.py`:
```sh
python examples/producer_example.py
```

### Consumer Example
See `examples/consumer_example.py`:
```sh
python examples/consumer_example.py
```

## Running Tests

To run all tests (Kafka must be running on localhost:9092):
```sh
pytest tests/test_producer.py
pytest tests/test_consumer.py
```
**Note:** Run the consumer test last, as it waits for a message sent by the producer test.

## Notes
- No brokers or topics are hardcoded; provide them via environment variables or parameters.
- See the code for advanced usage (batch consumption, custom configs, etc).
