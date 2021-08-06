import auth
import channel
import error
from validate_email import validate_email
'''
USER_DB['u_id'] = {
    'email':'validemail@email.com',
    'admin': True or False,
    'password': "123456",
    'u_id': 10086,
    'name_first': "admin",
    'name_last': "admin",
    'channels':[],
    'HANDLE'
}
'''
def user_profile(token, u_id):
    '''
    user_profile(token, u_id)
    extract user data from database
    '''
    channel.valid_token(token)
    if str(u_id) not in auth.USER_DB.keys():
        raise error.InputError("Invalid u_id")
    # take out user info from database
    user_info = auth.USER_DB[str(u_id)]
    return {
        'user': {
        	'u_id': user_info['u_id'],
        	'email': user_info['email'],
        	'name_first': user_info['name_first'],
        	'name_last': user_info['name_last'],
        	'handle_str': user_info['HANDLE'],
            'profile_img_url': user_info['img_url'],
        },
    }

def channel_reload_user_names(u_id):
    '''
    channel_reload_user_names(u_id)
    upon username update, names in channel page will also be updated
    '''
    for ch_id in channel.CHANNEL_DB.keys():
        for owner in channel.CHANNEL_DB[ch_id]['owner_members']:
            # change user's name in channels (owner_member) by individual u_id
            if owner['u_id'] == u_id:
                user_info = auth.USER_DB[str(u_id)]
                owner['name_first'] = user_info['name_first']
                owner['name_last'] = user_info['name_last']
                owner['profile_img_url'] = user_info['img_url']
        for all_mem in channel.CHANNEL_DB[ch_id]['all_members']:
            # change user's name in channels (all_memebr) by individual u_id
            if all_mem['u_id'] == u_id:
                user_info = auth.USER_DB[str(u_id)]
                all_mem['name_first'] = user_info['name_first']
                all_mem['name_last'] = user_info['name_last']
                all_mem['profile_img_url'] = user_info['img_url']
    return {}

def user_profile_setname(token, name_first, name_last):
    '''
    user_profile_setname(token, name_first, name_last)
    change names of a user
    '''
    channel.valid_token(token)
    # check if new names are valid
    if len(name_first) < 1 or len(name_first) > 50:
        raise error.InputError("name_first too long or too short")
    if len(name_last) < 1 or len(name_last) > 50:
        raise error.InputError("name_last too long or too short")
    # update user database
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    user_info['name_first'] = name_first
    user_info['name_last'] = name_last
    # to update names in channel.CHANNEL_DB
    channel_reload_user_names(auth.token_to_u_id(token))
    return {
    }

def user_profile_setemail(token, email):
    '''
    user_profile_setemail(token, email)
    change the email of a user
    '''
    channel.valid_token(token)
    if not validate_email(email):
        raise error.InputError('Not Valid Email')
    if email in auth.EMAIL_DB:
        raise error.InputError('Email already taken by others')
    # update user email in database
    # also pop old email from email_password(hashed) database
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    auth.EMAIL_DB.pop(user_info['email'], None)
    user_info['email'] = email
    auth.EMAIL_DB[user_info['email']] = auth.token_to_u_id(token)
    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    user_profile_sethandle(token, handle_str)
    change user handle
    '''
    channel.valid_token(token)
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise error.InputError('handle_str too long or too short')
    # make sure new handles are unique
    for user in auth.USER_DB.keys():
        if auth.USER_DB[user]['HANDLE'] == handle_str:
            raise error.InputError('handle_str already taken by others')
    # update handle in database
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    user_info['HANDLE'] = handle_str
    return {
    }

def user_profile_uploadphoto(token, img_url):
    '''
    user_profile_uploadphoto(token, img_url)
    upload photo for user profile
    '''
    channel.valid_token(token)
    user_info = auth.USER_DB[str(auth.token_to_u_id(token))]
    user_info['img_url'] = img_url
    channel_reload_user_names(auth.token_to_u_id(token))