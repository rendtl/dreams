import re
from src.error import InputError, AccessError
from src.database import data
from src.utils import get_user_id_from_token, make_dm_name, valid_userid, valid_dmid

'''
Direct Messages
'''
def dm_create_v1(token, u_ids):
    
    #Obtain user id of creator from token
    auth_user_id = get_user_id_from_token(token)

    # Set dm_id to length of dmlist in database
    total_ids = [auth_user_id]
    total_ids.extend(u_ids)

    dm_id = len(data["dmList"])

    # Make dm name as alphabetically sorted list of handles
    dm_name = make_dm_name(total_ids)

    dmData = {
        'dm_name': dm_name,
        'id': dm_id,
        'messages': [],
        'member_ids': total_ids,
        'owner_ids': [auth_user_id],
    }

    # Adding user data and database
    data["dmList"].append(dmData)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }



def dm_list_v1(token):
    auth_user_id = get_user_id_from_token(token)

    newdmList = []

    for dm in data["dmList"]:
        if auth_user_id in dm.get('member_ids'):
            dmDict = {}
            dmDict['dm_id'] = dm.get('id')
            dmDict['dm_name'] = dm.get('dm_name')
            newdmList.append(dmDict)
    
    return {'dms': newdmList}

def dm_invite_v1(token, dm_id, u_id):
    # Obtain user id from token
    #
    auth_user_id = get_user_id_from_token(token)

    # Check if dm_id exists
    dmExists = False
    for dm in data["dmList"]:
        if dm_id is dm["id"]:
            # Dm exists
            dmExists = True
            break
    if dmExists is False:
        # Dm doesnt exist
        raise InputError(description="DM does not exist")

    # Check if u_id refers to a valid user
    if valid_userid(u_id) is False:
        raise InputError(description="User ID does not exist")

    # Check if the inviter is part of the dm
    authorised = False
    for dm in data["dmList"]:
        if dm.get("id") is dm_id:
            if auth_user_id in dm.get("member_ids"):
                authorised = True
                break
    if authorised is False:
        raise AccessError(description="User is not a part of the DM to be able to invite")

    # Security measures complete
    # assumption they will not be in the dm already?
    # Add user id into the list of member ids
    for dm in data["dmList"]:
        if dm.get("id") is dm_id:
            dm["member_ids"].append(u_id)

    return {}

def dm_messages_v1(token, dm_id, start):

    auth_user_id = get_user_id_from_token(token)

    # Check if user id is valid
    if valid_userid(auth_user_id) is False:
        raise AccessError(description="Error: Invalid user id")

    # Check if dm id is valid
    if valid_dmid(dm_id) is False:
        raise InputError(description="Error: Invalid dm")

    #Check if user is authorised to be in the dm
    authorisation = False
    for dm in data["dmList"]:
        if dm["id"] is dm_id:
            for user in dm["member_ids"]:
                if user is auth_user_id:
                    authorisation = True
                    break
    if authorisation is False:
        raise AccessError(description="User is not in dm")

    # Return Function
    for dm in data["dmList"]:
        if dm["id"] is dm_id:
            messages = dm["messages"]

    if start > len(messages):
        raise InputError(description="Start is greater than total number of messages")

    # 0th index is the most recent message... therefore must reverse list?
    messages.reverse()
    
    # start + 50 messages is what is shown, so must create a list with these
    # messages within and transfer data from messages to messages_shown
    messages_shown = []
    end = start + 50
    msg_amt = 0
    while msg_amt < 50:
        # Where we start and increment from
        starting_index = start + msg_amt
        if starting_index >= end or starting_index >= len(messages):
            break

        messages_shown.append(messages[starting_index])
        msg_amt = msg_amt + 1
    if len(messages) == 0 or msg_amt < 50:
        end = -1
    return {
        'messages': messages_shown,
        'start': start,
        'end': end,
    }

def dm_leave_v1(token, dm_id):

    auth_user_id = get_user_id_from_token(token)

    # Invalid dm_id
    if valid_dmid(dm_id) is False:
        raise InputError(description="Error: DM id is not valid")
    # Main Implemenation
    for dm in data["dmList"]:
        if dm_id is dm["id"]:
            for users in dm["member_ids"]:
                if auth_user_id is users:
                    dm["member_ids"].remove(auth_user_id)
                    return
    raise AccessError
                    

def dm_remove_v1(token, dm_id):

    auth_user_id = get_user_id_from_token(token)

    # Invalid dm_id
    if valid_dmid(dm_id) is False:
        raise InputError(description="Error: DM id is not valid")

    # User is not DM creator and main Implementation
    for dm in data["dmList"]:
        if dm_id is dm["id"]:
            if auth_user_id not in dm["owner_ids"]:
                raise AccessError(description="Not an authorised user")
            else:
                data["dmList"].remove(dm)
                return
