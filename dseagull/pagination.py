from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    max_page_size = 100
    page_size_query_param = 'page_size'
    page_query_description = '页数'
    page_size_query_description = '每页限定行数'
    invalid_page_message = '已经没有更多了'

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        return Response({
            'paging': {
                'page_size': page_size,
                'skip': (self.page.number - 1) * page_size,
                'total': self.page.paginator.count,
                'page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
            },
            'results': data
        })
