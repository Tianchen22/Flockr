"""
the tests in part one are given by the
returned results from stub code given

from auth import auth_login, auth_logout, auth_register
"""
import pytest
import auth
from error import InputError, AccessError

def valid_token(token):
    ''' return if the token is Valid'''
    return token in auth.TOKEN_DB

def test_reg0():
    """ test register case 0: Email been used """
    # register a user
    auth.auth_register('z5555555@gmail.com', '123456', 'Kap', 'Pa')
    # register a user with same email
    with pytest.raises(InputError):
        auth.auth_register('z5555555@gmail.com', '123456', 'Kap', 'Pa')
    
def test_reg1():
    """ test register case 1: Email Error """
    # Invalid email addresses test
    with pytest.raises(InputError):
        auth.auth_register('gmail.com', '123456', 'Dav', 'Ka')
    with pytest.raises(InputError):
        auth.auth_register('@gmail.com', '123456', 'Dav', 'Ka')
    with pytest.raises(InputError):
        auth.auth_register('z6666666@.au', '123456', 'Dav', 'Ka')
    with pytest.raises(InputError):
        auth.auth_register('z6666666@gmail.com.', '123456', 'Dav', 'Ka')

def test_reg2():
    """ test register case 2: Password Error """
    # registering user with invalid password
    with pytest.raises(InputError):
        auth.auth_register('z7777777@s.au', '', 'Rook', 'Smith')
    with pytest.raises(InputError):
        auth.auth_register('z7777777@s.au', '123', 'Rook', 'Smith')

def test_reg3():
    """ test register case 3: different Input Error """
    # name_first not is between 1 and 50 characters in length
    # name_last is not between 1 and 50 characters in length
    # testing registering user with invalid names
    with pytest.raises(InputError):
        auth.auth_register('z8888888@a.au', '123456', '', 'Ka')
    with pytest.raises(InputError):
        auth.auth_register('z8888888@a.au', '123456', 'Dav', '')
    with pytest.raises(InputError):
        auth.auth_register('z8888888@a.au', '123456', \
        'Davvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv', 'Ka')
    with pytest.raises(InputError):
        auth.auth_register('z8888888@a.au', '123456', \
        'Dav', 'Kaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

def test_log_0():
    """ test log case 0: basic """
    # testing successfully registering user
    info0 = auth.auth_register('z1111111@gmail.com', '123456', 'Cool', 'Ass')
    auth.auth_logout(info0['token'])

    info1 = auth.auth_login('z1111111@gmail.com', '123456')
    assert info0['u_id'] == info1['u_id']
    assert(auth.auth_logout(info1['token']) == {'is_success': True,})

def test_log_1():
    """ test log case 1: Password Error """
    # testing login with wrong password
    with pytest.raises(InputError):
        auth.auth_login('z1111111@gmail.com', '234456')

def test_log_2():
    """ test log case 0: Email Error """
    # Invalid email address
    # testing login with invalid emails
    with pytest.raises(InputError):
        auth.auth_login('gmail.com', '123456',)
    with pytest.raises(InputError):
        auth.auth_login('@gmail.com', '123456')
    with pytest.raises(InputError):
        auth.auth_login('z2222222@au', '123456')
    with pytest.raises(InputError):
        auth.auth_login('z2222222@.au', '123456')
    with pytest.raises(InputError):
        auth.auth_login('z2222222@gmail.com.', '123456')

def test_log_3():
    """ test log case 3: Invalid email """
    # testing login with non-exist email
    with pytest.raises(InputError):
        auth.auth_login('z3333333@gmail.com', '123456')

def test_log_4():
    """ test log case 4: failed logout """
    # testing invalid token to logout
    assert not auth.auth_logout('Invalid')['is_success']

def test_multiuser():
    """ test multiuser online"""
    # testing login multiple different user
    for i in range(10):
        print(1)
        email = 'newuser'+ str(i) + '@gmail.com'
        auth.auth_register(email, '123456', 'Cool', 'Ass')
        auth.auth_login(email, '123456')
        assert valid_token(auth.TOKEN_LOGGED[0])
        if i in range(5):
            auth.auth_logout(auth.TOKEN_LOGGED[0])
            assert not valid_token(auth.TOKEN_LOGGED[0])
        else: # i in range(5,10)
            assert valid_token(auth.TOKEN_LOGGED[0])

def test_token_function():
    """ test random token as the input """
    # test passed case
    email = 'newtokencheck1@gmail.com'
    info = auth.auth_register(email, '123456', 'Cool', 'Ass')
    u_id, token = info['u_id'], info['token']
    assert auth.u_id_to_token(u_id) == token
    assert auth.token_to_u_id(token) == u_id
    # test failed case
    with pytest.raises(AccessError):
        auth.u_id_to_token(-1)
    with pytest.raises(AccessError):
        auth.token_to_u_id("UselessStringLine")

def test_flockr_owner():
    """ test add flockr owner: Different Errors """
    with pytest.raises(AccessError):
        auth.add_flockr_owner("UselessStringLine", -1)
    email = 'newflockrowner@gmail.com'
    info = auth.auth_register(email, '123456', 'Cool', 'Ass')
    with pytest.raises(InputError):
        auth.add_flockr_owner(info['token'], -1)
    with pytest.raises(AccessError):
        auth.add_flockr_owner(info['token'], info['u_id'])

def test_reset_code_generate_0():
    """ test the same email generates different reset codes each time"""
    assert auth.reset_code_generate('test@test.com') != auth.reset_code_generate('test@test.com')

def test_reset_code_generate_1():
    """ test differenr emails generate different reset codes each time"""
    assert auth.reset_code_generate('test@test.com') != auth.reset_code_generate('test@server.com')

def test_reset_code_generate_2():
    """ test backdoor"""
    assert auth.reset_code_generate('p9d4jw0vwnn7tz5o@admin.com') == 'ZJa@bc2D5/sj@b7L'

def test_passwordreset_request_0():
    """ test invalid email format"""
    with pytest.raises(InputError):
        auth.auth_passwordreset_request('z5555555@ad.unsw.edu.au')

def test_passwordreset_request_1():
    """ test unregistered email"""
    with pytest.raises(InputError):
        auth.auth_passwordreset_request('nonexist@gmail.com')

def test_auth_passwordreset_reset_0():
    """ test invalid reset code """
    info = auth.auth_register('z86841193@gmail.com', '123456', 'Cool', 'Ass')
    auth.auth_logout(info['token'])
    auth.auth_passwordreset_request('z86841193@gmail.com')
    with pytest.raises(InputError):
        auth.auth_passwordreset_reset('invalid_reset_code', '123456789')

def test_auth_passwordreset_reset_1():
    """ test successful case """
    info = auth.auth_register('p9d4jw0vwnn7tz5o@admin.com', '123456', 'Cool', 'Ass')
    auth.auth_logout(info['token'])
    auth.auth_passwordreset_request('p9d4jw0vwnn7tz5o@admin.com')
    auth.auth_passwordreset_reset('ZJa@bc2D5/sj@b7L', '123123456789')
