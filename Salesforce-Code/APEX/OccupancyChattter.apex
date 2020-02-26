Trigger OccupancyChattter on Occupancy_Record__c (before insert,after insert) 
{
    List<FeedItem> feedItems = new List<FeedItem>(); //This is the list of chatter feeds
    Private Static void addFeeds(String roomName,Id userId)
    {
        FeedItem post = new FeedItem();
        post.ParentId = userId;
        post.Body = 'The '+roomName+' is Vacant now !';
        feedItems.add(post);
        
        //This code is not being used because the "Automated Process User" doesn't have permission to this package.
        /*
String Body = '{'+temp_user.Id+'} '+'The '+roomName+' is vacant now !';
ConnectApi.FeedItem fi = (ConnectApi.FeedItem) ConnectApiHelper.postFeedItemWithMentions(Network.getNetworkId(), 'me', Body);
`       */
    }
    
    if(Trigger.isAfter)
    {
        if(Trigger.isInsert)
        {
            Set<Id> meetingRoomVacantMap = new Set<Id>();
            for(Occupancy_Record__c oc_R: [select id,Meeting_Room_Id__r.Id from Occupancy_Record__c where id in :Trigger.New and Occupancy_Status__c = 'Vacant'])
            {   
                meetingRoomVacantMap.add(oc_R.Meeting_Room_Id__r.Id);
            }
            System.debug('meetingRoomVacantMap '+meetingRoomVacantMap);
            List<Notification_Alert__c> notificationList = [select User__c,Meeting_Object__r.Name from Notification_Alert__c where Meeting_Object__c In :meetingRoomVacantMap]; 
            if(notificationList.size() > 0)
            {
                for(Notification_Alert__c no_A : notificationList)
                {
                    addFeeds(no_A.Meeting_Object__r.Name,no_A.User__c);
                } 
                System.debug('notificationList '+notificationList);
                if(feedItems.size() > 0)
                {
                    Database.SaveResult[] srList = Database.insert(feedItems, true);
                    for (Database.SaveResult sr : srList) 
                    {
                        if (sr.isSuccess()) 
                        {
                            System.debug('Successfully inserted account. Account ID: ' + sr.getId());
                        }
                        else 
                        {            
                            for(Database.Error err : sr.getErrors()) 
                            {
                                System.debug('The following error has occurred.');                    
                                System.debug(err.getStatusCode() + ': ' + err.getMessage());
                                System.debug('Account fields that affected this error: ' + err.getFields());
                            }
                        }
                    } 
                    if(notificationList.size() > 0)
                        delete notificationList; //Each time when notificaion is sent to the user we delete the notification record created by user.
                }
            }
        }
    }
}
