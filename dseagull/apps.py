from django.apps import AppConfig


class DseagullConfig(AppConfig):
    name = 'dseagull'
    verbose_name = "dseagull"

    def ready(self):
        from django.conf import settings
        from .checks import jwt_check  # noqa

        # 指定默认分页类
        if 'DEFAULT_PAGINATION_CLASS' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'dseagull.pagination.PageNumberPagination'
