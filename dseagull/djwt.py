import time

import jwt
from django.conf import settings


class JWTHS256:
    """ 使用对称加密:HS256 """

    def __init__(self, ):
        self.key = settings.JWT_KEY  # 密钥
        self.exp = settings.JWT_EXP

    def encode(self, payload: dict) -> str:
        """ 编码 """
        payload["exp"] = time.time() + self.exp
        token = jwt.encode(
            payload=payload,
            key=self.key,
            algorithm='HS256',
            headers={'alg': 'HS256', 'typ': 'JWT', },
        )
        return token

    def decode(self, jwt_data: str) -> dict:
        """ 解码 """
        payload = jwt.decode(
            jwt_data,
            self.key,
            verify=True,
            algorithms='HS256',
            leeway=60,  # 每个服务器时间不一样, 允许误差60秒
        )
        return payload


class JWTUser:

    def __init__(self, user_id: int, user_type: str, headers: dict = {}, *args, **kwargs):  # noqa
        self.user_id = user_id
        self.user_type = user_type
        self.headers = headers
