import json
from .kafka_producer import KafkaProducer


class Producer:

    def __init__(self, config):
        self.config = config
        self.kafka_producer = KafkaProducer(self.config)

    @classmethod
    def fromfilename(cls, filename):
        with open(filename) as f:
            cls.config = json.load(f)
            cls.kafka_producer = KafkaProducer(cls.config)
            return cls.kafka_producer

    @classmethod
    def fromdict(cls, datadict):
        cls.config = datadict
        cls.kafka_producer = KafkaProducer(cls.config)
        return cls.kafka_producer

    def send(self, value, key=None, param="", filename=None, custom_topic=None, kafka_partitioner=None):
        self.kafka_producer.send(value=value, key=key, custom_topic=custom_topic, kafka_partitioner=kafka_partitioner)

