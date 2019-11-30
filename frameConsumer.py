import json

from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from ObjectDetection import Detect

with open('kafka/kafkaconfig.json') as configFile:
    config = json.load(configFile)

consumer = AvroConsumer({
    'bootstrap.servers': config['broker'],
    'group.id': config['groupId'],
    'schema.registry.url': config['schemaRegistryUrl']
    })

consumer.subscribe([config['topic']])

detect = Detect.Detect()

detect.processFrame(consumer)  # TODO think a better way
