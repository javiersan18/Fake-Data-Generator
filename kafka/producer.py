from .kafka_producer import KafkaProducer

KAFKA_CONFIGUTRATION_JSON_FILE = 'kafka_producer.json'


class Producer:
    def __init__(self, user_config):
        self.kafka_producer = KafkaProducer(user_config)

    def send(self, value, key=None, param="", filename=None, custom_topic=None, kafka_partitioner=None):
        self.kafka_producer.send(value=value, key=key, custom_topic=custom_topic, kafka_partitioner=kafka_partitioner)

