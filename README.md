# Dseagull

快速构建 RESTful API

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

