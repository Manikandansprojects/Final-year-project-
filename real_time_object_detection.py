# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
# import argparse
import imutils
import time
import cv2
import subprocess

# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--prototxt", required=True,
# 	help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
# 	help="path to Caffe pre-trained model")
# ap.add_argument("-c", "--confidence", type=float, default=0.2,
# 	help="minimum probability to filter weak detections")
# args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(
    r"C:\Users\mania\Desktop\Final year project\project\MobileNetSSD_deploy.prototxt",
    r"C:\Users\mania\Desktop\Final year project\project\MobileNetSSD_deploy.caffemodel"
)

# print(args["prototxt"])
# print(args["model"])

print("[INFO] starting video stream...")
cap = cv2.VideoCapture("video.mp4.mp4")  # Or use 0 for webcam

if not cap.isOpened():
    print("[ERROR] Cannot open video stream or file.")
    exit()

# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()

while True:
	count = 0
	ret, frame = cap.read()

	if not ret or frame is None:
		print("[INFO] End of stream or failed to grab frame.")
		break

	frame = imutils.resize(frame, width=400)
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	net.setInput(blob)
	detections = net.forward()

	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		idx = int(detections[0, 0, i, 1])

		if confidence > 0.7 and CLASSES[idx] == "person":
			print("People Count ", count)
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			print(startX, endX)
			count += 1
			label1 = "People Count " + str(count)

			cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15

			cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	label1 = "People Count " + str(count)
	cv2.putText(frame, label1, (20, 20),
				cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 0, 0), 1)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

	fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
cap.release()
# vs.stop()

