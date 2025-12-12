import base64
import hashlib
import hmac
import time
import urllib.parse

import requests


class DingDingWebhook:

    def __init__(self, webhook_url, secret):
        '''
        传入钉钉机器人webhook url以及对应的密钥
        '''
        self.timestamp = str(round(time.time() * 1000))
        self.secret_enc = secret.encode('utf-8')
        self.string_to_sign_enc = '{}\n{}'.format(self.timestamp, secret).encode('utf-8')
        self.hmac_code = hmac.new(self.secret_enc, self.string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = urllib.parse.quote_plus(base64.b64encode(self.hmac_code))
        self.webhook_url = f"{webhook_url}&timestamp={self.timestamp}&sign={self.sign}"

    def send_autotest_report(self, result, title='接口自动化测试结果', text=None):
        if not text:
            text = f"#### {title} \n  > ###### 用例总数：%s\n > ###### 成功用例数量：%s\n > ###### 失败用例数量：%s\n > ###### 报错用例数量：%s\n > ###### 跳过用例数量：%s \n > ###### 报告生成时间：%s" % (
                result._numcollected, len(result.stats.get('passed', [])), len(result.stats.get('failed', [])),
                len(result.stats.get('error', [])), len(result.stats.get('skipped', [])),
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "#接口自动化测试报告",
                "text": text
            },
        }
        res = requests.post(url=self.webhook_url, json=data)
        # print(res.json())

    def send_msg(self, title, text):
        data = {
            "msgtype": 'markdown',
            "markdown": {
                "title": title,
                "text": text
            }
        }
        res = requests.post(url=self.webhook_url, data=data)
