'''encoding: utf-8'''
import unittest

from validate_email import validate_email

class AddressPatternTests(unittest.TestCase):
    ''' address test'''

    def test_ascii_regular(self):
        ''' test gmail'''
        self.assertTrue(validate_email(r'someone@gmail.com'))
        self.assertTrue(validate_email(r'some.one@gmail.com'))

        self.assertFalse(validate_email(r's-@gmail.com'))
        self.assertFalse(validate_email(r'someone+plus@gmail.com'))
        self.assertFalse(validate_email(r'someone@gmail'))
        self.assertFalse(validate_email(r'someonegmail.com'))
        self.assertFalse(validate_email(r'@gmail.com'))
        self.assertFalse(validate_email(r'someone @gmail.com'))

    def test_chinese_regular(self):
        ''' test chinese email'''
        self.assertFalse(validate_email(r'用户@互联网.中国')) # Chinese

    def test_1(self):
        ''' test qq email'''
        self.assertTrue(validate_email(r'1111111@qq.com'))

        self.assertFalse(validate_email(r'qq.com'))
        self.assertFalse(validate_email(r'com'))
        self.assertFalse(validate_email(r'1111111qq.com')) # No @
        self.assertFalse(validate_email(r'1111111@qqcom')) # No .
        self.assertFalse(validate_email(r'1111111@qq.')) # Nothing after the .
        self.assertFalse(validate_email(r'1111111@qq')) # No .com
        self.assertFalse(validate_email(r'@qq.com')) # Nothing before the @
        self.assertFalse(validate_email(r' 1111111@qq.com')) # has ' '
        self.assertFalse(validate_email(r'@qq.com')) # has ' '
        self.assertFalse(validate_email(r'1111 111@qq.com')) # has ' '

    def test_2(self):
        ''' test unsw email'''
        self.assertTrue(validate_email(r'z1111111@gmail.com'))
        self.assertTrue(validate_email(r'z_1111111@gmail.com'))

        self.assertFalse(validate_email(r'z1111111gmail.com')) # No @
        self.assertFalse(validate_email(r'z1111111@adunsweduau')) # No .
        self.assertFalse(validate_email(r'z1111111@ad.')) # Nothing after the .
        self.assertFalse(validate_email(r'z1111111@ad.unsw.')) # Nothing after the .
        self.assertFalse(validate_email(r'z1111111@ad.unsw.edu.')) # Nothing after the .

        self.assertFalse(validate_email(r'@gmail.com')) # Nothing before the @
        self.assertFalse(validate_email(r'z 1111111@gmail.com')) # has ' '

    def test_3(self):
        '''test outlook email'''
        self.assertTrue(validate_email(r'aaaaaaaaa@outlook.com'))

        self.assertFalse(validate_email(r'aaaaaaaaaoutlook.com')) # No @
        self.assertFalse(validate_email(r'aaaaaaaaa@outlookcom')) # No .
        self.assertFalse(validate_email(r'aaaaaaaaa@outlook.')) # Nothing after the .
        self.assertFalse(validate_email(r'@outlook.com')) # Nothing before the @

    def test_4(self):
        '''test yahoo email'''
        self.assertTrue(validate_email(r'aaaaaaaaa@yahoo.com'))

        self.assertFalse(validate_email(r'aaaaaaaaayahoo.com')) # No @
        self.assertFalse(validate_email(r'aaaaaaaaa@yahoocom')) # No .
        self.assertFalse(validate_email(r'aaaaaaaaa@yahoo.')) # Nothing after the .
        self.assertFalse(validate_email(r'@yahoo.com')) # Nothing before the @

    def test_5(self):
        '''test aol email'''
        self.assertTrue(validate_email(r'aaaaaaaaa@aol.com'))

        self.assertFalse(validate_email(r'aaaaaaaaaaol.com')) # No @
        self.assertFalse(validate_email(r'aaaaaaaaa@aolcom')) # No .
        self.assertFalse(validate_email(r'aaaaaaaaa@aol.')) # Nothing after the .
        self.assertFalse(validate_email(r'@aol.com')) # Nothing before the @

    def test_6(self):
        '''no number'''
        self.assertFalse(validate_email(r'#$%&?@gmail.com'))
        self.assertFalse(validate_email(r'#$%&?gmail.com')) # No @
        self.assertFalse(validate_email(r'#$%&?@gmailcom')) # No .
        self.assertFalse(validate_email(r'#$%&?@gmail.')) # Nothing after the .
        self.assertFalse(validate_email(r'@gmail.com')) # Nothing before the @
