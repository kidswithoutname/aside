import cv2
import logging
import numpy as np

from pathlib import Path
from .utils import *

log = logging.getLogger(Path(__file__).stem)


def publish_camera(avroProducer, topic, camvalue):
    np.set_printoptions(infstr='inf')
    cap = cv2.VideoCapture(0)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('capturing.mp4', fourcc, 25, (1280, 720))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            try:
                key, value = prepare_binary(frame)
                avroProducer.produce(topic=topic, value=value, key=key, callback=acked)
                avroProducer.flush()
            except Exception as ex:
                e, _, ex_traceback = sys.exc_info()
                log_traceback(log, ex, ex_traceback)
                return {"logtrace": "HOST UNREACHABLE", "status": "UNKNOWN"}

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


