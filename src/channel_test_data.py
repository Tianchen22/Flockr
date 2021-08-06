"""
This file is used as the helper functions for channel tests.
The main idea is to automatically generate a complex channel detailed token.
"""

from copy import deepcopy

import string
import random
import time
import auth
import channel_constant


def id_generator(n_id=1):
    """Return specificed number(n_id, 1 by default) of ids
       Set id minimum to 1000 to prevent occationally collision
       with real test user, whose ids in [1, 2, 3]
    """
    return random.sample(range(1000, channel_constant.N), n_id)

def string_generator(n_char=channel_constant.MAX_CHAR):
    """Return specificed number(n_char, channel_constant.MAX_CHAR by default) len of strings"""
    return ''.join(random.sample(string.ascii_letters,
                                 random.randint(1, n_char)))

def make_msg(members, n_msg=1):
    """Return specificed number(n_char, channel_constant.MAX_CHAR by default) len of strings"""
    msgs = [deepcopy(channel_constant.MSG_TEMPLATE) for _ in range(n_msg)]
    uid_lst = [member['u_id'] for member in members]
    for i in range(n_msg):
        msgs[i]['message_id'] = i
        msgs[i]['u_id'] = random.choice(uid_lst)
        msgs[i]['message'] = string_generator(10)
        msgs[i]['time_created'] = int(time.time())
        msgs[i]['reacts'] = []
        msgs[i]['is_pinned'] = False

    return msgs

def make_member(n_member=1):
    """Return specificed number(n_member, 1 by default) of member infos"""
    members = [deepcopy(channel_constant.MEMBERS_TEMPLATE) for _ in range(n_member)]
    id_lst = id_generator(n_member)
    for i in range(n_member):
        members[i]['u_id'] = id_lst[i]
        members[i]['name_first'] = string_generator()
        members[i]['name_last'] = string_generator()
    return members

def make_admin():
    """Return an admin info for testing"""
    admin_member = [deepcopy(channel_constant.MEMBERS_TEMPLATE)]
    admin_member[0]['u_id'] = 1
    admin_member[0]['name_first'] = 'admin'
    admin_member[0]['name_last'] = 'admin'
    return admin_member

def make_msg_token(member_lst):
    """Return a member list based on member_lst"""
    msg_token = deepcopy(channel_constant.MSG_TOKEN_TEMPLATE)
    n_msg = 100
    start_idx = 0
    msg_token['messages'].extend(make_msg(member_lst, n_msg))
    msg_token['start'] = start_idx
    msg_token['end'] = n_msg
    return msg_token

def register_member(member_lst):
    """Return a member list based on member_lst"""
    for member in member_lst:
        auth.auth_register(str(member['u_id'])+'@gmail.com',
                           '1234567', member['name_first'], member['name_last'])

def make_channel_token(channel_infos):
    """Return a channel list based on channel_infos"""
    channel_tokens = [deepcopy(channel_constant.CHANNEL_TOKEN_TEMPLATE)
                      for n, _ in enumerate(channel_infos)]
    member_lst = make_member(10)
    register_member(member_lst)
    for i, _ in enumerate(channel_tokens):
        channel_tokens[i]['name'] = channel_infos[i][1]
        channel_tokens[i]['channel_id'] = channel_infos[i][0]
        channel_tokens[i]['is_public'] = True
        channel_tokens[i]['all_members'].extend(member_lst + make_admin())
        channel_tokens[i]['owner_members'].extend(random.sample(member_lst, 3) + make_admin())
        channel_tokens[i]['message_history'] = make_msg_token(member_lst)
    return channel_tokens

def make_token(token_n=1):
    """Return an auto-generated channel detail token"""
    channel_ids = id_generator(token_n)

    channel_infos = [(channel_id, string_generator()) for channel_id in channel_ids]
    channel_tokens = make_channel_token(channel_infos)

    return {str(channel_id): channel_token for channel_id,
            channel_token in zip(channel_ids, channel_tokens)}, channel_tokens
