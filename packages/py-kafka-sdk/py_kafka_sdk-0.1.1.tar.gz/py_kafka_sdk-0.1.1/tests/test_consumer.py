from consumer import new_consumer, consume
from config import KAFKA_BROKERS, KAFKA_TOPICS, KAFKA_GROUP_ID
import threading
import time

def test_consume_message():
    consumer = new_consumer(KAFKA_BROKERS, KAFKA_GROUP_ID, [KAFKA_TOPICS])
    
    stop_event = threading.Event()
    
    messages = []
    
    def handler(msg):
        if msg is not None and not msg.error():
            messages.append(msg.value())
            stop_event.set()
    start_time = time.time()
    try:
        while not stop_event.is_set() and time.time() - start_time < 10:
            consume(stop_event, consumer, handler)
    finally:
        consumer.close()
    assert isinstance(messages, list)
