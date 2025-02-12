from django.conf import settings
from django.test import TestCase

from dseagull.checks import jwt_check


class TestChecks(TestCase):

    def test_pagination_settings(self):
        self.assertFalse(hasattr(settings, 'JWT_KEY'))
        self.assertFalse(hasattr(settings, 'JWT_EXP'))

        errors = jwt_check(app_configs=None)
        error_msg = ';'.join([error.msg for error in errors])
        self.assertIn('请配置 jwt 的加密秘钥 JWT_KEY', error_msg)
        self.assertIn('请配置 jwt 的过期时间(单位秒) JWT_EXP', error_msg)
