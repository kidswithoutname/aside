import os
import traceback
import logging
import sys
import json

from pathlib import Path
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from frameproducers.utils import prepare_binary


log = logging.getLogger(Path(__file__).stem)
logfile = 'operations.log'


def read_config(config):
    config = json.loads(config)
    return config


def send_to_kafka(config, frame):
    # config = read_config(config)
    config['root_dir'] = os.path.dirname(os.path.abspath(__file__))
    avroProducer = get_avro_producer(config)
    print("-----1-----")
    try:
        print("-----2-----")
        key, value = prepare_binary(frame)
        avroProducer.produce(topic=config['topic'], value=value, key=key, callback=acked)
        avroProducer.flush()
    except Exception as ex:
        e, _, ex_traceback = sys.exc_info()
        log_traceback(log, ex, ex_traceback)
        print("logtrace: {}, status: {}".format("HOST UNREACHABLE", "UNKNOWN"))
    return

def get_avro_producer(config):
    value_schema2 = avro.loads(load_schema_file(os.path.join(config['root_dir'], config['avsc_dir'], 'frames_value.avsc')))
    key_schema2 = avro.loads(load_schema_file(os.path.join(config['root_dir'], config['avsc_dir'], 'frames_key.avsc')))

    try:
        avroProducer = AvroProducer({
            'bootstrap.servers': config['brookers'],
            'schema.registry.url': config['scheme_registry'],
            'message.max.bytes': config['params']['message.max.bytes']
        }, default_key_schema=key_schema2, default_value_schema=value_schema2)
    except Exception as ex:
        e, _, ex_traceback = sys.exc_info()
        log_traceback(log, ex, ex_traceback)
        return {"logtrace": "HOST UNREACHABLE", "status": "UNKNOWN"}

    return avroProducer


def log_traceback(log, ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    log.error(tb_lines)


def get_schema_path(fname):
    dname = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dname, fname)


def load_schema_file(fname):
    fname = get_schema_path(fname)
    with open(fname) as f:
        return f.read()


def acked(error, message):
    # print("delivery_callback. error={}.".format(error, message))
    print("------------------ delivery callback ------------------")
    print("error={}.".format(error))
    print("message.topic={}".format(message.topic()))
    print("message.timestamp={}".format(message.timestamp()))
    print("message.key={}".format(message.key()))
    # print("message.value={}".format(message.value()))
    print("message.partition={}".format(message.partition()))
    print("message.offset={}".format(message.offset()))

