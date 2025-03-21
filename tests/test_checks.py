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
        self.assertEqual(4, len(errors))
        self.assertIn('请配置 jwt 的加密秘钥 JWT_KEY', errors[0])
        self.assertIn('请配置 jwt 的过期时间(单位秒) JWT_EXP', errors[1])
        self.assertIn('请为 LOGGING 添加配置 django.request', errors[2])
        self.assertIn('请配置 DJANGO_REQUEST_ERROR_WEBHOOK', errors[3])

    @override_settings(DJANGO_REQUEST_ERROR_WEBHOOK="test", LOGGING={'version': 1, "handlers": {}, 'loggers': {'django.request': {"handlers": []}}})
    def test_django_request_error_webhook(self):
        config = apps.get_app_config('dseagull')
        config.ready()
        errors = jwt_check(app_configs=None)
        errors = [error.msg for error in errors]
        self.assertEqual(0, len(errors), errors)
        self.assertIn("django.request", settings.LOGGING['loggers'])
