# -*- coding: utf-8 -*-

"""
这段代码有点烧脑子，也没啥注释，第二遍也看不懂，能凑合用就行！！！！
原理是以字符串中的括号引号将字符串划分层级，进行后续处理，就多出了很多思路
例如：<我喜欢吃【水果（香蕉(banana)）】>
按层级：
    我喜欢吃
        【
        水果
            （
            香蕉
                "
                banana
                "
            ）
        】
"""

import re

symbol = {
    '(': ')',
    '[': ']',
    '{': '}',
    '【': '】',
    '《': '》',
    '<': '>',
    '〈': '〉',
    '（': '）',
    '‘': '’',
    '“': '”',
    '"': '"',
    "'": "'",
}

symbols = {k + y for k, y in symbol.items()}
symbol_swapped = {v: k for k, v in symbol.items()}


def join_c_up(lr=True):  # 上一个层级
    global level_text, indentation
    indentation = indentation[:-4]
    level_text += '\n' + indentation + c + '\n' + (indentation if lr else indentation[:-4])


def join_c_now(lr=True):  # 当前层级
    global level_text
    level_text += '\n' + indentation + c + '\n' + (indentation if lr else indentation[:-4])


def join_c_down():  # 下一个层级
    global level_text, indentation, max_indentation_len
    indentation += '' if level_text == '' else (' ' * 4)
    level_text += '\n' + indentation + c + '\n' + indentation


symbol_list = []
level_text = ''
indentation = ' ' * 0  # 缩进空格数
left_right_mark = 'left'


def 文本括号及引号不匹配检查(text, 是否将最外层括号改为中括号=False):
    """
    :param text: 需要检查的文本
    :param 是否将最外层括号改为中括号:
    :return: 返回错误格式是错误的符号和错误符号所在的从左往右位置
    """
    global level_text, symbol_list, indentation, left_right_mark, c
    level_text = ''
    for i, c in enumerate(text):
        if c == '"':
            if symbol_list and symbol_list[-1][0] == '"':
                join_c_now(False)
                symbol_list.pop()
                left_right_mark = 'right'
            else:
                join_c_down()
                symbol_list.append((c, i))
                left_right_mark = 'left'
        elif c == "'":
            if symbol_list and symbol_list[-1][0] == "'":
                join_c_now(False)
                symbol_list.pop()
                left_right_mark = 'right'
            else:
                join_c_down()
                symbol_list.append((c, i))
                left_right_mark = 'left'
        elif c in symbol:
            if left_right_mark == 'right':
                join_c_now()
            else:
                join_c_down()
            symbol_list.append((c, i))
            left_right_mark = 'left'
        elif c in symbol_swapped:
            if not symbol_list:
                return (c, i)
            if symbol_swapped.get(c) != symbol_list[-1][0]:
                return symbol_list[-1]
            if left_right_mark == 'left':
                join_c_now(False)
            else:
                join_c_up(False)
            left_right_mark = 'right'
            symbol_list.pop()
        else:
            level_text += c

    level_text = [t for t in level_text.split('\n') if t.strip() != '']

    symbol_index = set()
    for t in level_text:
        if t.strip() in symbol:
            symbol_index.add(len(t) - 1)
    if symbol_index:
        first_level = min(symbol_index)
    else:
        return text
    symbol_level = {i: [] for i in symbol_index}
    for i in symbol_index:
        for ti, t in enumerate(level_text):
            if (t.strip() in symbol or t.strip() in symbol_swapped) and len(t) - 1 == i:
                symbol_level[i].append((t.strip(), ti))

    for value in sorted([(k, v) for k, v in symbol_level.items()]):
        value = value[1]
        for i in range(len(value))[::2]:
            try:
                if symbol.get(value[i][0]) != value[i + 1][0]:
                    return (
                    level_text[value[i][1]].strip(), len(''.join([t.strip() for t in level_text[:value[i][1]]])) + 1)
            except:
                return (
                level_text[value[i][1]].strip(), len(''.join([t.strip() for t in level_text[:value[i][1]]])) + 1)

    re_text = re.sub(r"""[^""" + ''.join(symbols).replace('[', r'\[').replace(']', r'\]') + """]+""", '*', text)
    for k1, v1 in symbol.items():
        for k2, v2 in symbol.items():
            zhc = f'{k1 + k2}*{v2 + v1}'
            if zhc in re_text:
                return (f'出现"{zhc}"异常情况', '')
            if (k1 + v1) in text:
                return (f'出现"{k1 + v1}"异常情况', '')
    if 是否将最外层括号改为中括号:
        end_text = ''
        for t in level_text:
            if (t.strip() in symbol or t.strip() in symbol_swapped) and len(t) - 1 == first_level:
                if t.strip() in symbol:
                    t = '['
                else:
                    t = ']'
            end_text += t.strip()
        return end_text
