import json

英文表头对应中文字典 = {'year': '年份', 'school_name': '院校名称', 'school_ljdm': '院校逻辑代码', 'major_name': '专业名称',
    'major_ljdm': '专业逻辑代码', 'gaokaofen': '高考分数', 'paim': '最低分位次', 'kelei': '科类代码',
    'kelei_name': '科类', 'region_name': '省份', 'batch': '批次', 'batch_fen': '批次线', 'batch_dm': '批次代码',
    'school_code': '院校代码', 'major_code': '专业代码', 'major_name_dm': '专业名称(代号)', 'maxfen': '最高分', 'pinfen': '平均分', 'minfen': '最低分',
    'minfenpai': '最低分位次', 'luqushu': '录取数', 'school_dm': '院校逻辑代码', 'major_dm': '专业逻辑代码',
    'group_name': '专业组', 'plan_num': '计划数', 'school_bc': '院校备注', 'xiuz_dm': '院校修正代码',
    'major_xzdm': '专业修正代码', 'cengci': '层次', 'weici': '最低分位次', 'poor': '分差', 'xiuzwei': '修正位次',
    'group_code': '专业组代码', 'group_xzdm': '专业组代码', 'two_fenlei': '二级大类', 'two_fenlei_dm': '二级大类代码',
    'shouxuan': '首选', 'zaixuan': '再选', 'zhaosheng_type': '招生类型', 'zhaosheng_tdm': '招生类型代码',
    'leibie': '类别', 'school_region': '院校所在省份', 'school_city': '院校所在城市', 'banxuexingzhi': '办学性质',
    'tebieshuxin': '特别属性', 'group_plan': '专业组计划数', 'new_plan': '最新一年计划数', 'zhao_plan': '计划数',
    'minfensort': '最低分位次', 'y': 'y值', 'xuezhi': '学制', 'xuefei': '学费',
    'zs_status': '招生状态(1：未招生 0：正常)', 'data_tag': '数据标签', 'tag': '属性标签(如：中外合作)',
    'one_fenlei': '一级大类', 'one_fenlei_dm': '一级大类代码', 'plan_name': '计划性质', 'plan_dm': '计划性质代码',
    'showtab': '展示位置 0：普通批次展示 1：提前批展示 2：都展示', 'batch_xh': '批次排序', 'xuanke': '选科',
    'assist_data_1': '辅助列_1','assist_data_2': '辅助列_2','assist_data_3': '辅助列_3','assist_data_4': '辅助列_4',
    'assist_data_5': '辅助列_5'}

def 英文表头对应中文(英文表头:list):
    return [英文表头对应中文字典.get(x,x) for x in 英文表头]

def 中文表头对应英文(中文表头:list):
    中文表头对应英文字典 = {v:k for k,v in 英文表头对应中文字典.items()}
    return [中文表头对应英文字典.get(x,x) for x in 中文表头]

def save_json(json_data, save_path):
    """保存为json文件
    :param json_data: 要保存的json数据
    """
    with open(save_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def read_json(json_path):
    """读取json文件
    :param json_path: 要读取的json文件路径
    """
    with open(json_path, 'r') as file:
        return json.load(file)

def get_relative_fields(item_fields: str, dict_data: dict):
    """获取相对字段

    :param item_fields:需要获取的字段 例如 "schoolname batch type"
    :param dict_data:字典数据
    :return 获取到的值，list
    """
    return [dict_data.get(item_field) for item_field in item_fields.split(" ")]