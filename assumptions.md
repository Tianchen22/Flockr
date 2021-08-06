Project Assumptions
==================

Features:
==================
Global input format:
------------------
    1. UTF-8 input only

User profile:
------------------
    1. set default profile_img_url as ''

Multi-user handling:
------------------
    1. support multiple user login, and stay online:
       * managed by monitering if 'token' stays in 'token_db' or not
       * probably adding a timer to 'token' valid-period
    2. a random token is generated each time the function is called (upon login not re-login)
    3. upon re-login, while 'token' alive (didn't logoff), 'token' is not refreshed
    4. upon logoff, token will be poped from 'token_db'
    5. token generated is assumed to be stored somewhere at client
    6. user has no read nor write access to his/her token

Data storage:
------------------
    1. user and channel data is assume to be stored at server
    2. currently, data is stored in certain global variables
    3. in future, data will be stored as stationary files
    4. while storing stationary files, a temporary backup file shall be saved daily
    5. while storing stationary files, write-access shall be action-exclusive (one at a time)

Privileges:
------------------
    flokr_owner level:
    1. free entry for all channels
    2. auto set to 'channel_owner' upon join
    3. has privileges of all levels below

    channel_owner level (In owner's channel):
    1. can promote 'channel_member' to 'channel_owner'
    2. can unset 'channel_owner' to 'channel_member'
    3. has privileges of all levels below

    channel_member level:
    1. free entry to 'public' channels
