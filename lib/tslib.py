# 推送类
# 作者：Ricky
# 日期：2024-11-22

from urllib.parse import quote
import requests

class Ts:
    def __init__(self, ts_types):
        self.ts_types = ts_types
        
        pass

    def send(self, content):
        pass
        self.ts_types.forEach(lambda ts_type: self.ts_type(content))


    # 推送通知
    # https://api.day.app/[token]/这里改成你自己的推送内容
    def bark_ts(self, content):
        # 1.推送内容，并urlencode编码
        content = quote(content)
        # 2.推送url,content参数需要urlencode编码
        url = 'https://api.day.app/[token]/' + content
        # 3.发送请求
        response = requests.get(url=url)
