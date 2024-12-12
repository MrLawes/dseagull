# Dseagull

快速构建 RESTful API

---

# serializers.Field

支持 required=True 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')

原本提示:这个字段是必填项。

现提示:姓名:这个字段是必填项。

