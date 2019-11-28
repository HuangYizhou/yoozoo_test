import cv2

import numpy as np

def generate_boxes_confidences_classids(outs, height, width, tconf):
    boxes = []
    confidences = []
    classids = []

    for out in outs:
        for detection in out:
            # Get the scores, classid, and the confidence of the prediction
            scores = detection[5:]
            classid = np.argmax(scores)
            confidence = scores[classid]
            
            if confidence > tconf:
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, bwidth, bheight = box.astype('int')

                # Using the center x, y coordinates to derive the top
                # and the left corner of the bounding box
                x = int(centerX - (bwidth / 2))
                y = int(centerY - (bheight / 2))

                # Append to list
                boxes.append([x, y, int(bwidth), int(bheight)])
                confidences.append(float(confidence))
                classids.append(classid)
                #print(confidence, labels[classid])

    return boxes, confidences, classids


def detectObjects(frame, net, outputlayers, object_confidence):
  height,width,channels = frame.shape
  #detecting objects
  blob = cv2.dnn.blobFromImage(frame,1/225.0,(416,416),True,crop=False)
  net.setInput(blob)
  outs = net.forward(outputlayers)

  boxes, confidences, classids = generate_boxes_confidences_classids(outs, height, width, object_confidence)
  idxs = cv2.dnn.NMSBoxes(boxes, confidences, object_confidence, 0.6)

  return (boxes, confidences, classids, idxs)
