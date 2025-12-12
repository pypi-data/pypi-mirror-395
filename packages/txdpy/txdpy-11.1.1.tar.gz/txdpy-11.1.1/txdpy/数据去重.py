# coding=utf-8
import inspect
import os
import sqlite3
import sys
from json import dumps,loads
from typing import Union
from loguru import logger
from re import findall

class CheckDuplicate:
    def __init__(self,key=None):
        """
        :param key: 去重项目名，默认为调用者的py文件名
        """
        if key:
            self.key = dumps(key,ensure_ascii=False)
        else:
            """
            获取调用者的py文件名（不包含路径和后缀），只有在这里调用才能读取到调用者的py文件名
            """
            # 获取当前帧（即get_caller_filename函数所在的帧）
            current_frame = inspect.currentframe()
            # 获取调用者的帧（即调用get_caller_filename函数的帧）
            caller_frame = current_frame.f_back
            # 获取调用者的文件名（完整路径）
            caller_filename = caller_frame.f_code.co_filename
            # 返回调用者的文件名（不包含路径，只包含文件名）
            self.key = os.path.basename(caller_filename).rsplit('.', 1)[0]

        logger.info(f'去重项目名：{self.key}')
        self.key = ''.join(findall("(\w+)", self.key))

        数据库存放目录 = 'python数据去重(勿删).db'
        if os.name == 'nt':
            # 获取当前用户的个人文件夹路径
            user_profile = os.getenv('USERPROFILE')
            数据库存放目录 = os.path.join(user_profile, 'python数据去重(勿删).db')

        # 连接到 SQLite 数据库（如果数据库不存在，则会自动创建）
        self.conn = sqlite3.connect(数据库存放目录)
        # 创建一个游标对象，用于执行 SQL 语句
        self.cursor = self.conn.cursor()
        # 创建表的 SQL 语句
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {self.key} (
            值 TEXT NOT NULL
        );
        '''
        # 执行创建表的 SQL 语句
        self.cursor.execute(create_table_sql)
        # 提交事务（对于创建表等更改数据库结构的操作是必需的）
        self.conn.commit()

        self._读取值列表()

    def _读取值列表(self):
        # 查询数据的 SQL 语句
        select_data_sql = f'SELECT * FROM {self.key}'
        # 执行查询数据的 SQL 语句
        self.cursor.execute(select_data_sql)
        # 获取查询结果
        rows = self.cursor.fetchall()
        # 打印查询结果
        self._值列表 = {row[0] for row in rows}

    def 值列表(self):
        return [loads(x) for x in self._值列表]

    def __call__(self, 值, 是否打印已存在=False):
        """
        :param 值:可以是任何类型
        :param 是否打印已存在:是否在打印已存在值
        """
        return self.是否已存在(值, 是否打印已存在)

    def 是否已存在(self,值,是否打印已存在=False):
        """
        :param 值:可以是任何类型
        :param 是否打印已存在:是否在打印已存在值
        """
        是否已存在 = dumps(值,ensure_ascii=False) in self._值列表
        if 是否打印已存在 and 是否已存在:
            logger.warning(f'值列表已存在该值：{值}')
        return 是否已存在

    def 添加值(self,值):
        """
        :param 值:可以是任何类型
        """
        # 插入数据的 SQL 语句
        insert_data_sql = f'''
        INSERT INTO {self.key} (值) VALUES (?);
        '''
        # 执行插入数据的 SQL 语句
        self.cursor.execute(insert_data_sql, (dumps(值,ensure_ascii=False),))
        # 提交事务（对于插入、更新或删除数据的操作是必需的）
        self.conn.commit()
        self._值列表.add(dumps(值,ensure_ascii=False))

    def 值列表删除值(self,删除值:Union[str,list,tuple,set]):
        """
        :param 删除值:可以是任何类型
                     列表、元组、集合会针对每一个元素进行删除，要把列表、元组、集合当单个值，传入时必须转为字符串
                     其他类型会被当做单个值删除
        """
        # 执行DELETE语句
        if type(删除值) in [list,tuple,set]:
            删除值 = [dumps(x,ensure_ascii=False) for x in 删除值]
            placeholders = ', '.join('?' for _ in 删除值)
            sql = f"DELETE FROM {self.key} WHERE 值 IN ({placeholders});"
            self.cursor.execute(sql, 删除值)
        else:
            sql = f"DELETE FROM {self.key} WHERE 值 = ?;"
            self.cursor.execute(sql, (dumps(删除值,ensure_ascii=False),))
        # 提交事务
        self.conn.commit()
        logger.success(f'值列表删除值：{删除值}，删除成功')

    def 清空值列表(self):
        # 删除表中所有的数据，删除表更快，再重新创建表
        # 执行删除所有数据的 SQL 语句，
        self.cursor.execute(f'DROP TABLE {self.key};')
        # 提交事务（对于插入、更新或删除数据的操作是必需的）
        self.conn.commit()
        # 创建表的 SQL 语句
        create_table_sql = f'''
                CREATE TABLE IF NOT EXISTS {self.key} (
                    值 TEXT NOT NULL
                );
                '''
        # 执行创建表的 SQL 语句
        self.cursor.execute(create_table_sql)
        # 提交事务（对于创建表等更改数据库结构的操作是必需的）
        self.conn.commit()
        logger.success(f'清空值列表：{self.key}，清空成功')

    def 删除值列表(self):
        # 执行删除表 SQL 语句，
        self.cursor.execute(f'DROP TABLE {self.key};')
        # 提交事务（对于插入、更新或删除数据的操作是必需的）
        self.conn.commit()
        logger.success(f'删除值列表：{self.key}，删除成功')
        sys.exit()

    def 查询所有去重项目名称(self):
        # 执行查询以获取所有表名
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        # 获取查询结果
        tables = self.cursor.fetchall()
        # 打印所有表名
        logger.info(dumps([table[0] for table in tables],ensure_ascii=False))

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()