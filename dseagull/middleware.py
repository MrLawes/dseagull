from types import SimpleNamespace

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from dseagull.dlogging import LOGGER


class BaseMiddleware(MiddlewareMixin):

    @classmethod
    def process_request(cls, request):
        request.start_at = timezone.localtime()
        try:
            body = request.body.decode('utf8')
            body = body[:1000]
            LOGGER.info(f'[request] method:{request.method};path={request.path}', )
            LOGGER.info(f"[request] body:{body}", )
        except:  # noqa
            pass

    def process_response(self, request, response):  # noqa

        response = response or SimpleNamespace(content=b'', status_code=201)
        try:
            response_content = response.content
        except:  # noqa
            return response
        if len(response_content) > 1000:
            response_content = response_content[:997] + b'...'
        try:
            response_content = response_content.decode('utf8')
        except:  # noqa
            pass

        duration = timezone.localtime() - request.start_at
        LOGGER.info(f'[process_response] status_code:{response.status_code};duration:{duration.seconds}.{duration.microseconds:0>6};content:{response_content}')
        if duration.seconds >= 10:
            LOGGER.info(f'[请求超时] method:{request.method};path={request.path};duration:{duration.seconds}.{duration.microseconds:0>6}', )
        return response
