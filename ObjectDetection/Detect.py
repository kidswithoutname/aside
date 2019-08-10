import cv2
import numpy as np
import zlib

from ObjectDection.Yolo import Yolo

class Detect:
    W, H, writer = None

    defaultConfidence = 0.5
    defaultTreshold = 0.3

    labelsPath = './.loaders/data/coco.names'
    weightsPath = './.loaders/weights/yolov3.weights'
    configPath = './.loaders/cfg/yolov3.cfg'

    def __init__(self):
        self.Yolo = Yolo(labelsPath, weightsPath, configPath)


    def processFrame(self, avroConsumer):
        net, labels, colors, layerNames = self.Yolo.run()

        while(True):
            try:
                # Capture frame-by-frame
                message = avroConsumer.poll()
                value = message.value()
                key = message.key()
                print(key)
                shape = val['shape']

                frame = zlib.decompress(val['frame'])
                frame = np.fromstring(frame, dtype=np.uint8)
                frame = np.reshape(frame, shape)
                    
                if W is None or H is None:
                    (H, W) = frame.shape[:2]

                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                net.setInput(blob)
                start = time.time()
                layerOutputs = net.forward(layerNames)
                end = time.time()
                
                boxes, confidences, classIDs = self.Yolo.getObjectPreds(layerOutputs)
                
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, defaultConfidence, defaultTreshold)
            
                self.Yolo.printPrediction(idxs, labels, colors, boxes, classIDs, confidences, frame)
                
                if writer is None:
                    filename = '{}.avi'.format(int(time.time()))
                    # initialize our video writer
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    writer = cv2.VideoWriter(filename, fourcc, 30,(frame.shape[1], frame.shape[0]), True)
            
                # write the output frame to disk
                writer.write(frame)
                cv2.imshow('frame',frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    writer.release()
                    cap.release()
                    break

            except Exception as e:
            # print(e)
            print(e)

            # release the file pointers
            print("[INFO] cleaning up...")
            writer.release()
            cap.release()
