import logging
import traceback

import requests
from django.conf import settings


class DjangoRequestErrorLOGGINGHandler(logging.Handler):

    def emit(self, record):

        webhook = getattr(settings, 'DJANGO_REQUEST_ERROR_WEBHOOK', None)
        if not webhook:
            return

        msg = record.msg or ""
        if msg.startswith("Task %") or msg.startswith("%s: %s"):
            record.msg = traceback.format_exc().replace('\n', '\n\n')

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "Seagull",
                "text": record.msg,
            }
        }
        # 钉钉文档: https://open.dingtalk.com/document/orgapp/custom-robot-access
        r = requests.post(webhook, json=payload, timeout=10)
        if r.status_code == 200 and b'"errmsg":"ok"' in r.content:
            pass
        else:
            print(f"[DjangoRequestErrorLOGGINGHandler] {r.content.decode()}")
