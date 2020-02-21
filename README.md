# Smart Meeting Room

*This scans the meeting room and update the status on Salesforce cloud. Then mobile application can be used to check the status of the meeting room (Occupied or Vacant)*

## Project Structure

* ***human_detector.py*** - This class will detect the presence of person in room.
* ***salesforce_connection.py*** - This class helps python to connect with your salesforce cloud.
* ***MeetingRoomPersonDetector.py*** - This is the main class which monitors the presence and post the data to cloud.

### Deep Neural Netwrok
* SSD Caffe model (Single shot multibox detector). It is by far the best model to detect multiple objects in realtime.
* Prototext Model

### Hardware
* Raspberry Pi 3 Model b+
* Pi Camera
<img src="https://www.raspberrypi.org/app/uploads/2011/10/Raspi-PGB001.png" height="100" width="100">

### Libraries
* OpenCV
* Imutils
* Simple_Salesforce

### Cloud
* Salesforce IoT

![Salesforce Cloud](https://jaimahakal-dev-ed.my.salesforce.com/img/seasonLogos/Spring_20_175x65.png)

> You can use saleforce iot cloud application for free. I have setup custom object, context, orchestrtion in salesforce.

## Coding Background

```python
    WINDOW_DETECTION = 5    # Number of loops a camera will check to take decision on the occupancy
    PRESENCE_THRESHOLD = 3  # Minimum Presence should be this to mark room as occupied else vacant
    VACANCY_THRESHOLD = 1   # Room will be marked as vacant after this threshold meets
```
