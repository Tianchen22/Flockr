'''
This file is for storing constants in channels test functions.
'''

# channels_create test data
CREATE_1_EXPECT_RESULT_1 = {
    'channel_id': 1
}

# channels_create test data
CREATE_1_EXPECT_RESULT_2 = {
    'channel_id': 2
}

# channels_create test data
CREATE_1_EXPECT_RESULT_3 = {
    'channel_id': 3
}

# channels_create test data
CREATE_1_EXPECT_RESULT_4 = {
    'channel_id': 4
}

# channels_create test data
CREATE_1_EXPECT_RESULT_5 = {
    'channel_id': 5
}

# channels_list test data
LIST_2_EXPECTED_RESULT = {
        'channels': [
            {
                'name': 'abc',
                'channel_id': 1,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            }

        ]
    }

# channels_list test data
LIST_4_EXPECTED_RESULT = {
        'channels': [
            {
                'name': 'abc123',
                'channel_id': 2,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abcABCdDeE',
                'channel_id': 3,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    },
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            }
        ]
    }

# channels_list test data
LIST_3_EXPECTED_RESULT = {
        'channels': [
            {
                'name': 'abcaaa123!!',
                'channel_id': 4,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'longlonglonglonglong',
                'channel_id': 5,
                'is_public': False,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            }

        ]
    }

# channels_listall test data
LISTALL_2_EXPECT_RESULT = {
        'channels': [
            {
                'name': 'abc',
                'channel_id': 1,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abc123',
                'channel_id': 2,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abcABCdDeE',
                'channel_id': 3,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    },
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    },
                ],
                'message_history': None,
            },
            {
                'name': 'abcaaa123!!',
                'channel_id': 4,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'longlonglonglonglong',
                'channel_id': 5,
                'is_public': False,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            }

        ]
    }
# channels_listall test data
LISTALL_2_USER2_EXPECT_RESULT = {
        'channels': [
            {
                'name': 'abc',
                'channel_id': 1,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abc123',
                'channel_id': 2,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abcABCdDeE',
                'channel_id': 3,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    },
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    },
                ],
                'message_history': None,
            },
            {
                'name': 'abcaaa123!!',
                'channel_id': 4,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
        ]
    }

# channels_listall test data
LISTALL_2_USER3_EXPECT_RESULT = {
        'channels': [
            {
                'name': 'abc',
                'channel_id': 1,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abc123',
                'channel_id': 2,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abcABCdDeE',
                'channel_id': 3,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    },
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    },
                ],
                'message_history': None,
            },
            {
                'name': 'abcaaa123!!',
                'channel_id': 4,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
        ]
    }

# channels_listall test data
LISTALL_2_USER4_EXPECT_RESULT = {
        'channels': [
            {
                'name': 'abc',
                'channel_id': 1,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 1,
                        'name_first': 'test',
                        'name_last': 'name1',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abc123',
                'channel_id': 2,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'abcABCdDeE',
                'channel_id': 3,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 3,
                        'name_first': 'test',
                        'name_last': 'name3',
                        'profile_img_url': '',
                    },
                    {
                        'u_id': 2,
                        'name_first': 'test',
                        'name_last': 'name2',
                        'profile_img_url': '',
                    },
                ],
                'message_history': None,
            },
            {
                'name': 'abcaaa123!!',
                'channel_id': 4,
                'is_public': True,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            },
            {
                'name': 'longlonglonglonglong',
                'channel_id': 5,
                'is_public': False,
                'owner_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 4,
                        'name_first': 'test',
                        'name_last': 'name4',
                        'profile_img_url': '',
                    }
                ],
                'message_history': None,
            }

        ]
    }
