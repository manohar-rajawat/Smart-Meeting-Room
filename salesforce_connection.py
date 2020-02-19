#!/usr/bin/python3.7

#Import important packages
from simple_salesforce import Salesforce
import requests
import json

class SalesforceApp:
 def __init__(self):
  self.platformEventUrl = "/services/data/v47.0/sobjects/Meeting_Room__e"
  self.params = {"grant_type": "password",
        "client_id": "3MVG9pe2TCoA1Pf7QaVQAlbbMXsg8iNI0ZeKL._F3UKKLdrbegx2Mfj_s_4M1UtdT01Pr7M3lI8FrLf_X3J1m",
        "client_secret": "577BDA6445FC6298CEE5F201E72D47880EE72394C8C18597FA2C61C922C840FE",
        "username": "manoharsingh1920@gmail.com",
        "password": "Ilovemymomalot10@XArZ9470S3G7budd3VvYgT9C"}
  self.tokenUrl = "https://login.salesforce.com/services/oauth2/token"
  self.statusCode = 0
  req = requests.post(self.tokenUrl,params=self.params)
  if req.status_code == 200:
   self.statusCode = 200
   self.access_token = req.json().get("access_token")
   self.instance_url = req.json().get("instance_url")
   self.createHeader()

 def createHeader(self):
  self.headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s' % self.access_token}
  print ("[HEADER] Headers Crated - Authorization ")

 def getStatusCode(self):
  return self.statusCode

 def getToken(self):
  if self.access_token:
   return self.access_token
  else:
   return 0

 def getInstanceUrl(self):
  if self.instance_url:
   return self.instance_url
  else:
   return 0

#This method is used to publish events
 def publishEvent(self,isEquipped,meetingRoomNumber):
  self.isEquipped = isEquipped
  self.meetingRoomNumber = meetingRoomNumber
  self.params_json = {"Equipped__c": self.isEquipped,"Meeting_Room_Id__c": self.meetingRoomNumber}
  self.resp = requests.post(self.instance_url+self.platformEventUrl,headers=self.headers,data=json.dumps(self.params_json),timeout=10)
  self.r_json = self.resp.json()
  self.data = json.loads(json.dumps(self.r_json))
  if "success" in self.data:
   self.is_success = self.r_json["success"]
   if self.is_success:
    print ("[EVENT] The Platform Event has been published")
    return True
   else:
    print ("[EVENT] There was some Error !!!")
    return False
  else:
   print ("[EVENT] The Event couldn't be published !!!")
   return False
