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

# Jwt

简化对称加密型的 JWT 编码和解码的过程, 需要配置 JWT_KEY 和 JWT_EXP,

    from dseagull.djwt import JWTHS256
    token = JWTHS256().encode({'username': 'admin'})
    payload = JWTHS256().decode(token)

---