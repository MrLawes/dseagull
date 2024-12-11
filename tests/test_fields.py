from rest_framework.serializers import Serializer

from dseagull.fields import BooleanField
from dseagull.fields import CharField
from dseagull.fields import DateField
from dseagull.fields import DateTimeField
from dseagull.fields import DictField
from dseagull.fields import DurationField
from dseagull.fields import EmailField
from dseagull.fields import Field
from dseagull.fields import FloatField
from dseagull.fields import HStoreField
from dseagull.fields import IPAddressField
from dseagull.fields import ImageField
from dseagull.fields import IntegerField
from dseagull.fields import JSONField
from dseagull.fields import ListField
from dseagull.fields import SlugField
from dseagull.fields import TimeField
from dseagull.fields import URLField
from dseagull.fields import UUIDField


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
