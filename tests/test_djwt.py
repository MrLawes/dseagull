import jwt
from django.conf import settings
from django.test import TestCase, override_settings

from dseagull.djwt import JWTHS256, JWTUser


class TestDjwt(TestCase):

    def test_encode_decode(self):
        """ 正常编码解码 """
        settings.JWT_EXP = 60
        jwt_obj = JWTHS256()
        token = jwt_obj.encode({'username': 'admin'})
        payload = jwt_obj.decode(token)
        payload.pop('exp')
        self.assertEqual(payload, {'username': 'admin'})

    def test_encode_decode_invalid_signature(self):
        """ 密钥错误测试 """
        jwt_obj = JWTHS256()
        token = jwt_obj.encode({'username': 'admin'})

        with self.assertRaises(jwt.InvalidSignatureError):
            jwt_obj.key = 'd6b15627964c43b290d803e0f4851d13'
            jwt_obj.decode(token)

    @override_settings(JWT_EXP=-61)
    def test_encode_decode_expired_signature(self):
        """ 过期测试 """
        jwt_obj = JWTHS256()
        token = jwt_obj.encode({'username': 'admin'})
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt_obj.decode(token)

    def test_jwtuser(self):
        JWTUser(user_id=1, user_type='user_type', )
