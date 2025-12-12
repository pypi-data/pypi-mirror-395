# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz
from loguru import logger

def 文本模糊搜索(文本,匹配文本列表,相似度最低阈值=70):
    highest_similarity = 0
    best_match = ""
    for string in 匹配文本列表:
        similarity = fuzz.ratio(文本, string)
        if similarity > highest_similarity:
            highest_similarity,best_match = similarity,string

    if highest_similarity>相似度最低阈值:
        print(f"原始:{文本}  替换:{best_match}")
        return best_match

    logger.error(f"{文本}未匹配到相似度大于{相似度最低阈值}%的文本")
    return 文本