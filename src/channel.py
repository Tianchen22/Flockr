'''
Channel.py provides in_channel operations.
'''
import channel_constant
import channel_test_data
import auth
import error
import message as msg

# Current id => variable place holder.
CURRENT_USER_ID = [1]
# place holder for CHANNEL_DB
CHANNEL_DB = {}

def valid_channel_id(channel_id):
    '''
    valid_channel_id(channel_id)
    Assert if channel_id is valid, or raise error.
    '''
    if not str(channel_id) in CHANNEL_DB.keys():
        raise error.InputError("Invalid channel ID: ", channel_id)

def valid_token(token):
    '''
    valid_token(token)
    Assert if token is valid with paired CURRENT_USER_ID, or raise error.
    '''
    # check if matching id:token pair
    if token not in auth.TOKEN_DB.keys() or not auth.TOKEN_DB[token]['log']:
        raise error.AccessError("Invalid token")
    CURRENT_USER_ID[0] = auth.token_to_u_id(token)

def valid_user(u_id):
    '''
    valid_user(u_id)
    Assert if target user is valid, or raise error
    '''
    if str(u_id) not in auth.USER_DB.keys():
        raise error.InputError("Invalid user ID: ", u_id)
    return True

def validate_info(token, channel_id):
    '''
    validate_info(token, channel_id)
    Validate token & channel_id
    '''
    valid_channel_id(channel_id)
    valid_token(token)

def is_owner(channel_id, u_id):
    '''
    is_owner(channel_id, u_id)
    Assert if target user is an owner of a channel, or raise error
    '''
    for member in CHANNEL_DB[str(channel_id)]['owner_members']:
        if u_id == member['u_id']:
            return True
    return False

def is_member(channel_id, u_id):
    '''
    is_member(channel_id, u_id)
    Assert if target user is an member of a channel, or raise error
    '''
    for member in CHANNEL_DB[str(channel_id)]['all_members']:
        if u_id == member['u_id']:
            return True
    return False

def create_new_member(u_id):
    '''
    create dict of new menmber including all info
    '''
    new_member = dict()
    new_member['u_id'] = int(u_id)
    new_member['name_first'] = auth.USER_DB[str(u_id)]['name_first']
    new_member['name_last'] = auth.USER_DB[str(u_id)]['name_first']
    new_member['profile_img_url'] = auth.USER_DB[str(u_id)]['img_url']
    return new_member

def channel_invite(token, channel_id, u_id):
    '''
    channel_invite(token, channel_id, u_id)
    Invite user to a channel
    '''
    # Error raising
    validate_info(token, channel_id)
    valid_user(u_id)
    if is_member(channel_id, u_id):
        raise error.InputError("Invalid user ID: ", u_id)
    if not is_member(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Permission denied: u_id = ", CURRENT_USER_ID[0])
    # actual functionalities
    new_member = create_new_member(u_id)
    CHANNEL_DB[str(channel_id)]['all_members'].append(new_member)
    # if admin is invited, promote to channel owner
    if auth.USER_DB[str(u_id)]['admin']:
        CHANNEL_DB[str(channel_id)]['owner_members'].append(new_member)
    return {
    }

def create_channel_detail(selected_channel):
    '''
    create a dict including channel_detail
    '''
    channel_detail = dict()
    channel_detail['name'] = selected_channel['name']
    channel_detail['owner_members'] = selected_channel['owner_members']
    channel_detail['all_members'] = selected_channel['all_members']
    return channel_detail

def channel_details(token, channel_id):
    '''
    channel_details(token, channel_id)
    output channel details
    '''
    validate_info(token, channel_id)
    # Error raising
    if not is_member(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Permission denied: u_id = ", CURRENT_USER_ID[0])
    # actual functionalities
    selected_channel = CHANNEL_DB[str(channel_id)]
    channel_detail = create_channel_detail(selected_channel)
    return channel_detail

def is_this_user_reacted(token, result):
    '''
    show thumbs up in message if current user reacts to the msg
    '''
    # get u_id of user
    u_id = auth.token_to_u_id(token)
    # when messages is not empty
    if result['messages'] is not None:
        for mssg in result['messages']:
            # put is_this_user_reacted into each message
            if mssg['reacts'] != []:
                # if user not in the u_ids list -- not thumbs up
                if u_id not in mssg['reacts'][0]['u_ids']:
                    mssg['reacts'][0]['is_this_user_reacted'] = False
                else:
                    # if user in the u_ids list -- thumbs up
                    mssg['reacts'][0]['is_this_user_reacted'] = True

def channel_msg_error(start, messagee):
    '''
    invalid start of msg
    '''
    if int(start) < int(messagee['start']):
        raise error.InputError("Invalid message start ID")
    if int(start) > len(messagee['messages']):
        raise error.InputError("Start({}) larger than total number of messages({})"\
                            .format(start, len(messagee['messages'])))

def channel_messages(token, channel_id, start):
    '''
    channel_messages(token, channel_id, start)
    output channel message history
    '''
    # Error raising
    validate_info(token, channel_id)
    if not is_member(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Permission denied: u_id = ", CURRENT_USER_ID[0])
    # actual functionalities
    messagee = CHANNEL_DB[str(channel_id)]['message_history']
    # if message is empty
    if messagee is None:
        return{
            'messages': list(), 
            'start': msg.DEFAULT_MESSAGE_HIST_START, 
            'end': msg.DEFAULT_MESSAGE_HIST_END,
        }
    # error -- invalid start
    channel_msg_error(start, messagee)

    # put all the messages into the new dic
    result = dict()
    result['messages'] = list()
    result['start'] = int(start)
    result['end'] = int(start) + 50
    n = 0
    for msgg in messagee['messages']:
        if n < (int(start) + 50) and n >= int(start):
            result['messages'].append(msgg)
        n += 1
    
    # show thumbs up in message --- is_this_user_reacted
    is_this_user_reacted(token, result)    

    # if messages are not up to 50
    if result['end'] > len(messagee['messages']):
        result['end'] = -1
    return result

def channel_leave(token, channel_id):
    '''
    channel_leave(token, channel_id)
    leave a channel from its member and owner list
    '''
    # Error raising
    validate_info(token, channel_id)
    if is_owner(channel_id, CURRENT_USER_ID[0]):
        channel_removeowner(token, channel_id, CURRENT_USER_ID[0])
    if not is_member(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Permission denied: u_id = ", CURRENT_USER_ID[0])
    # looking for who to remove
    member_leave(channel_id)
    return {
    }

def member_leave(channel_id):
    '''
    user leave channel
    '''
    # looking for who to remove
    for index in range(len(CHANNEL_DB[str(channel_id)]['all_members'])):
        if CHANNEL_DB[str(channel_id)]['all_members'][index]['u_id'] == CURRENT_USER_ID[0]:
            # found who to remove
            CHANNEL_DB[str(channel_id)]['all_members'].pop(index)

def channel_join(token, channel_id):
    '''
    channel_join(token, channel_id)
    join a channel as member by default
    '''
    # Error raising
    validate_info(token, channel_id)
    if is_member(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Already a member: u_id = ", CURRENT_USER_ID[0])
    if auth.USER_DB[str(auth.token_to_u_id(token))]['admin']:
        channel_admin_join(token, channel_id, channel_constant.SECRET_PASSWORD)
        return {}
    # if channel is not public
    if not CHANNEL_DB[str(channel_id)]['is_public']:
        # print("Channel is private")
        raise error.AccessError("Channel is private")
    # add current user to channel member
    member_join(channel_id)
    return {
    }

def member_join(channel_id):
    '''
    add current user to channel member
    '''
    new_member = dict()
    new_member['u_id'] = int(CURRENT_USER_ID[0])
    new_member['name_first'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['name_first']
    new_member['name_last'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['name_last']
    new_member['profile_img_url'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['img_url']
    CHANNEL_DB[str(channel_id)]['all_members'].append(new_member)

def channel_addowner(token, channel_id, u_id):
    '''
    channel_addowner(token, channel_id, u_id)
    add user as an owner
    '''
    # Error raising
    validate_info(token, channel_id)
    if not is_owner(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Permission denied: u_id = ", CURRENT_USER_ID[0])
    # if not member, then make a member, then owner
    if not is_member(channel_id, u_id):
        channel_invite(token, channel_id, u_id)
    # Actual functionalities
    if is_owner(channel_id, u_id):
        raise error.InputError("Target user is already an owner")
    # permission check end
    # add owner to channel
    add_owner(channel_id, u_id)
    return {
    }

def add_owner(channel_id, u_id):
    '''
    add owner to channel
    '''
    new_member = dict()
    new_member['u_id'] = int(u_id)
    new_member['name_first'] = auth.USER_DB[str(u_id)]['name_first']
    new_member['name_last'] = auth.USER_DB[str(u_id)]['name_first']
    new_member['profile_img_url'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['img_url']
    CHANNEL_DB[str(channel_id)]['owner_members'].append(new_member)

def channel_removeowner(token, channel_id, u_id):
    '''
    channel_removeowner(token, channel_id, u_id)
    remove user from owner list
    '''
    # Error raising
    validate_info(token, channel_id)
    if not is_owner(channel_id, CURRENT_USER_ID[0]):
        raise error.AccessError("Permission denied: u_id = ", CURRENT_USER_ID[0])
    if not is_owner(channel_id, u_id):
        raise error.InputError("Target user is not an owner")
    remove_owner(channel_id, u_id)
    return {
    }

def remove_owner(channel_id, u_id):
    '''
    remove owner from channel
    '''
    # find owner
    for owner in CHANNEL_DB[str(channel_id)]['owner_members']:
        if owner['u_id'] == u_id:
            # found who to remove
            CHANNEL_DB[str(channel_id)]['owner_members'].remove(owner)

def channel_admin_join(token, channel_id, password): # never callable directly by any user
    '''
    channel_admin_join(token, channel_id, password)
    join a channel as owner by default (if is flokr owner)
    !!! never callable directly by any user !!!
    '''
    validate_info(token, channel_id)
    # add admin user to channel owner and member
    if password != channel_constant.SECRET_PASSWORD:
        raise error.AccessError("Wrong secret_password?????? \
                                This function should not be callable directly as well!!!!!!")
    join_admin(channel_id)
    return {
    }

def join_admin(channel_id):
    '''
    join a channel as owner
    '''
    new_member = dict()
    new_member['u_id'] = int(CURRENT_USER_ID[0])
    new_member['name_first'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['name_first']
    new_member['name_last'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['name_last']
    new_member['profile_img_url'] = auth.USER_DB[str(CURRENT_USER_ID[0])]['img_url']
    CHANNEL_DB[str(channel_id)]['owner_members'].append(new_member)
    CHANNEL_DB[str(channel_id)]['all_members'].append(new_member)
