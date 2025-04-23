from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView


class SaeCheckPreloadView(APIView):
    def get(self, request):  # noqa
        return Response('successful')


def include_sae_urls():
    urls = [
        path('checkpreload', SaeCheckPreloadView.as_view(authentication_classes=[], permission_classes=[]), name='sae-checkpreload'),
    ]
    return include((urls, 'sae'), namespace='sae')
