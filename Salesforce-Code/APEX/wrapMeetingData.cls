public class wrapMeetingData 
{
    @AuraEnabled public Id id {get; set;}
    @AuraEnabled public Boolean isEquipped {get; set;}
    @AuraEnabled public String description {get; set;}
    @AuraEnabled public Decimal floor {get; set;}
    @AuraEnabled public String meetingRoomId {get; set;}
    @AuraEnabled public String name {get; set;}
    @AuraEnabled public String phone {get; set;}
    @AuraEnabled public Boolean entryAllowed {get; set;}
    
    public wrapMeetingData(Id temp_id, String temp_name, Boolean temp_isEquipped, String temp_description, Decimal temp_floor, String temp_phone, String temp_meetingRoomId, Boolean temp_entryAllowed) {
        id = temp_id;
        isEquipped = temp_isEquipped;
        description = temp_description;
        floor = temp_floor;
        meetingRoomId = temp_meetingRoomId;
        name = temp_name;
        phone = temp_phone;
        entryAllowed = temp_entryAllowed;
    }
}
