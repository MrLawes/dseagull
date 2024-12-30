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

        # 默认 OpenAPI 规范文档类为 rest_framework.schemas.coreapi.AutoSchema
        if 'DEFAULT_SCHEMA_CLASS' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'rest_framework.schemas.coreapi.AutoSchema'

        # 默认每页 10 条数据
        if 'PAGE_SIZE' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['PAGE_SIZE'] = 10
