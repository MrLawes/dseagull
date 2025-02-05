# todo
# import logging
import threading
from uuid import uuid4

#
from django.utils.deprecation import MiddlewareMixin

from dseagull.djwt import JWTHS256

#
# # pip install python-json-logger
# from pythonjsonlogger import jsonlogger
# # 创建一个全局线程局部存储，用于保存请求 ID
thread_local = threading.local()


#
#
# class RequestIDFilter(logging.Filter):
#     def filter(self, record):
#         record.__dict__.update(vars(thread_local))
#         return True
#
#
# # 配置日志
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(request_id)s - %(message)s')
# formatter = jsonlogger.JsonFormatter('%(asctime)s %(user_id)s %(levelname)s %(request_id)s %(message)s')
#
# handler.setFormatter(formatter)
# logger.addHandler(handler)
#
# # 添加自定义的 Filter
# logger.addFilter(RequestIDFilter())
#
#
# # 日志：
# # 服务端日志输出格式通常会根据具体的应用场景和需求而有所不同，但一般来说，大厂的服务端日志输出会遵循一定的结构化格式，以便于后续的日志分析和监控。常见的日志格式包括 JSON、文本格式、Apache 日志格式等。
# #
# # 以下是一个常见的服务端日志输出样例，采用 JSON 格式：
# #
# # json
# # {
# #   "timestamp": "2023-10-01T12:34:56Z",
# #   "level": "INFO",
# #   "service": "user-service",
# #   "instance": "instance-1",
# #   "requestId": "abc123",
# #   "userId": "user-456",
# #   "userType": "user-456",
# #   "action": "login",
# #   "status": "success",
# #   "responseTime": 123,
# #   "ip": "192.168.1.1",
# #   "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
# #   "message": "User logged in successfully"
# # }
# # 在这个示例中，包含了以下字段：
# #
# # timestamp: 日志生成的时间。
# # level: 日志级别（如 INFO、ERROR、DEBUG 等）。
# # service: 产生日志的服务名称。
# # instance: 服务实例标识。
# # requestId: 唯一的请求标识符，方便追踪请求。
# # userId: 用户标识。
# # userType: user-456,
# # action: 用户执行的操作。
# # status: 操作的状态（成功或失败）。
# # responseTime: 处理请求所需的时间（毫秒）。
# # ip: 用户的 IP 地址。
# # userAgent: 用户的浏览器信息。
# # message: 具体的日志信息描述。
# # 这种结构化的日志格式可以方便地进行搜索、过滤和分析，适合大规模的分布式系统和微服务架构。大厂通常会使用 ELK（Elasticsearch, Logstash, Kibana）等工具来集中管理和分析日志。

class LoggerMiddleware(MiddlewareMixin):

    @classmethod
    def process_request(cls, request):
        authorization = request.META.get('HTTP_AUTHORIZATION') or request.GET.get('Authorization') or ''
        if authorization:
            request.META['HTTP_AUTHORIZATION'] = authorization

        # 先清空之前的值
        for attr in list(thread_local.__dict__.keys()):
            delattr(thread_local, attr)

        if authorization.startswith('Bearer '):
            try:
                payload = JWTHS256().decode(authorization.removeprefix('Bearer '))
            except:  # noqa
                return

            thread_local.userId = payload.get('userId')
            thread_local.userType = payload.get('userType')

        thread_local.remote_ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR') or ''
        thread_local.remote_ip = thread_local.remote_ip.split(',')[0]
        thread_local.request_id = request.META.get('HTTP_X_REQUEST_ID', uuid4().hex)

    def process_response(self, request, response):  # noqa
        return response
