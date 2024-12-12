from rest_framework.serializers import Serializer

from dseagull.serializers import BooleanField
from dseagull.serializers import CharField
from dseagull.serializers import DateField
from dseagull.serializers import DateTimeField
from dseagull.serializers import DictField
from dseagull.serializers import DurationField
from dseagull.serializers import EmailField
from dseagull.serializers import Field
from dseagull.serializers import FloatField
from dseagull.serializers import HStoreField
from dseagull.serializers import IPAddressField
from dseagull.serializers import ImageField
from dseagull.serializers import IntegerField
from dseagull.serializers import JSONField
from dseagull.serializers import ListField
from dseagull.serializers import SlugField
from dseagull.serializers import TimeField
from dseagull.serializers import URLField
from dseagull.serializers import UUIDField


class TestFieldErrorMessages:
    def test_required(self):
        for field in (BooleanField, CharField, DateField, DateTimeField, DictField, DurationField,
                      EmailField, Field, FloatField, HStoreField, IPAddressField, ImageField,
                      IntegerField, JSONField, ListField, SlugField,
                      TimeField, URLField, UUIDField):
            class ExampleSerializer(Serializer):
                name = field(help_text='姓名')

            serializer = ExampleSerializer(data={})
            serializer.is_valid()
            assert serializer.errors['name'][0] == '姓名:这个字段是必填项。', field

        class ExampleSerializer(Serializer):
            name = field(help_text='姓名', error_messages={'required': '请填入姓名。'})

        serializer = ExampleSerializer(data={})
        serializer.is_valid()
        assert serializer.errors['name'][0] == '请填入姓名。'

    def test_null(self):

        class ExampleSerializer(Serializer):
            name = CharField(help_text='姓名')

        serializer = ExampleSerializer(data={'name': None})
        serializer.is_valid()
        assert serializer.errors['name'][0] == '姓名:不能为空。'

    def test_blank(self):

        class ExampleSerializer(Serializer):
            name = CharField(help_text='姓名')

        serializer = ExampleSerializer(data={'name': ''})
        serializer.is_valid()
        assert serializer.errors['name'][0] == '姓名:不能为空白。'
