import channel
import auth
import error
import time
import threading

USED_MESSAGE_ID = 0
DEFAULT_MESSAGE_HIST_START = 0
DEFAULT_MESSAGE_HIST_END = 50

# minor fix to compate with standups.py
NOT_SENT_MSG_EMPTY = -1
STANDUP_SEND_PENDING = -7

# a place holder for senf treading timer
send = None

def reset_id_gen():
    '''
    reset_id_gen()
    reset global values for each test
    '''
    global USED_MESSAGE_ID
    global DEFAULT_MESSAGE_HIST_START
    global DEFAULT_MESSAGE_HIST_END
    USED_MESSAGE_ID = 0
    DEFAULT_MESSAGE_HIST_START = 0
    DEFAULT_MESSAGE_HIST_END = 50

def message_id_generator():
    '''
    message_id_generator()
    generate unique message id (unique in entire flockr)
    '''
    global USED_MESSAGE_ID
    USED_MESSAGE_ID += 1
    return USED_MESSAGE_ID

def message_id_finder(message_id, mode = 0, strr = ""):
    '''
    message_id_finder(message_id, mode = 0, strr = "")
    find the specific message by message_id
    also returns the channel_id it belongs to;
    if not found, return None
    '''
    # look for channel from database
    for chid in channel.CHANNEL_DB.keys():
        if channel.CHANNEL_DB[chid]['message_history'] != None \
        and channel.CHANNEL_DB[chid]['message_history'] != {}:
            # look for message_id fits
            for mess in channel.CHANNEL_DB[chid]['message_history']['messages']:
                if mess['message_id'] == message_id:
                    if mode == -1: # remove mode
                        channel.CHANNEL_DB[chid]['message_history']['messages'].remove(mess)
                        return None
                    if mode == 1: # edit mode
                        mess['message'] = strr
                    return {
                        'channel_id': channel.CHANNEL_DB[chid]['channel_id'],
                        'message_id': message_id,
                        'poster_id': mess['u_id']
                    }
    raise error.InputError(f"Message ID ({str(message_id)}) does not exist")


def create_message(u_id, message):
    '''
    create_message(u_id, message)
    a module for new message as dict();
    create and return a message object to 
    message history list
    '''
    new_message = dict()
    new_message['message_id'] = message_id_generator()
    new_message['u_id'] = u_id
    new_message['message'] = message
    new_message['time_created'] = int(time.time())
    new_message['reacts'] = []
    new_message['is_pinned'] = False
    return new_message
    

def initiat_message_history(channel_id, new_message):
    '''
    initiat_message_history(channel_id, new_message)
    if the channel is just created
    and has an empty 'message_history'
    '''
    curr = channel.CHANNEL_DB[str(channel_id)]
    # if message history is empty -- create the info of it
    if curr['message_history'] is None or curr['message_history'] == {}:
        curr['message_history'] = {}
        curr['message_history']['messages'] = [new_message]
        curr['message_history']['start'] = DEFAULT_MESSAGE_HIST_START
        curr['message_history']['end'] = DEFAULT_MESSAGE_HIST_END
        return True
    else:
        # not empty --> insert to the top of messages
        curr['message_history']['messages'].insert(0, new_message)
        return False

def message_send_error(token, channel_id, message):
    '''
    message_send_error(token, channel_id, message)
    error for message_send
    '''
    channel.valid_token(token)
    channel.valid_channel_id(channel_id)
    #if user is not member of channel
    if not channel.is_member(channel_id, auth.token_to_u_id(token)):
        raise error.AccessError("Permission denied: u_id = ", auth.token_to_u_id(token))
    # if msg is too long
    if len(message) > 1000:
        raise error.InputError("Message too long")

def message_send(token, channel_id, message):
    '''
    message_send(token, channel_id, message)
    Send a message from authorised_user to the channel specified by channel_id
    '''
    # test error
    message_send_error(token, channel_id, message)
    # create msg format
    new_message = create_message(auth.token_to_u_id(token), message)
    # insert the msg into the channel_db
    initiat_message_history(channel_id, new_message)
    return {
        'message_id': new_message['message_id']
    }

def message_remove(token, message_id):
    '''
    message_remove(token, message_id)
    remove a message if message_id exist, and if token valid
    '''
    channel.valid_token(token)
    result = message_id_finder(message_id)
    # must be admin or poster
    if not channel.is_owner(result['channel_id'], auth.token_to_u_id(token)) or \
        result['poster_id'] != auth.token_to_u_id(token):
        raise error.AccessError("Permission denied: u_id = ", auth.token_to_u_id(token))
    message_id_finder(message_id, mode = -1)
    return {
    }

def message_edit(token, message_id, message):
    '''
    message_edit(token, message_id, message)
    edit a message if message_id exist, and if token valid
    if new message is "", then remove message
    '''
    channel.valid_token(token)
    result = message_id_finder(message_id)
    # must be admin or poster
    if not channel.is_owner(result['channel_id'], auth.token_to_u_id(token)) or \
        result['poster_id'] != auth.token_to_u_id(token):
        raise error.AccessError("Permission denied: u_id = ", auth.token_to_u_id(token))
    # if new message is "", then remove message
    if message == "":
        message_id_finder(message_id, mode = -1)
    else:
        message_id_finder(message_id, mode = 1, strr = message)
    return {
    }

def message_sendlater(token, channel_id, message, time_sent):
    '''
    message_sendlater(token, channel_id, message, time_sent)
    Send a message from authorised_user to the channel specified by channel_id 
    automatically at a specified time in the future
    '''
    message_send_error(token, channel_id, message)

    time_now = int(time.time())
    time_diff = time_sent - time_now
    # if time sent is the time in the past
    if time_diff < 0:
        raise error.InputError("Time sent is the time in the past!")
    # create the msg format firstly and get the message_id
    new_message = create_message(auth.token_to_u_id(token), message)
    # user Timer to make msg insert to the channel_db later -- then send later
    global send
    send = threading.Timer(time_diff, initiat_message_history,[channel_id, new_message])
    send.start()
    return {
        'message_id': new_message['message_id']
    }

def check_sendlater():
    '''
    check_sendlater()
    test whether Timer works or not
    '''
    return send.is_alive()

def react_error(token, message_id, react_id):
    '''
    react_error(token, message_id, react_id)
    inputerror and return channel_id, u_id
    '''
    channel.valid_token(token)
    # find the message in which channel
    result = message_id_finder(message_id)
    ch_id = result['channel_id']
    # get user id
    u_id = auth.token_to_u_id(token)
    # check if the user is member of channel
    if not channel.is_member(ch_id, u_id):
        raise error.InputError('message_id is not a valid message within a channel that the authorised user has joined.')
    # check if react_id is 1
    if react_id != 1:
        raise error.InputError('react_id is not a valid React ID.')
    return ch_id, u_id

def message_react(token, message_id, react_id):
    '''
    message_react(token, message_id, react_id)
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message
    { react_id, u_ids, is_this_user_reacted }
    is_this_user_reacted --> channel_message
    '''
    ch_id, u_id = react_error(token, message_id, react_id)
    # get the msg location and put react
    for msg in channel.CHANNEL_DB[str(ch_id)]['message_history']['messages']:
        if msg['message_id'] == message_id:
            # if user reacted before
            if msg['reacts'] != [] and u_id in msg['reacts'][0]['u_ids']:
                raise error.InputError('Already contains an active React.')

            if msg['reacts'] == []:
                # when msg['reacts'] is empty
                react_dict = {
                    'react_id': react_id,
                    'u_ids': [u_id]
                }
                msg['reacts'].append(react_dict)
            else:
                # if msg['reacts'] is not empty an just add u_id in the u_ids list
                msg['reacts'][0]['u_ids'].append(u_id)
            break
    return {
    }

def message_unreact(token, message_id, react_id):
    '''
    message_unreact(token, message_id, react_id)
    Given a message within a channel the authorised user is part of, 
    remove a "react" to that particular message
    '''
    ch_id, u_id = react_error(token, message_id, react_id)
    # get the msg location and put react
    for msg in channel.CHANNEL_DB[str(ch_id)]['message_history']['messages']:
        if msg['message_id'] == message_id:
            # if no react in the msg
            if msg['reacts'] == [] or u_id not in msg['reacts'][0]['u_ids']:
                raise error.InputError(f'{message_id} does not contain an active React.')
            else:
                # if msg has react, remove the user u_id in the u_ids list
                msg['reacts'][0]['u_ids'].remove(u_id)
            break
    return {
    }

def pin_error(token, message_id):
    '''
    pin_error(token, message_id)
    message_pin and message_unpin errors
    return channel id
    '''
    channel.valid_token(token)
    result = message_id_finder(message_id)
    ch_id = result['channel_id']
    u_id = auth.token_to_u_id(token)
    if not channel.is_member(ch_id, u_id):
        raise error.AccessError(f'{u_id} is not a member of the channel.')
    if not channel.is_owner(ch_id, u_id):
        raise error.AccessError(f'{u_id} is not an owner of the channel.')
    return ch_id

def message_pin(token, message_id):
    '''
    message_pin(token, message_id)
    Given a message within a channel, 
    mark it as "pinned" to be given special display treatment by the frontend
    '''
    ch_id = pin_error(token, message_id)
    # get the msg location
    for msg in channel.CHANNEL_DB[str(ch_id)]['message_history']['messages']:
        if msg['message_id'] == message_id:
            # if msg is already pinned -- error
            if msg['is_pinned'] == True:
                raise error.InputError(f'{message_id} is already pinned.')
            # if not
            msg['is_pinned'] = True
            break
    return {
    }

def message_unpin(token, message_id):
    '''
    message_unpin(token, message_id)
    Given a message within a channel, remove it's mark as unpinned
    '''
    ch_id = pin_error(token, message_id)
    # get the msg location
    for msg in channel.CHANNEL_DB[str(ch_id)]['message_history']['messages']:
        if msg['message_id'] == message_id:
            # if the msg is already unpinned -- error
            if msg['is_pinned'] == False:
                raise error.InputError(f'{message_id} is already unpinned.')
            # if not
            msg['is_pinned'] = False
            break
    return {
    }
