from django.apps import AppConfig

from django.conf import settings


class DseagullConfig(AppConfig):
    name = 'dseagull'
    verbose_name = "dseagull"

    def ready(self):
        from .checks import jwt_check  # noqa
        self.default_rest_framework()

    @classmethod
    def default_rest_framework(cls):

        if not hasattr(settings, 'REST_FRAMEWORK'):
            settings.REST_FRAMEWORK = {}

        # 指定默认分页类
        if 'DEFAULT_PAGINATION_CLASS' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'dseagull.pagination.PageNumberPagination'

        # 默认每页 10 条数据
        if 'PAGE_SIZE' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['PAGE_SIZE'] = 10

        # 默认 OpenAPI 规范文档类为 rest_framework.schemas.coreapi.AutoSchema
        if 'DEFAULT_SCHEMA_CLASS' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'rest_framework.schemas.coreapi.AutoSchema'

        # 默认指定 DEFAULT_FILTER_BACKENDS
        if 'DEFAULT_FILTER_BACKENDS' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] = [
                'django_filters.rest_framework.DjangoFilterBackend',
                'rest_framework.filters.SearchFilter',
                'rest_framework.filters.OrderingFilter',
            ]

        # 默认指定 TEST_REQUEST_DEFAULT_FORMAT
        if 'TEST_REQUEST_DEFAULT_FORMAT' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'

        # 默认指定 DEFAULT_RENDERER_CLASSES
        if 'DEFAULT_RENDERER_CLASSES' not in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)
