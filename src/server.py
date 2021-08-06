# import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError, AccessError
import auth
import channel
import channels
import message as msgg
import user
import other
import urllib.request
from PIL import Image
import standups

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data,
    })
    
@APP.route("/auth/login", methods=['POST'])
def auth_login():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        result = auth.auth_login(email, password)
    except InputError:
        raise InputError()
    return dumps({
        'u_id': result['u_id'],
        'token': result['token']
    })

@APP.route("/auth/register", methods=['POST'])
def auth_register():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    try:
        result = auth.auth_register(email, password, name_first, name_last)
    except InputError:
        raise InputError()
    return dumps({
        'u_id': result['u_id'],
        'token': result['token']
    })

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    result = auth.auth_logout(token)
    return dumps({
        'is_success': result['is_success'],
    })

@APP.route("/channel/invite", methods=['POST'])
def channel_invite():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel.channel_invite(token, channel_id, u_id)
    return dumps({
    })

@APP.route("/channel/details", methods=['GET'])
def channel_details():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    try:
        result = channel.channel_details(token, channel_id)
    except AccessError:
        raise AccessError()
    return dumps({
        'name': result['name'], 
        'owner_members': result['owner_members'],
        'all_members': result['all_members'],
    })

@APP.route("/channel/messages", methods=['GET'])
def channel_messages():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    result = channel.channel_messages(token, channel_id, start)
    return dumps({
        'messages': result['messages'], 
        'end': result['end'],
        'start': result['start'] 
    })

@APP.route("/channel/leave", methods=['POST'])
def channel_leave():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()    
    token = data['token']
    channel_id = data['channel_id']
    channel.channel_leave(token, channel_id)
    return dumps({
    })

@APP.route("/channel/join", methods=['POST'])
def channel_join():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()    
    token = data['token']
    channel_id = data['channel_id']
    channel.channel_join(token, channel_id)
    return dumps({
    })

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()    
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel.channel_addowner(token, channel_id, u_id)
    return dumps({
    })

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()    
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel.channel_removeowner(token, channel_id, u_id)
    return dumps({
    })

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    result = channels.channels_list(token)
    return dumps({
        'channels': result['channels']
    })

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    result = channels.channels_listall(token) 
    return dumps({
        'channels': result['channels']
    })

@APP.route("/channels/create", methods=['POST'])
def channels_create():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    result = channels.channels_create(token, name, is_public)
    return dumps({
        'channel_id': result['channel_id'],
    })

@APP.route("/message/send", methods=['POST'])
def message_send():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    result = msgg.message_send(token, channel_id, message)
    return dumps({
        'message_id': result['message_id'],
    })

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    msgg.message_remove(token, message_id)
    return dumps({
    })

@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    msgg.message_edit(token, message_id, message)
    return dumps({
    })

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    time_sent = data['time_sent']
    result = msgg.message_sendlater(token, channel_id, message, time_sent)
    return dumps({
        'message_id': result['message_id'],
    })

@APP.route("/message/react", methods=['POST'])
def message_react():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']
    msgg.message_react(token, message_id, react_id)
    return dumps({
    })

@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']
    msgg.message_unreact(token, message_id, react_id)
    return dumps({
    })

@APP.route("/message/pin", methods=['POST'])
def message_pin():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    msgg.message_pin(token, message_id)
    return dumps({
    })

@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    msgg.message_unpin(token, message_id)
    return dumps({
    })

@APP.route("/user/profile", methods=['GET'])
def user_profile():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    result = user.user_profile(token, u_id)
    return dumps({
        'user': result['user']
    })

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    user.user_profile_setname(token, name_first, name_last)
    return dumps({
    })
    
@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    email = data['email']
    user.user_profile_setemail(token, email)
    return dumps({
    })

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    user.user_profile_sethandle(token, handle_str)
    return dumps({
    })

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_uploadphoto():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    img_url = data['img_url']

    if not img_url.endswith('.jpg'):
        raise InputError('Only support jpg image')

    img_name = str(auth.token_to_u_id(data['token'])) + '.jpg'
    path = './src/static/' + img_name
    urllib.request.urlretrieve(img_url, path)
    img = Image.open(path)
    cropped = img.crop((int(data['x_start']), int(data['y_start']), \
                        int(data['x_end']), int(data['y_end'])))
    cropped.save(path)

    img_url = request.host_url + 'static/' + img_name
    user.user_profile_uploadphoto(data['token'], img_url)
    return dumps({
    })

@APP.route("/static/<path:path>", methods=['GET'])
def send_jpg(path):
    '''
    server side function, load pic from local path
    '''
    return send_from_directory('', path)

@APP.route("/users/all", methods=['GET'])
def user_all():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    result = other.users_all(token)
    return dumps({
        'users': result['users']
    })

@APP.route("/clear", methods=['DELETE'])
def clear():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    other.clear()
    return dumps({
    })

@APP.route("/admin/userpermission/change", methods=['POST'])
def permission_change():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    try:
        other.admin_userpermission_change(token, u_id, permission_id)
    except InputError:
        raise InputError('Error test')
    return dumps({
    })

@APP.route("/standup/start", methods=['POST'])
def standup_start():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    length = data['length']
    try:
        result = standups.standup_start(token, channel_id, length)
    except InputError:
        raise InputError('InputError Error test')
    return dumps({
        'time_finish': result
    })

@APP.route("/standup/active", methods=['GET'])
def standup_active():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    try:
        result = standups.standup_active(token, channel_id)
    except InputError:
        raise InputError('InputError Error test')
    return dumps({
        'is_active': result['is_active'],
        'time_finish': result['time_finish']
    })

@APP.route("/standup/send", methods=['POST'])
def standup_send():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    try:
        standups.standup_send(token, channel_id, message)
    except AccessError:
        raise AccessError('AccessError Error test')
    except InputError:
        raise InputError('InputError Error test')
    return dumps({
    })

@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    email = data['email']
    auth.auth_passwordreset_request(email)
    return dumps({
    })

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    data = request.get_json()
    reset_code = data['reset_code']
    new_password = data['new_password']
    auth.auth_passwordreset_reset(reset_code, new_password)
    return dumps({
    })

@APP.route("/clear", methods=['DELETE'])
def other_clear():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    other.clear()
    return dumps([
        auth.U_ID_NUM[0],
        len(auth.USER_DB),
        len(auth.EMAIL_DB),
        len(auth.TOKEN_DB),
        len(auth.HANDLE),
        len(channel.CHANNEL_DB),
        msgg.USED_MESSAGE_ID,
    ])

@APP.route("/search", methods=['GET'])
def other_search():
    '''
    server side function, unbundle args for functions
    within json package and return either server error
    or function response within json package
    '''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    result = other.search(token, query_str)
    return dumps({
        'messages': result['messages']
    })

@APP.route("/get_all", methods=['GET'])
def get_all():
    '''
    server side function, a small hacking function to 
    return database from server for debugging
    '''
    return dumps(channel.CHANNEL_DB)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
