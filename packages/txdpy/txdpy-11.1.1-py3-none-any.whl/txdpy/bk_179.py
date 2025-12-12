# -*- coding: utf-8 -*-
# @File  : 通用代码.py
# @Time  : 2023/6/9 13:12
# @Author: 唐旭东
from .excel数据或mysql操作 import optstr, ReadData, prvadepl, MysqlConn
import sys,re,json
from loguru import logger
from .字符串工具 import is_num
from .列表操作 import list_dupl
from os import path
from .路径操作 import FileFolderPath
from .省市区名称的提取或判断 import get_ssq
from bs4 import BeautifulSoup
from json import loads

#老高考批次
# batch_dict1 = {'本科一批A': '本科一批', '专科': '专科', '本科一批A1': '本科一批', '本科一批B': '本科一批',
#                  '本科二批A': '本科二批', '本科二批B': '本科二批', '本科二批C': '本科二批', '高本贯通批': '专科',
#                  '本科提前A': '本科一批', '本科提前批A': '本科一批', '本科提前批B': '本科一批', '本科提前B': '本科一批',
#                  '本科一批': '本科一批', '蒙授本科一批': '本科一批', '本科二批': '本科二批', '蒙授本科二批': '本科二批',
#                  '专科提前': '专科', '专科提前批': '专科', '蒙授本科提前A': '本科一批', '蒙授本科提前批A': '本科一批',
#                  '蒙授专科': '专科', '蒙授本科提前B': '本科一批', '蒙授本科提前批B': '本科一批', '蒙授专科提前': '专科',
#                  '蒙授专科提前批': '专科', '国家专项': '本科一批', '本科提前批': '本科一批', '提前批': '本科一批',
#                  '地方专项': '本科一批', '提前批公安专科': '专科', '公安专科院校': '专科', '提前本科二批': '本科二批',
#                  '提前本科一批': '本科一批', '专项计划批': '本科一批', '本科提前批其他类': '本科一批',
#                  '本科一批预科': '本科一批', '本科二批预科B类': '本科二批', '本科二批预科A类': '本科二批',
#                  '专科提前批定向类': '专科', '专科提前批其他类': '专科', '本科提前批空军招飞批': '本科一批',
#                  '本科二批预科B': '本科二批', '专项计划': '本科一批', '本科二批预科A': '本科二批',
#                  '本科一批高校专项': '本科一批', '本科二批预科': '本科二批', '本科提前批预科': '本科一批',
#                  '本科提前批高校专项': '本科一批', '一类模式本科二批预科': '本科二批', '一类模式专科预科': '专科',
#                  '专科预科': '专科', '一类模式本科一批预科': '本科一批', '帮扶专项': '本科一批',
#                  '提前本科批': '本科一批', '一本预科': '本科一批', '二本及预科': '本科二批', '提前专项批': '本科二批',
#                  '提前专科批': '专科', '专项提前批': '本科二批', '高职专项': '专科',
#                  '本科提前批B段(国家专项)': '本科一批', '本科提前批少数民族紧缺人才专项（G段）': '本科一批',
#                  '本科提前批地方专项（D段）': '本科一批', '本科提前批省属院校贫困地区国家专项（C段）': '本科一批',
#                  '本科提前批精准扶贫专项（E段）': '本科一批', '本科提前批革命老区专项（F段）': '本科一批',
#                  '提前批一本': '本科二批', '提前批二本': '本科二批', '提前二批专科': '本科二批',
#                  '本科一批(普通类)': '本科一批', '本科二批(普通类)': '本科二批', '专科批(普通类)': '专科批(普通类)',
#                  '本科一批(单列类-选考外语)': '本科一批', '本科二批(单列类-选考外语)': '本科二批',
#                  '本科一批(单列类-选考民族语文)': '本科一批', '本科二批(单列类-选考民族语文)': '本科二批',
#                  '专科批(单列类-选考外语)': '专科', '专科批(单列类-选考民族语文)': '专科',
#                  '【内高】18级单列本科二批（四年）': '本科二批', '【内高】19级单列本科二批': '本科二批',
#                  '本科二批单列': '本科二批', '【内高】18级单列本科一批': '本科一批',
#                  '【内高】18级单列本科一批（四年）': '本科一批', '【内高】18级普通本科一批': '本科一批',
#                  '【内高】19级单列本科一批': '本科一批', '【内高】19级普通本科一批': '本科一批', '本科一批单列': '本科一批',
#                  '【内高】18级单列专科': '专科', '【内高】18级单列专科（四年）': '专科', '【内高】18级普通专科': '专科',
#                  '【内高】19级单列专科': '专科', '【内高】19级普通专科': '专科', '专科单列': '专科',
#                  '【内高】18级单列本科二批': '本科二批', '【内高】18级普通本科二批': '本科二批',
#                  '【内高】19级普通本科二批': '本科二批', '【内高】18级单列本科提前批': '本科一批',
#                  '【内高】18级普通本科提前批': '本科一批', '【内高】19级单列本科提前批': '本科一批',
#                  '【内高】19级普通本科提前批': '本科一批', '【内高】18级单列本科提前批（四年）': '本科一批'}
#
# #新高考批次
# batch_dict2 = {'bk': '本科', 'zk': '专科', '本科': '本科', '专科': '专科','专科提前': '专科', '专科提前批': '专科',
#                  '蒙授专科': '专科', '蒙授专科提前': '专科', '蒙授专科提前批': '专科', '提前批公安专科': '专科', '公安专科院校': '专科',
#                  '专科提前批定向类': '专科', '专科提前批其他类': '专科', '一类模式专科预科': '专科','专科预科': '专科', '提前专科批': '专科', '高职专项': '专科'
#                 }

#转换批次名称
def convert_pc(pc):
# def convert_pc(pc,prurar=None):
    # if prurar:
    #     new_pc = batch_dict1.get(pc) if prurar in prurar_code('老高考省份') else batch_dict2.get(pc,'特殊类')
    #     if new_pc:
    #         return new_pc
    if '本科' in pc and '提前' in pc:
        return '本科提前批'
    elif '专科' in pc and '提前' in pc:
        return '专科提前批'
    elif '本科' in pc or 'bk' in pc or '一段' in pc:
        return '本科'
    elif '专科' in pc or 'zk' in pc or '二段' in pc:
        return '专科'
    else:
        return '特殊类'

#返回省市区名称和地区编号
def prurar_code(gkle='all',ssq=None):
    gkle=gkle.strip('省份')
    prurar_code={"北京": 11, "天津": 12, "河北": 13, "山西": 14, "内蒙古": 15, "辽宁": 21, "吉林": 22, "黑龙江": 23,
           "上海": 31, "江苏": 32, "浙江": 33, "安徽": 34, "福建": 35, "江西": 36, "山东": 37, "河南": 41, "湖北": 42,
           "湖南": 43, "广东": 44, "广西": 45, "海南": 46, "重庆": 50, "四川": 51, "贵州": 52, "云南": 53,
           "陕西": 61, "甘肃": 62, "青海": 63, "宁夏": 64, "新疆": 65}
    if ssq:
        return prurar_code[ssq]
    if gkle in ('专业类','专业组','老高考','综合'):
        prurar_dict = {x[0]: x[1] for x in ReadData('各省份高考分类').data}
        return json.loads(prurar_dict.get(gkle))
    return prurar_code

#转换科类名称
def convert_kl(kl):
    if 'li' in kl or '理' in kl:
        return '物理'
    if 'wen' in kl or '文' in kl:
        return '历史'
    if 'all' in kl or '不限' in kl:
        return '综合'
    return kl

#删除了数据中判断为Flase(判断0的返回值为Flase)的数据
def delete_flase_empty(ls):
    nls=[]
    for l in ls:
        type_l=type(l)
        if type_l!=int and type_l!=float and l:
            logger.error(f"数据集中存在非数字类型数据！\n{ls}")
            sys.exit()
        if l:
            nls.append(l)
    return nls

#求平均数默认保留小数
def txdavg(ls,zero_in=False,dp=2,valid=True):
    """
    :param zero_in 0是否参与计算，默认不参与
    :param dp 默认保留2位小数
    :param valid 默认保留有效小数位
    """
    ls_0=[]
    if zero_in:
        ls_0 = [l for l in ls if l==0]
    ls = delete_flase_empty(ls)+ls_0
    if ls:
        if valid:
            return prvadepl(round(sum(ls)/len(ls), dp))
        return round(sum(ls) / len(ls), dp)
    else:
        return None

#求百分比平均数默认保留百分比中两位小数
def txdpercavg(ls,dp=2):
    nls=[]
    for l in ls:
        if l is None:
            continue
        if type(l)==str:
            if re.search('^([0-9.]+%)$',l):
                nls.append(float(l[:-1])/100)
            else:
                logger.error(f'计算平均百分比时，发现存在非百分比数据\n{ls}')
                sys.exit()
    ls = delete_flase_empty(nls)
    if ls:
        return txdperc(sum(ls)/len(ls), dp)
    else:
        return None

#求最小数
def txdmin(ls):
    ls = delete_flase_empty(ls)
    if ls:
        return min(ls)
    else:
        return None

#将数字转换为百分比，默认百分比中数字保留两位小数
def txdperc(num,dp=2):
    return f'{round(num * 100, dp)}%' if is_num(num) else None

class QueryScoreRank:
    """
    查询分数位次，省份批次线
    """
    def __init__(self,year,simplify_pcname=True):
        """
        :param year:年份
        :param mysql:mysql连接对象
        :param simplify_pcname:是否将批次转换为只有本专科，默认为True
        """
        self.year=year
        self.simplify_pcname=simplify_pcname
        self.batch_xian_dict={}
        self.frac_rank_dict={'北京':{},'天津':{},'上海':{},'江苏':{},'广东':{},'江西':{},'other':{}}
        self.get_batch_xian()#获取当前年份所有省份所有科类批次线生成字典数据
        self.get_frac_rank()#获取当前年份所有省份所有科类所有批次分数排名生成字典数据

    def get_batch_xian(self):
        """
        获取当前年份所有省份所有科类批次线生成字典数据
        """
        batch_dict = {'本科批': '本科', '本科一批(普通类)': '本科一批', '本科二批(普通类)': '本科二批','专科批(普通类)': '专科', }
        batch_xians = ReadData('批次线表', ['region_name', 'kelei_name', 'batch', 'batch_fen'],select_sql=f"`year` = '{self.year}'", replace_th=False).data
        if self.simplify_pcname:
            # 将批次转换为只有本专科
            for batch_xian in batch_xians:
                pc = batch_dict.get(batch_xian[2], batch_xian[2])
                pc = '专科' if '专科' in convert_pc(pc) else '本科'
                pc = "专科" if ("专科" in pc or "二段" in pc) else "本科"
                key = f'{batch_xian[0]}_{pc}_{convert_kl(batch_xian[1])}'
                if key in self.batch_xian_dict:
                    if self.batch_xian_dict[key] - batch_xian[-1] > 0:
                        self.batch_xian_dict[key] = batch_xian[-1]
                else:
                    self.batch_xian_dict[key] = batch_xian[-1]
        else:
            for batchds in batch_xians:
                pc = batch_dict.get(batchds[2], batchds[2])
                self.batch_xian_dict[f"{batchds[0]}_{batchds[2]}_{batchds[1]}"] = int(batchds[-1])
                self.batch_xian_dict[f"{batchds[0]}_{batchds[2]}_{batchds[1]}"] = int(batchds[-1])

    def get_frac_rank(self):
        """
        获取当前年份所有省份所有科类所有批次分数排名生成字典数据
        """
        frac_ranks = ReadData('一分一段表', ['region_name','kelei_name','tag','gaokaofen','paim'],select_sql=f"`year` = '{self.year}'",replace_th=False).data
        for frac_rank in frac_ranks:
            region_name=frac_rank[0]
            if region_name in ['北京','天津','上海','江苏','江西','广东']:
                # print(region_name)
                if region_name in ['江苏']:
                    key = f'{region_name}_{convert_kl(frac_rank[1])}_{"本科" if "一" in frac_rank[2] else "专科"}'
                else:
                    key = f'{region_name}_{convert_kl(frac_rank[1])}_{"专科" if "专科" in frac_rank[2] else "本科"}'
                if key in self.frac_rank_dict[region_name]:
                    self.frac_rank_dict[region_name][key][0].append(frac_rank[-2])
                    self.frac_rank_dict[region_name][key][1].append(frac_rank[-1])
                else:
                    self.frac_rank_dict[region_name].update({key: [[frac_rank[-2]], [frac_rank[-1]]]})
            else:
                key=f'{frac_rank[0]}_{convert_kl(frac_rank[1])}'
                if key in self.frac_rank_dict['other']:
                    self.frac_rank_dict['other'][key][0].append(frac_rank[-2])
                    self.frac_rank_dict['other'][key][1].append(frac_rank[-1])
                else:
                    self.frac_rank_dict['other'].update({key:[[frac_rank[-2]],[frac_rank[-1]]]})

    #返回分数位次和位次百分比
    def rfrac_rank(self,prurar,pc,kl,frac,isrrp=False):
        """
        :param prurar:省市区名称
        :param pc:批次
        :param kl:科类
        :param frac:要查询位次的分数
        :param isrrp:是否返回位次百分比
        :return 分数位次，（批次线，批次线位次，分数位次百分比）
        """
        kl = convert_kl(kl)
        if not frac:
            if isrrp:
                return None,(None,None,None)
            return None

        frac_rank=self.rfrac_rank1(prurar, pc, kl, frac)
        if isrrp:
            batch_xian,batch_xian_rank=self.rbx_rank(prurar,pc,kl)
            return frac_rank, (batch_xian,batch_xian_rank,txdperc(frac_rank/batch_xian_rank) if batch_xian_rank and frac_rank else None)
        return frac_rank

    #返回批次线和批次线位次
    def rbx_rank(self,prurar,pc,kl,rbxr=True):
        """
        :param prurar:省市区
        :param pc:批次
        :param kl:科类
        :param rbxr:是否返回位次
        :return:返回批次线和批次线位次
        """
        kl = convert_kl(kl)
        if f'{prurar}_{pc}_{kl}' in self.batch_xian_dict:
            key = f'{prurar}_{pc}_{kl}'
        elif f'{prurar}_{"专科" if ("专科" in pc or "二段" in pc) else "本科"}_{kl}' in self.batch_xian_dict:
            key = f'{prurar}_{"专科" if ("专科" in pc or "二段" in pc) else "本科"}_{kl}'
        else:
            key = None

        if key:
            batch_xian = self.batch_xian_dict[key]
            if rbxr:
                batch_xian_rank = self.rfrac_rank1(prurar, pc, kl, batch_xian)
                return batch_xian, batch_xian_rank
            return batch_xian

    def x(self,prurar,pc,kl,score_ranking,typ):
        if not is_num(score_ranking):
            return
        try:
            kl = convert_kl(kl)
            if prurar in ['北京','天津','上海','江苏','江西','广东']:
                fens=self.frac_rank_dict[prurar][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][0]
                paims=self.frac_rank_dict[prurar][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][1]
            else:
                if prurar == '内蒙古':
                    if '蒙授' in prurar and '蒙授' not in kl:
                        kl='蒙授'+kl
                fens=self.frac_rank_dict['other'][f'{prurar}_{kl}'][0]
                paims=self.frac_rank_dict['other'][f'{prurar}_{kl}'][1]
            if typ==1:
                return paims[fens.index(min(fens, key=lambda x: abs(float(x) - float(score_ranking))))]
            return fens[paims.index(min(paims, key=lambda x: abs(float(x) - float(score_ranking))))]
        except:
            return

    #返回分数位次
    def rfrac_rank1(self,prurar,pc,kl,score):
        """
        :param prurar:省市区
        :param pc:批次
        :param kl:科类
        :param score:分数
        :return:返回分数对应位次
        """
        return self.x(prurar,pc,kl,score,1)

    #返回位次对应分数
    def rfrac_rank2(self,prurar,pc,kl,rank):
        """
        :param prurar:省市区
        :param pc:批次
        :param kl:科类
        :param rank:分数
        :return:返回位次对应分数
        """
        return self.x(prurar, pc, kl, rank, 2)
        # kl = convert_kl(kl)
        # if prurar in '江苏':
        #     fens=self.frac_rank_dict['江苏'][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][0]
        #     paims=self.frac_rank_dict['江苏'][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][1]
        # else:
        #     fens=self.frac_rank_dict['other'][f'{prurar}_{kl}'][0]
        #     paims=self.frac_rank_dict['other'][f'{prurar}_{kl}'][1]
        # return fens[paims.index(min(paims, key=lambda x: abs(float(x) - float(ranking))))]

def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info("开始时间：{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info('共耗时：%f秒' % (time.time() - start_time))
        logger.info("结束时间：{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))))
        return result
    return wrapper

#提取专业名称中招生标签
def exenla(major,maispb=False,return_string=False):
    """
    :param major:专业名称
    :param maispb:是否查找匹配标签
    :param return_string:返回字符串
    :return: 专业名称中的标签
    """
    bqs={'招生标签':list(list_dupl([v for v in
              ['国家专项', '地方专项', '帮扶专项', '预科', '联合培养', '中外合作', '校企合作', '高职本科', '高校专项', '联合办学','精准扶贫','少数民族', '民族班', '少民', '闽台', '优师', '公费', '订单', '双语', '定向']
                if v in major and f'非{v}' not in major])),
    '匹配标签': list(list_dupl([v for v in
                       ['师范','苏区专项']
                    if v in major and f'非{v}' not in major]))
     }
    zhonhwaihezuo=re.search('中[^心]合作',major)
    if zhonhwaihezuo and '中外合作' not in bqs['招生标签']:
        bqs['招生标签'].append('中外合作')
    if return_string:
        return '、'.join(bqs['招生标签'])
    return bqs if maispb else bqs['招生标签']

#获取表头中字段名称索引，表头以列表形式传入
# def getexcelth(rowdatas0,ht):
#     """
#     :param rowdatas0:表头以列表形式传入
#     :param ht:表头中字段名称
#     :return: 字段索引
#     """
#     for i,v in enumerate(rowdatas0):
#         if ht == v:
#             return i
#     if '科类' == ht:
#         ht='文\理科'
#     for i,v in enumerate(rowdatas0):
#         if ht == v:
#             return i
#     if '招生标签' == ht:
#         ht='招生类型'
#     for i,v in enumerate(rowdatas0):
#         if ht in v:
#             return i
#     ht='专业名称' if ht=='业名称' else ht
#     ht='招生标签' if ht=='招生类型' else ht
#     ht='科类' if ht=='文\理科' else ht
#     raise ValueError(f'表头中未找到“{ht}”相关字段名称，可以将“{ht}”字段添加至表中或将相应字段修改为“{ht}”')

#提取专业名称中专业名称和括号部分内容，根据需要返回一级大类和二级大类
class ExtractEnrollmentLabels:
    def __init__(self):
        major_data = ReadData('专业、大类以及逻辑代码',replace_th=False).data
        self.data1={f'{v[0]}_{v[1]}':v[1:] for v in major_data}
        self.data2={v[1]:v[1:] for v in major_data}

    def __call__(self,major,batch,school_name):
        return self.exmana(major,batch,school_name)

    def exmana(self,major,batch,school_name):
        """
        :param major:专业名称
        :param batch:批次
        :param school_name:学校名称，学校名称中有“职业”关键字优先在职业本科查找专业名称信息
        :return:专业名称、专业名称逻辑代码、一级大类、一级大类代码、二级大类、二级大类代码、七大类、七大类代码
        """
        major_name = get_major_name(major)
        row = None
        if '专科' in batch:
            row = self.data1.get('专科' + '_' + major_name)
        else:
            major_class = self.data1.get('本科' + '_' + major_name)
            if major_class:
                row = major_class
            elif '职业' in school_name or school_name in ['山东青年政治学院']:
                row = self.data1.get('职业本科' + '_' + major_name)

        if not row:
            row = self.data2.get(major_name,[major_name]+[None]*7)

        if '师范' in major and row[-1]:
            row = row.copy()
            row[-2:] = ['教师与教育科学类','6']

        return row

#对列表中的多个列表以第某个元素进行排序
def sortedlbys(lists,i,reverse=False):
    """
    :param lists:数据列表
    :param i:一维数据中基准索引
    :param reverse:排序方式，默认False，有小到大
    :return:排序后的数据列表
    """
    return sorted(lists, key=lambda x: x[i], reverse=reverse)

class UpdateName():
    """
    更新院校名称和专业名称
    """
    def __init__(self):
        self.school_names_change = []
        for x in sorted(ReadData('院校',['院校名称','更名历史']).data, key=lambda x: len(x[0]), reverse=True):
            if x[1]:
                for school_name_old in loads(x[1]):
                    self.school_names_change.append([school_name_old,x[0]])

        zk_majors, bk_majors = [], []
        majors=ReadData('更新专业名称名单').data
        for v in majors:
            if v[0] == '本科':
                bk_majors.append(v[1:])
            elif v[0] == '专科' and v[1] != '汽车检测与维修技术':
                zk_majors.append(v[1:])
        self.zk_majors = sorted(zk_majors, key=lambda x: len(x[0]), reverse=True)
        self.bk_majors = sorted(bk_majors, key=lambda x: len(x[0]), reverse=True)

    def update_school_name(self, school_name):
        school_name=optstr(school_name)
        for school_old_new in self.school_names_change:
            if school_name.startswith(school_old_new[0]):
                return school_name.replace(school_old_new[0], school_old_new[1], 1)
        return school_name

    def update_major_name(self,batch, name):
        name=optstr(name)
        re_name=re.search('(^[\u4e00-\u9fa5、]+)(.*)',name)
        if re_name:
            re_name=re_name.groups(1)
            if '专科' in batch or '二段' in batch:
                for major in self.zk_majors:
                    if re_name[0]==major[0]:
                        return major[0]+re_name[1]
            else:
                for major in self.bk_majors:
                    if re_name[0]==major[0]:
                        return major[0]+re_name[1]
        return name

# def is_school(string):
#     """
#     判断是否为学校名称
#     """
#     re_string=re.search('([\u4e00-\u9fa5]+)',optstr(string))
#     if re_string:
#         re_string=re_string.group(1)
#         if re_string.endswith('大学') or re_string.endswith('学院') or re_string.endswith('学校') or re_string.endswith('分校'):
#             return True

def unify_keys(ks):
    """
    统一表头字段名称
    """
    key_dict={x[0]: x[1] for x in ReadData('读取数据时表头字段统一化参考表').data}
    for i,k1 in enumerate(ks):
        for k2,ys in key_dict.items():
            for y in ys.split(','):
                if y==k1:
                    ks[i]=k2
                    break
    return ks

def school_ljdm():
    """
    :return: 返回院校逻辑代码字典
    """
    school_ljdm_dict = {}
    for x in sorted(ReadData('院校', ['院校名称', '院校逻辑代码', '更名历史']).data, key=lambda x: len(x[0]), reverse=True):
        school_names = [x[0]]
        if x[2]:
            for school_name_old in loads(x[2]):
                school_names.append(school_name_old)
        for school_name in school_names:
            school_ljdm_dict[school_name] = x[1]
    return school_ljdm_dict

def school_info():
    """
    :return: 返回院校所有相关信息
    """
    # schools = [x[0] for x in ReadData('院校名称').data]
    school_dict = {}
    院校库 = ReadData('院校库')
    for x in 院校库.data:
        school_name = optstr(x[1])
        # x_0_re = re.search(r'\((.+?)\)', school_name)
        # if x_0_re:
        #     old_school_name = x_0_re.group(1)
            # if old_school_name.strip('原') in schools:
            #     school_name = school_name.replace(f'({old_school_name})', '')
            #     school_dict[old_school_name.strip('原')] = x[0]
        school_dict[school_name] = dict(zip(院校库.columns,x))
    return school_dict

def get_major_name(major):
    major_re = re.search('([\u4e00-\u9fa5、]+)',major)
    return major_re.group(1) if major_re else None

def get_name_note(major):
    major_re = re.search('([\u4e00-\u9fa5、]+)(.*)',major)
    return major_re.groups(1) if major_re else [None,None]

def school_names():
    """
    :return: 返回所有院校名称（包含更名和停办）
    """
    names = []
    for x in ReadData('院校', ['院校名称', '更名历史']).data:
        names.append(x[0])
        if x[1]:
            names += loads(x[1])
    return names

major_names = lambda :[x[0] for x in ReadData('专业名称').data]

class GetSchoolNameBz():
    def __init__(self):
        self.school_names = sorted(school_names(), key=lambda x: len(x), reverse=True)
        self.ssq = [x for ssq in get_ssq().values() for x in ssq]

    def __call__(self,v):
        v = v.replace('（', '(').replace('）', ')')
        for school_name in self.school_names:
            if v.startswith(school_name):
                备注 = v.replace(school_name, '', 1) or None
                if 备注:
                    if 备注.startswith('(') and 备注.endswith(')') and '(' not in 备注[1:-1] and ')' not in 备注[1:-1]:
                        备注 = 备注.strip('(').strip(')')
                    # 删除备注中不需要的信息
                    # for 文字 in re.findall('([\u4e00-\u9fa5]+)',备注):
                    #     if any([文字.endswith(x) for x in ('省','市','区','自治州','县')]):
                    #         备注=备注.replace(文字,'')
                    for 文字 in self.ssq+['民办','公办','()','【】','[]']:
                        备注=备注.replace(文字, '')
                return [school_name,备注]
        raise ValueError(f'{v} 字符串中未获取到学校名称')

class GetMajorNameBz():
    def __init__(self):
        self.major_names = sorted(major_names(), key=lambda x: len(x), reverse=True)

    def __call__(self,v):
        v = v.replace('（', '(').replace('）', ')')
        for major_name in self.major_names:
            if v.startswith(major_name):
                备注 = v.replace(major_name, '', 1) or None
                if 备注:
                    if 备注.startswith('(') and 备注.endswith(')') and '(' not in 备注[1:-1] and ')' not in 备注[1:-1]:
                        备注 = 备注.strip('(').strip(')')
                return [major_name,备注]
        raise ValueError(f'{v} 字符串中未获取到专业名称')

class XiuzCode:
    """
    生成修正代码
    """
    def __init__(self,x=1000):
        self.x=x
        self.修正代码_dict = {}
        self.i=1

    def __call__(self,key):
        if key not in self.修正代码_dict:
            self.修正代码_dict[key] = self.x+self.i
            self.i += 1
        return self.修正代码_dict[key]

class YjsMajorInfo:
    """
    获取研究生专业信息
    """
    def __init__(self):
        with MysqlConn('bk179saas') as conn:
            rd = ReadData(conn.select('bk_graduate_major'),['major_name','major_ljdm','major_code','master_type','one_fenlei_dm','one_fenlei','two_fenlei_dm','two_fenlei'],replace_th=False)
            self.专业信息字典 = rd.group('major_name')

    def __call__(self,专业名称):
        """
        return:
            [major_name,major_ljdm,major_code,master_type,one_fenlei,two_fenlei,two_fenlei_dm,one_fenlei_dm]
            [专业名称,专业逻辑代码,专业代码,硕士类型,一级分类代码,一级分类,二级分类代码,二级分类]
        """
        专业信息 = self.专业信息字典.get(专业名称,self.专业信息字典.get('(专业学位)'+专业名称,[[None]*8]))
        return 专业信息[0]

# class BkZkMajorInfo:
#     """
#     获取本专科专业信息
#     """
#     def __init__(self):
#         with MysqlConn('bk179saas') as conn:
#             rd = ReadData(conn.select('bk_major'),['cengci','major_name','major_ljdm','major_code','one_fenlei_dm','one_fenlei','two_fenlei_dm','two_fenlei'],replace_th=False)
#             self.专业信息字典 = rd.group('cengci','major_name')
#
#     def __call__(self,层次,专业名称):
#         """
#         return:
#             [cengci,major_name,major_ljdm,major_code,,one_fenlei,two_fenlei,two_fenlei_dm,one_fenlei_dm]
#             [层次,专业名称,专业逻辑代码,专业代码,一级分类代码,一级分类,二级分类代码,二级分类]
#         """
#         专业信息 = self.专业信息字典.get(层次+','+专业名称,[[None]*8])
#         return 专业信息[0]

def 删除html标签属性(html, want_remove_title=False):
    """
    删除html中的标签除了特定属性以外的所有属性
    :param html: html文本
    :param want_remove_title: 是否删除文章第一个标题所在的标签
    :return: 新的html文本
    """
    soup = BeautifulSoup(html, 'html.parser')

    if want_remove_title:
        # 查找第一个以'h'开头的标签，不区分大小写
        first_h_tag = soup.find(compile(r'^h[1-6]$'))

        if first_h_tag:
            first_h_tag.decompose()  # 使用decompose()方法来移除标签及其内容

    # 遍历所有的标签
    for tag in soup.find_all(True):  # True表示匹配所有标签
        # 删除所有属性
        for attr in list(tag.attrs.keys()):
            if attr not in ['rowspan','colspan','src','alt','href']:#表留合并单元格、链接属性
                del tag.attrs[attr]

    return str(soup)

def 读取图片列表(路径):
    """
    :param 路径: 图片路径或图片所在文件夹路径
    :return: 图片路径列表
    """
    路径 = 路径.strip('"')
    if path.isfile(路径):
        return [路径] if path.splitext(路径)[1].lower() in ['.jpg', '.jpeg', '.png'] else []
    elif path.isdir(路径):
        return [fp.绝对路径 for fp in FileFolderPath(路径).所有文件() if fp.后缀.lower() in ['.jpg', '.jpeg', '.png']]
    else:
        raise ValueError(f"{路径} 既不是文件也不是文件夹")