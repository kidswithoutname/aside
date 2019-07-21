from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from ObjectDetection.Detect import Detect
import json

with open('kafkaconfig.json') as configFile:
    config = json.load(configFile)

consumer = AvroConsumer({
    'bootstrap.servers': config.broker,
    'group.id': config.groupId,
    'schema.registry.url': config.schemaRegistryUrl
    })

consumer.subscribe([config.topic])

Detect.processFrame(consumer) #@todo think a better way