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

EMAIL_DB['email'] = u_id

user_data['token'] = {
    'email':'validemail@email.com',
    'password': "123456",
    'u_id': 10086,
    'name_first': "admin",
    'name_last': "admin",
    'channels':[],
    'HANDLE':
}

'''
import hashlib
import jwt
import time
from random import randint
import email_robot
from error import InputError, AccessError
from validate_email import validate_email

# local database holders
U_ID_NUM = [0]
TOKEN_LOGGED = [""] # should be unknown to user
USER_DB = dict() # member of flockr
EMAIL_DB = dict()
TOKEN_DB = dict()
HANDLE = dict()
RESET_DB = dict()
# used in white box test for sending emaili to reset password
SECRET_TOKEN = '72!wTEcge?8LdM!k'
SECRET_EMAIL = 'p9d4jw0vwnn7tz5o@admin.com'
SECRET_CODE = 'ZJa@bc2D5/sj@b7L'

def get_handle(name):
    """
    get_handle(name) 
    return HANDLE through the given name
    """
    name = name.lower()[:20]
    HANDLE[name] = HANDLE.get(name, 0) + 1
    return name + str(HANDLE[name])

def token_generate(email):
    """ 
    token_generate(email)
    gengerate a new token through the given token
    """
    new_token = str(jwt.encode({'email': email, 'time': time.time()}, SECRET_TOKEN, algorithm='HS256'))
    return new_token if new_token not in TOKEN_DB.keys() else token_generate(email)

def u_id_to_token(u_id):
    """ 
    u_id_to_token(u_id)
    return the token through the given u_id
    """
    for key in TOKEN_DB:
        if u_id == TOKEN_DB[key]['u_id']:
            return key
    raise AccessError()

def token_to_u_id(token):
    """ 
    token_to_u_id(token)
    return the u_id through the given token
    """
    if str(token) in TOKEN_DB.keys():
        return TOKEN_DB[token]['u_id']
    raise AccessError()

# Main Part
def auth_login(email, password):
    """ 
    auth_login(email, password)
    check and login in the account 
    """
    # error raising for InputError
    if not validate_email(email):
        raise InputError('Not Valid Email')
    if email not in EMAIL_DB:
        raise InputError('Email not Registered')
    if USER_DB[str(EMAIL_DB[email])]['password'] != hashlib.sha256(password.encode()).hexdigest():
        raise InputError('Wrong Password')
    # if login again without log out
    for key in TOKEN_DB:
        if EMAIL_DB[email] == TOKEN_DB[key]['u_id']:
            TOKEN_LOGGED[0] = key
            return {
                'u_id': EMAIL_DB[email],
                'token': TOKEN_LOGGED[0],
            }
    # if login first time or after logout
    TOKEN_LOGGED[0] = token_generate(email)
    TOKEN_DB[TOKEN_LOGGED[0]] = dict()
    TOKEN_DB[TOKEN_LOGGED[0]]['log'] = True
    TOKEN_DB[TOKEN_LOGGED[0]]['u_id'] = EMAIL_DB[email]
    return {
        'u_id': EMAIL_DB[email],
        'token': TOKEN_LOGGED[0],
    }

def auth_logout(token):
    """ 
    auth_logout(token)
    logout the current user(token) 
    """
    # disqualify related token
    if token in TOKEN_DB:
        TOKEN_DB.pop(token)
        return {
            'is_success': True,
        }
    return {
        'is_success': False,
    }

def auth_register(email, password, name_first, name_last):
    """ 
    auth_register(email, password, name_first, name_last)
    register the account in the database 
    """
    if not validate_email(email):
        raise InputError('Not Valid Email')
    if email not in EMAIL_DB:
        if len(password) < 6:
            raise InputError('Password is too short')
        if not name_first or not name_last or len(name_first) > 50 or len(name_last) > 50:
            raise InputError('Name is too short or too long')
        # if no error, create new user
        U_ID_NUM[0] += 1
        EMAIL_DB[email] = U_ID_NUM[0]
        USER_DB[str(U_ID_NUM[0])] = {
            'email': email,
            'admin': False,
            'u_id': U_ID_NUM[0],
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'name_first': name_first,
            'name_last': name_last,
            'channels': [],
            'HANDLE': get_handle(name_first + name_last),
            'img_url': '',
            'log': False,
        }
        # make first user as admin of server
        if len(USER_DB) == 1:
            USER_DB[str(U_ID_NUM[0])]['admin'] = True
        # after register user into database, then auto login user
        return auth_login(email, password)
    raise InputError('Email has been used')

def add_flockr_owner(admin_token, u_id):
    """
    add_flockr_owner(admin_token, u_id)
    Promote the member of flockr to an admin(owner) of flockr
    """
    # testing if user has permission
    if admin_token not in TOKEN_DB.keys() or not TOKEN_DB[admin_token]['log']:
        raise AccessError("Invalid token")
    admin_id = token_to_u_id(admin_token)
    # test if target user is valid
    if str(u_id) not in USER_DB.keys():
        raise InputError("Invalid user ID: ", u_id)
    if not USER_DB[str(admin_id)]['admin']: # if not admin
        raise AccessError("Not admin")
    # Make new admin
    USER_DB[str(u_id)]['admin'] = True # :)

def is_admin(token):
    '''
    is_admin(token)
    true <- is admin
    false <- not admin
    '''
    admin_id = token_to_u_id(token)
    if USER_DB[str(admin_id)]['admin']: # if admin
        return True
    return False

def reset_code_generate(email):
    """ 
    reset_code_generate(email)
    gengerate a new token through the given token
    """
    reset_code = str(randint(100000,999999))
    if (email == SECRET_EMAIL):
        return SECRET_CODE
    return reset_code

def auth_passwordreset_request(email):
    '''
    send passwordret request
    '''
    if email not in EMAIL_DB:
        raise InputError('Email not Registered')
    # create code and send email
    RESET_DB[email] = reset_code_generate(email)
    u_id = str(EMAIL_DB[email])
    email_robot.email_send(USER_DB[u_id]['name_last'], email, RESET_DB[email])

def change_password(reset_code, new_password):
    '''
    use for loop to find the reset_code and reset password
    '''
    for email, code in RESET_DB.items():
        if code == reset_code:
            # find the correct code
            u_id = str(EMAIL_DB[email])
            USER_DB[u_id]['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            break

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password provided
    '''
    # invalid rest code and invalid password
    if reset_code not in RESET_DB.values():
        raise InputError('not a valid reset code')
    if len(new_password) < 6:
        raise InputError('not a valid password: password is too short')
    # find the reset_code by loop and reset password in user_db
    change_password(reset_code, new_password)
