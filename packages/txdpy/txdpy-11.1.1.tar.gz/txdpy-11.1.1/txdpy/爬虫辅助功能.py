# -*- coding: utf-8 -*-

from tqdm import tqdm
from loguru import logger
import requests
from requests import get
from lxml import etree
from colorama import Fore, init

init()

def req(url:str,param=None,data=None,json=None,headers=None,verify:bool=False,zhencod=True,**kwargs):
    """
    :param url: 请求的url
    :param param: get请求参数默认为空
    :param data: post请求参数默认为空
    :param json: post请求参数默认为空
    :param headers: 默认随机User-Agent
    :param verify: 是否认证证书，默认为False
    :param tree: 是否直接返回etree.HTML()对象，默认为False
    :return: 返回reponese对象
    """
    if headers:
        if type(headers) == str:
            h=format_string_dict(headers)
        else:
            h=headers
    else:
        h= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.244.400 QQBrowser/12.5.5646.400"}
    if param:
        res=requests.get(url,params=format_string_dict(param) if type(param)==str else param,headers=h,verify=verify,**kwargs)
    elif json:
        res=requests.post(url,json=format_string_dict(json) if type(json)==str else json,headers=h,verify=verify,**kwargs)
    elif data:
        res=requests.post(url,data=format_string_dict(data) if type(data)==str else data,headers=h,verify=verify,**kwargs)
    else:
        res=requests.get(url, headers=h,verify=verify,**kwargs)
    if zhencod:
        res.encoding = res.apparent_encoding
    if res.apparent_encoding=='GB2312' and data:
        data={key:bytes(value,"gbk") for key,value in data.items()}
        res = requests.post(url, data=format_string_dict(data) if type(data) == str else data, headers=h, verify=verify,**kwargs)
        res.encoding = res.apparent_encoding
    try:
        res.tree=etree.HTML(res.text)
    except:
        res.tree =None
    status_code=res.status_code
    if 200<=status_code<=201:
        logger.info(f'\t地址：{url}\t\t状态码：'+Fore.GREEN + str(res.status_code))
    elif status_code>=400:
        logger.info(f'\t地址：{url}\t\t状态码：' + Fore.RED + str(res.status_code))
    else:
        logger.info(f'\t地址：{url}\t\t状态码：' + Fore.YELLOW + str(res.status_code))

    return res

def format_string_dict(string):
    if string is None:
        return None
    string=string.strip()
    str_split_lines = string.splitlines()
    dict_format = [line.strip().lstrip(':').split(":", 1) for line in str_split_lines]

    result_dict = {}
    for item in dict_format:
        if not len(item) == 2:
            continue
        item_key = item[0].strip()
        item_value = item[1].strip()
        result_dict[item_key] = item_value

    return result_dict

def webptablesl(res, xpath, i=1):
    """传入网页中table表格xpath，方便生成二维列表数据
    :param res: url响应的html(例如response.text)
    :param xpath: 表格xpath(例如//table[1])
    :param i: 多个表格索引，默认使用第一个xpath匹配到的表格
    :return: 拆分后的表格数据，以列表返回
    """
    tree = etree.HTML(res)
    tables = tree.xpath(xpath)
    if tables:
        table = tables[i - 1]
    else:
        return []
    trs = table.xpath('.//tr')

    # 提取表格合并信息
    al = []
    for tr in trs:
        l = []
        tds = tr.xpath('./td|th')
        for td in tds:
            td_text = ''.join([text.strip() for text in (td.xpath('.//text()'))])
            colspan = td.xpath('./@colspan')
            colspan = int(colspan[0]) if colspan else 1
            rowspan = td.xpath('./@rowspan')
            rowspan = int(rowspan[0]) if rowspan else 1
            l.append({td_text: (colspan, rowspan)})
        al.append(l)

    new_al = []
    for n in range(len(al)):
        new_al.append([])

    # 处理横向合并
    a = 0
    for l in al:
        new_l = new_al[a]
        i = 0
        for d in l:
            for key, value in d.items():
                for c in range(value[0]):
                    new_l.insert(i, key)
                    i += 1
            i += 1
        new_al.pop(a)
        new_al.insert(a, new_l)
        a += 1

    # 处理纵向合并
    a = 0
    for l in al:
        for d in l:
            for key, value in d.items():
                if value[1] > 1:
                    for r in range(1, value[1]):
                        i = new_al[a + r - 1].index(key)
                        new_l = new_al[a + r]
                        new_l.insert(i, key)
                        new_al.pop(a + r)
                        new_al.insert(a + r, new_l)
        a += 1

    return new_al

def dow_file(path_name, href, add_suffix=True):
    """
    :param path_name: 下载路径及文件名，c:/a.pdf
    :param href: 下载链接
    :param add_suffix: 从链接中提取文件后缀
    :return:
    """
    name = path_name.split('/')[-1]
    if add_suffix:
        path_name += '.'+href.split('.')[-1]
    print('开始下载：', name, href)
    res = get(href, stream=True,verify=False)
    if res.status_code == 404:
        return False
    if 'Content-Length' in res.headers:
        file_size = int(res.headers.get('Content-Length'))  # 获取文件的总大小
    else:
        print('未找到文件大小标识', name, href)
        file_size=30000000
    pbar = tqdm(total=file_size)  # 设置进度条的长度
    with open(path_name, 'wb') as f:
        for chunk in res.iter_content(1024 * 1024 * 2):
            f.write(chunk)
            pbar.set_description('正在下载中......')
            pbar.update(1024 * 1024 * 2)  # 更新进度条长度
        pbar.close()
    print('下载完成：', name, href)