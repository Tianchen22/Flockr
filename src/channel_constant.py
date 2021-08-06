"""
 This is then constants used for channel function tests
"""
SECRET_PASSWORD = "1n9e8ycaie7q2bt1327i"
N = 10000
MAX_CHAR = 20

# Template constant
MSG_TEMPLATE = {
    'message_id': None, # int
    'u_id': None, # int
    'message': None, # str
    'time_created': None, # Unix Timestamp
}

# Template constant
MEMBERS_TEMPLATE = {
    'u_id': None, # int
    'name_first': None, # str
    'name_last': None, # str
}

# Template constant
MSG_TOKEN_TEMPLATE = {
    'messages': [], # list of MSG_TEMPLATE object
    'start': None, # int
    'end': None, # int
}

# Template constant
CHANNEL_TOKEN_TEMPLATE = {
    'name': None, # str
    'channel_id': None, # int
    'is_public': False, # boolean ---24-sep-2020 added (Haoran Lyu)
    'owner_members': [], # list of MEMBERS_TEMPLATE
    'all_members': [], # list of MEMBERS_TEMPLATE
    'message_history': None, # MSG_TOKEN_TEMPLATE object
}

# channel_db test data
CHANNEL_COMBINED_DB_0 = {
        '12':{
            'name': "Empty channel",
            'is_public': True,
            'channel_id': 12,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
        '123':{
            'name': "Hayden_channel",
            'is_public': True,
            'channel_id': 123,
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
            'message_history':{
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789,
                        'reacts': [],
                        'is_pinned': False
                    }
                ],
                'start': 0,
                'end': 50,
            }
        }
    }

# channel_db test data
CHANNEL_COMBINED_DB_1 = {
        '12':{
            'name': "Empty channel",
            'is_public': True,
            'channel_id': 12,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
        '123':{
            'name': "Hayden_channel",
            'is_public': True,
            'channel_id': 123,
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
            'message_history':{
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789,
                    }
                ],
                'start': 0,
                'end': 50,
            }
        }
    }

# channel_db test data
EXPECTED_CHANNEL_COMBINED_CHANNEL_1 = {
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
    }

# channel_combined_message test data
EXPECTED_CHANNEL_COMBINED_MESSAGES = {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
                'reacts': [],
                'is_pinned': False
            },
        ],
        'start': 0,
        'end': -1,
    }

# channel_combined_message test data
EXPECTED_CHANNEL_COMBINED_EMPTY_DETAIL = {
        'name': "Empty channel",
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
    }

# channel_combined_message test data
EXPECTED_CHANNEL_COMBINED_CHANNEL_2 = {
        'name': "Hayden_channel",
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': '',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': '',
            },
            {
                'u_id': 2,
                'name_first': 'guest1',
                'name_last': 'guest1',
                'profile_img_url': '',
            }
        ],
    }

# channel_combined_message test data
EXPECTED_CHANNEL_COMBINED_CHANNEL_3 = {
        'name': "Hayden_channel",
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': '',
            },
            {
                'u_id': 2,
                'name_first': 'guest1',
                'name_last': 'guest1',
                'profile_img_url': '',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': '',
            },
            {
                'u_id': 2,
                'name_first': 'guest1',
                'name_last': 'guest1',
                'profile_img_url': '',
            }
        ],
    }

# channel_combined_message test data
EXPECTED_CHANNEL_COMBINED_CHANNEL_4 = {
        'name': "Hayden_channel",
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': '',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': '',
            },
            {
                'u_id': 2,
                'name_first': 'guest1',
                'name_last': 'guest1',
                'profile_img_url': '',
            }
        ],
    }

# channel_db test data
CHANNEL_EXCEPTIONS_DB_0 = {
        '12':{
            'name': "Empty channel",
            'is_public': True,
            'channel_id': 12,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
        '123':{
            'name': "Hayden_channel",
            'is_public': True,
            'channel_id': 123,
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
            'message_history':{
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789,
                    }
                ],
                'start': 0,
                'end': 50,
            }
        },
        '1234':{
            'name': "Private channel",
            'is_public': False,
            'channel_id': 1234,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
    }

# channel_db test data
CHANNEL_EXCEPTIONS_DB_1 = {
        '12':{
            'name': "Empty channel",
            'is_public': True,
            'channel_id': 12,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
        '123':{
            'name': "Hayden_channel",
            'is_public': True,
            'channel_id': 123,
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
            'message_history':{
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789,
                    }
                ],
                'start': 0,
                'end': 50,
            }
        },
        '1234':{
            'name': "Private channel",
            'is_public': False,
            'channel_id': 1234,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
    }

# channel_db test data
CHANNEL_EXCEPTIONS_DB_2 = {
        '12':{
            'name': "Empty channel",
            'is_public': True,
            'channel_id': 12,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
        '123':{
            'name': "Hayden_channel",
            'is_public': True,
            'channel_id': 123,
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
            'message_history':{
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789,
                    }
                ],
                'start': 0,
                'end': 50,
            }
        },
        '1234':{
            'name': "Private channel",
            'is_public': False,
            'channel_id': 1234,
            'owner_members': [
            ],
            'all_members': [
            ],
            'message_history':[]
        },
    }

# channel_flockr_owner test data
CHANNEL_FLOCKR_OWNER_DB = {
    '1':{
        'name': "Hayden_Private_channel",
        'is_public': False,
        'channel_id': 123,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '123':{
        'name': "Hayden_Public_channel",
        'is_public': True,
        'channel_id': 123,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
}

# channel_flockr_owner test data
CHANNEL_FLOCKR_OWNER_DB_2 = {
    '234':{
        'name': "Hayden_Private_channel",
        'is_public': False,
        'channel_id': 123,
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
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '123':{
        'name': "Hayden_Public_channel",
        'is_public': True,
        'channel_id': 123,
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
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
}

# channel_user_react test data
MESSAGE_TEST_USER_REACTED = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426089,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [],
                        }
                    ],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
                        }
                    ],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1,2],
                        }
                    ],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [2],
                        }
                    ],
                    'is_pinned': False
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1,2],
                        }
                    ],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# channel_user_react test data
EXPECT_MESSAGE_TEST_USER_REACTED_1 = {
    'messages': [
        {
            'message_id': 1,
            'u_id': 1,
            'message': 'Hello',
            'time_created': 1582426089,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False,
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 2,
            'u_id': 1,
            'message': 'Hello world',
            'time_created': 1582426189,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [1],
                    'is_this_user_reacted': True
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 3,
            'u_id': 1,
            'message': 'Hhh',
            'time_created': 1582426289,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [1,2],
                    'is_this_user_reacted': True
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 4,
            'u_id': 1,
            'message': 'How are u',
            'time_created': 1582426389,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [2],
                    'is_this_user_reacted': False
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 5,
            'u_id': 1,
            'message': 'great',
            'time_created': 1582426489,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [1,2],
                    'is_this_user_reacted': True
                }
            ],
            'is_pinned': False
        }
    ],
    'start': 0,
    'end': -1,
}

# channel_user_react test data
EXPECT_MESSAGE_TEST_USER_REACTED_2 = {
    'messages': [
        {
            'message_id': 1,
            'u_id': 1,
            'message': 'Hello',
            'time_created': 1582426089,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False,
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 2,
            'u_id': 1,
            'message': 'Hello world',
            'time_created': 1582426189,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [1],
                    'is_this_user_reacted': False
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 3,
            'u_id': 1,
            'message': 'Hhh',
            'time_created': 1582426289,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [1,2],
                    'is_this_user_reacted': True
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 4,
            'u_id': 1,
            'message': 'How are u',
            'time_created': 1582426389,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [2],
                    'is_this_user_reacted': True
                }
            ],
            'is_pinned': False
        },
        {
            'message_id': 5,
            'u_id': 1,
            'message': 'great',
            'time_created': 1582426489,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [1,2],
                    'is_this_user_reacted': True
                }
            ],
            'is_pinned': False
        }
    ],
    'start': 0,
    'end': -1,
}
