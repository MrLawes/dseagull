import hashlib
import uuid

import httpx


class SMS:

    def __init__(self, host, account, password):
        self.host = host
        self.account = account
        self.password = password

    def create_payload(self, **kwargs):
        if 'hbsmservice' in self.host:
            transaction_id = uuid.uuid4().hex
            payload = {
                'account': self.account,
                'transactionId': transaction_id,
            }
            password = f"{self.account}{self.password}{transaction_id}"
            payload['password'] = hashlib.md5(f"{password}".encode()).hexdigest()
            payload['content'] = kwargs['content']
            payload['list'] = []
            for to in kwargs['to_list']:
                payload['list'].append({
                    "mobile": to,
                    "uuid": uuid.uuid4().hex,
                })
        else:
            raise ValueError("无法识别 host")
        return payload

    def send(self, to_list: list[str], content: str):
        payload = self.create_payload(to_list=to_list, content=content)
        if 'hbsmservice' in self.host:
            r = httpx.post(f"{self.host}/sms/v2/send-same", json=payload)
            return r.status_code, r.json()
        else:
            raise ValueError("无法识别 host")
