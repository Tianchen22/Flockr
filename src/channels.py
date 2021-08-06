""" channels.py """

from error import InputError, AccessError
import auth
import channel

CHANNEL_NUM = [0]

def is_valid_token(token):
    """ 
    is_valid_token(token)
    check if token is valid 
    """
    if token not in auth.TOKEN_DB.keys() or not auth.TOKEN_DB[token]['log']:
        return False
    return True

def copy_user(token):
    '''
    copy user info
    '''
    member = dict()
    member['u_id'] = auth.TOKEN_DB[token]['u_id']
    member['name_first'] = auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['name_first']
    member['name_last'] = auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['name_last']
    member['profile_img_url'] = auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['img_url']
    return member

def channels_list(token):
    """
    channels_list(token)
    channels_list includes only the channels
    the authorised user has access to (either a member or owner).
    """
    # invalid token
    if is_valid_token(token) is False:
        raise AccessError("Invalid token!")
    # put channels into the new dict
    new_channels_list = {
        'channels': [],
    }
    # copy info of user
    member = copy_user(token)
    # find channels thay the user has access to by loop
    for channel_db in channel.CHANNEL_DB:
        if member in channel.CHANNEL_DB[channel_db]['all_members']:
            new_channels_list['channels'].append(channel.CHANNEL_DB[channel_db])

    return new_channels_list

def channels_listall(token):
    """
    channels_listall(token)
    channels_listall lists all channels,
    regardless of whether the authorised user has access to them.
    """
    if is_valid_token(token) is False:
        raise AccessError("Invalid token!")
    # put channels into the new dict
    new_channels_list = {
        'channels': [],
    }
    # copy all channels info
    for channel_db in channel.CHANNEL_DB:
        if channel.CHANNEL_DB[channel_db]['is_public'] or auth.is_admin(token) or channel.is_member(channel.CHANNEL_DB[channel_db]['channel_id'], auth.token_to_u_id(token)):
            new_channels_list['channels'].append(channel.CHANNEL_DB[channel_db])

    return new_channels_list

def channels_create(token, name, is_public):
    """ 
    channels_create(token, name, is_public)
    create a new channel
    """
    if is_valid_token(token) is False:
        raise AccessError("Invalid token!")

    if len(name) <= 20:
        CHANNEL_NUM[0] += 1
        # create new channel info with template
        # auto join creator into member list and owner list
        channel.CHANNEL_DB[str(CHANNEL_NUM[0])] = {
            'name': name,
            'channel_id': CHANNEL_NUM[0],
            'is_public' : is_public,
            'owner_members': [
                {
                    'u_id': auth.TOKEN_DB[token]['u_id'],
                    'name_first': auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['name_first'],
                    'name_last': auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['name_last'],
                    'profile_img_url': auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['img_url'],
                }
            ],
            'all_members': [
                {
                    'u_id': auth.TOKEN_DB[token]['u_id'],
                    'name_first': auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['name_first'],
                    'name_last': auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['name_last'],
                    'profile_img_url': auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['img_url'],
                }
            ],
            'message_history': None,
        }
        channel.CHANNEL_DB[str(CHANNEL_NUM[0])] = channel.CHANNEL_DB[str(CHANNEL_NUM[0])]
        # put into USER_DB
        auth.USER_DB[str(auth.TOKEN_DB[token]['u_id'])]['channels']\
                .append(channel.CHANNEL_DB[str(CHANNEL_NUM[0])])
    else:
        raise InputError("The name of channel is over 20 characters!")

    return {
        'channel_id': CHANNEL_NUM[0],
    }
