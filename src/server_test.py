'''
    Template example for server test in Iteration 2
    follow this structure and style
    the test should be different from the test in Iteration 1
'''
import signal
import re
from subprocess import Popen, PIPE
from time import sleep
import json
import requests
import pytest
import error
import urllib
import channel
import auth
import other
import message
import time
import standups

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    '''
    Get the server url(and oprn the server if off)
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_clear(url):
    '''
    simple test to clear all history
    '''
    resp = requests.delete(url + 'clear')
    assert sum(resp.json()) == 0 
    # all lengths of dicts and initial values are zero

def test_auth_register(url):
    '''
    A simple test to check auth/register
    '''
    resp = requests.post(url + 'auth/register', json={
        'email': 'z55555@gmail.com',
        'password': '123123',
        'name_first': 'Bruce',
        'name_last': 'Wayne',
    })
    resp = resp.json()
    assert resp['token'] and resp['u_id'] 
    return resp['token']
    
def test_auth_login(url):
    '''
    A simple test to check auth/login
    '''
    test_auth_register(url)
    resp = requests.post(url + 'auth/login', json={
        'email': 'z55555@gmail.com',
        'password': '123123',
    })
    assert resp != {}

def test_auth_login_wrong_password(url):
    '''
    A simple test to check auth/login wrong password
    with pytest.raises(error.InputError):
        requests.post(url + 'auth/login', json={
            'email': 'z55555@gmail.com',
            'password': '0xFFFF',
    '''
    test_auth_register(url)
    resq = requests.post(url + 'auth/login', json={
        'email': 'z55555@gmail.com',
        'password': '0xFFFF',
    })
    resq = resq.json()
    assert resq['code'] == 400 # 400 is the return value of InputError

def test_auth_register_invalid_email(url):
    '''
    A simple test to check auth/register invalid_email
    '''
    resq = requests.post(url + 'auth/register', json={
        'email': '@gmail.com',
        'password': '123123',
        'name_first': 'Bruce',
        'name_last': 'Wayne',
    })
    resq = resq.json()
    assert resq['code'] == 400 # 400 is the return value of InputError

def test_auth_logout(url):
    '''
    A simple test to check auth/logout
    '''
    token = test_auth_register(url)
    resp = requests.post(url + 'auth/logout', json={
        'token': token,
    })
    resp = resp.json()
    assert resp['is_success']

def test_auth_logout_twice(url):
    '''
    A simple test to check auth/logout twice
    '''
    token = test_auth_register(url)
    requests.post(url + 'auth/logout', json={
        'token': token,
    })
    resp = requests.post(url + 'auth/logout', json={
        'token': token,
    })
    resp = resp.json()
    assert resp['is_success'] == False

def user1(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + 'auth/login', json={
        'email': 'z55555@gmail.com',
        'password': '123123',
    })
    user = resp.json()
    return user['token'], user['u_id']

def user1_create(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + 'auth/register', json={
        'email': 'z55555@gmail.com',
        'password': '123123',
        'name_first': 'Test',
        'name_last': 'Name',
    })
    user = resp.json()
    return user['token'], user['u_id']

def user2(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + "auth/login", json={
        'email': 'z11111@gmail.com',
        'password': '123456',
    })
    user = resp.json()
    return user['token'], user['u_id']

def user2_create(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + "auth/register", json={
        'email': 'z11111@gmail.com',
        'password': '123456',
        'name_first': 'Test2',
        'name_last': 'Name2',
    })
    user = resp.json()
    return user['token'], user['u_id']

def test_channels_create_user1(url):
    '''
    test for channels/create(post)
    one user create 2 channels
    '''
    token_1 = user1_create(url)[0]
    ch_resp = requests.post(url + "channels/create", json={
        'token': token_1,
        'name': 'testname1',
        'is_public': True,
    })

    channel = ch_resp.json()
    assert channel['channel_id'] == 1

    ch_resp2 = requests.post(url + "channels/create", json={
        'token': token_1,
        'name': 'testname2',
        'is_public': True,
    })

    channel2 = ch_resp2.json()
    assert channel2['channel_id'] == 2

def test_channels_create_user2(url):
    '''
    test for channels/create(post)
    another user create 2 channels
    '''
    token_2 = user2_create(url)[0]

    ch_resp = requests.post(url + "channels/create", json={
        'token': token_2,
        'name': 'testname3',
        'is_public': True,
    })
    assert ch_resp

    ch_resp2 = requests.post(url + "channels/create", json={
        'token': token_2,
        'name': 'testname4',
        'is_public': True,
    })
    assert ch_resp2

def test_channels_list_user1(url):
    '''
    test for channels/list (get)
    '''
    test_clear(url)
    test_channels_create_user1(url)
    token_1, u_id1 = user1(url)
    expect = {
        'channels': [
            {
                'name': 'testname1',
                'channel_id': 1,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': u_id1,
                        'name_first': 'Test',
                        'name_last': 'Name',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': u_id1,
                        'name_first': 'Test',
                        'name_last': 'Name',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'testname2',
                'channel_id': 2,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': u_id1,
                        'name_first': 'Test',
                        'name_last': 'Name',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': u_id1,
                        'name_first': 'Test',
                        'name_last': 'Name',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
        ]
    }

    ch_rep = requests.get(url + 'channels/list', params ={'token': token_1})
    ch_list = ch_rep.json()
    assert ch_list['channels'] == expect['channels']

def test_channels_listall(url):
    '''
    test for channels/listall(get)
    '''
    test_clear(url)
    test_channels_create_user1(url)
    test_channels_create_user2(url)
    token_1, u_id1 = user1(url)
    token_2, u_id2 = user2(url)

    expect = [
        {
            'name': 'testname1',
            'channel_id': 1,
            'is_public': True,
            'owner_members': [
                {
                    'u_id': u_id1,
                    'name_first': 'Test',
                    'name_last': 'Name',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': u_id1,
                    'name_first': 'Test',
                    'name_last': 'Name',
                    'profile_img_url': '',
                }
            ],
            'message_history': None,
        },
        {
            'name': 'testname2',
            'channel_id': 2,
            'is_public': True,
            'owner_members': [
                {
                    'u_id': u_id1,
                    'name_first': 'Test',
                    'name_last': 'Name',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': u_id1,
                    'name_first': 'Test',
                    'name_last': 'Name',
                    'profile_img_url': '',
                }
            ],
            'message_history': None,
        },
        {
            'name': 'testname3',
            'channel_id': 3,
            'is_public': True,
            'owner_members': [
                {
                    'u_id': u_id2,
                    'name_first': 'Test2',
                    'name_last': 'Name2',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': u_id2,
                    'name_first': 'Test2',
                    'name_last': 'Name2',
                    'profile_img_url': '',
                }
            ],
            'message_history': None,
        },
        {
            'name': 'testname4',
            'channel_id': 4,
            'is_public': True,
            'owner_members': [
                {
                    'u_id': u_id2,
                    'name_first': 'Test2',
                    'name_last': 'Name2',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': u_id2,
                    'name_first': 'Test2',
                    'name_last': 'Name2',
                    'profile_img_url': '',
                }
            ],
            'message_history': None,
        },
    ]

    listall1 = requests.get(url + 'channels/listall', params ={'token': token_1})
    listall2 = requests.get(url + 'channels/listall', params ={'token': token_2})
    ch_listall1 = listall1.json()
    ch_listall2 = listall2.json()

    assert ch_listall1['channels'] == expect
    assert ch_listall2['channels'] == expect

def channel_user_create_0(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + 'auth/register', json={
        'email': 'z5555555@gmail.com',
        'password': '1234567',
        'name_first': 'admin',
        'name_last': 'admin',
    })
    user = resp.json()
    return user['token'], user['u_id']

def channel_user_create_1(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + 'auth/register', json={
        'email': 'z3333333@gmail.com',
        'password': '1234567',
        'name_first': 'guest1',
        'name_last': 'guest1',
    })
    user = resp.json()
    return user['token'], user['u_id']

def channel_user_create_2(url):
    '''
    return token and u_id
    '''
    resp = requests.post(url + 'auth/register', json={
        'email': 'z4444444@gmail.com',
        'password': '1234567',
        'name_first': 'guest2',
        'name_last': 'guest2',
    })
    user = resp.json()
    return user['token'], user['u_id']

def test_channel_invite_and_details_and_messages(url):
    '''
    test to show channel details
    '''
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    guest1_tk, guest1_id = channel_user_create_1(url)
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    # invite another user to channel
    requests.post(url + "channel/invite", json={
        'token': admin_tk,
        'channel_id': 1,
        'u_id': guest1_id,
    })
    # let him access channel_details
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['name'] == test_channels['name']
    owner_members = [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ]
    assert channel_detail_resp['owner_members'] == owner_members
    all_members = [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                },
                {
                    'u_id': 2,
                    'name_first': 'guest1',
                    'name_last': 'guest1',
                    'profile_img_url': '',
                }
            ]
    assert channel_detail_resp['all_members'] == all_members

    resp_m = requests.get(url + "channel/messages", params={
        'token': guest1_tk,
        'channel_id': 1,
        'start': 0
    })
    resp_message = resp_m.json()
    assert resp_message == {
        'messages': [], 
        'start': 0, 
        'end': 50,
    }

def test_channel_details_exception(url):
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    guest1_tk = channel_user_create_1(url)[0]
    # create a private channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': False,
    }
    requests.post(url + "channels/create", json=test_channels)
    # user attempts to get channel details
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['code'] == 400 # 400 is the return value of AccessError

def test_channel_leave_and_join(url):
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    guest1_tk = channel_user_create_1(url)[0]
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    # should fail
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['code'] == 400 # 400 is the return value of AccessError
    # should success
    requests.post(url + "channel/join", json = {
        'token': guest1_tk,
        'channel_id': 1,
    })
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['name'] == test_channels['name']
    all_members = [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                },
                {
                    'u_id': 2,
                    'name_first': 'guest1',
                    'name_last': 'guest1',
                    'profile_img_url': '',
                }
            ]
    assert channel_detail_resp['all_members'] == all_members
    # should fail
    requests.post(url + "channel/leave", json = {
        'token': guest1_tk,
        'channel_id': 1,
    })
    requests.post(url + "channel/leave", json=test_channels)
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['code'] == 400 # 400 is the return value of AccessError

def test_channel_add_and_remove_owner(url):
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    guest1_tk, guest1_id = channel_user_create_1(url)
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    # invite another user to channel and add to owner
    requests.post(url + "channel/invite", json={
        'token': admin_tk,
        'channel_id': 1,
        'u_id': guest1_id,
    })
    requests.post(url + "channel/addowner", json={
        'token': admin_tk,
        'channel_id': 1,
        'u_id': guest1_id,
    })
    # let him access channel_details
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['name'] == test_channels['name']
    owner_members = [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                },
                {
                    'u_id': 2,
                    'name_first': 'guest1',
                    'name_last': 'guest1',
                    'profile_img_url': '',
                }
            ]
    assert channel_detail_resp['owner_members'] == owner_members
    # remove owner_ship
    requests.post(url + "channel/removeowner", json={
        'token': admin_tk,
        'channel_id': 1,
        'u_id': guest1_id,
    })
    # let him access channel_details
    resp = requests.get(url + "channel/details", params={
        'token': guest1_tk,
        'channel_id': 1,
    })
    channel_detail_resp = resp.json()
    assert channel_detail_resp['name'] == test_channels['name']
    owner_members = [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                },
            ]
    assert channel_detail_resp['owner_members'] == owner_members

def test_message_send(url):
    """
    test the meessage_send function via server
    """
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    ch_id_resp = requests.post(url + "channels/create", json=test_channels)
    ch_id = ch_id_resp.json()

    resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0   
    })
    channel_msgs_resp = resp.json()
    assert channel_msgs_resp == {
        'messages': [], 
        'start': 0, 
        'end': 50,
    }
    
    test_message = {
        'token': admin_tk,
        'channel_id': ch_id['channel_id'],
        'message': 'Hello'
    }
    resp = requests.post(url + "message/send", json=test_message)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 1
    
    resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0, 
    })
    channel_msgs_resp = resp.json()
    assert channel_msgs_resp['messages'][0]['message_id'] == 1
    assert channel_msgs_resp['messages'][0]['u_id'] == 1
    assert channel_msgs_resp['messages'][0]['message'] == 'Hello'

def test_message_remove(url):
    """
    test the meessage_remove function via server
    """
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)

    test_message_1 = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'Hello'
    }
    resp = requests.post(url + "message/send", json=test_message_1)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 1

    test_message_2 = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'Hello Again'
    }
    resp = requests.post(url + "message/send", json=test_message_2)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 2

    test_remove_msg_1 = {
        'token': admin_tk,
        'message_id': 1      
    }
    resp = requests.delete(url + "message/remove", json=test_remove_msg_1)
    message_remove_resp = resp.json()
    assert message_remove_resp == {}

    test_channel_msgs_1 = {
        'token': admin_tk,
        'channel_id': 1,
        'start': 0,
    }
    resp = requests.get(url + "channel/messages", params=test_channel_msgs_1)
    channel_msgs_resp = resp.json()
    assert channel_msgs_resp['messages'][0]['message_id'] == 2
    assert channel_msgs_resp['messages'][0]['u_id'] == 1
    assert channel_msgs_resp['messages'][0]['message'] == 'Hello Again'

    test_remove_msg_2 = {
        'token': admin_tk,
        'message_id': 2
    }
    resp = requests.delete(url + "message/remove", json=test_remove_msg_2)
    message_remove_resp = resp.json()
    assert message_remove_resp == {}

    resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0, 
    })
    channel_msgs_resp = resp.json()
    assert channel_msgs_resp['messages'] == []
    
def test_message_edit(url):
    """
    test the meessage_edit function via server
    """
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True
    }
    requests.post(url + "channels/create", json=test_channels)

    test_message_1 = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'Hello'
    }
    resp = requests.post(url + "message/send", json=test_message_1)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 1

    test_message_2 = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'Hello Again'
    }
    resp = requests.post(url + "message/send", json=test_message_2)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 2

    test_edit_msg_1 = {
        'token': admin_tk,
        'message_id': 1,
        'message': 'No Hello'        
    }
    resp = requests.put(url + "message/edit", json=test_edit_msg_1)
    message_edit_resp = resp.json()
    assert message_edit_resp == {}

    test_channel_msgs_1 = {
        'token': admin_tk,
        'channel_id': 1,
        'start': 0,
    }
    resp = requests.get(url + "channel/messages", params=test_channel_msgs_1)
    channel_msgs_resp = resp.json()
    assert channel_msgs_resp['messages'][0]['message_id'] == 2
    assert channel_msgs_resp['messages'][0]['u_id'] == 1
    assert channel_msgs_resp['messages'][0]['message'] == 'Hello Again'

    test_edit_msg_2 = {
        'token': admin_tk,
        'message_id': 2,
        'message': 'No Hello Again'           
    }
    resp = requests.put(url + "message/edit", json=test_edit_msg_2)
    message_edit_resp = resp.json()
    assert message_edit_resp == {}

    test_channel_msgs_2 = {
        'token': admin_tk,
        'channel_id': 1,
        'start': 0,
    }
    resp = requests.get(url + "channel/messages", params=test_channel_msgs_2)
    channel_msgs_resp = resp.json()
    assert channel_msgs_resp['messages'][1]['message_id'] == 1
    assert channel_msgs_resp['messages'][1]['u_id'] == 1
    assert channel_msgs_resp['messages'][1]['message'] == 'No Hello'

def test_other_search(url):
    """
    test the search function via server
    """
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]
    guest1_tk, guest1_id = channel_user_create_1(url)

    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True
    }
    requests.post(url + "channels/create", json=test_channels)
    
    test_channels = {
        'token': admin_tk,
        'name': 'channel_2',
        'is_public': True
    }
    requests.post(url + "channels/create", json=test_channels)

    requests.post(url + "channel/invite", json={
        'token': admin_tk,
        'channel_id': 1,
        'u_id': guest1_id,
    })

    requests.post(url + "channel/invite", json={
        'token': admin_tk,
        'channel_id': 2,
        'u_id': guest1_id,
    })

    test_admin_message_1 = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'Hello'
    }
    resp = requests.post(url + "message/send", json=test_admin_message_1)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 1

    test_guest_message_1 = {
        'token': guest1_tk,
        'channel_id': 1,
        'message': 'A Hello'
    }
    resp = requests.post(url + "message/send", json=test_guest_message_1)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 2

    test_message_2 = {
        'token': admin_tk,
        'channel_id': 2,
        'message': 'AA Hello'
    }
    resp = requests.post(url + "message/send", json=test_message_2)
    message_send_resp = resp.json()
    assert message_send_resp['message_id'] == 3

    test_search = {
        'token': admin_tk,
        'query_str': 'A'
    }
    resp = requests.get(url + "search", params=test_search)
    search_resp = resp.json()
    assert len(search_resp['messages']) == 2
    search_result = [messages['message'] for messages in search_resp['messages']]
    assert search_result == ['A Hello', 'AA Hello']

    test_search = {
        'token': admin_tk,
        'query_str': 'a'
    }
    resp = requests.get(url + "search", params=test_search)
    search_resp = resp.json()
    assert len(search_resp['messages']) == 0
    search_result = [messages['message'] for messages in search_resp['messages']]
    assert search_result == []

def test_user_profile(url):
    """
    test the user_profile via server
    """
    test_clear(url)
    admin_tk, admin_id = channel_user_create_0(url)

    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'z5555555@gmail.com'
    assert profile_resp['user']['name_first'] == 'admin'
    assert profile_resp['user']['name_last'] == 'admin'

def test_user_profile_setname(url):
    """
    test the user_profile_setname via server
    """
    test_clear(url)
    admin_tk, admin_id = channel_user_create_0(url)

    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'z5555555@gmail.com'
    assert profile_resp['user']['name_first'] == 'admin'
    assert profile_resp['user']['name_last'] == 'admin'

    test_profile_setname = {
        'token': admin_tk,
        'name_first': 'new_first',
        'name_last': 'new_last'
    }
    requests.put(url + "user/profile/setname", json=test_profile_setname)
    
    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'z5555555@gmail.com'
    assert profile_resp['user']['name_first'] == 'new_first'
    assert profile_resp['user']['name_last'] == 'new_last'

def test_user_profile_setemail(url):
    """
    test the user_profile_setemail via server
    """
    test_clear(url)
    admin_tk, admin_id = channel_user_create_0(url)

    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'z5555555@gmail.com'
    assert profile_resp['user']['name_first'] == 'admin'
    assert profile_resp['user']['name_last'] == 'admin'

    test_profile_setemail = {
        'token': admin_tk,
        'email': 'fake@gmail.com'
    }
    requests.put(url + "user/profile/setemail", json=test_profile_setemail)
    
    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'fake@gmail.com'
    assert profile_resp['user']['name_first'] == 'admin'
    assert profile_resp['user']['name_last'] == 'admin'

def test_user_profile_sethandle(url):
    """
    test the user_profile_sethandle via server
    """
    test_clear(url)
    admin_tk, admin_id = channel_user_create_0(url)

    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'z5555555@gmail.com'
    assert profile_resp['user']['name_first'] == 'admin'
    assert profile_resp['user']['name_last'] == 'admin'

    test_profile_sethandle = {
        'token': admin_tk,
        'handle_str': 'fake_handle'
    }
    requests.put(url + "user/profile/sethandle", json=test_profile_sethandle)
    
    test_profile = {
        'token': admin_tk,
        'u_id': admin_id
    }
    resp = requests.get(url + "user/profile", params=test_profile)
    profile_resp = resp.json()
    assert profile_resp['user']['u_id'] == admin_id
    assert profile_resp['user']['email'] == 'z5555555@gmail.com'
    assert profile_resp['user']['name_first'] == 'admin'
    assert profile_resp['user']['name_last'] == 'admin'
    assert profile_resp['user']['handle_str'] == 'fake_handle'

def test_user_permission_change_and_clear(url):
    """
    test user_permission_change and clear via server
    """
    test_clear(url)
    resp = requests.post(url + 'auth/register', json={
        'email': 'test_permission@gmail.com',
        'password': '123123',
        'name_first': 'Bruce',
        'name_last': 'Wayne',
    })
    user = resp.json()

    token = user['token']
    u_id = user['u_id']
    permission_id = 123 #other.PERM_ID_FLOCKR_ADMIN
    
    resp = requests.post(url + 'admin/userpermission/change', json={
        'token': token,
        'u_id': u_id,
        'permission_id': permission_id,
    })
    resp = resp.json()
    assert resp == {}

    resp = requests.post(url + 'admin/userpermission/change', json={
        'token': token,
        'u_id': u_id,
        'permission_id': permission_id,
    })
    resp = resp.json()
    assert resp == {}
  
    resp = requests.post(url + 'admin/userpermission/change', json={
        'token': token,
        'u_id': u_id + 1,
        'permission_id': permission_id,
    })
    resp = resp.json()
    assert resp['code'] == 400

def test_message_sendlater(url):
    '''
    test message_sendlater function
    '''
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]

    test_channel = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True
    }
    requests.post(url + 'channels/create', json=test_channel)
    
    test_sendlater = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hhhh',
        'time_sent': int(time.time()) + 3
    }

    sendlater_resp = requests.post(url + 'message/sendlater', json=test_sendlater)
    msg_id = sendlater_resp.json()
    assert msg_id['message_id'] == 1

    test_sendlater2 = {
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hhhh again',
        'time_sent': int(time.time()) + 2
    }

    sendlater_resp2 = requests.post(url + 'message/sendlater', json=test_sendlater2)
    msg_id2 = sendlater_resp2.json()
    assert msg_id2['message_id'] == 2

def test_message_react(url):
    '''
    test message_react
    '''
    test_clear(url)
    admin_tk, admin_id = channel_user_create_0(url)
    guest_tk, guest_id = channel_user_create_1(url)

    requests.post(url + 'channels/create', json={
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True
    })

    # msg1
    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'yeah'
    })
    # msg2
    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'how are u'
    })

    # admin react to msg1
    resp1 = requests.post(url + 'message/react', json={
        'token': admin_tk,
        'message_id': 1,
        'react_id': 1
    })

    react_resp1 = resp1.json()
    assert react_resp1 == {}

    msg_resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg_resp = msg_resp.json()
    # test msg1 -- react -- admin view
    assert msg_resp['messages'][1]['message_id'] == 1
    assert msg_resp['messages'][1]['reacts'][0]['react_id'] == 1
    assert msg_resp['messages'][1]['reacts'][0]['u_ids'] == [admin_id]
    assert msg_resp['messages'][1]['reacts'][0]['is_this_user_reacted'] == True

    # test msg2 -- no react -- admin view
    assert msg_resp['messages'][0]['message_id'] == 2
    assert msg_resp['messages'][0]['reacts'] == []

    # invite guest into channel1
    requests.post(url + 'channel/invite', json={
        'token':admin_tk,
        'channel_id': 1,
        'u_id': guest_id
    })

    # guest react to msg1
    requests.post(url + 'message/react', json={
        'token': guest_tk,
        'message_id': 1,
        'react_id': 1
    })
    
    msg_resp2 = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg_resp2 = msg_resp2.json()
    # msg1 -- admin view
    assert msg_resp2['messages'][1]['message_id'] == 1
    assert msg_resp2['messages'][1]['reacts'][0]['react_id'] == 1
    assert msg_resp2['messages'][1]['reacts'][0]['u_ids'] == [admin_id, guest_id]
    assert msg_resp2['messages'][1]['reacts'][0]['is_this_user_reacted'] == True

    # admin react to msg2
    requests.post(url + 'message/react', json={
        'token': admin_tk,
        'message_id': 2,
        'react_id': 1
    })
    msg_resp3 = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg_resp3 = msg_resp3.json()
    # msg2 -- admin view
    assert msg_resp3['messages'][0]['message_id'] == 2
    assert msg_resp3['messages'][0]['reacts'][0]['react_id'] == 1
    assert msg_resp3['messages'][0]['reacts'][0]['u_ids'] == [admin_id]
    assert msg_resp3['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

    # msg2--guest view-- test [is_this_user_reacted]
    msg_resp4 = requests.get(url + "channel/messages", params={
        'token': guest_tk,
        'channel_id': 1,
        'start': 0
    })
    msg_resp4 = msg_resp4.json()
    assert msg_resp4['messages'][0]['message_id'] == 2
    assert msg_resp4['messages'][0]['reacts'][0]['react_id'] == 1
    assert msg_resp4['messages'][0]['reacts'][0]['u_ids'] == [admin_id]
    assert msg_resp4['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

def test_message_unreact(url):
    '''
    test message_unreact
    '''
    test_clear(url)
    admin_tk, admin_id = channel_user_create_0(url)
    guest_tk, guest_id = channel_user_create_1(url)

    requests.post(url + 'channels/create', json={
        'token': admin_tk,
        'name': 'ch1',
        'is_public': True
    })
    # msg
    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hello'
    })

    requests.post(url + "message/react", json={
        'token': admin_tk,
        'message_id': 1,
        'react_id': 1
    })

    unreact_resp = requests.post(url + "message/unreact", json={
        'token': admin_tk,
        'message_id': 1,
        'react_id': 1
    })
    unreact_resp = unreact_resp.json()
    assert unreact_resp == {}

    msg_resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg = msg_resp.json()
    assert msg['messages'][0]['message_id'] == 1
    assert msg['messages'][0]['reacts'][0]['react_id'] == 1
    assert msg['messages'][0]['reacts'][0]['u_ids'] == []
    assert msg['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
    # two users react and one user unreacts later
    requests.post(url + 'channel/invite', json={
        'token': admin_tk,
        'channel_id': 1,
        'u_id': guest_id
    })

    requests.post(url + "message/react", json={
        'token': admin_tk,
        'message_id': 1,
        'react_id': 1
    })

    requests.post(url + "message/react", json={
        'token': guest_tk,
        'message_id': 1,
        'react_id': 1
    })

    requests.post(url + "message/unreact", json={
        'token': guest_tk,
        'message_id': 1,
        'react_id': 1
    })
    msg_resp2 = requests.get(url + "channel/messages", params={
        'token': guest_tk,
        'channel_id': 1,
        'start': 0
    })
    msg2 = msg_resp2.json()
    assert msg2['messages'][0]['message_id'] == 1
    assert msg2['messages'][0]['reacts'][0]['react_id'] == 1
    assert msg2['messages'][0]['reacts'][0]['u_ids'] == [admin_id]
    assert msg2['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

def test_message_pin(url):
    '''
    test message_pin
    '''
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]

    requests.post(url + 'channels/create', json={
        'token': admin_tk,
        'name': 'ch1',
        'is_public': True
    })
    # msg
    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hello'
    })
    pin_resp = requests.post(url + 'message/pin', json={
        'token': admin_tk,
        'message_id': 1,
    })
    pin = pin_resp.json()
    assert pin == {}

    msg_resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg = msg_resp.json()
    assert msg['messages'][0]['message_id'] == 1
    assert msg['messages'][0]['is_pinned'] == True

    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hello'
    })
    requests.post(url + 'message/pin', json={
        'token': admin_tk,
        'message_id': 2,
    })
    msg_resp2 = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg2 = msg_resp2.json()
    assert msg2['messages'][0]['message_id'] == 2
    assert msg2['messages'][0]['is_pinned'] == True

def test_message_unpin(url):
    '''
    test message_unpin
    '''
    test_clear(url)
    admin_tk = channel_user_create_0(url)[0]

    requests.post(url + 'channels/create', json={
        'token': admin_tk,
        'name': 'ch1',
        'is_public': True
    })
    # msg
    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hello'
    })
    requests.post(url + 'message/pin', json={
        'token': admin_tk,
        'message_id': 1,
    })

    unpin_resp = requests.post(url + 'message/unpin', json={
        'token': admin_tk,
        'message_id': 1,
    })
    unpin = unpin_resp.json()
    assert unpin == {}

    msg_resp = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg = msg_resp.json()
    assert msg['messages'][0]['message_id'] == 1
    assert msg['messages'][0]['is_pinned'] == False

    requests.post(url + 'message/send', json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'hello'
    })
    requests.post(url + 'message/pin', json={
        'token': admin_tk,
        'message_id': 2,
    })

    requests.post(url + 'message/unpin', json={
        'token': admin_tk,
        'message_id': 2,
    })

    msg_resp2 = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    msg2 = msg_resp2.json()
    assert msg2['messages'][0]['message_id'] == 2
    assert msg2['messages'][0]['is_pinned'] == False

def test_standup_start_and_active(url):
    test_clear(url)
    # admin_tk, admin_id = channel_user_create_0(url)
    # guest1_tk, guest1_id = channel_user_create_1(url)
    admin_tk = channel_user_create_0(url)[0]
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    test_length = 3
    test_standups_start = {
        'token': admin_tk,
        'channel_id': 1,
        'length': test_length,
    }
    requests.post(url + "/standup/start", json=test_standups_start)
    # provide redundency for system time cost
    test_standups_active = {
        'token': admin_tk,
        'channel_id': 1,
    }
    resp = requests.get(url + "/standup/active", \
                params=test_standups_active).json()
    assert resp['is_active'] == True
    sleep(test_length + 1)
    resp = requests.get(url + "/standup/active", \
                params=test_standups_active).json()
    assert resp['is_active'] == False
    pass

def test_standup_start_and_active_error(url):
    test_clear(url)
    # admin_tk, admin_id = channel_user_create_0(url)
    admin_tk = channel_user_create_0(url)[0]
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    # wrong channel_id
    test_length = 3
    test_standups_start = {
        'token': admin_tk,
        'channel_id': 111,
        'length': test_length,
    }
    resp = requests.post(url + "/standup/start", \
                json=test_standups_start).json()
    assert resp['code'] == 400
    test_standups_start = {
        'token': admin_tk,
        'channel_id': 1,
        'length': test_length,
    }
    requests.post(url + "/standup/start", json=test_standups_start)
    test_standups_active = {
        'token': admin_tk,
        'channel_id': 111,
    }
    resp = requests.get(url + "/standup/active", \
                params=test_standups_active).json()
    assert resp['code'] == 400
    # post standups again
    resp = requests.post(url + "/standup/start", \
                json=test_standups_start).json()
    assert resp['code'] == 400
    sleep(test_length + 1)
    pass

def test_standup_send(url):
    test_clear(url)
    # admin_tk, admin_id = channel_user_create_0(url)
    # guest1_tk, guest1_id = channel_user_create_1(url)
    admin_tk = channel_user_create_0(url)[0]
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    test_length = 3
    test_standups_start = {
        'token': admin_tk,
        'channel_id': 1,
        'length': test_length,
    }
    requests.post(url + "/standup/start", json=test_standups_start)
    requests.post(url + "/standup/send", json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'line 1',
    })
    requests.post(url + "/standup/send", json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'line 2',
    })
    sleep(test_length + 1)
    # retrieve from channel/message
    resp_m = requests.get(url + "channel/messages", params={
        'token': admin_tk,
        'channel_id': 1,
        'start': 0
    })
    resp_message = resp_m.json()
    assert resp_message['messages'][0]['message'] == \
                'adminadmin1: line 1\nadminadmin1: line 2'
    pass

def test_standup_send_err(url):
    test_clear(url)
    # admin_tk, admin_id = channel_user_create_0(url)
    admin_tk = channel_user_create_0(url)[0]
    guest1_tk = channel_user_create_1(url)[0]
    # create a channel
    test_channels = {
        'token': admin_tk,
        'name': 'channel_1',
        'is_public': True,
    }
    requests.post(url + "channels/create", json=test_channels)
    test_length = 3
    test_standups_start = {
        'token': admin_tk,
        'channel_id': 1,
        'length': test_length,
    }
    requests.post(url + "/standup/start", json=test_standups_start)
    
    resp = requests.post(url + "/standup/send", json={
        'token': guest1_tk,
        'channel_id': 1,
        'message': 'line 1',
    }).json()
    assert resp['code'] == 400

    resp = requests.post(url + "/standup/send", json={
        'token': admin_tk,
        'channel_id': 111,
        'message': 'line 1',
    }).json()
    assert resp['code'] == 400

    resp = requests.post(url + "/standup/send", json={
        'token': admin_tk,
        'channel_id': 1,
        'message': 'i' * 1001,
    }).json()
    assert resp['code'] == 400
    # provide redundency for system time cost
    sleep(test_length + 1)
    pass