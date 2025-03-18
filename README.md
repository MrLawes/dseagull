# Dseagull

快速构建 RESTful API

---

# INSTALLED_APPS

添加 dseagull 到 INSTALLED_APPS 中, 注意必须要放在 rest_framework 前面

```
INSTALLED_APPS = [
    ...
    'dseagull',
    'rest_framework',
]
```

---

# MIDDLEWARE

添加 dseagull.logger.LoggerMiddleware 到 MIDDLEWARE 中, 用于收集日志的字段

```
MIDDLEWARE = [
    'dseagull.logger.LoggerMiddleware',
    ...
]
```

---

添加 dseagull.middleware.BaseMiddleware 到 MIDDLEWARE 中, 用于请求的基本输出

```
MIDDLEWARE = [
    'dseagull.middleware.BaseMiddleware',
    ...
]
```

---

# REST_FRAMEWORK

不需要配置 REST_FRAMEWORK, 默认配置如下:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'dseagull.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
}
```

---

# models.BaseModel

提供基础模型, 添加了 created, updated

    from django.db import models
    
    
    class BaseModel(models.Model):
        class Meta:
            abstract = True
    
        created = models.DateTimeField(
            auto_now_add=True, verbose_name='创建时间', db_index=True,
        )
        updated = models.DateTimeField(
            auto_now=True, verbose_name='更新时间', db_index=True,
        )

---

# serializers.Field

支持 required=True 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')
    ExampleSerializer(data={}).is_valid()

原本提示:这个字段是必填项。

现提示:姓名:这个字段是必填项。

---

支持 required=True, null=False 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')
    ExampleSerializer(data={'name': None}).is_valid()

原本提示:This field may not be null.
现提示:姓名:不能为空。

---

支持 required=True, null=False 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')
    ExampleSerializer(data={'name': ''}).is_valid()

原本提示:This field may not be blank.
现提示:姓名:不能为空白。

---

# Filters

支持时间区间的查询

    from dseagull.filters import BaseFilterSet
    class PersonFilter(BaseFilterSet):
        last_name = filters.CharFilter()
        created = filters.CharFilter(method='filter_datetime', )
    
        class Meta:
            model = Person
            fields = ('id',)

在查询时, 参数输入 /?created=1738771200,1738771201 即可过滤出对应的数据

---

# Commands

## startmodel

    python manage.py startmodel -n Apple

执行上面的命令, 可以自动创建和修改标准化的 model, serializer, viewset, routers

---

# JWT

简化对称加密型的 JWT 编码和解码的过程, 需要配置 JWT_KEY 和 JWT_EXP,

    from dseagull.djwt import JWTHS256
    token = JWTHS256().encode({'username': 'admin'})
    payload = JWTHS256().decode(token)

---