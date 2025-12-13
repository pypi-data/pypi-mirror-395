import uuid
import json
from confluent_kafka import Producer, Consumer
import time
import logging

logging.basicConfig(
    filename='./logs/app.log',        
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)


class KafkaCluster:
    producer: Producer
    consumer: Consumer
    config: dict = {}
    topic_request: str = None
    topic_response: str = None
    timeout: int = None
    promise: dict = {}

    def __init__(self, config):
        self.config = config
        self.topic_request = config.get("topic", "app")
        self.topic_response = f"{config.get("topic", "app")}-response"
        self.timeout = config.get("kafka_timeout", 30000)
        self.producer = Producer({'bootstrap.servers': config['kafka_urls']})
        self.consumer = Consumer({
            'bootstrap.servers': config['kafka_urls'],
            'group.id': f"{config.get("topic", "app")}-group",
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([self.topic_request, self.topic_response])

        log_info(f'init kafka cluster subscribe topic: {self.topic_request} of group: {config.get("topic", "app")}-group')

    
    def send_message(self, topic, uri, data):
        msg =  {
            "uri": uri,
            "data": data,
            "transaction_id": data.get('transaction_id', str(uuid.uuid4())),
            "topic_request": self.topic_request,
        }

        msg = json.dumps(msg)

        log_info(f'[txId: {data.get("transaction_id")}] send_message to topic: {topic} with data: {msg}')

        self.producer.produce(
            topic=topic,
            key=data.get("transaction_id"),
            value=msg
        )
        self.producer.flush()
    
    def send_message_async(self, topic, uri, data, header = {}):

        msg = {
            "uri": uri,
            "header": header,
            "data": data,
            "transaction_id": data.get('transaction_id', str(uuid.uuid4())),
            "topic_request": self.topic_request,
            "topic_response": self.topic_response,
        }

        self.producer.produce(
            topic=topic,
            key=data.get("transaction_id"),
            value=json.dumps(msg)
        )
        self.producer.flush()

        start = time.time()

        data_response = {}

        while time.time() - start < self.timeout:
            
            if self.promise.get(msg.get("transaction_id")):
                data_response = self.promise.get(msg.get("transaction_id"))
                log_info(f'[txId: {msg.get("transaction_id")}] get response with data: {data_response}')
                self.promise.pop(msg.get("transaction_id"))
                return data_response.get('data', {})
        
        raise TimeoutError("Timeout waiting for response")

    def create_message(self, uri, data, header = {}):
        message =  {
            "uri": uri,
            "header": header,
            "data": data,
            "transaction_id": data.get('transaction_id', str(uuid.uuid4())),
            "topic_request": self.topic_request,
            "topic_response": self.topic_response,
        }
        return json.dumps(message)

    def consume_message(self, topic, callback):
        if len(topic) > 0:
            self.consumer.subscribe(topic)
        while True:
            try:
                msg = self.consumer.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    log_info("Consumer error: {}".format(msg.error()))
                    continue

                data = json.loads(msg.value()) if self.is_json(msg.value()) else {}
                log_info(f'[txId: {data.get("transaction_id")}] consume_message from topic: {msg.topic()} partition: {msg.partition()} offset: {msg.offset()} with data: {data}')
                
                if msg.topic() == self.topic_response:
                    self.promise[data.get("transaction_id")] = data
                    log_info(f"set promise with data: {data}")
                else:
                    res = callback(data)
                    log_info(f'res: {res}')
                    if data.get("topic_response"):
                        self.send_message(data.get("topic_response"), res)
            except Exception as e:
                log_info(f'consume_message error: {e}')
    
    def is_json(self, value = None):
        try:
            json.loads(value)
            return True
        except (ValueError, TypeError):
            return False

