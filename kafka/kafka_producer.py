import sys
import json
import logging

from confluent_kafka import avro, Producer, KafkaException
from confluent_kafka.avro import AvroProducer
from confluent_kafka import KafkaError


class KafkaProducer:

    def __init__(self, user_config):
        self.log = logging.getLogger("KafkaProducer")
        self._config = user_config
        self._properties = {}
        self.producer = self.get_kafka_producer()

    def get_kafka_producer(self):
        # return a producer instance
        # :param: producer configuration
        self._properties["error_cb"] = self.error_cb
        self._properties["bootstrap.servers"] = self._config.get('bootstrap.servers')
        # self._properties["schema.registry.url"] = self._config.get('schema.registry')
        # if self._config.get('security_protocol') != 'None':
        #     self.add_property("security.protocol", self._config.get('security_protocol'))
        #     self.add_property("ssl.key.password", self._config.get('kafka-cert-password'))

        if self._config.get('avro_producer') and self._config.get('schema_registry') is not None:
            self.add_property("schema.registry.url", self._config.get('schema_registry'))
            key_schema = avro.loads(self._AVRO_SCHEMA_KEY)
            value_schema = avro.loads(self._AVRO_SCHEMA_VALUE)
            producer = AvroProducer(self._properties, default_key_schema=key_schema, default_value_schema=value_schema)
        else:
            producer = Producer(self._properties)

        return producer

    def send(self, key=None, value=None, param="", topic="undefined", partition=None):
        #source_type = self._config.get(self._SOURCE_TYPE)
        #partition = self.get_partition_from_source(param=param)  # Obtain dataloha partition from dictionary

        # (key, value) = self.utils.getKeyValue(key, value, self._config)

        #if source_type == self._SOURCE_TYPE_FOLDER:
        #    self.send_folder(topic, value, key, partition)
        #elif source_type == self._SOURCE_TYPE_FILE:
        #    self.send_file(topic, value, key, partition)
        #else:
         #   if sys.getsizeof(value) > 1000000:
          #      self.send_values(topic, value, key, partition)
                # self.send_values(topic, kafka_partitioner(value), key, partition)
         #   else:
        #        if isinstance(value, (list,)):
        #            self.send_values(topic, value, key, partition)
        #        elif isinstance(value, (dict,)):
        #            self.send_value(topic, value, key, partition)
        #        else:
        self.send_value(topic, value, key, partition)



    def send_folder(self, topic, value, key=None, partition=None):
        '''
        get all the files contained in a folder
        '''
        files = self.utils.getFiles(value)        
        for f in files:
            self.send_file(topic, f, key, partition)

    def send_file(self, topic, value, key=None, partition=None):
        '''
        read file and send to broker line by line
        '''
        with open(value, 'r') as f:
            for line in f:
                self.send_value(topic, line, key, partition, flush=False)
            self.flush(True)

    def send_values(self, topic, values, key=None, partition=None):
        try:
            for value in values:
                self.producer.produce(topic=topic, value=self.prepare_value(value), key=self.prepare_key(key),
                                      partition=partition,
                                      callback=(None, self.utils.delivery_callback)[self._config.get(self._DEBUG_MODE)])
                
            self.flush(True)
        except KafkaException as e:
            self.log.error("An error was encountered while producing a kafka message: %s", str(e.args[0]))

    def send_value(self, topic, value, key=None, partition=0, flush=True):
        try:  
            self.producer.produce(topic=topic, value=self.prepare_value(value), key=self.prepare_key(key),  callback=self.delivery_callback)
            self.flush(flush)
        except KafkaException as e:
            self.log.error("An error was encountered while producing a kafka message: %s", str(e.args[0]))

    def flush(self, flush):
        if flush:
            if len(self.producer) > 0:
                self.log.debug('%% Waiting for %d deliveries\n' % len(self.producer))
            self.producer.flush()

    def prepare_value(self, value):
        if self._config.get('avro_producer') and self._config.get('schema_registry'):
            return value
        else:
            return json.dumps(value)

    def prepare_key(self, key):
        if self._config.get('avro_producer') and self._config.get('schema_registry'):
            return key
        else:
            return json.dumps(key)

    def error_cb(self, err):
        self.log.error('ERROR_CB --> {}'.format(err))
        if err.code() == KafkaError._ALL_BROKERS_DOWN:
            raise ValueError('ERROR: all brokers down...')
        else:
            print(err.code())
            raise ValueError(err.code())

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(self, err, msg):
        if err:
            self.log.error('Message {} delivery failed: {}'.format(msg.value(), err))
        else:
            self.log.debug('Message {} delivered to {} [{}] Offset: {}'.format(msg.value(), msg.topic(), msg.partition(), msg.offset()))


# Monkey patch to get hashable avro schemas
# https://issues.apache.org/jira/browse/AVRO-1737
# https://github.com/confluentinc/confluent-kafka-python/issues/122
from avro import schema

def hash_func(self):
    return hash(str(self))

schema.EnumSchema.__hash__ = hash_func
schema.RecordSchema.__hash__ = hash_func
schema.PrimitiveSchema.__hash__ = hash_func
schema.ArraySchema.__hash__ = hash_func
schema.FixedSchema.__hash__ = hash_func
schema.MapSchema.__hash__ = hash_func
