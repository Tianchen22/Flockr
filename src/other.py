import auth
import user
import channel
import channels
import message
import standups
import error

PERM_ID_FLOCKR_ADMIN = 123
PERM_ID_FLOCKR_MEMBER = 1

def clear():
    '''
    clear()
    empty all database and buffer 
    '''
    # auth part
    auth.U_ID_NUM[0] = 0
    auth.USER_DB.clear()
    auth.EMAIL_DB.clear()
    auth.TOKEN_DB.clear()
    auth.HANDLE.clear()
    # channel part
    channel.CHANNEL_DB.clear()
    # channels part
    channels.CHANNEL_NUM = [0]
    # standup buffer clear
    standups.STANDUP_BUFFER = {}
    # reset message id generator count
    message.reset_id_gen()

def users_all(token):
    '''
    users_all(token)
    returns a list of all users
    '''
    channel.valid_token(token)
    u_ids = [x['u_id'] for x in auth.USER_DB.values()]
    users_info = [user.user_profile(token, u_id)['user'] for u_id in u_ids]
    return { 
        'users': users_info
    }

def admin_userpermission_change(token, u_id, permission_id):
    '''
    admin_userpermission_change(token, u_id, permission_id)
    change a user's permission level by a admin
    '''
    channel.valid_token(token)
    admin_id = auth.token_to_u_id(token)
    if not auth.USER_DB[str(admin_id)]['admin']: # if not admin
        raise error.AccessError("Not admin")
    if str(u_id) not in auth.USER_DB.keys():
        raise error.InputError("Invalid user ID: ", u_id)
    if permission_id == PERM_ID_FLOCKR_ADMIN:
        auth.add_flockr_owner(token, u_id)
    elif permission_id == PERM_ID_FLOCKR_MEMBER:
        # Make new admin
        auth.USER_DB[str(u_id)]['admin'] = False # :(
    else:
        raise error.InputError("Invalid permission_id")
    return {}

def search(token, query_str):
    '''
    search(token, query_str)
    search message by matching substring with query_str
    '''
    rt_dict = {'messages': []}
    for ch_id in channel.CHANNEL_DB.keys():
        if channel.is_member(ch_id, auth.token_to_u_id(token)):
            for mess in channel.CHANNEL_DB[ch_id]['message_history']['messages']:
                if query_str in mess['message']:
                    rt_dict['messages'].append(mess)
    return rt_dict
