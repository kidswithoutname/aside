import cv2
import time
# import json
# import pickle
# import sys
# import base64
import logging
from pathlib import Path
import zlib
import numpy as np
from .utils import *

log = logging.getLogger(Path(__file__).stem)


def prepare_binary(frame):
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

    return value


def publish_camera(avroProducer, topic, camvalue):
    np.set_printoptions(infstr='inf')
    cap = cv2.VideoCapture(0)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('capturing.mp4', fourcc, 25, (1280, 720))
    while(cap.isOpened()):
        ret, frame = cap.read()
        print('image dtype ', frame.dtype)

        if ret == True:
            cv2.imshow('frame', frame)
            value = prepare_binary(frame)

            # ser = ndarray.serialize(frame, compressed=False)
            ser = zlib.compress(frame.tostring())
            # Convert image to a byte array

            # print(type(frame.ravel().tostring()))
            # exit(0)
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

            # print(frame.reshape(-1).dtype)

            # floatImage = np.int(frame.reshape(-1))
            # print('floatImage dtype ', floatImage)



            # x = np.arange(2764800, dtype=np.uint8)
            # np.full_like(x, 1)
            # # print(x)
            # print("len x:", len(x))

            # print(type(image_array))
            # data = cv2.imencode('.jpg', frame)[1].tostring()
            # flat = bytes(image_array[0], encoding='utf-8')
            # print(data)
            # data = pickle.dumps(frame.flatten())
            # print(type(str(data)))

            # print(type(value_bytes))
            # exit(0)
            timestamp = int(time.time())
            try:
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

                # avroProducer.produce(topic, '{0}'.format(frame), callback=acked)
                # avroProducer.produce(topic, frame.raven(), callback=acked)
                # avroProducer.produce(topic, data, callback=acked)
                avroProducer.produce(topic=topic, value=value, key=key, callback=acked)
                avroProducer.flush()

            except Exception as ex:
                e, _, ex_traceback = sys.exc_info()
                log_traceback(log, ex, ex_traceback)
                print(" ---------- ERROR on webcam ----------")
                exit(0)
                return {"logtrace": "HOST UNREACHABLE", "status": "UNKNOWN"}

            # except Exception as e:
            #     print("----------- Error on producer: Webcam -------------")
            #     print(e)
            #     # print("some_error")
            #     exit(0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Imposible to execute directly")
    exit(0)


