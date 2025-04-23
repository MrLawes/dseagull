import json
import uuid

from django.conf import settings
from django.core.checks import Tags, register, Critical


@register(Tags.compatibility)
def jwt_check(app_configs, **kwargs) -> list:  # noqa
    errors = []
    if not hasattr(settings, 'JWT_KEY') or not settings.JWT_KEY:
        errors.append(
            Critical(
                f"请配置 jwt 的加密秘钥 JWT_KEY, 比如: JWT_KEY = '{uuid.uuid4().hex}{uuid.uuid4().hex}'"
            )
        )

    if not hasattr(settings, 'JWT_EXP') or not settings.JWT_EXP:
        errors.append(
            Critical(
                "请配置 jwt 的过期时间(单位秒) JWT_EXP, 比如: JWT_EXP = 60 * 60 * 24 * 30"
            )
        )

    logging = getattr(settings, 'LOGGING', {})
    logger = logging.get('loggers', {}).get('django.request')
    if not logger:
        conf = {
            'version': 1,
            'formatters': {
                'django.request': {
                    'format': '[%(levelname)1.1s %(asctime)s %(module)s.%(funcName)s:%(lineno)d];%(message)s'
                },
            },
            'handlers': {
                'webhook': {'level': 'ERROR', 'class': 'dseagull.dlogging.DjangoRequestErrorLOGGINGHandler'},
                'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'django.request', },
            },
            'loggers': {
                'django.request': {'handlers': ['console', 'webhook'], 'level': 'INFO', 'propagate': False, 'encoding': 'utf8'}
            }
        }
        errors.append(
            Critical(
                f"请为 LOGGING 添加配置 django.request: \n{json.dumps(conf, indent=4)}"
            )
        )

        webhook = getattr(settings, 'DJANGO_REQUEST_ERROR_WEBHOOK', None)
        if webhook is None:
            errors.append(
                Critical(
                    f"请配置 DJANGO_REQUEST_ERROR_WEBHOOK, 目前只支持钉钉机器人的 webhook, 配置文档: https://open.dingtalk.com/document/robots/custom-robot-access, 安全设置->自定义关键词填入 Seagull"
                )
            )

    return errors
