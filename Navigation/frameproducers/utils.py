import sys
import traceback
import logging
import zlib
import time

from pathlib import Path

log = logging.getLogger(Path(__file__).stem)


def prepare_binary(frame):
    print("-----3-----")
    ser = zlib.compress(frame.tostring())
    data = str(frame.ravel())
    log.debug("------------------ Metadata ------------------")

    log.debug("type ser:" + str(type(ser)))
    log.debug("type frame:" + str(type(frame)))
    log.debug("type data:" + str(type(data)))
    log.debug("type reshape:" + str(type(frame.reshape(-1))))

    log.debug("size ser:" + str(sys.getsizeof(ser)))
    log.debug("size frame:" + str(sys.getsizeof(frame)))
    log.debug("size data:" + str(sys.getsizeof(data)))
    log.debug("size reshape:" + str(sys.getsizeof(frame.reshape(-1))))

    log.debug("len ser:" + str(len(ser)))
    log.debug("len frame:" + str(len(frame)))
    log.debug("len data:" + str(len(data)))
    log.debug("len reshape:" + str(len(frame.reshape(-1))))

    log.debug("type a:" + str(type(frame.reshape(-1)[0])))

    log.debug("type asint:" + str(type(frame.reshape(-1).astype(int)[0])))
    timestamp = int(time.time())
    try:
        print("-----4-----")
        # value_bytes = bytes(str(frame.flatten()), encoding='utf-8')
        # value_bytes = str(frame.ravel())
        # value_bytes = frame.tobytes()
        key = {"key": str(time.time())}
        # value = {"frame": list(frame.reshape(-1).astype('int')), "shape": list(frame.shape)}
        value = {"frame": ser, "shape": list(frame.shape), "timestamp": str(timestamp), "camid": str("drone1")}

        log.debug("------------------ Key ------------------")
        log.debug(key)

        log.debug("------------------ Value without frame------------------")
        log.debug({"shape": list(frame.shape), "timestamp": str(timestamp), "camid": str("drone1")})
    except Exception as ex:
        e, _, ex_traceback = sys.exc_info()
        log_traceback(log, ex, ex_traceback)
        print(" ---------- ERROR on binary preparation ----------")
        exit(0)

    return key, value

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


def log_traceback(log, ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    log.error(tb_lines)



def acked2(err, msg):
    if err is not None:
        # print("Failed to deliver message: {0}: {1}".format(msg.value(), err.str()))
        # print("Failed to deliver message: {0}: {1}".format(msg.value(), err.str()))
        print("Failed to deliver message: {}".format(err))
    else:
        print("no kaka")
        print("Failed to deliver message: {}".format(msg))
        # print("Message produced: {0}".format(msg.value()))
        # print('Message delivered to topic:{} partition:[{}]'.format(msg))
        # print('Message delivered withg key: {} to topic:{} partition:[{}]'.format(msg.key().decode('utf-8'), msg.topic(), msg.partition()))


