public class meetingRoomController {
    
    @AuraEnabled
    public static List<wrapMeetingData> getMeetingDetails()
    {
        List<Meeting_Object__c> meetingObjects = new List<Meeting_Object__c>();
        List<wrapMeetingData> wrappedMeetingData = new List<wrapMeetingData>();
        meetingObjects = [select id,name,Equipped__c,Description__c,Floor__c,Phone__c,Meeting_Room_Id__c,Entry_Allowed__c from Meeting_Object__c where Entry_Allowed__c = true order by Meeting_Room_Id__c];
        if(meetingObjects.size() > 0)
        {
            for(Meeting_Object__c mO : meetingObjects)
            {
                wrappedMeetingData.add(new wrapMeetingData(mO.id,mO.Name,mO.Equipped__c,mO.Description__c,mO.Floor__c,mO.Phone__c,mO.Meeting_Room_Id__c,mO.Entry_Allowed__c));
            }
            if(wrappedMeetingData.size() > 0)
                return wrappedMeetingData;
            else
                return null;
        }
        else
            return null;
    }
    
    @AuraEnabled
    public static String notificationModeOn(String roomId)
    {
        Id userId = UserInfo.getUserId(); //Returns the user id of current logged in user;
        Meeting_Object__c[] m_Os = [select Id from Meeting_Object__c where Meeting_Room_Id__c = :roomId];
        if(m_Os.size() > 0)
        { 
            List<Notification_Alert__c> no_As = [Select id from Notification_Alert__c where User__c =:userId and Meeting_Object__c =:m_Os[0].Id];
            if(no_As.size() > 0)
            {
                return 'Exists';
            }
            else
            {
                Meeting_Object__c m_O = m_Os[0];
                Notification_Alert__c no_A = new Notification_Alert__c(User__c=userId,Meeting_Object__c=m_O.Id);
                Database.SaveResult srList = Database.insert(no_A, false);
                if (srList.isSuccess()) 
                {
                    System.debug('Successfully inserted account. Account ID: ' + srList.getId());
                    return srList.getId();
                }
                else 
                {        
                    for(Database.Error err : srList.getErrors()) {
                        System.debug('The following error has occurred.');                    
                        System.debug(err.getStatusCode() + ': ' + err.getMessage());
                        System.debug('Account fields that affected this error: ' + err.getFields());
                    }
                    return null;
                }
            }
            
        }
        else
        {
            return null;
        }
    }
}
