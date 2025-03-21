from django.apps import apps
from django.conf import settings
from django.test import TestCase, override_settings

from dseagull.checks import jwt_check


class TestChecks(TestCase):

    @override_settings(JWT_KEY=None, JWT_EXP=None)
    def test_pagination_settings(self):
        self.assertIsNone(settings.JWT_KEY)
        self.assertIsNone(settings.JWT_EXP)

        errors = jwt_check(app_configs=None)
        errors = [error.msg for error in errors]
        self.assertEqual(3, len(errors))
        self.assertIn('请配置 jwt 的加密秘钥 JWT_KEY', errors[0])
        self.assertIn('请配置 jwt 的过期时间(单位秒) JWT_EXP', errors[1])
        self.assertIn('请配置 DJANGO_REQUEST_ERROR_WEBHOOK', errors[2])

    @override_settings(DJANGO_REQUEST_ERROR_WEBHOOK="test")
    def test_django_request_error_webhook(self):
        config = apps.get_app_config('dseagull')
        config.ready()
        errors = jwt_check(app_configs=None)
        errors = [error.msg for error in errors]
        self.assertEqual(0, len(errors))
        self.assertIn("django.request", settings.LOGGING['loggers'])
