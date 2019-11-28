import cv2
import numpy as np

def draw_face_boxes(frame,face_locations, face_names, scale):
	#draw facial box
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		top = int(top/scale)
		right = int(right/scale)
		bottom = int(bottom/scale)
		left = int(left/scale)

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	return frame

def draw_object_boxes(frame, boxes, confidences, classids, idxs, labels):
	colors= np.random.uniform(0,255,size=(len(labels),3))
	if len(idxs) > 0:
		for i in idxs.flatten():
			if labels[classids[i]] != "":
				x, y = boxes[i][0], boxes[i][1]
				w, h = boxes[i][2], boxes[i][3]
				
				# Get the unique color for this class
				color = [int(c) for c in colors[classids[i]]]

				# Draw the bounding box rectangle and label on the image
				cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
				text = "{}: {:4f}".format(labels[classids[i]], confidences[i])
				cv2.putText(frame, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

	return frame