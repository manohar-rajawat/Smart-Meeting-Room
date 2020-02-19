#!/usr/bin/python3.7

#Importing files
import imutils
import time
import numpy as np
import cv2 as cv

class Detector:

#Class Constructor
 def __init__(self,conf):
  self.init_confidence = conf
  self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
  self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
  print ("[INFO] Loading model !!!")
  self.net = cv.dnn.readNetFromCaffe("models/MobileNetSSD_deploy.prototxt.txt","models/MobileNetSSD_deploy.caffemodel")
  self.W = None
  self.H = None

#Class Method to detect the person
 def detect(self,frame):
  self.countPerson = 0;
  self.frame = imutils.resize(frame,width=300)
  if self.W is None or self.H is None:
   (self.H,self.W) = self.frame.shape[:2]
  self.startTime = time.time()
  self.blob = cv.dnn.blobFromImage(self.frame, 0.007843, (self.W,self.H), 127.5)
  print ("[INFO] Detecting Objects ...")
  self.net.setInput(self.blob)
  self.detections = self.net.forward()
  for i in np.arange(0, self.detections.shape[2]):
   self.confidence = self.detections[0,0,i,2]
   if self.confidence > self.init_confidence:
    self.idx = int(self.detections[0,0,i,1])
    if self.CLASSES[self.idx] != "person":
     continue
    self.countPerson += 1
    self.box = self.detections[0,0,i,3:7] * np.array([self.W,self.H,self.W,self.H])
    #(self.startX, self.startY, self.endX, self.endY) = self.box.astype("int")
    self.label = "{}: {:.2f}%".format(self.CLASSES[self.idx], self.confidence * 100)
    print ("[INFO] {}".format(self.label))
    #cv.rectangle(self.frame, (self.startX,self.startY), (self.endX,self.endY),
    #   self.COLORS[self.idx], 2)
    #self.y = self.startY - 15 if self.startY - 15 > 15 else self.startY + 15
  self.endTime = time.time()
  print ("[TIME] Time Taken During Object Detection is : ",self.endTime-self.startTime)
  return self.countPerson

