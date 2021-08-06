'''
test other.py
'''

import time
import pytest
import channel_test
import channels
import channel
import message
import auth
import user
import other
import error
import standups

def test_clear():
    '''
    test clear function correctly emties all databases
    '''
    other.clear()
    assert auth.U_ID_NUM[0] == 0
    assert auth.USER_DB == {}
    assert auth.EMAIL_DB == {}
    assert auth.TOKEN_DB == {}
    assert auth.HANDLE == {}
    assert channel.CHANNEL_DB == {}
    assert channels.CHANNEL_NUM == [0]
    assert standups.STANDUP_BUFFER == {}
    assert message.USED_MESSAGE_ID == 0

@channel_test.clear_history
def test_user_all():
    '''
    test user_all correctly shows user profile of all users in sequence of user id
    '''
    token = channel_test.ADMIN_TOKEN[0]
    test_user1 = user.user_profile(token, 1)['user']
    test_user2 = user.user_profile(token, 2)['user']
    test_user3 = user.user_profile(token, 3)['user']
    test_users = {
        'users': [test_user1, test_user2, test_user3]
    }
    assert other.users_all(token) == test_users

@channel_test.clear_history
def test_admin_userpermission_change():
    '''
    test admin_userpermission_change correctly modifies other users' permission
    '''
    auth.auth_login('z3333333@gmail.com', '1234567')
    channel_test.GUEST_1_TOKEN[0] = auth.TOKEN_LOGGED[0]
    token = channel_test.GUEST_1_TOKEN[0]
    u_id = 2
    permission_id = other.PERM_ID_FLOCKR_ADMIN
    with pytest.raises(error.AccessError):
        other.admin_userpermission_change(token, u_id, permission_id)

    token = channel_test.ADMIN_TOKEN[0]
    u_id = 500
    permission_id = other.PERM_ID_FLOCKR_ADMIN
    with pytest.raises(error.InputError):
        other.admin_userpermission_change(token, u_id, permission_id)

    token = channel_test.ADMIN_TOKEN[0]
    u_id = 2
    permission_id = -1 * other.PERM_ID_FLOCKR_ADMIN
    with pytest.raises(error.InputError):
        other.admin_userpermission_change(token, u_id, permission_id)

    # black box testing:
    # a set b to admin, b set a to member, a failed to set b to member
    token = channel_test.ADMIN_TOKEN[0]
    u_id = 2
    permission_id = other.PERM_ID_FLOCKR_ADMIN
    other.admin_userpermission_change(token, u_id, permission_id)

    token = channel_test.GUEST_1_TOKEN[0]
    u_id = 1
    permission_id = other.PERM_ID_FLOCKR_MEMBER
    other.admin_userpermission_change(token, u_id, permission_id)

    token = channel_test.ADMIN_TOKEN[0]
    u_id = 2
    permission_id = other.PERM_ID_FLOCKR_MEMBER
    with pytest.raises(error.AccessError):
        other.admin_userpermission_change(token, u_id, permission_id)

@channel_test.clear_history
def test_search():
    '''
    test search can find message based on given sub_string (case matching) 
    also make sure user will not get message from channels which he/she is 
    not a member of
    '''
    token_admin = channel_test.ADMIN_TOKEN[0]
    auth.auth_login('z3333333@gmail.com', '1234567')
    token_guest_1 = auth.TOKEN_LOGGED[0]
    # print(channel.CHANNEL_DB)
    ch_id_1 = channels.channels_create(token_admin, 'channel1', True)
    me_id_1 = message.message_send(token_admin, ch_id_1['channel_id'], 'hello')
    message.message_send(token_admin, ch_id_1['channel_id'], 'how are u')

    # test just one channel has 'hello'
    expect_one_ch = {
        'messages':[
            {
                'message_id': me_id_1['message_id'],
                'u_id': 1,
                'message': 'hello',
                'time_created': int(time.time()),
                'reacts': [],
                'is_pinned': False
            },
        ],
    }
    assert other.search(token_admin, 'hello') == expect_one_ch

    # test one channel has more than one 'hello'
    me_id_5 = message.message_send(token_admin, ch_id_1['channel_id'], 'hello')
    expect_same_ch = {
        'messages':[
            {
                'message_id': me_id_5['message_id'],
                'u_id': 1,
                'message': 'hello',
                'time_created': int(time.time()),
                'reacts': [],
                'is_pinned': False
            },
            {
                'message_id': me_id_1['message_id'],
                'u_id': 1,
                'message': 'hello',
                'time_created': int(time.time()),
                'reacts': [],
                'is_pinned': False
            },
        ],
    }
    assert other.search(token_admin, 'hello') == expect_same_ch

    # test diff channels have 'hello'
    ch_id_2 = channels.channels_create(token_admin, 'channel2', True)
    me_id_3 = message.message_send(token_admin, ch_id_2['channel_id'], 'hello')
    message.message_send(token_admin, ch_id_2['channel_id'], "what's up")

    expect_diff_ch = {
        'messages':[
            {
                'message_id': me_id_5['message_id'],
                'u_id': 1,
                'message': 'hello',
                'time_created': int(time.time()),
                'reacts': [],
                'is_pinned': False
            },
            {
                'message_id': me_id_1['message_id'],
                'u_id': 1,
                'message': 'hello',
                'time_created': int(time.time()),
                'reacts': [],
                'is_pinned': False
            },
            {
                'message_id': me_id_3['message_id'],
                'u_id': 1,
                'message': 'hello',
                'time_created': int(time.time()),
                'reacts': [],
                'is_pinned': False
            },
        ],
    }
    assert other.search(token_admin, 'hello') == expect_diff_ch
    assert other.search(token_guest_1, 'hello') == {'messages':[]}
