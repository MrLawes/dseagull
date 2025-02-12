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
    return errors
