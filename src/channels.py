import re
from src.database import accData, channelList
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError

'''
channels_list_v1 takes in a user_id string.
The functions then checks if the user_id is valid.
If the user_id is valid, the function then returns all the channels associated
with the user_id in a list.
Arguments:
    auth_user_id (string) - ID of user
Exceptions:
    AccessError - Occurs when given id does not match accData
Return Value:
    Returns list | {'channels': newchannelList}
'''
def channels_list_v1(auth_user_id):
    id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            id_status = True
            break
    
    if id_status is False:
        raise AccessError("Error: Invalid user id")

    newchannelList = []
    for channel in channelList:
        if auth_user_id in channel.get('member_ids'):
                channelDict = {}
                channelDict['channel_id'] = channel.get('id')
                channelDict['name'] = channel.get('name')
                newchannelList.append(channelDict)
    

    return {'channels': newchannelList}

'''
channels_list_v1 takes in a user_id string.
The functions then checks if the user_id is valid.
If the user_id is valid, the function then returns all channels.
Arguments:
    auth_user_id (string) - ID of user
Exceptions:
    AccessError - Occurs when given id does not match accData
Return Value:
    Returns list | {'channels': newchannelList}
'''
def channels_listall_v1(auth_user_id):
    id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            id_status = True
            break
    
    if id_status is False:
        raise AccessError("Error: Invalid user id")

    newchannelList = []
    for channel in channelList:
        channelDict = {}
        channelDict['channel_id'] = channel.get('id')
        channelDict['name'] = channel.get('name')
        newchannelList.append(channelDict)

    return {'channels': newchannelList}

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    # Check if length of name is valid
    if len(name) > 20:
        raise InputError("Error: Name is greater than 20 characters")

    if len(name) < 1:
        raise InputError("Error: Name is less than 1 character")

    # Check if valid user id
    id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            id_status = True
            break
    
    if id_status is False:
        raise AccessError("Error: Invalid user id")
    
    channel_id = len(channelList)

    channelData = {
        'name': name,
        'id': channel_id,
        'is_public': is_public,
        'member_ids': [],
        'owner_ids': [],
        'messages': [],
    }

    # Adding user data
    channelData['owner_ids'].append(auth_user_id)
    channelData['member_ids'].append(auth_user_id)

    channelList.append(channelData)


    return {
        'channel_id': channel_id,
    }


'''
if __name__ == "__main__":
    user0 = auth_register_v1("email2@gmail.com", "password1", "1Name", "1Lastname")
    user1 = auth_register_v1("email3@gmail.com", "password3", "3Name", "3Lastname")
    user2 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    
    for user in accData:
        print(user.get("id"))

    print(user2.get("auth_user_id"))
    
    print(channels_create_v1(user2.get("auth_user_id"), "Channel", True))
'''