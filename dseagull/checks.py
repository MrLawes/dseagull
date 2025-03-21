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
    logger = logging.get('loggers', {}).get('django.request')  # todo 提示配置 LOGGING 和 DJANGO_REQUEST_ERROR_WEBHOOK, 并提供一个模板
    if not logger:
        conf = {
            'version': 1,
            'handlers': {
                'webhook': {'level': 'ERROR', 'class': 'dseagull.dlogging.DjangoRequestErrorLOGGINGHandler'}
            },
            'loggers': {
                'django.request': {'handlers': ['webhook'], 'level': 'INFO', 'propagate': False, 'encoding': 'utf8'}
            }
        }
        errors.append(
            Critical(
                f"请为 LOGGING 添加配置 django.request: \n{json.dumps(conf)}"
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
