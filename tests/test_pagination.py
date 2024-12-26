from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from dseagull.pagination import PageNumberPagination


class TestPageNumberPagination:

    def setup_method(self):
        class ExamplePagination(PageNumberPagination):
            page_size = 5

        self.pagination = ExamplePagination()
        self.queryset = range(1, 101)

    def paginate_queryset(self, request):
        return list(self.pagination.paginate_queryset(self.queryset, request))

    def get_paginated_content(self, queryset):
        response = self.pagination.get_paginated_response(queryset)
        return response.data

    def test_second_page(self):
        request = Request(APIRequestFactory().get('/', {'page': 2}))
        queryset = self.paginate_queryset(request)
        content = self.get_paginated_content(queryset)
        assert queryset == [6, 7, 8, 9, 10]
        assert content == {
            'paging': {'page_size': 5, 'skip': 5, 'total': 100, 'page': 2, 'total_pages': 20},
            'results': [6, 7, 8, 9, 10]
        }
