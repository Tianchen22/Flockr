'''
    message_test
'''

import time
import pytest
import error
import auth
import channel
import channels
import message
import message_constant
import channel_test

def test_message_id_generator():
    '''
    test message_id_generator generates correct sequence of message ids
    '''
    message.reset_id_gen()
    assert message.message_id_generator() == 1

@channel_test.clear_history
def test_message_id_finder_0():
    '''
    test_message_id_finder_0 returns an error while looking for non-exist message id
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_0_ID_FINDER
    with pytest.raises(error.InputError):
        message.message_id_finder(1)

@channel_test.clear_history
def test_message_id_finder_1():
    '''
    test_message_id_finder_1 correctly find a message while message exist
    '''
    # create channel_db
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_ID_FINDER
    # expect result foe msg1
    result = {
        'channel_id': 12,
        'message_id': 1,
        'poster_id': 1
    }
    assert message.message_id_finder(1) == result
    # expect result foe msg2
    result = {
        'channel_id': 123,
        'message_id': 2,
        'poster_id': 2
    }
    assert message.message_id_finder(2) == result

@channel_test.clear_history
def test_create_message():
    '''
    test_create_message creates a intended pattern and correct message
    '''
    u_id = 1
    strr = "Hello Heyden"
    # expect msg info
    new_message = dict()
    new_message['message_id'] = 1
    new_message['u_id'] = u_id
    new_message['message'] = strr
    new_message['time_created'] = int(time.time())
    created_msg = message.create_message(u_id, strr)
    # test if the result and expect msg info are equal
    assert new_message['message_id'] == created_msg['message_id']
    assert new_message['u_id'] == created_msg['u_id']
    assert new_message['message'] == created_msg['message']

@channel_test.clear_history
def test_initiat_message_history():
    '''
    test_initiat_message_history correctly handles "None" inital 
    value inside message_history
    '''
    # create channel_db
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_INIT_HISTORY
    assert message.initiat_message_history(12, "new_msg") == True
    assert channel.CHANNEL_DB['12']['message_history'] != None and \
            channel.CHANNEL_DB['12']['message_history'] != {}
    # expect result
    init_template = {
        'messages': ["new_msg"],
        'start': message.DEFAULT_MESSAGE_HIST_START,
        'end': message.DEFAULT_MESSAGE_HIST_END
    }
    assert channel.CHANNEL_DB['12']['message_history'] == init_template
    assert message.initiat_message_history(123, "new_msg") == False

@channel_test.clear_history
def test_message_send():
    '''
    test_message_send pushed messages into message history in correct order
    '''
    # create channel_db
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_0_SEND
    # get an user token and let the user join the channel
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 12
    channel.channel_join(token, channel_id)
    # send msg and test return the correct message_id
    strr = "Oops Heyden"
    send_return = message.message_send(token, channel_id, strr)
    assert send_return == {'message_id': 1}
    strr2 = "oshit"
    send_return = message.message_send(token, channel_id, strr2)
    assert send_return == {'message_id': 2}
    # test msg has the correct info in channel_db
    # test msg1
    new_message = dict()
    new_message['message_id'] = 1
    new_message['u_id'] = auth.token_to_u_id(channel_test.ADMIN_TOKEN[0])
    new_message['message'] = strr
    new_message['time_created'] = int(time.time())
    assert new_message['message_id'] == \
        channel.CHANNEL_DB[str(channel_id)]['message_history']['messages'][1]['message_id']
    assert new_message['u_id'] == \
        channel.CHANNEL_DB[str(channel_id)]['message_history']['messages'][1]['u_id']
    assert new_message['message'] == \
        channel.CHANNEL_DB[str(channel_id)]['message_history']['messages'][1]['message']
    # test msg2
    new_message_1 = dict()
    new_message_1['message_id'] = 2
    new_message_1['u_id'] = auth.token_to_u_id(channel_test.ADMIN_TOKEN[0])
    new_message_1['message'] = strr2
    new_message_1['time_created'] = int(time.time())
    assert new_message_1['message_id'] == \
        channel.CHANNEL_DB[str(channel_id)]['message_history']['messages'][0]['message_id']
    assert new_message_1['u_id'] == \
        channel.CHANNEL_DB[str(channel_id)]['message_history']['messages'][0]['u_id']
    assert new_message_1['message'] == \
        channel.CHANNEL_DB[str(channel_id)]['message_history']['messages'][0]['message']

@channel_test.clear_history
def test_message_remove():
    '''
    test_message_remove correctly removes intended message 
    and leaves message history data structure unharmed
    '''
    # create channel_db and get an user token
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_0_MSG_REMOVE
    token = channel_test.ADMIN_TOKEN[0]
    channel_id_0 = 12
    channel_id_1 = 123
    # let user join the channels
    channel.channel_join(token, channel_id_0)
    channel.channel_join(token, channel_id_1)
    # remove msg
    message.message_remove(token, 1)
    # if list of messages is empty then message_remove works
    assert 0 == \
        len(channel.CHANNEL_DB[str(channel_id_0)]['message_history']['messages'])
    message.message_remove(token, 2)
    assert 0 == \
        len(channel.CHANNEL_DB[str(channel_id_1)]['message_history']['messages'])
    pass

@channel_test.clear_history
def test_message_edit():
    '''
    test_message_edit correctly alters message into new message entered
    '''
    # create channel_db and get an user token
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_0_MSG_EDIT
    token = channel_test.ADMIN_TOKEN[0]
    channel_id_0 = 12
    channel_id_1 = 123
    # let the user join the channel
    channel.channel_join(token, channel_id_0)
    channel.channel_join(token, channel_id_1)
    # change the msg to empty string "", 
    # if new message is "", then remove message
    message.message_edit(token, 1, "")
    assert 0 == \
        len(channel.CHANNEL_DB[str(channel_id_0)]['message_history']['messages'])
    # change msg to new_msg
    new_msg = "Viva Heyden"
    message.message_edit(token, 2, new_msg)
    assert 1 == \
        len(channel.CHANNEL_DB[str(channel_id_1)]['message_history']['messages'])
    assert new_msg == \
        channel.CHANNEL_DB[str(channel_id_1)]['message_history']['messages'][0]['message']

@channel_test.clear_history
def test_error_send():
    '''
    test_error_send check if message_send raises correct error with invalid inputs
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_0_ERROR
    token = channel_test.ADMIN_TOKEN[0]
    # test if user is not in the channel
    channel_id_0 = 12
    strr = "".join(["i" for i in range(20)])
    with pytest.raises(error.AccessError):
        message.message_send(token, channel_id_0, strr)
    channel.channel_join(token, channel_id_0)
    # test msg is too long
    strr = "".join(["i" for i in range(1001)])
    with pytest.raises(error.InputError):
        message.message_send(token, channel_id_0, strr)

@channel_test.clear_history
def test_error_remove_and_edit():
    '''
    test_error_remove_and_edit check if message_remove and message_edit 
    raises correct error with invalid inputs
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_ERROR
    token = channel_test.ADMIN_TOKEN[0]
    channel_id_0 = 12
    # if user is not in the channel
    with pytest.raises(error.AccessError):
        message.message_remove(token, 2)
    with pytest.raises(error.AccessError):
        message.message_edit(token, 2, "???")
    channel.channel_join(token, channel_id_0)
    # invalid message_id
    with pytest.raises(error.InputError):
        message.message_remove(token, 3)
    with pytest.raises(error.InputError):
        message.message_edit(token, 3, "??????")

@channel_test.clear_history
def test_message_sendlater():
    '''
    simple test for message_sendlater
    but maybe coverage of this function cannot be up to 100% since it is hard to test
    '''
    # create channel_db and get an user token
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_SEND
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 1
    # join the channel
    channel.channel_join(token, channel_id)
    # send msg1 later
    strr = "Oops Heyden"
    time_now = int(time.time())
    time_sent = time_now + 2
    result_sendlater = message.message_sendlater(token, channel_id, strr, time_sent)
    # test if threding is working
    assert message.check_sendlater() == True
    assert result_sendlater['message_id'] == 1
    # send msg2 later
    strr2 = "oshit"
    send_return = message.message_send(token, channel_id, strr2)
    assert send_return['message_id'] == 2
    # send msg3 later
    strr3 = "ohhhhh"
    time_sent2 = time_now + 3
    send_return2 = message.message_sendlater(token, channel_id, strr3, time_sent2)
    assert send_return2['message_id'] == 3

@channel_test.clear_history
def test_message_sendlater_inputerror():
    '''
    test inputerror of sendlater while invalid inputs
    '''
    # create channel_db and get token
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_2_SEND
    token = channel_test.ADMIN_TOKEN[0]
    # join channel
    channel_id = 2
    channel.channel_join(token, channel_id)
    # invalid channel_id
    wrong_ch_id = 100
    strr = 'hhh'
    time_now = int(time.time())
    time_sent = time_now + 2
    with pytest.raises(error.InputError):
        message.message_sendlater(token, wrong_ch_id, strr, time_sent)
    # message more than 1000
    strr2 = "".join(["i" for i in range(1001)])
    time_now = int(time.time())
    time_sent = time_now + 2
    with pytest.raises(error.InputError):
        message.message_sendlater(token, channel_id, strr2, time_sent)
    # time sent is a time in the past
    strr3 = 'hhhh'
    wrong_time_sent = time_now - 3
    with pytest.raises(error.InputError):
        message.message_sendlater(token, channel_id, strr3, wrong_time_sent)

@channel_test.clear_history
def test_message_sendlater_accesserror():
    '''
    test AccessError if a invalid user is using the function
    '''
    # create channel and get token
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_3_ERROR
    token = channel_test.ADMIN_TOKEN[0]
    channel_id_0 = 1
    time_now = int(time.time())
    time_sent = time_now + 2
    strr = "".join(["i" for i in range(20)])
    # user is not in the channel -- AccessError
    with pytest.raises(error.AccessError):
        message.message_sendlater(token, channel_id_0, strr, time_sent)

@channel_test.clear_history
def test_message_react():
    '''
    use two tokens to test
    just in one message
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_REACT
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 1
    # the first user joins the channel and react the msg1
    channel.channel_join(token, channel_id)
    message.message_react(token, 1, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_1_REACT

    # the second user react the msg1
    auth.auth_login('z3333333@gmail.com', '1234567')
    token2 = auth.TOKEN_LOGGED[0]
    channel.channel_join(token2, channel_id)
    message.message_react(token2, 1, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_2_REACT

    # already contains an active React
    with pytest.raises(error.InputError):
        message.message_react(token2, 1, 1)

    # invalid React Id:
    with pytest.raises(error.InputError):
        message.message_react(token, 1, 0)
    with pytest.raises(error.InputError):
        message.message_react(token2, 1, 11)

@channel_test.clear_history
def test_message_react_more_msg():
    '''
    use one token and more msgs
    '''
    # create channel_db and get token
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_3_REACT
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 3
    channel.channel_join(token, channel_id)
    # react to 2 msgs
    message.message_react(token, 1, 1)
    message.message_react(token, 2, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_3_REACT

@channel_test.clear_history
def test_message_react_error():
    '''
    invalid token
    '''
    message.reset_id_gen()
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_2_REACT
    token = channel_test.ADMIN_TOKEN[0]
    with pytest.raises(error.InputError):
        message.message_react(token, 1, 1)

@channel_test.clear_history
def test_message_unreact():
    '''
    test message_unreact
    remove two reacts
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_UNREACT
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 1
    channel.channel_join(token, channel_id)
    message.message_unreact(token, 1, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_1_UNREACT
    message.message_unreact(token, 2, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_2_UNREACT

    # not valid message id
    with pytest.raises(error.InputError):
        message.message_unreact(token, 3, 1)

    # invalid react_id
    with pytest.raises(error.InputError):
        message.message_unreact(token, 1, 0)
    with pytest.raises(error.InputError):
        message.message_unreact(token, 1, 10)

    # not contain an active React
    with pytest.raises(error.InputError):
        message.message_unreact(token, 1, 1)

@channel_test.clear_history
def test_message_unreact_error():
    '''
    test if errors are correctly raised with invalid token 
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_2_UNREACT
    token = channel_test.ADMIN_TOKEN[0]
    with pytest.raises(error.InputError):
        message.message_unreact(token, 1, 1)

@channel_test.clear_history
def test_message_pin():
    '''
    test message_pin correctly pins messages
    '''
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_PIN
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 1
    channel.channel_join(token, channel_id)
    # user pins the msg1 and msg4 in channel 1
    message.message_pin(token, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_1_PIN
    message.message_pin(token, 4)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_2_PIN
    # user pins the msg10 in channel 2
    channel_id2 = 2
    channel.channel_join(token, channel_id2)
    message.message_pin(token, 10)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_3_PIN

    # invalid message_id
    with pytest.raises(error.InputError):
        message.message_pin(token, 8)

    # is already pinned
    with pytest.raises(error.InputError):
        message.message_pin(token, 1)
    with pytest.raises(error.InputError):
        message.message_pin(token, 10)

@channel_test.clear_history
def test_message_pin_error():
    '''
    invalid token
    user is not a member and owner of channel
    '''
    channel_id = 1
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_PIN_ERROR
    token = channel_test.ADMIN_TOKEN[0]
    # not member and not owner
    with pytest.raises(error.AccessError):
        message.message_pin(token, 1)
    # is member not owner
    auth.auth_login('z3333333@gmail.com', '1234567')
    token2 = auth.TOKEN_LOGGED[0]
    channel.channel_join(token2, channel_id)
    with pytest.raises(error.AccessError):
        message.message_pin(token2, 1)

@channel_test.clear_history
def test_message_unpin():
    '''
    test message_unpin successfully unpins message
    '''
    channel_id = 1
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_2_PIN
    token = channel_test.ADMIN_TOKEN[0]
    channel_id = 1
    channel_id2 = 2
    channel.channel_join(token, channel_id)
    channel.channel_join(token, channel_id2)
    # user unpins the msg1 in channel 1
    message.message_unpin(token, 1)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_4_PIN
    # user unpins the msg10 in channel 2
    message.message_unpin(token, 10)
    assert channel.CHANNEL_DB == message_constant.EXPECT_MESSAGE_TEST_5_PIN

    # invalid message_id
    with pytest.raises(error.InputError):
        message.message_unpin(token, 7)

    # message_id already unpinned
    with pytest.raises(error.InputError):
        message.message_unpin(token, 2)

@channel_test.clear_history
def test_message_unpin_error():
    '''
    test if error is correctly raised while a invalid token is given
    user is not a member and owner of channel
    '''
    channel_id = 1
    channel.CHANNEL_DB = message_constant.MESSAGE_TEST_1_UNPIN_ERROR
    token = channel_test.ADMIN_TOKEN[0]
    # not member and not owner
    with pytest.raises(error.AccessError):
        message.message_unpin(token, 1)
    # is member not owner
    channel.channel_join(token, channel_id)
    auth.auth_login('z3333333@gmail.com', '1234567')
    token2 = auth.TOKEN_LOGGED[0]
    channel.channel_join(token2, channel_id)
    with pytest.raises(error.AccessError):
        message.message_unpin(token2, 1)
