import pytest
import error
import user
import auth
import channel
import channel_test

@channel_test.clear_history
def test_user_profile():
    '''
    test_user_profile gives desired user's info
    '''
    token = channel_test.ADMIN_TOKEN[0]
    u_id = 1
    user_info = auth.USER_DB[str(u_id)]
    admin = {
        'user': {
        	'u_id': user_info['u_id'],
        	'email': user_info['email'],
        	'name_first': user_info['name_first'],
        	'name_last': user_info['name_last'],
        	'handle_str': user_info['HANDLE'],
            'profile_img_url': user_info['img_url'],
        }
    }
    assert user.user_profile(token, u_id) == admin
    with pytest.raises(error.AccessError):
        user.user_profile("INVALID_TOKEN", 1)
    with pytest.raises(error.InputError):
        user.user_profile(token, 4)

@channel_test.clear_history
def test_user_profile_setname():
    '''
    test_user_profile_setname set user name to new name correctly
    '''
    token = channel_test.ADMIN_TOKEN[0]
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    channel.CHANNEL_DB = {
        '12':{
            'name': "Hayden_channel",
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ],
        },
        '123':{
            'name': "Hayden_channel",
            'owner_members': [
                {
                    'u_id': 2,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': 2,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ],
        }
    }
    user.user_profile_setname(token,"heyden1","heyden2")
    admin = {
        'user': {
        	'u_id': user_info['u_id'],
        	'email': user_info['email'],
        	'name_first': "heyden1",
        	'name_last': "heyden2",
        	'handle_str': user_info['HANDLE'],
            'profile_img_url': user_info['img_url'],
        }
    }
    assert user.user_profile(token, auth.token_to_u_id(token)) == admin
    with pytest.raises(error.InputError):
        user.user_profile_setname(token,"","heyden2")
    with pytest.raises(error.InputError):
        user.user_profile_setname(token,"123","")
    strr = "".join(["i" for i in range(51)])
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, strr, "111")
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, "333", strr)
    assert channel.CHANNEL_DB == {
        '12':{
            'name': "Hayden_channel",
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': "heyden1",
                    'name_last': "heyden2",
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': "heyden1",
                    'name_last': "heyden2",
                    'profile_img_url': '',
                }
            ],
        },
        '123':{
            'name': "Hayden_channel",
            'owner_members': [
                {
                    'u_id': 2,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ],
            'all_members': [
                {
                    'u_id': 2,
                    'name_first': 'admin',
                    'name_last': 'admin',
                    'profile_img_url': '',
                }
            ],
        }
    }

@channel_test.clear_history
def test_user_profile_setemail():
    '''
    test_user_profile_setemail correctly raise error or set email to new valid email
    '''
    token = channel_test.ADMIN_TOKEN[0]
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    user.user_profile_setemail(token,"valid@email.com")
    admin = {
        'user': {
        	'u_id': user_info['u_id'],
        	'email': "valid@email.com",
        	'name_first': user_info['name_first'],
        	'name_last': user_info['name_last'],
        	'handle_str': user_info['HANDLE'],
            'profile_img_url': user_info['img_url'],
        }
    }
    assert user.user_profile(token, auth.token_to_u_id(token)) == admin
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token,"invalidEmail")
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token,"z3333333@gmail.com")
    auth.auth_logout(token)
    assert auth.auth_login("valid@email.com","1234567")['u_id'] == 1

@channel_test.clear_history
def test_user_profile_sethandle():
    '''
    test_user_profile_sethandle successfully changes handle to a new unique handle
    '''
    token = channel_test.ADMIN_TOKEN[0]
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    user.user_profile_sethandle(token,"123456789")
    admin = {
        'user': {
        	'u_id': user_info['u_id'],
        	'email': user_info['email'],
        	'name_first': user_info['name_first'],
        	'name_last': user_info['name_last'],
        	'handle_str': "123456789",
            'profile_img_url': user_info['img_url'],
        }
    }
    assert user.user_profile(token, auth.token_to_u_id(token)) == admin
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token,"12")
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token,"0123456789-0123456789")
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token,"123456789")

@channel_test.clear_history
def test_user_profile_uploadphoto():
    '''
    test_user_profile_uploadphoto successfully change user 
    profile phote to uploaded picture
    '''
    token = channel_test.ADMIN_TOKEN[0]
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    user.user_profile_uploadphoto(token, "img.com/img.jpg")
    admin = {
        'user': {
        	'u_id': user_info['u_id'],
        	'email': user_info['email'],
        	'name_first': user_info['name_first'],
        	'name_last': user_info['name_last'],
        	'handle_str': user_info['HANDLE'],
            'profile_img_url': "img.com/img.jpg",
        }
    }
    assert user.user_profile(token, auth.token_to_u_id(token)) == admin
