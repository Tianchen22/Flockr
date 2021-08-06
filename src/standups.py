'''
***standups***
requirements:
    6.9. Standups
    Once standups are finished, all of the messages 
    sent to standup/send are packaged together in one 
    single message posted by the user who started the 
    standup and sent as a message to the channel the 
    standup was started in, timestamped at the moment 
    the standup finished.
'''
import time
import threading
import error
import auth
import message as msg
import channel 
# a template for buffer format
# STANDUP_BUFFER = {
#     'channel_id_1': {'time_finish': int(time.time()),
#                      'message_buffer': ('handle_1: message_1' + '\n',
#                                         'handle_2: message_2' + '\n',
#                                         ...)
#                   },
#     'channel_id_2': {...}
# }
STANDUP_BUFFER = {}

def standup_buffer_pop(token, channel_id, length):
    '''
    helper function to pack message in buffer
    and send to channel message history
    '''
    time.sleep(int(length))
    global STANDUP_BUFFER
    assert str(channel_id) in STANDUP_BUFFER.keys()
    combined_standup = STANDUP_BUFFER.pop(str(channel_id))
    standup_buffer_send(token, channel_id, combined_standup['message_buffer'])
    return {}

def standup_buffer_send(token, channel_id, message):
    '''
    standup_buffer_send(token, channel_id, message)
    standup version of message_send
    '''
    new_message = msg.create_message(auth.token_to_u_id(token), message)
    msg.initiat_message_history(channel_id, new_message)
    pass

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period 
    whereby for the next "length" seconds if someone 
    calls "standup_send" with a message, it is buffered 
    during the X second window then at the end of the X 
    second window a message will be added to the message 
    queue in the channel from the user who started the 
    standup. X is an integer that denotes the number of 
    seconds that the standup occurs for
    '''
    channel.valid_token(token)
    channel.valid_channel_id(channel_id)
    if standup_active(token, channel_id)['is_active']:
        raise error.InputError("A standup already active in current channel.")
    ###
    time_start = int(time.time())
    time_finish = int(time_start + length)
    # create a term inside buffer to store message
    STANDUP_BUFFER[str(channel_id)] = {'time_finish': time_finish,
                                       'message_buffer': ''}
    # create a thread to send message
    t = threading.Thread(target=standup_buffer_pop, args=(token, channel_id, length))
    t.start()
    # DO NOT wait for thread to end, but returns time_finish
    return time_finish

def standup_active(token, channel_id):
    '''
    For a given channel, return whether 
    a standup is active in it, 
    and what time the standup finishes. 
    If no standup is active, 
    then time_finish returns None
    '''
    channel.valid_token(token)
    channel.valid_channel_id(channel_id)
    ###
    global STANDUP_BUFFER
    # check if standup active by checking if channel_id as key presents in buffer dict
    if str(channel_id) in STANDUP_BUFFER.keys():
        return {'is_active': True, 'time_finish': STANDUP_BUFFER[str(channel_id)]['time_finish']}
    else:
        return {'is_active': False, 'time_finish': None}

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue, 
    assuming a standup is currently active
    '''
    channel.valid_token(token)
    channel.valid_channel_id(channel_id)
    if not channel.is_member(channel_id, auth.token_to_u_id(token)):
        raise error.AccessError("Standup: user has no access to send standup msg")
    if len(message) > 1000:
        raise error.InputError("Standup: message length > 1000")
    ###
    if not standup_active(token, channel_id)['is_active']:
        raise error.InputError("Standup not active in current channel")
    # otherwise active
    # append message and handle to buffer
    global STANDUP_BUFFER
    handle = auth.USER_DB[str(auth.token_to_u_id(token))]['HANDLE']
    msg = str(handle) + ': ' + str(message)
    if len(STANDUP_BUFFER[str(channel_id)]['message_buffer']) != 0:
        STANDUP_BUFFER[str(channel_id)]['message_buffer'] += '\n'
    STANDUP_BUFFER[str(channel_id)]['message_buffer'] += msg
    return {}
