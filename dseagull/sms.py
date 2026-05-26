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
            payload['list'] = []
            for sign_name, mobile, content in kwargs['to_list']:
                payload['list'].append({
                    "mobile": mobile,
                    "uuid": uuid.uuid4().hex,
                    'content': f"【{sign_name}】{content}",
                })
        else:
            raise ValueError("无法识别 host")
        return payload

    def send(self, to_list: list[tuple]):
        """
        :param to_list: [('签名', '手机号', '短信内容'), ]
        :return:
        """
        payload = self.create_payload(to_list=to_list)
        if 'hbsmservice' in self.host:
            r = httpx.post(f"{self.host}/sms/v2/send-different", json=payload)
            results = r.json()
            results['results'] = [
                {
                    "mobile": item['mobile'],  # noqa
                    "uuid": item['uuid'],  # noqa
                    "content": item['content'],  # noqa
                } for item in payload['list']
            ]
            return r.status_code, results
        else:
            raise ValueError("无法识别 host")
