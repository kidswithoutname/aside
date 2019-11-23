import cv2
import numpy as np
import zlib
import time
from ObjectDetection.Yolo import Yolo


class Detect(object):
    W = None
    H = None
    writer = None

    defaultConfidence = 0.5
    defaultThreshold = 0.3

    def __init__(self):
        self.Yolo = Yolo()

    def processFrame(self, avroConsumer):
        net, labels, colors, layerNames = self.Yolo.run()

        while (True):
            try:
                # Capture frame-by-frame
                message = avroConsumer.poll()
                value = message.value()
                key = message.key()
                print(key)
                shape = value['shape']

                frame = zlib.decompress(value['frame'])
                frame = np.fromstring(frame, dtype=np.uint8)
                frame = np.reshape(frame, shape)

                if self.W is None or self.H is None:
                    (self.H, self.W) = frame.shape[:2]

                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                net.setInput(blob)
                start = time.time()
                layerOutputs = net.forward(layerNames)
                end = time.time()

                boxes, confidences, classIDs = self.Yolo.getObjectsPreds(layerOutputs, self.W, self.H)

                idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.defaultConfidence, self.defaultThreshold)

                self.Yolo.printPrediction(idxs, labels, colors, boxes, classIDs, confidences, frame)

                if self.writer is None:
                    filename = '{}.avi'.format(int(time.time()))
                    # initialize our video writer
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    self.writer = cv2.VideoWriter(filename, fourcc, 30, (frame.shape[1], frame.shape[0]), True)

                # write the output frame to disk
                self.writer.write(frame)
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("[INFO] cleaning up...")
                    self.writer.release()
                    avroConsumer.close()
                    cv2.destroyAllWindows()
                    break

            except Exception as e:
                print('Errorrrr!!!!!')
                print(e)
                # release the file pointers
                avroConsumer.close()
                # cv2.destroyAllWindows()
