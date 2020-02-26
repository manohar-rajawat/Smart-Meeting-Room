({
    checkStatus : function(component, event, helper) 
    {
        //helper.showSpinner(component);
        var action = component.get("c.getMeetingDetails");
        action.setCallback(this, function(response) {
            var state = response.getState();
            if (state === "SUCCESS") {
                component.set("v.meetingRooms", response.getReturnValue());
                //helper.hideSpinner(component);
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
                }
        });
        $A.enqueueAction(action);
    },
    
    showBox: function(component, event, helper) 
    {
        let roomName = event.currentTarget.dataset.roomname;
        let roomId = event.currentTarget.dataset.roomid;
        let isnotificationset = event.currentTarget.dataset.isnotificationmodeon;
        if(isnotificationset == "false")
        {
            if(roomName)
            {
                component.set("v.meetingRoomsNotificationName",roomName); 
            }
            else
            {
                component.set("v.meetingRoomsNotificationName",'');
            }
            if(roomId)
            {
                component.set("v.meetingRoomsNotificationId",roomId); 
            }
            else
            {
                component.set("v.meetingRoomsNotificationId",'');
            }
            component.set("v.isModalOpen",true); 
        }
        else if(isnotificationset == "true")
        {
            helper.showAlreadyNotificationSet(component,event,helper,roomName);
        }
    },
    
    closeModel: function(component, event, helper) {
        component.set("v.isModalOpen", false);
    },
    
    notificationSelected: function(component, event, helper) {
        component.set("v.isModalOpen", false);
        let roomName = component.get("v.meetingRoomsNotificationName");
        let roomId = component.get("v.meetingRoomsNotificationId");
        helper.NotificationOn(component,event,helper,roomName,roomId);
    },
})
