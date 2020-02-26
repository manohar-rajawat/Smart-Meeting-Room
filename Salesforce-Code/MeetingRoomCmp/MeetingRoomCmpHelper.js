({
    showSpinner: function(component) {
        var spinnerMain =  component.find("Spinner");
        $A.util.removeClass(spinnerMain, "slds-hide");
    },
    
    hideSpinner : function(component) {
        var spinnerMain =  component.find("Spinner");
        $A.util.addClass(spinnerMain, "slds-hide");
    },
    
    showSuccess: function(component,event,helper,roomName)
    {
        let message_toast = "You will be notified when "+roomName+" becomes available.";
        this.showToast(component, event, helper, message_toast, "success");
    },
    
    showError: function(component,event,helper)
    {
        let message_toast = "Sorry ! Notification can not be set for this room";
        this.showToast(component, event, helper, message_toast, "error");
    },
    
    showAlreadyNotificationSet: function(component,event,helper,roomName)
    {
        let message_toast = "Hi ! You have already selected notification mode for "+roomName;
        this.showToast(component, event, helper, message_toast, "info");
    },
    
    
    
    NotificationOn: function(component,event,helper,roomName,roomId) {
        var action = component.get("c.notificationModeOn");
        action.setParams({ 
            roomId : component.get("v.meetingRoomsNotificationId")
        });
        action.setCallback(this, function(response) {
            var state = response.getState();
            if (state === "SUCCESS") {
                let returnValue = response.getReturnValue();
                if(returnValue != null)
                {
                    if(returnValue != 'Exists')
                    {
                        let uniqueRoomId = 'room'+roomId;
                        let notification = document.getElementById(uniqueRoomId);
                        if(notification)
                        {
                            notification.dataset.isnotificationmodeon=true;
                        }
                        this.showSuccess(component,event,helper,roomName);
                    }
                    else if (returnValue == 'Exists')
                    {
                        this.showAlreadyNotificationSet(component,event,helper,roomName);
                    }
                }
                else{
                    this.showError(component,event,helper);
                }
            }
            else if (state === "INCOMPLETE") {
                alert('Incomplete !!!');
            }
                else if (state === "ERROR") {
                    var errors = response.getError();
                    if (errors) {
                        if (errors[0] && errors[0].message) {
                            console.log("Error message: " + 
                                        errors[0].message);
                        }
                    } else {
                        console.log("Unknown error");
                    }
                    this.showError(component,event,helper);
                }
        });
        $A.enqueueAction(action);  
    },
    
    showToast: function(component, event, helper, message_toast, msg_type)
    {
        var toastEvent = $A.get("e.force:showToast");
        toastEvent.setParams({
            "type": msg_type,
            "title": "Success : ",
            "message": message_toast
        });
        toastEvent.fire();
    },
    
    
    
    helperMethod : function() {
        /*
        
List<Meeting_Room__e> meetingRoom = new List<Meeting_Room__e>();
List<String> devices = new List<String>{'2001','2002','2003','2004'};
Map<String,Boolean> availability = new Map<String,Boolean>{'2001' => true,'2002' => true,
    '2003' => false, '2004' => false};
List<Database.SaveResult> results = new List<Database.SaveResult>();
    
    public void setV(List<String> devices,Boolean bool)
{
    for(String key : availability.keySet())
    {
        meetingRoom.add(new Meeting_Room__e(Equipped__c=availability.get(key),
                                            Meeting_Room_Id__c=key));
    }
}

setV(devices,false);
System.debug(meetingRoom.size());
if(meetingRoom.size() > 0)
    results = EventBus.publish(meetingRoom);

if(results.size() > 0)
    for(Database.SaveResult sr : results)
{
    if(sr.isSuccess())
        System.debug('Events published successfully !');
    else
    {
        for(Database.Error err : sr.getErrors())
        {
            System.debug('Error returned: ' +
                         err.getStatusCode() +
                         ' - ' +
                         err.getMessage());
        }
    }
}        
         */
    }
})
