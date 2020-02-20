#!/usr/bin/python3.7

#Import packages from libraries
from salesforce_connection import SalesforceApp
from human_detector import Detector
from imutils.video import VideoStream
import time
import sys


#Defining Constants

VACANT = 0
OCCUPIED = 1

if __name__ == "__main__":
#Calling salesforce class
 MeetingRoomId = "2001"
 sf = SalesforceApp()
 isConnected = sf.getStatusCode();
 if (isConnected == 200):
  print ("[INFO] Salesforce Connection Done !!!")
  detector = Detector(0.6);

#Initialize Camera And Warming it up
  cap = VideoStream(usePiCamera=1).start()
  time.sleep(1.5)

  print ("[INSIDE] Going inside while loop !!!")

  try:
   WINDOW_DETECTION = 5
   PRESENCE_THRESHOLD = 3
   VACANCY_THRESHOLD = 1
   ROOM = VACANT
   COUNTER_VACANCY = 0
   while True:
     #INFINITE LOOP TO CHECK THE STATUS
     DETECTION_VAR = 0
     COUNTER_DETECTION = 0
     while DETECTION_VAR < WINDOW_DETECTION:
      time.sleep(1)
      frame = cap.read()
      frame_2 = detector.detect(frame)
      if frame_2 > 0:
       COUNTER_DETECTION += 1
       COUNTER_VACANCY = 0
      DETECTION_VAR += 1
     print("CounterDetection",COUNTER_DETECTION);
     if ROOM == VACANT and COUNTER_DETECTION >= PRESENCE_THRESHOLD:
      ROOM = OCCUPIED
      sf.publishEvent(True,MeetingRoomId);
      print ("The Room has been set as OCCUPIED");

     if COUNTER_DETECTION < PRESENCE_THRESHOLD:
      COUNTER_VACANCY += 1

     if ROOM == OCCUPIED and COUNTER_VACANCY == VACANCY_THRESHOLD:
      ROOM = VACANT
      sf.publishEvent(False,MeetingRoomId);
      print ("The Room has been set as VACANT");
  except KeyboardInterrupt:
   if ROOM == OCCUPIED:
    ROOM = VACANT
    sf.publishEvent(False,MeetingRoomId)
    print ("The Room has been set as VACANT");

   print ("You pressed CTRL+C !")
   cap.stop()
   print ("Cleanup Done !!!")
   sys.exit(0)

 else:
  print ("[INFO] Error While Connecting Salesforce !!!")
