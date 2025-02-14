import pytest
from django.test import RequestFactory, TestCase
from django_filters import rest_framework as filters
from rest_framework import (
    serializers
)
from rest_framework.viewsets import ModelViewSet

from dseagull.djwt import JWTHS256
from dseagull.filters import BaseFilterSet
from dseagull.logger import LoggerMiddleware, thread_local
from tests.models.modeltest import Person


class PersonFilter(BaseFilterSet):
    last_name = filters.CharFilter()
    created = filters.CharFilter(method='filter_datetime', )

    class Meta:
        model = Person
        fields = ('id',)


class PersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()

    class Meta:
        model = Person
        fields = ('id', 'first_name',)


class PersonViewSet(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    ordering_fields = ('first_name',)
    search_fields = ['first_name', ]
    filterset_class = PersonFilter


class TestFilter(TestCase):
    #
    def setUp(self):
        Person.objects.create(first_name='name1', last_name='last_name1')
        Person.objects.create(first_name='name2', last_name='last_name2')

    @pytest.mark.django_db
    def test_ordering(self):
        thread_local.remote_ip = 'remote_ip'
        view = PersonViewSet.as_view({'get': 'list'}, )
        factory = RequestFactory()
        factory.META = factory.GET = {'HTTP_AUTHORIZATION': f'Bearer x'}
        LoggerMiddleware(get_response=lambda x: None)(factory)  # noqa
        factory.META = factory.GET = {'HTTP_AUTHORIZATION': f'Bearer {JWTHS256().encode({})}'}
        LoggerMiddleware(get_response=lambda x: None)(factory)  # noqa
        request = factory.get('/?ordering=first_name', )
        response = view(request)
        assert response.data['results'] == [{'id': 1, 'first_name': 'name1'}, {'id': 2, 'first_name': 'name2'}]

        request = factory.get('/?ordering=-first_name', )
        response = view(request)
        assert response.data['results'] == [{'id': 2, 'first_name': 'name2'}, {'id': 1, 'first_name': 'name1'}]

    @pytest.mark.django_db
    def test_search(self):
        view = PersonViewSet.as_view({'get': 'list'})
        factory = RequestFactory()
        request = factory.get('/?search=name1', )
        response = view(request)
        assert response.data['results'] == [{'id': 1, 'first_name': 'name1'}, ]

        request = factory.get('/?search=name2', )
        response = view(request)
        assert response.data['results'] == [{'id': 2, 'first_name': 'name2'}, ]

    @pytest.mark.django_db
    def test_filter(self):
        view = PersonViewSet.as_view({'get': 'list'})
        factory = RequestFactory()
        request = factory.get('/?last_name=last_name1', )
        response = view(request)
        assert response.data['results'] == [{'id': 1, 'first_name': 'name1'}, ]

        request = factory.get('/?last_name=last_name2', )
        response = view(request)
        assert response.data['results'] == [{'id': 2, 'first_name': 'name2'}, ]

    @pytest.mark.django_db
    def test_base_filter(self):
        view = PersonViewSet.as_view({'get': 'list'})
        factory = RequestFactory()
        Person.objects.filter(id=1).update(created='2025-02-06 00:00')
        Person.objects.filter(id=2).update(created='2025-01-06 00:00')
        request = factory.get('/?created=1738771200,1738771201', )
        response = view(request)
        assert response.data['results'] == [{'id': 1, 'first_name': 'name1'}, ]
        request = factory.get('/?created=1735179200,1738771199', )
        response = view(request)
        assert response.data['results'] == [{'id': 2, 'first_name': 'name2'}, ]
