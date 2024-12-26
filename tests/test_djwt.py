import jwt
from django.conf import settings
from django.test import TestCase

from dseagull.djwt import JWTHS256


class TestDjwt(TestCase):

    def test_encode_decode(self):
        # 正常编码解码
        settings.JWT_KEY = '86594cb2102a4c43a3a4a5e0b2ff1ac8'
        settings.JWT_EXP = 60
        jwt_obj = JWTHS256()
        token = jwt_obj.encode({'username': 'admin'})
        payload = jwt_obj.decode(token)
        payload.pop('exp')
        self.assertEqual(payload, {'username': 'admin'})

        # 密钥错误测试
        settings.JWT_KEY = 'd6b15627964c43b290d803e0f4851d13'
        jwt_obj = JWTHS256()
        with self.assertRaises(jwt.InvalidSignatureError):
            jwt_obj.decode(token)

        # 过期测试
        settings.JWT_KEY = '86594cb2102a4c43a3a4a5e0b2ff1ac8'
        settings.JWT_EXP = -61
        jwt_obj = JWTHS256()
        token = jwt_obj.encode({'username': 'admin'})
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt_obj.decode(token)
