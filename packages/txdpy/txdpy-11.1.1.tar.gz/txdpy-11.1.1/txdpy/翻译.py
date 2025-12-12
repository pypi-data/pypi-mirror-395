# -*- coding: utf-8 -*-
from loguru import logger
from random import randint
from hashlib import md5
from requests import get

translator = None

def translate(foreign_languages):
    """外语翻译成汉语
    :param foreign_languages:要翻译成汉语的外语
    :return: 返回汉语
    """
    foreign_languages = str(foreign_languages)
    # 百度翻译
    try:
        appid = '20220712001270949'
        secret_key = 'ODwtPobgXFes3sBML_NM'
        salt = str(randint(1000000000, 9999999999))
        m = md5()
        m.update((appid + foreign_languages + salt + secret_key).encode("utf8"))
        s = f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={foreign_languages}&from=en&to=zh&appid={appid}&salt={salt}&sign={m.hexdigest()}'
        result = get(s).json()["trans_result"][0]['dst']
        return result
    except:
        pass
    # 谷歌翻译
    try:
        global translator
        if not translator:
            from translate import Translator
            translator = Translator(to_lang="zh")
        return translator.translate(foreign_languages)
    except:
        logger.warning(f'{foreign_languages}，无法识别或翻译')
        return None