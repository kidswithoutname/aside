import numpy as np
import cv2


class Yolo(object):

    # def __new__(self):
    #     if not hasattr(self, 'instance'):
    #         self.instance = super().__new__(self)
    #     return self.instance

    def __init__(self):

        self.labelsPath = '/Users/elvingomez/3lv27/projects/aside/old/tello/TelloTV/objectdetection/data/coco.names'
        self.weightsPath = '/Users/elvingomez/3lv27/projects/aside/old/tello/TelloTV/objectdetection/weights/yolov3.weights'
        self.configPath = '/Users/elvingomez/3lv27/projects/aside/old/tello/TelloTV/objectdetection/cfg/yolov3.cfg'

    def run(self):
        labels = open(self.labelsPath).read().strip().split("\n")

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

        print("[INFO] loading YOLO from disk...", self.__dict__)
        net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)

        layerNames = net.getLayerNames()
        layerNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return net, labels, colors, layerNames

    def getObjectsPreds(self, layerOutputs, W, H, defaultConfidence=0.5):
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > defaultConfidence:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        return boxes, confidences, classIDs

    def printPrediction(self, idxs, labels, colors, boxes, classIDs, confidences, frame):
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in colors[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
