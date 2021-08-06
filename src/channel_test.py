'''
This file is used to test all functions in Channel.py
'''

import ast
import random
import pytest
import auth
import channel
import channel_constant
import channels
import error
import channel_test_data
import other
import message as msg

# global variable place holder
ADMIN_TOKEN = [None]
ADMIN_U_ID = [None]
GUEST_1_TOKEN = [None]
GUEST_1_U_ID = [None]
GUEST_2_TOKEN = [None]
GUEST_2_U_ID = [None]

def clear_history(function):
    '''
    reset USER_DB and re-register certain accounts
    '''
    def wrapper():
        other.clear()
        #channels part
        auth.auth_register('z5555555@gmail.com', '1234567', 'admin', 'admin') # u_id = 1
        ADMIN_TOKEN[0] = auth.TOKEN_LOGGED[0] # auth.token_generate('z5555555@gmail.com')
        ADMIN_U_ID[0] = auth.token_to_u_id(ADMIN_TOKEN[0])
        auth.auth_logout(ADMIN_TOKEN[0])
        auth.auth_register('z3333333@gmail.com', '1234567', 'guest1', 'guest1') # u_id = 2
        GUEST_1_TOKEN[0] = auth.TOKEN_LOGGED[0] # auth.token_generate('z3333333@gmail.com')
        GUEST_1_U_ID[0] = auth.token_to_u_id(GUEST_1_TOKEN[0])
        auth.auth_logout(GUEST_1_TOKEN[0])
        auth.auth_register('z4444444@gmail.com', '1234567', 'guest2', 'guest2') # u_id = 3
        GUEST_2_TOKEN[0] = auth.TOKEN_LOGGED[0] # auth.token_generate('z4444444@gmail.com')
        GUEST_2_U_ID[0] = auth.token_to_u_id(GUEST_2_TOKEN[0])
        auth.auth_logout(GUEST_2_TOKEN[0])
        auth.auth_login('z5555555@gmail.com', '1234567')
        ADMIN_TOKEN[0] = auth.TOKEN_LOGGED[0]
        return function()
    return wrapper

@clear_history
def clear_history_test_part_1():
    '''
    testing if database is correctly cleared
    '''
    assert auth.U_ID_NUM[0] == 0
    assert len(auth.USER_DB) == 0
    assert len(auth.EMAIL_DB) == 0

@clear_history
def clear_history_test_part_2():
    '''
    testing if database is correctly cleared
    '''
    assert len(auth.TOKEN_DB) == 0
    assert len(auth.HANDLE) == 0
    assert len(channel.CHANNEL_DB) == 0

# tests combined effect of functions and
# states after individual executions
@clear_history
def test_combined_0():
    '''
    test db stats step by step, test all functions
    '''
    # make channel_db
    channel.CHANNEL_DB = channel_constant.CHANNEL_COMBINED_DB_0
    expect_channel_detail = channel_constant.EXPECTED_CHANNEL_COMBINED_CHANNEL_1
    expect_message_detail = channel_constant.EXPECTED_CHANNEL_COMBINED_MESSAGES

    # test channel_details, channel_message and channel_join in the same channel_db
    assert auth.TOKEN_LOGGED[0] in auth.TOKEN_DB.keys()
    channel.channel_join(auth.TOKEN_LOGGED[0], 12)
    expect_empty_detail = channel_constant.EXPECTED_CHANNEL_COMBINED_EMPTY_DETAIL
    assert channel.channel_details(auth.TOKEN_LOGGED[0], 12) == expect_empty_detail
    assert channel.channel_details(auth.TOKEN_LOGGED[0], 123) == expect_channel_detail
    assert channel.channel_messages(auth.TOKEN_LOGGED[0], 123, 0) == expect_message_detail
    channel.channel_invite(auth.TOKEN_LOGGED[0], 123, 2)
    print("Pass test_combined_0()")

@clear_history
def test_combined_1():
    '''
    test db stats step by step, test all functions through some regular operation
    '''
    # create channel_db
    channel.CHANNEL_DB = channel_constant.CHANNEL_COMBINED_DB_1
    # test channel_invite 
    assert auth.TOKEN_LOGGED[0] in auth.TOKEN_DB.keys()
    channel.channel_invite(auth.TOKEN_LOGGED[0], 123, 2)
    expect_channel_detail = channel_constant.EXPECTED_CHANNEL_COMBINED_CHANNEL_2
    # test chanel_details
    assert channel.channel_details(auth.TOKEN_LOGGED[0], 123) == expect_channel_detail
    channel.channel_addowner(auth.TOKEN_LOGGED[0], 123, 2)
    expect_channel_detail = channel_constant.EXPECTED_CHANNEL_COMBINED_CHANNEL_3
    assert channel.channel_details(auth.TOKEN_LOGGED[0], 123) == expect_channel_detail
    channel.channel_removeowner(auth.TOKEN_LOGGED[0], 123, 2)
    expect_channel_detail = channel_constant.EXPECTED_CHANNEL_COMBINED_CHANNEL_4
    assert channel.channel_details(auth.TOKEN_LOGGED[0], 123) == expect_channel_detail
    print("Pass test_combined_1()")

@clear_history
def test_is_owner():
    '''
    test is_owner() correctly identify a user is a channel owner or not
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    # test is_owner in each channel
    for channel_token in channel_tokens:
        channel_id = channel_token['channel_id']
        owner_lst = channel_token['owner_members']
        member_lst = channel_token['all_members']
        only_member_lst = [ast.literal_eval(item) for item in list(set([str(member) \
                           for member in member_lst])-set([str(owner) for owner in owner_lst]))]
        for owner in owner_lst:
            assert channel.is_owner(channel_id, owner['u_id'])
        for only_member in only_member_lst:
            assert not channel.is_owner(channel_id, only_member['u_id'])
    print("Pass test_is_owner()")

@clear_history
def test_is_member():
    '''
    test is_member() correctly identify a user is a channel member or not
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    # test is_member in each channel
    for channel_token in channel_tokens:
        channel_id = channel_token['channel_id']
        member_lst = channel_token['all_members']
        for member in member_lst:
            assert channel.is_member(channel_id, member['u_id'])
    print("Pass test_is_member()")

@clear_history
def test_channel_invite():
    '''
    test channel_invite() correctly invites a user to channel
    '''
    # craete channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    channel_id_lst = [channel_token['channel_id'] for channel_token in channel_tokens]
    # login a user
    auth.auth_login('z5555555@gmail.com', '1234567')
    ADMIN_TOKEN[0] = auth.TOKEN_LOGGED[0]
    # test if user is member or owner and then test channel_invite
    for sample_idx, _ in enumerate(channel_id_lst):
        for sample_member in channel_tokens[sample_idx]['all_members']:
            assert channel.is_member(channel_tokens[sample_idx]['channel_id'],
                                     sample_member['u_id'])
        assert not channel.is_member(channel_tokens[sample_idx]['channel_id'], GUEST_1_U_ID[0])
        channel.channel_invite(ADMIN_TOKEN[0], channel_id_lst[sample_idx], GUEST_1_U_ID[0])
        assert channel.is_member(channel_tokens[sample_idx]['channel_id'], GUEST_1_U_ID[0])
    print("Pass test_channel_invite()")

@clear_history
def test_channel_details():
    '''
    test channel_details() correctly shows details inside a channel
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    channel_id_lst = [channel_token['channel_id'] for channel_token in channel_tokens]
    pop_lst = ['channel_id', 'is_public', 'message_history']
    # login user
    auth.auth_login('z5555555@gmail.com', '1234567')
    ADMIN_TOKEN[0] = auth.TOKEN_LOGGED[0]
    # test details by loop
    for channel_token, channel_id in zip(channel_tokens, channel_id_lst):
        member_lst = channel_token['all_members']
        for key in pop_lst:
            channel_token.pop(key)
        detail = channel_token
        for sample_member in member_lst:
            channel.current_user_id = sample_member['u_id']
            assert detail == channel.channel_details(ADMIN_TOKEN[0], channel_id)
    print("Pass test_channel_details()")

@clear_history
def test_channel_messages():
    '''
    test channel_messages() shows message accordingly to function inputs
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    # test each channel by loop
    for channel_token in channel_tokens:
        # create expect results
        msgs_max = len(channel_token['message_history']['messages'])-1
        invalid_start = -5
        start_idx = random.randint(0, msgs_max-50)
        end_idx = min(start_idx + 50, msgs_max)
        new_msg_history = channel_token['message_history']['messages'][start_idx: end_idx]
        new_msg = channel_constant.MSG_TOKEN_TEMPLATE
        new_msg['messages'], new_msg['start'], new_msg['end'] = new_msg_history, start_idx, end_idx
        # login an user
        auth.auth_login('z5555555@gmail.com', '1234567')
        with pytest.raises(error.InputError):
            channel.channel_messages(auth.TOKEN_LOGGED[0],
                                     channel_token['channel_id'], invalid_start)
        assert new_msg == channel.channel_messages(auth.TOKEN_LOGGED[0], \
                                channel_token['channel_id'], start_idx)
    print("Pass test_channel_messages()")

@clear_history
def test_channel_messages_empty():
    '''
    test if function returns correct info while message history is empty
    '''
    # get token and channel_id
    token = ADMIN_TOKEN[0]
    ch_id = channels.channels_create(token, 'ch1', True)
    # expect result
    expect = {
        'messages': list(),
        'start': msg.DEFAULT_MESSAGE_HIST_START,
        'end': msg.DEFAULT_MESSAGE_HIST_END,
    }
    assert channel.channel_messages(token, ch_id['channel_id'], 0) == expect

@clear_history
def test_channel_leave_and_join():
    '''
    test channel_leave() and channel_join() correctly alters 
    member_list in specified channel
    '''
    # create chanenl_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    channel_id_lst = [channel_token['channel_id'] for channel_token in channel_tokens]
    # test each channel channel_leave and channel_join
    for sample_idx, _ in enumerate(channel_id_lst):
        auth.auth_login('z5555555@gmail.com', '1234567')
        assert channel.is_member(channel_tokens[sample_idx]['channel_id'], ADMIN_U_ID[0])
        channel.channel_leave(auth.TOKEN_LOGGED[0], channel_id_lst[sample_idx])
        assert not channel.is_member(channel_tokens[sample_idx]['channel_id'], ADMIN_U_ID[0])
        channel.channel_join(auth.TOKEN_LOGGED[0], channel_id_lst[sample_idx])
        assert channel.is_member(channel_tokens[sample_idx]['channel_id'], ADMIN_U_ID[0])
        with pytest.raises(error.AccessError):
            # join again while already joined
            channel.channel_join(auth.TOKEN_LOGGED[0], channel_id_lst[sample_idx])
    print("Pass test_channel_leave_and_join()")

@clear_history
def test_channel_addowner_and_removeowner_0():
    '''
    test channel_addowner() and channel_removeowner() correctly alters 
    owner_member_list in specified channel
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    channel_id_lst = [channel_token['channel_id'] for channel_token in channel_tokens]
    # test each channel channel_addowner and channel_removeowner
    for sample_idx, _ in enumerate(channel_id_lst):
        # login an user
        auth.auth_login('z5555555@gmail.com', '1234567')
        assert not channel.is_owner(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
        assert not channel.is_member(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
        channel.channel_addowner(auth.TOKEN_LOGGED[0],
                                 channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        #  test inputerror
        with pytest.raises(error.InputError):
            channel.channel_addowner(auth.TOKEN_LOGGED[0],
                                     channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        # test is_owner and is_member
        assert channel.is_owner(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
        assert channel.is_member(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
    print("Pass test_channel_removeowner_and_addowner()_0")

@clear_history
def test_channel_addowner_and_removeowner_1():
    '''
    test channel_addowner() and channel_removeowner() correctly alters 
    owner_member_list in specified channel
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    channel_id_lst = [channel_token['channel_id'] for channel_token in channel_tokens]
    # test each channel channel_addowner and channel_removeowner
    for sample_idx, _ in enumerate(channel_id_lst):
        # login user
        auth.auth_login('z5555555@gmail.com', '1234567')
        channel.channel_addowner(auth.TOKEN_LOGGED[0],
                                 channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        channel.channel_removeowner(auth.TOKEN_LOGGED[0],
                                    channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        # test inputerror
        with pytest.raises(error.InputError):
            channel.channel_removeowner(auth.TOKEN_LOGGED[0],
                                        channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        assert not channel.is_owner(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
        assert channel.is_member(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
        channel.channel_addowner(auth.TOKEN_LOGGED[0], channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        #  test is_owner and is_member
        assert channel.is_owner(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
        assert channel.is_member(channel_tokens[sample_idx]['channel_id'], GUEST_2_U_ID[0])
    print("Pass test_channel_removeowner_and_addowner_1()")

@clear_history
def test_channel_addowner_and_removeowner_2():
    '''
    test channel_addowner() and channel_removeowner() correctly alters 
    owner_member_list in specified channel
    '''
    # create channel_db
    token, channel_tokens = channel_test_data.make_token()
    channel.CHANNEL_DB = token
    channel_id_lst = [channel_token['channel_id'] for channel_token in channel_tokens]
    # test each channel channel_addowner and channel_removeowner
    for sample_idx, _ in enumerate(channel_id_lst):
        # user login
        auth.auth_login('z5555555@gmail.com', '1234567')
        channel.channel_addowner(auth.TOKEN_LOGGED[0],
                                 channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        channel.channel_removeowner(auth.TOKEN_LOGGED[0],
                                    channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        channel.channel_addowner(auth.TOKEN_LOGGED[0], channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        channel.channel_removeowner(auth.TOKEN_LOGGED[0],
                         channel_id_lst[sample_idx], GUEST_2_U_ID[0])
        assert not channel.is_owner(channel_tokens[sample_idx]['channel_id'], 
                            GUEST_2_U_ID[0])
        # switch current user
        auth.auth_login('z3333333@gmail.com', '1234567')
        with pytest.raises(error.AccessError):
            channel.channel_removeowner(auth.TOKEN_LOGGED[0],
                                        channel_id_lst[sample_idx], GUEST_2_U_ID[0])
    print("Pass test_channel_removeowner_and_addowner_2()")

@clear_history
def test_exceptions_0():
    '''
    test possible exceptions for all functions in channel.py part 0
    '''
    auth.auth_login('z5555555@gmail.com', '1234567')
    channel.CHANNEL_DB = channel_constant.CHANNEL_EXCEPTIONS_DB_0
    # invalid channel_id
    with pytest.raises(error.InputError):
        channel.valid_channel_id(1)
    # invalid email
    with pytest.raises(error.AccessError):
        channel.valid_token(auth.token_generate("invalid@email"))
    # invalid user
    with pytest.raises(error.InputError):
        channel.valid_user(str(5))
    print("Pass test_exceptions_0()")

@clear_history
def test_exceptions_1():
    '''
    test possible exceptions for all functions in channel.py part 1
    '''
    auth.auth_login('z5555555@gmail.com', '1234567')
    channel.CHANNEL_DB = channel_constant.CHANNEL_EXCEPTIONS_DB_1
    # assumes channel_id and u_id are valid
    # test channel_invite
    with pytest.raises(error.AccessError):
        channel.channel_invite(auth.TOKEN_LOGGED[0], 12, 1)

    with pytest.raises(error.InputError):
        channel.channel_invite(auth.TOKEN_LOGGED[0], 123, 1)
    # test channel_details
    with pytest.raises(error.AccessError):
        channel.channel_details(auth.TOKEN_LOGGED[0], 12)
    # test channel_messages
    with pytest.raises(error.InputError):
        channel.channel_messages(auth.TOKEN_LOGGED[0], 123, 100)
    # test channel_leave
    with pytest.raises(error.AccessError):
        channel.channel_leave(auth.TOKEN_LOGGED[0], 12)

    print("Pass test_exceptions_1()")

@clear_history
def test_exceptions_2():
    '''
    test possible exceptions for all functions in channel.py part 2
    '''
    # login users and create channel_db
    auth.auth_login('z5555555@gmail.com', '1234567')
    channel.CHANNEL_DB = channel_constant.CHANNEL_EXCEPTIONS_DB_2
    auth.auth_login('z4444444@gmail.com', '1234567')
    # channel_join
    with pytest.raises(error.AccessError):
        channel.channel_join(auth.TOKEN_LOGGED[0], 1234)
    # test channel_messages
    with pytest.raises(error.AccessError):
        channel.channel_messages(auth.TOKEN_LOGGED[0], 1234, 0)
    # test channel_addowner
    with pytest.raises(error.AccessError):
        channel.channel_addowner(auth.TOKEN_LOGGED[0], 1234, 1)
    print("Pass test_exceptions_2()")

@clear_history
def test_channel_join_flockr_owner():
    '''
    test flockr owner directly join private/public channel
    automaticly adds him/her to owner_member list
    '''
    # login user and create channel_db
    auth.auth_login('z5555555@gmail.com', '1234567')
    channel.CHANNEL_DB = channel_constant.CHANNEL_FLOCKR_OWNER_DB
    # join channel 1
    channel.channel_join(auth.TOKEN_LOGGED[0], 1)
    assert channel.is_owner(1, auth.token_to_u_id(auth.TOKEN_LOGGED[0]))
    assert channel.is_member(1, auth.token_to_u_id(auth.TOKEN_LOGGED[0]))
    # join channel 123
    channel.channel_join(auth.TOKEN_LOGGED[0], 123)
    assert channel.is_owner(123, auth.token_to_u_id(auth.TOKEN_LOGGED[0]))
    assert channel.is_member(123, auth.token_to_u_id(auth.TOKEN_LOGGED[0]))
    with pytest.raises(error.AccessError):
        channel.channel_admin_join(auth.TOKEN_LOGGED[0], 123, "wrong_password")
    print("Pass test_channel_join_flockr_owner()")

@clear_history
def test_channel_addowner_and_removeowner_flockr_owner():
    '''
    test the permission of flockr owner is correctly implemented
    so he/she can directly add/remove channel owner while inside a channel
    '''
    auth.auth_login('z5555555@gmail.com', '1234567')
    channel.CHANNEL_DB = channel_constant.CHANNEL_FLOCKR_OWNER_DB_2
    auth.add_flockr_owner(auth.TOKEN_LOGGED[0], GUEST_1_U_ID[0])
    # while a flokr owner is INVITED, he automatically becomes one of the channel owner
    channel.channel_invite(auth.TOKEN_LOGGED[0], 234, GUEST_1_U_ID[0])
    assert channel.is_member(234, GUEST_1_U_ID[0])
    assert channel.is_owner(234, GUEST_1_U_ID[0])
    # well, a flokr owner can de-owner himself from a channel :P
    # To reset himself back to channel owner group, just leave and join again :P
    channel.channel_removeowner(auth.TOKEN_LOGGED[0], 234, GUEST_1_U_ID[0])
    assert channel.is_member(234, GUEST_1_U_ID[0])
    assert not channel.is_owner(234, GUEST_1_U_ID[0])
    print("Pass test_channel_addowner_and_removeowner_flockr_owner()")

@clear_history
def test_channel_messages_react():
    '''
    test is_this_user_reacted in reacts
    '''
    # reset all info
    msg.reset_id_gen()
    # create channel_db
    channel.CHANNEL_DB = channel_constant.MESSAGE_TEST_USER_REACTED
    # create user1 and let admin joins the channel 1
    token = ADMIN_TOKEN[0] 
    channel_id = 1
    channel.channel_join(token, channel_id)
    # create user2 and let admin joins the channel 1
    auth.auth_login('z3333333@gmail.com', '1234567')
    token2 = auth.TOKEN_LOGGED[0]
    channel.channel_join(token2, channel_id)

    # the react version that user1 can see
    result_msg_for_token = channel.channel_messages(token, channel_id, 0)
    assert result_msg_for_token == channel_constant.EXPECT_MESSAGE_TEST_USER_REACTED_1

    # the react version that user2 can see
    result_msg_for_token2 = channel.channel_messages(token2, channel_id, 0)
    assert result_msg_for_token2 == channel_constant.EXPECT_MESSAGE_TEST_USER_REACTED_2

