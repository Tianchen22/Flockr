'''
validate_email.py
'''
# This package is based on the work of Noel Bush <noel@platformer.org>
# https://github.com/noelbush/py_email_validation
#
# RFC 2822 - style email validation for Python
# (c) 2011 Noel Bush <noel@aitools.org>
# This code is made available to you under the GNU LGPL v3.

import re

WSP = r'[\s]'
CRLF = r'(?:\r\n)'
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'
QUOTED_PAIR = r'(?:\\.)'
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + r'+)'
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'
CCONTENT = r'(?:' + CTEXT + r'|' + \
           QUOTED_PAIR + r')'
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                r'?' + QCONTENT + r')*' + FWS + \
                r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                 r'(?:' + FWS + r'?' + DCONTENT + \
                 r')*' + FWS + r'?\]' + CFWS + r'?'
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN

VALID_ADDRESS_REGEXP = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def validate_email(email):
    """ check if the email is valid"""
    try:
        assert re.match(VALID_ADDRESS_REGEXP, email) is not None
    except AssertionError:
        return False
    return True
