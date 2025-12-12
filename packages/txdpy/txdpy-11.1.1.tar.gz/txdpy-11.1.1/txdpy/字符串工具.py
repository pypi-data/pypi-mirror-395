# -*- coding: utf-8 -*-
import re

def 字符串相似度(str1,str2):
    """
    计算两个字符串中相同汉字字符的个数，作为字符串的相似度。
    Args:
        str1 (str): 第一个字符串。
        str2 (str): 第二个字符串。
    Returns:
        int: 两个字符串中相同汉字字符的个数。
    """
    str1_汉字 = re.findall(r'([\w])', str1)
    str2_汉字 = re.findall(r'([\w])', str2)
    return len([x for x in str1_汉字 if x in str2_汉字])

# 提取汉字
def get_chinese(s: str):
    """提取汉字
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([\u4e00-\u9fa5]+)', s)


# 提取字母
def get_letter(s: str):
    """提取字母
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([a-zA-Z]+)', s)


# 提取大写字母
def get_bletter(s: str):
    """提取大写字母
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([A-Z]+)', s)


# 提取小写字母
def get_sletter(s: str):
    """提取小写字母
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([a-z]+)', s)


# 提取数字
def get_num(s: str):
    """提取数字
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([0-9]+)', s)


# 提取数字或字母或数字和字母
def get_num_letter(s: str):
    """提取数字或字母或数字和字母
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([0-9a-zA-Z]+)', s)


# 判断是否为纯数字
def is_num(s):
    if type(s) == int or type(s) == float or re.search(r'^([0-9\.]+)$', str(s)):
        return True
    return False


# 判断是否为纯小写字母
def is_sletter(s: str):
    if re.search('^([a-z]+)$', s):
        return True
    return False


# 判断是否为纯大写字母
def is_bletter(s: str):
    if re.search('^([A-Z]+)$', s):
        return True
    return False


# 判断是否为纯字母
def is_letter(s: str):
    if re.search('^([a-zA-Z]+)$', s):
        return True
    return False


# 判断是否为纯数字和字母
def is_num_letter(s):
    if type(s) == int:
        return True
    if type(s) != str:
        return False
    if re.search(r'^([\da-zA-Z]+)$', s):
        return True
    return False


# 判断是否为纯汉字
def is_chinese(s: str):
    if re.search('^([\u4e00-\u9fa5]+)$', s):
        return True
    return False
