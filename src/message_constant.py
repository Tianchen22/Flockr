# a channel template from channel_constant
import time

# message_id_finder test data
MESSAGE_TEST_0_ID_FINDER = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [],
            'start': 0,
            'end': 50,
        }
    }
}

# message_id_finder test data
MESSAGE_TEST_1_ID_FINDER = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
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
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 123,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 2,
                    'u_id': 2,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# initiat_message_history test data
MESSAGE_TEST_1_INIT_HISTORY = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{}
    },
    '123':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 123,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 2,
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

# message_send test data
MESSAGE_TEST_0_SEND = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [],
            'start': 0,
            'end': 50,
        }
    }
}

MESSAGE_TEST_1_SEND = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [],
            'start': 0,
            'end': 50,
        }
    }
}

# message_send test data
MESSAGE_TEST_2_SEND = {
    '2':{
        'name': "ahah",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [],
            'start': 0,
            'end': 50,
        }
    }
}

# message_remove test data
MESSAGE_TEST_0_MSG_REMOVE = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
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
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 123,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 2,
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

# message_edit test data
MESSAGE_TEST_0_MSG_EDIT = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
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
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 123,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 2,
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

# message_error test data
MESSAGE_TEST_0_ERROR = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [],
            'start': 0,
            'end': 50,
        }
    }
}

# message_error test data
MESSAGE_TEST_1_ERROR = {
    '12':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 12,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 2,
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

# message_error test data
MESSAGE_TEST_3_ERROR = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [],
            'start': 0,
            'end': 50,
        }
    }
}

# message_react test data
MESSAGE_TEST_1_REACT = {
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
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [],
                    'is_pinned': False
                },
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_react test data
MESSAGE_TEST_2_REACT = {
    '2':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [],
                    'is_pinned': False
                },
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_react test data
MESSAGE_TEST_3_REACT = {
    '3':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 3,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795822,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_react test data
EXPECT_MESSAGE_TEST_1_REACT = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
                        }
                    ],
                    'is_pinned': False
                },
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_react test data
EXPECT_MESSAGE_TEST_2_REACT = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            },
            {
                'u_id': 2,
                'name_first': 'guest1',
                'name_last': 'guest1',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1,2],
                        }
                    ],
                    'is_pinned': False
                },
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_react test data
EXPECT_MESSAGE_TEST_3_REACT = {
    '3':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 3,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
                        }
                    ],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795822,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
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

# message_unreact test data
MESSAGE_TEST_1_UNREACT = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [],
        'all_members': [],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
                        }
                    ],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795822,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
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

# message_unreact test data
MESSAGE_TEST_2_UNREACT = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [],
        'all_members': [],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
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
                    'message': 'hello',
                    'time_created': 1604795822,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [],
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

# message_unreact test data
EXPECT_MESSAGE_TEST_1_UNREACT = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
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
                    'message': 'hello',
                    'time_created': 1604795822,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [1],
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

# message_unreact test data
EXPECT_MESSAGE_TEST_2_UNREACT = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'hello',
                    'time_created': 1604795821,
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
                    'message': 'hello',
                    'time_created': 1604795822,
                    'reacts': [
                        {
                            'react_id': 1,
                            'u_ids': [],
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

# message_pin test data
MESSAGE_TEST_1_PIN = {
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
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_pin_error test data
MESSAGE_TEST_1_PIN_ERROR = {
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
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_unpin_error test data
MESSAGE_TEST_1_UNPIN_ERROR = {
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
                    'reacts': [],
                    'is_pinned': True
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_pin test data
MESSAGE_TEST_2_PIN = {
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
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': True
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_pin test data
EXPECT_MESSAGE_TEST_1_PIN = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426089,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_pin test data
EXPECT_MESSAGE_TEST_2_PIN = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426089,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
        ],
        'all_members': [
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_pin test data
EXPECT_MESSAGE_TEST_3_PIN = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426089,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': True
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}


# message_pin test data
EXPECT_MESSAGE_TEST_4_PIN = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426089,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': True
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}

# message_pin test data
EXPECT_MESSAGE_TEST_5_PIN = {
    '1':{
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 1,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426089,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426189,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 3,
                    'u_id': 1,
                    'message': 'Hhh',
                    'time_created': 1582426289,
                    'reacts': [],
                    'is_pinned': False
                },
                {
                    'message_id': 4,
                    'u_id': 1,
                    'message': 'How are u',
                    'time_created': 1582426389,
                    'reacts': [],
                    'is_pinned': True
                },
                {
                    'message_id': 5,
                    'u_id': 1,
                    'message': 'great',
                    'time_created': 1582426489,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    },
    '2': {
        'name': "Empty channel",
        'is_public': True,
        'channel_id': 2,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'admin',
                'name_last': 'admin',
                'profile_img_url': ''
            }
        ],
        'message_history':{
            'messages': [
                {
                    'message_id': 10,
                    'u_id': 1,
                    'message': 'Hello',
                    'time_created': 1582426900,
                    'reacts': [],
                    'is_pinned': False
                }
            ],
            'start': 0,
            'end': 50,
        }
    }
}
