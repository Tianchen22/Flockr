'''test channels.py'''
import pytest
from error import InputError, AccessError
import channels
import auth
import channel
import channels_constant

# global variable place holders for test (token)
TOKEN_1 = [None]
TOKEN_2 = [None]
TOKEN_3 = [None]
TOKEN_4 = [None]

# global variable place holders for test (channel)
CH_1 = [None]
CH_2 = [None]
CH_3 = [None]
CH_4 = [None]
CH_5 = [None]


def registe_all(function):
    '''get some sample user from auth.py'''
    def wrapper():
        # clear history
        auth.U_ID_NUM[0] = 0
        auth.USER_DB.clear()
        auth.EMAIL_DB.clear()
        auth.TOKEN_DB.clear()
        auth.HANDLE.clear()
        channels.CHANNEL_NUM = [0]
        # create users
        auth.auth_register("z5555550@gmail.com", "1111111", 'test', 'name1')
        TOKEN_1[0] = auth.TOKEN_LOGGED[0]
        auth.auth_register("z5555554@gmail.com", "1111111", 'test', 'name2')
        TOKEN_2[0] = auth.TOKEN_LOGGED[0]
        auth.auth_register("z5555553@gmail.com", "1111111", 'test', 'name3')
        TOKEN_3[0] = auth.TOKEN_LOGGED[0]
        auth.auth_register("z5555552@gmail.com", "1111111", 'test', 'name4')
        TOKEN_4[0] = auth.TOKEN_LOGGED[0]
        return function()
    return wrapper

@registe_all
def test_channels_create_1():
    '''test channels_create
    valid token and valid name'''
    # connect channel_db
    channels.channel_db = channel.CHANNEL_DB
    channels.channel_db.clear()
    # expect channel_create results
    expect_result_1 = channels_constant.CREATE_1_EXPECT_RESULT_1
    expect_result_2 = channels_constant.CREATE_1_EXPECT_RESULT_2
    expect_result_3 = channels_constant.CREATE_1_EXPECT_RESULT_3
    expect_result_4 = channels_constant.CREATE_1_EXPECT_RESULT_4
    expect_result_5 = channels_constant.CREATE_1_EXPECT_RESULT_5
    # login and create channel
    auth.auth_login("z5555550@gmail.com", "1111111")
    CH_1[0] = channels.channels_create(TOKEN_1[0], "abc", True)
    auth.auth_login("z5555554@gmail.com", "1111111")
    CH_2[0] = channels.channels_create(TOKEN_2[0], "abc123", True)
    auth.auth_login("z5555553@gmail.com", "1111111")
    CH_3[0] = channels.channels_create(TOKEN_3[0], "abcABCdDeE", True)
    auth.auth_login("z5555552@gmail.com", "1111111")
    CH_4[0] = channels.channels_create(TOKEN_4[0], "abcaaa123!!", True)
    CH_5[0] = channels.channels_create(TOKEN_4[0], "longlonglonglonglong", False)
    # test they are the same
    assert CH_1[0] == expect_result_1
    assert CH_2[0] == expect_result_2
    assert CH_3[0] == expect_result_3
    assert CH_4[0] == expect_result_4
    # exactly 20 characters , same token and not public
    assert CH_5[0] == expect_result_5

@registe_all
def test_channels_create_2():
    '''test invalid token'''
    temp_token = auth.token_generate("z50000000@gmail.com")
    with pytest.raises(AccessError):
        channels.channels_create(temp_token, "abcaaa123!", True)

@registe_all
def test_channels_create_3():
    '''test invalid name'''
    auth.auth_login("z5555550@gmail.com", "1111111")
    with pytest.raises(InputError):
        channels.channels_create(TOKEN_1[0], "longlonglonglonglonglong", True)

@registe_all
def test_channels_list_1():
    '''test in valid token'''
    temp_token = auth.token_generate("z50000000@gmail.com")
    with pytest.raises(AccessError):
        channels.channels_list(temp_token)

@registe_all
def test_channels_list_2():
    '''if TOKEN1 just has one channel and he is the owner of channel'''
    auth.auth_login("z5555550@gmail.com", "1111111")
    assert channels.channels_list(TOKEN_1[0]) == channels_constant.LIST_2_EXPECTED_RESULT

@registe_all
def test_channels_list_3():
    '''if user owns more than one channels'''
    auth.auth_login("z5555552@gmail.com", "1111111")
    assert channels.channels_list(TOKEN_4[0]) == channels_constant.LIST_3_EXPECTED_RESULT

@registe_all
def test_channels_list_4():
    ''' test TOKEN2 if TOKEN2 is member in other channel'''
    auth.auth_login("z5555554@gmail.com", "1111111")
    channel.channel_join(TOKEN_2[0], 3)
    assert channels.channels_list(TOKEN_2[0]) == channels_constant.LIST_4_EXPECTED_RESULT

@registe_all
def test_channels_listall_1():
    ''' test invalid token'''
    temp_token = auth.token_generate("z55000000@gmail.com")
    with pytest.raises(AccessError):
        channels.channels_listall(temp_token)

@registe_all
def test_channels_listall_2():
    '''test channels_listall'''
    # test different users
    auth.auth_login("z5555550@gmail.com", "1111111")
    assert channels.channels_listall(TOKEN_1[0]) == channels_constant.LISTALL_2_EXPECT_RESULT
    auth.auth_login("z5555554@gmail.com", "1111111")
    assert channels.channels_listall(TOKEN_2[0]) == channels_constant.LISTALL_2_USER2_EXPECT_RESULT
    auth.auth_login("z5555553@gmail.com", "1111111")
    assert channels.channels_listall(TOKEN_3[0]) == channels_constant.LISTALL_2_USER3_EXPECT_RESULT
    auth.auth_login("z5555552@gmail.com", "1111111")
    assert channels.channels_listall(TOKEN_4[0]) == channels_constant.LISTALL_2_USER4_EXPECT_RESULT
