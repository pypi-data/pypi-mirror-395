from producer import KafkaProducer
from config import KAFKA_BROKERS, KAFKA_TOPICS

def test_send_message():
    def dummy_report(err, msg):
        pass
    producer = KafkaProducer(KAFKA_BROKERS)
    producer.start_delivery_handler(dummy_report)
    try:
        producer.produce(KAFKA_TOPICS, b"test message from test_send_message")
    except Exception as e:
        assert False, f"Error sending message: {e}"
    finally:
        producer.close()
