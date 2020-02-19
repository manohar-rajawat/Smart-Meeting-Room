#!/usr/bin/python3.7

#Import packages from libraries
from salesforce_connection import SalesforceApp
from human_detector import Detector
import cv2 as cv
import time
import sys

if __name__ == "__main__":
#Calling salesforce class
 sf = SalesforceApp()
 isConnected = sf.getStatusCode();
 if (isConnected == 200):
  print ("[INFO] Salesforce Connection Done !!!")
  detector = Detector(0.5);

#Initialize Camera And Warming it up
  cap = cv.VideoCapture(0)
  time.sleep(1.5)

  print ("[INSIDE] Going inside while loop !!!")

  try:
   PreviousStateEquipped = False
   RoomEquipped = False
   count = 0;
   lst = [];
   while True:
     if count % 5 == 0:
      print ("[LIST] : ",lst)
      if len(lst):
       if lst.count(1)/len(lst) > 0.5:
        RoomEquipped = True
       else:
        RoomEquipped = False
       sf.publishEvent(RoomEquipped,2001)
       lst.clear()
       print ("[LIST] List cleared !!!")

     time.sleep(2) #Wait for 1 second to reduce load
     _,frame = cap.read()
     frame_2 = detector.detect(frame)
     count += 1
     lst.append(1) if frame_2 > 0 else lst.append(0)
     print (" ")
     print ("[OBJECT_COUNT] Objects count is : ",frame_2)
     print (" ")
  except KeyboardInterrupt:
   print ("You pressed CTRL+C !")
   cap.release()
   cv.destroyAllWindows()
   print ("Cleanup Done !!!")
   sys.exit(0)

 else:
  print ("[INFO] Error While Connecting Salesforce !!!")
