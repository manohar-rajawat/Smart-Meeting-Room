#!/usr/bin/python3.7

#Import important packages
from simple_salesforce import Salesforce
import requests
import json
import pytz
import time
import datetime
import sys

LOGIN_DICT =  {'users':{}}
LOGIN_DICT.get('users').update({'SA':{'Email':'YourEmail','Password':'YourPassword','Token':'YourToken'}})
LOGIN_AS = 'SA'


class SalesforceApp:
 def __init__(self):
  self.platformEventUrl = "/services/data/v47.0/sobjects/Meeting_Room__e"
  self.params = {"grant_type": "password",
        "client_id": "YourClientId",
        "client_secret": "YourClientSecret",
        "username": LOGIN_DICT.get('users').get(LOGIN_AS).get('Email'),
        "password": LOGIN_DICT.get('users').get(LOGIN_AS).get('Password')+LOGIN_DICT.get('users').get(LOGIN_AS).get('Token')
        }
  self.tokenUrl = "https://login.salesforce.com/services/oauth2/token"
  self.statusCode = 0
  self.req = requests.post(self.tokenUrl,params=self.params)
  
  if self.req.status_code == 200:
   self.statusCode = 200
   self.access_token = self.req.json().get("access_token")
   self.instance_url = self.req.json().get("instance_url")
   self.createHeader()
  else:
   print ("Couldn't connect to Salesforce")
   sys.exit(0)

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

#Creating occupancy record
 def createOccupancyRecord(self,status,meetingRoom,changedTime):
  oc_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", changedTime)
  createdOc = self.sf.Occupancy_Record__c.create({'Meeting_Room_Id__c':meetingRoom,'Occupancy_Changed_At__c':oc_time,'Occupancy_Status__c':status})
  print ("The occupancy record is created for meeting room {} with status {}: ".format(meetingRoom,status));

 def getRecordId(self,meetingRoom):
  query = "SELECT Id FROM Meeting_Object__c WHERE Meeting_Room_Id__c = "+"'"+meetingRoom+"'"
  record = self.sf.query(query)
  if len(record['records']) > 0:
   return record['records'][0]['Id']
