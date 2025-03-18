import pytest
from django.test import RequestFactory, TestCase
from rest_framework import (
    serializers
)
from rest_framework.viewsets import ModelViewSet

from dseagull.logger import thread_local
from dseagull.middleware import BaseMiddleware
from tests.models.modeltest import Person


class PersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()

    class Meta:
        model = Person
        fields = ('id', 'first_name',)


class PersonViewSet(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class TestMiddleware(TestCase):
    #
    def setUp(self):
        Person.objects.create(first_name='name1', last_name='last_name1')
        Person.objects.create(first_name='name2', last_name='last_name2')

    @pytest.mark.django_db
    def test_base_middleware(self):
        thread_local.remote_ip = 'remote_ip'
        factory = RequestFactory()
        factory.META = factory.GET = {'HTTP_AUTHORIZATION': f'Bearer x'}
        BaseMiddleware(get_response=lambda x: None)(factory)  # noqa
        factory.content = factory.body = b'{}'
        factory.path = '/'
        factory.method = 'POST'
        BaseMiddleware(get_response=lambda x: None)(factory)  # noqa
