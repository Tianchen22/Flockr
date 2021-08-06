import time
import pytest
import standups
import error
import auth
import other
import channel
import channels

# global variable as place holder for test-use variables
ADMIN_TOKEN = [None]
ADMIN_U_ID = [None]
GUEST_1_TOKEN = [None]
GUEST_1_U_ID = [None]

def clear_buffer(function):
    '''
    clear_buffer as wrapper
    clear database, and test if the standup buffer is cleared
    '''
    def wrapper():
        other.clear()
        standups.STANDUP_BUFFER = {}
        assert len(standups.STANDUP_BUFFER) == 0
        # set up valid users for later tests
        auth.auth_register('z5555555@gmail.com', '1234567', 'admin', 'admin') # u_id = 1
        ADMIN_TOKEN[0] = auth.TOKEN_LOGGED[0] # auth.token_generate('z5555555@gmail.com')
        ADMIN_U_ID[0] = auth.token_to_u_id(ADMIN_TOKEN[0])
        # auth.auth_logout(ADMIN_TOKEN[0])
        auth.auth_register('z3333333@gmail.com', '1234567', 'guest1', 'guest1') # u_id = 2
        GUEST_1_TOKEN[0] = auth.TOKEN_LOGGED[0] # auth.token_generate('z3333333@gmail.com')
        GUEST_1_U_ID[0] = auth.token_to_u_id(GUEST_1_TOKEN[0])
        # auth.auth_logout(GUEST_1_TOKEN[0])
        channels.channels_create(ADMIN_TOKEN[0], "standup_test_channel", True)
        pass
        return function()
    return wrapper

@clear_buffer
def test_standup_start():
    '''
    test_standup_start correctly starts a standup with specified time length
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    assert str(channel_id) in standups.STANDUP_BUFFER.keys()
    time.sleep(length + 1)
    assert str(channel_id) not in standups.STANDUP_BUFFER.keys()
    pass

@clear_buffer
def test_standup_start_error_input_0():
    '''
    test_standup_start_error_input_0 correctly 
    raises an error if channel id is invalid
    '''
    channel_id = 111
    length = 3
    with pytest.raises(error.InputError):
        standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    pass

@clear_buffer
def test_standup_start_error_input_1():
    '''
    test_standup_start_error_input_1 correctly 
    raises an error if a standup is active at the moment
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    # testing starting while active
    with pytest.raises(error.InputError):
        standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    time.sleep(length + 1)
    pass

@clear_buffer
def test_standup_active():
    '''
    test_standup_active tells the correct state of standup in specified channel
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    assert standups.standup_active(ADMIN_TOKEN[0], channel_id)['is_active']
    time.sleep(length + 1)
    assert not standups.standup_active(ADMIN_TOKEN[0], channel_id)['is_active']
    pass 

@clear_buffer
def test_standup_active_error_input():
    '''
    test_standup_active raises errors if inputs are invalid
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    time.sleep(length + 1)
    with pytest.raises(error.InputError):
        invalid_channel_id = 111
        standups.standup_active(ADMIN_TOKEN[0], invalid_channel_id)
    pass 

@clear_buffer
def test_standup_send():
    '''
    test_standup_send correctly adds message to standup buffer
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    message_1 = 'line_1'
    message_2 = 'line_2'
    # send message to buffer
    standups.standup_send(ADMIN_TOKEN[0], channel_id, message_1)
    channel.channel_invite(ADMIN_TOKEN[0], channel_id, GUEST_1_U_ID[0])
    standups.standup_send(GUEST_1_TOKEN[0], channel_id, message_2)
    assert standups.STANDUP_BUFFER[str(channel_id)]['message_buffer'] \
                == 'adminadmin1: line_1\nguest1guest11: line_2'
    time.sleep(length + 1)
    assert channel.CHANNEL_DB[str(channel_id)]['message_history'] \
                             ['messages'][0]['message'] \
                == 'adminadmin1: line_1\nguest1guest11: line_2'
    pass

@clear_buffer
def test_standup_send_error_access():
    '''
    test_standup_send raises error if a user not in current channel 
    tries to send standup message
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    message_1 = 'line_1'
    message_2 = 'line_2'
    standups.standup_send(ADMIN_TOKEN[0], channel_id, message_1)
    # channel.channel_invite(ADMIN_TOKEN[0], channel_id, GUEST_1_U_ID[0])
    with pytest.raises(error.AccessError):
        standups.standup_send(GUEST_1_TOKEN[0], channel_id, message_2)
    time.sleep(length + 1)
    assert channel.CHANNEL_DB[str(channel_id)]['message_history'] \
                             ['messages'][0]['message'] \
                == 'adminadmin1: line_1'
    pass

@clear_buffer
def test_standup_send_error_input_0():
    '''
    test_standup_send raises errors if channel id is invalid
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    message_1 = 'line_1'
    # channel.channel_invite(ADMIN_TOKEN[0], channel_id, GUEST_1_U_ID[0])
    with pytest.raises(error.InputError):
        invalid_channel_id = 111
        standups.standup_send(ADMIN_TOKEN[0], invalid_channel_id, message_1)
    time.sleep(length + 1)
    pass

@clear_buffer
def test_standup_send_error_input_1():
    '''
    test_standup_send raises errors if message is too long
    '''
    channel_id = 1
    length = 3
    standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    message_2 = 'i' * 1001
    # channel.channel_invite(ADMIN_TOKEN[0], channel_id, GUEST_1_U_ID[0])
    with pytest.raises(error.InputError):
        standups.standup_send(ADMIN_TOKEN[0], channel_id, message_2)
    time.sleep(length + 1)
    pass

@clear_buffer
def test_standup_send_error_input_2():
    '''
    test_standup_send raises errors if a standup is never started
    '''
    channel_id = 1
    length = 3
    # standups.standup_start(ADMIN_TOKEN[0], channel_id, length)
    message_1 = 'i'
    # standups.standup_send(ADMIN_TOKEN[0], channel_id, message_1)
    # channel.channel_invite(ADMIN_TOKEN[0], channel_id, GUEST_1_U_ID[0])
    with pytest.raises(error.InputError):
        standups.standup_send(ADMIN_TOKEN[0], channel_id, message_1)
    time.sleep(length + 1)
    pass