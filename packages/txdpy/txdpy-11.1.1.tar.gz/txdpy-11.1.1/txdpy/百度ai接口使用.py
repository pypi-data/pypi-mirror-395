# -*- coding: utf-8 -*-
from requests import post, request, get
from hashlib import md5
from random import randint
from time import sleep
from json import dumps
from .excel数据或mysql操作 import ReadData
import urllib.parse

# class TextSimilar:
#     def __init__(self):
#         params = {"grant_type": "client_credentials", "client_id": "bfLANvXUYkfhJhp7knzDBSkB",
#                   "client_secret": "oatCi4BsYrvx8ZBJHUelSEdoxo70a4ZH"}
#         self.access_token = str(
#             post("https://aip.baidubce.com/oauth/2.0/token", params=params).json().get("access_token"))
#
#     def __call__(self, text_1, text_2):
#         """文本相似度
#         :param text_1:文本一
#         :param text_2:文本二
#         :return: 返回文本相似度
#         """
#         i = 0
#         response, e = None, None
#         while i < 10:
#             try:
#                 url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=&access_token=" + self.access_token
#                 payload = dumps({
#                     "text_1": text_1,
#                     "text_2": text_2
#                 })
#                 response = request("POST", url,
#                                    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
#                                    data=payload).json()
#                 return response['score']
#             except Exception as e:
#                 sleep(10)
#                 i += 1
#         else:
#             raise ValueError(f'百度相似度匹配异常：{response}')


# def translate(text):
#     """外语翻译成汉语
#     :param text:要翻译成汉语的外语
#     :return: 返回汉语
#     """
#     appid = '20220712001270949'
#     q = str(text)
#     secret_key = 'ODwtPobgXFes3sBML_NM'
#     salt = str(randint(1000000000, 9999999999))
#     m = md5()
#     m.update((appid + q + salt + secret_key).encode("utf8"))
#     s = f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={urllib.parse.quote(q)}&from=en&to=zh&appid={appid}&salt={salt}&sign={m.hexdigest()}'
#     result = get(s).json()
#     # print(result)
#     return result["trans_result"][0]['dst']


class 文本错别字检查():
    """
    百度的错别字识别接口
    """
    def __init__(self):
        API_KEY, SECRET_KEY = \
        ReadData('百度ai接口验证参数', ['API Key', 'Secret Key'], select_sql="`云api类型` = '自然语言处理'").data[-1]
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        self.access_token = str(
            post("https://aip.baidubce.com/oauth/2.0/token", params=params).json().get("access_token"))

    def __call__(self, 文本):
        """
        :param 文本: 要识别错别字的文本
        :return: [(错误文本,可能正确的文本,错误文本出现的位置),]
        """
        sleep(.5)
        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet?charset=utf-8&access_token=" + self.access_token
        payload = dumps({
            "text": 文本
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = request("POST", url, headers=headers, data=payload).json()
        return ([(v['ori_frag'], v['correct_frag'], v['begin_pos']) for v in response['item']['vec_fragment'] if
                 '(' not in v['ori_frag'] and ')' not in v['ori_frag'] and v['ori_frag'] != v['correct_frag']] or None)