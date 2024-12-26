from django.conf import settings
from django.test import TestCase

from dseagull.checks import jwt_check


class TestChecks(TestCase):

    def test_pagination_settings(self):
        self.assertFalse(hasattr(settings, 'JWT_KEY'))
        self.assertFalse(hasattr(settings, 'JWT_EXP'))

        errors = jwt_check(app_configs=None)
        errors_msg = [error.msg for error in errors]
        self.assertEqual(errors_msg, ['请配置 jwt 的加密秘钥 JWT_KEY = YOURS', '请配置 jwt 的过期时间(单位秒) JWT_EXP = YOURS'])
