#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from collections import OrderedDict
from tqdm import tqdm
import pandas as pd
import numpy as np
import datetime
import decimal
import showlog
import pymysql
import time
import copy
import envx

silence_default = False  # 默认静默参数为True
show_sql_default = True
env_file_name_default = 'mysql.env'  # 默认数据库连接环境文件名
reconnect_errors = (ConnectionError, ConnectionAbortedError, TimeoutError)
default_charset = 'utf8'
default_show_sql = False
default_reconnect_wait = 60
default_connect_timeout = 60 * 10


class Dict2Object:

    """
    将字典转换为对象
    """

    def __init__(self, dict_input: dict):
        for key, value in dict_input.items():
            setattr(self, key, value)


class QueryGet:
    """
    从query的查询结果中获取数据

    values只有在查询一条数据时才会有
    """
    def __init__(self, cur: pymysql.connect.cursor):
        self.rowcount = cur.rowcount
        self.fetchall = cur.fetchall()
        self.description = cur.description

        if not self.description:
            self.keys = []
        else:
            self.keys = [i[0] for i in cur.description]

        self.data = list()
        self.values = list()
        if len(self.keys) == 1:
            for i in self.fetchall:
                self.data.append(dict(zip(self.keys, i)))
                self.values.append(i[0])
        else:
            for i in self.fetchall:
                self.data.append(dict(zip(self.keys, i)))


class LazyMySQL(object):
    def __init__(
            self,
            env_file_name: str = env_file_name_default,
            silence: bool = silence_default,
            show_sql: bool = show_sql_default,
            ssc: bool = False,
            auto_reconnect: bool = True,
            database: str = None,
            reconnect_wait: int = default_reconnect_wait,
            connect_timeout: int = None
    ):
        self.env_file_name = env_file_name
        self.silence = silence
        self.con_info = self.make_con_info()
        if self.con_info:
            pass
        else:
            if silence:
                pass
            else:
                showlog.warning(':( 连接数据库失败')
            return
        self.host = self.con_info.get("host")
        self.username = self.con_info.get("username")
        self.password = self.con_info.get("password")
        self.database = database
        self.port = self.con_info.get("port", 3306)
        self.charset = self.con_info.get("charset", "utf8mb4")
        self.ssc = ssc
        self.auto_reconnect = auto_reconnect
        self.reconnect_wait = reconnect_wait
        self.connect_timeout = connect_timeout
        self.show_sql = show_sql

        self.con, self.cur = self.connect()

        self.data_to_dict = None

    def connect(self):
        """
        连接数据库，包含重试机制
        """
        while True:
            try:
                if not self.silence:
                    showlog.info(f'User [{self.username}] are trying to connect to the database [{self.database}] ...')
                if not self.connect_timeout:
                    con = pymysql.connect(
                        host=self.host,
                        user=self.username,
                        password=self.password,
                        database=self.database,
                        port=self.port,
                        charset=self.charset
                    )
                else:
                    con = pymysql.connect(
                        host=self.host,
                        user=self.username,
                        password=self.password,
                        database=self.database,
                        port=self.port,
                        charset=self.charset,
                        connect_timeout=self.connect_timeout
                    )
                if self.ssc is False:
                    cur = con.cursor()
                else:
                    cur = pymysql.cursors.SSCursor(con)  # 使用流式游标
                cur.execute(query='SET NAMES utf8mb4')
                cur.execute(query='SET CHARACTER SET utf8mb4')
                cur.execute(query='SET character_set_connection=utf8mb4')
                if not self.silence:
                    showlog.info(':) connection success.')
                return con, cur
            except reconnect_errors:
                if self.auto_reconnect:
                    if not self.silence:
                        showlog.error(f':( connection failed, trying to reconnect in {self.reconnect_wait} seconds ...')
                    time.sleep(self.reconnect_wait)
                else:
                    return
            except:
                if self.auto_reconnect:
                    if not self.silence:
                        showlog.error(f':( connection failed, trying to reconnect in {self.reconnect_wait} seconds ...')
                    time.sleep(self.reconnect_wait)
                else:
                    return

    def make_con_info(
            self
    ):
        """
        读取当前环境的环境文件信息并生成连接信息
        """
        inner_env = envx.read(file_name=self.env_file_name)
        con_info = dict()
        if not inner_env:
            if not self.silence:
                showlog.warning(f'环境文件[ {self.env_file_name} ]不存在！')
        else:
            host = inner_env.get('host')
            if host:
                con_info['host'] = host
            else:
                if not self.silence:
                    showlog.warning('host 未填写，将设置为默认值：localhost')
                con_info['host'] = 'localhost'

            port = inner_env.get('port')
            if port:
                try:
                    con_info['port'] = int(port)
                except:
                    if not self.silence:
                        showlog.warning('port 填写错误，必须为int')
            else:
                if not self.silence:
                    showlog.warning('port 未填写，将设置为默认值：3306')
                con_info['port'] = 3306

            username = inner_env.get('username')
            if username:
                con_info['username'] = username
            else:
                if not self.silence:
                    showlog.warning('username 未填写，将设置为默认值：root')
                con_info['username'] = 'root'

            password = inner_env.get('password')
            if password:
                con_info['password'] = password
            else:
                if not self.silence:
                    showlog.warning('password 未填写，将设置为默认值：空')
                con_info['password'] = ''

            charset = inner_env.get('charset')
            if charset:
                con_info['charset'] = charset
            else:
                con_info['charset'] = default_charset

        return con_info

    def query(
            self,
            sql: str,
            args=None,
            database: str = None,
            commit: bool = False
    ):
        """
        查询结果以list(dict)形式输出

        :param sql: 查询语句，例如：SELECT * FROM users WHERE username = %s

        :param args: Sequence of sequences or mappings. It is used as parameter.
        :type args: tuple or list

        :param database: 指定数据库名，默认为None
        :param commit: False:不提交操作（默认），True:提交操作
        :return: {"data": [], "affected_rows": 0}
        """
        retries = 0
        while True:
            if self.show_sql:
                showlog.info(f"Executing：{sql} ...")
            try:
                if database:
                    self.cur.execute(f"USE {database};")
                if not args:
                    self.cur.execute(
                        query=sql
                    )
                else:
                    self.cur.executemany(
                        query=sql,
                        args=args
                    )
                if commit:
                    self.con.commit()  # 提交操作
                return QueryGet(cur=self.cur)
            except reconnect_errors:
                retries += 1
                if self.silence:
                    pass
                else:
                    showlog.warning(f'数据库连接失败，将在{self.reconnect_wait}秒后重试第{retries}次...')
                time.sleep(self.reconnect_wait)

            except Exception as e:
                self.con.rollback()  # 回滚事务
                raise e

    # def query2df(
    #         self,
    #         sql: str,
    #         parameter=None
    # ):
    #     """
    #     针对数据量较大的情况，将数据存储到pandas的dataframe中
    #     :param sql:
    #     :param parameter:
    #     """
    #     retries = 0
    #     while True:
    #         connection = self.POOL.connection()  # 从连接池中获取连接对象
    #         try:
    #             with connection.cursor() as cursor:
    #                 cursor.execute(
    #                     query=sql,
    #                     args=parameter
    #                 )
    #                 p_bar = tqdm(cursor.fetchall())
    #                 result = list()
    #                 for bar in p_bar:
    #                     p_bar.set_description_str("==> Downloading data")
    #                     result.extend(bar)
    #                 res_ = {
    #                     'data': pd.DataFrame(result),
    #                     'affected_rows': cursor.rowcount
    #                 }
    #                 return res_
    #         except reconnect_errors:
    #             retries += 1
    #             if self.silence:
    #                 pass
    #             else:
    #                 showlog.warning(f'数据库连接失败，将在{self.reconnect_wait}秒后重试第{retries}次...')
    #             time.sleep(self.reconnect_wait)
    #
    #         except Exception as e:
    #             connection.rollback()  # 回滚事务
    #             raise e
    #         finally:
    #             # 将连接对象返还给连接池
    #             connection.close()

    def table_data(
            self,
            database: str,  # 必须为内部参数，防止注入
            table: str,  # 必须为内部参数，防止注入
            order_col: str = None,  # 需要排序的列，必须为内部参数，防止注入
            order_index: str = "DESC",  # 排序规则，必须为内部参数，防止注入
    ):
        """
        获取表所有数据
        :param database: 必须为内部参数，防止注入
        :param table: 必须为内部参数，防止注入
        :param order_col: 需要排序的列，必须为内部参数，防止注入
        :param order_index: 排序规则，必须为内部参数，防止注入
        查询某个表的所有数据
        查询结果以list(dict)形式输出
        """
        if not order_col:
            sql = f"SELECT * FROM `{database}`.`{table}`"
        else:
            sql = f"SELECT * FROM `{database}`.`{table}` ORDER BY `{order_col}` {order_index}"
        return self.query(
            database=database,
            sql=sql
        )

    def show_databases(
            self
    ):
        """
        获取MySQL的连接权限范围内的所有db列表
        """
        sql = "SHOW DATABASES;"
        return self.query(sql=sql)

    def show_tables(
            self,
            database: str = None
    ):
        """
        获取所有表，若不指定database，将获取所有
        :param database: 指定数据库，若不指定，将获取所有
        """
        sql = f"SHOW TABLES FROM `{database}`;"
        return self.query(sql=sql)

    def tb_info(
            self,
            database: str,
            table: str
    ):
        """
        输出表信息，其中：
        COLUMN_NAME：列名
        DATA_TYPE：数据类型
        【包含重试机制】
        :param database:
        :param table:
        """
        where_string = f"TABLE_SCHEMA='{database}' and TABLE_NAME='{table}'"
        sql = f"SELECT * FROM `information_schema`.`COLUMNS` WHERE {where_string}"
        return self.query(sql=sql)

    def columns(
            self,
            db_name: str,
            tb_name: str
    ):
        """
        获取某个表的列信息
        :param db_name:
        :param tb_name:
        """
        sql_all_columns = """
        SELECT
            `COLUMN_NAME` 
        FROM
            `information_schema`.`COLUMNS` 
        WHERE
            `TABLE_SCHEMA` = %s 
            AND `TABLE_NAME` = %s;
        """
        all_columns_res = self.query(
            sql=sql_all_columns,
            args=(db_name, tb_name)
        )
        column_name_list = list()  # 所有列
        if all_columns_res.get('data'):
            for each in all_columns_res.get('data'):
                column_name_list.extend(each.values())

        sql_key_columns = """
        SELECT
            `COLUMN_NAME`
        FROM
            `information_schema`.`KEY_COLUMN_USAGE`
        WHERE
            `TABLE_SCHEMA` = %s
            AND `TABLE_NAME` = %s
        """
        key_columns_res = self.query(
            sql=sql_key_columns,
            args=(db_name, tb_name)
        )
        pk_column_name_list = list()  # 主键列
        if key_columns_res.get('data'):
            for each in key_columns_res.get('data'):
                pk_column_name_list.extend(each.values())

        data_column_name_list = list(
            set(column_name_list).difference(pk_column_name_list)
        )  # 纯数据列
        return {
            'column_list': column_name_list,
            'pk_column_list': pk_column_name_list,
            'data_column_list': data_column_name_list,
        }

    def information_schema(
            self,
            db_name: str,
            tb_name: str
    ):
        """
        输出表信息，其中：
        COLUMN_NAME：列名
        DATA_TYPE：数据类型
        :param db_name:
        :param tb_name:
        """
        where_string = "TABLE_SCHEMA='%s' and TABLE_NAME='%s'" % (db_name, tb_name)
        sql = "SELECT * FROM `information_schema`.`COLUMNS` WHERE %s;" % where_string
        information_schema_res = self.query(
            sql=sql
        )
        if information_schema_res.get('data'):
            return information_schema_res.get('data')[0]
        else:
            return

    def make_query_data(
            self,
            data_dict_list: list,
            db_name: str,
            tb_name: str,
            replace_space_to_none: bool = True,  # 自动将空值null改为None
            sql_head: str = 'REPLACE',
            int64_to_int: bool = True,
            decimal2str: bool = True
    ):
        """
        功能性模块：格式化数据
        :param data_dict_list:
        :param db_name:
        :param tb_name:
        :param replace_space_to_none:
        :param sql_head:
        :param int64_to_int:
        """
        query_sql = None
        query_args = None
        column_info = self.columns(
            db_name=db_name,
            tb_name=tb_name
        )  # 获取列名信息
        if column_info:
            column_list = column_info.get('column_list')
            pk_column_list = column_info.get('pk_column_list')
            data_column_list = column_info.get('data_column_list')

            data_dict_list_temp = copy.deepcopy(data_dict_list)  # 深度拷贝，不更改源数据
            if ('replace' in sql_head.lower()) or ('insert' in sql_head.lower()):
                # 按照目标表的结构格式化data_dict_list，去除额外列的数据，只保留预设列的数据
                # step1: 清洗数据
                operate_param_set = set()
                for each_data_dict in data_dict_list_temp:  # 遍历数据list里的所有dict
                    each_data_dict_copy = copy.deepcopy(each_data_dict)  # 深度拷贝
                    for each_key, each_value in each_data_dict_copy.items():  # 遍历单个dict的所有的key
                        if each_key in column_list:  # 若key在all_col_list中，则收集该key，否则将删除key以及对应的数据，最终得到需要插入数据的列名列表
                            operate_param_set.add(each_key)
                        else:
                            del each_data_dict[each_key]

                # step2: 生成操作语句模板
                operate_param_list = list(operate_param_set)  # 生成插入参数list
                operate_clause_tuple = "`,`".join(operate_param_list)
                insert_data_arg_list = list()
                for _ in operate_param_list:
                    insert_data_arg_list.append("%s")
                data_tuple = ",".join(insert_data_arg_list)
                # 生成插入语句模板
                query_sql = f'{sql_head} INTO `{db_name}`.`{tb_name}`(`{operate_clause_tuple}`) VALUES ({data_tuple})'

                # step3:
                # 生成插入数据tuple
                data_list = list()
                for each_data_dict in data_dict_list_temp:
                    each_data_list = list()
                    for each_data_key in operate_param_list:
                        temp_data = each_data_dict.get(each_data_key)
                        if temp_data == "":
                            if replace_space_to_none is True:
                                each_data_list.append(None)
                            else:
                                each_data_list.append("")
                        else:
                            if isinstance(temp_data, np.int64) and int64_to_int:
                                each_data_list.append(int(temp_data))  # 将Int64转换为int
                            elif isinstance(temp_data, decimal.Decimal) and decimal2str:
                                each_data_list.append(str(temp_data))  # 将decimal转换为str
                            else:
                                each_data_list.append(temp_data)
                    data_list.append(tuple(each_data_list))  # 转换为tuple确保不变
                query_args = list(set(data_list))  # set去重
            elif 'update' in sql_head.lower():
                update_clause_list = list()
                for each_data_dict in data_dict_list_temp:  # 遍历数据list里的所有dict
                    set_clause_list = list()  # set语句列表
                    for each in each_data_dict:  # 遍历单个dict的所有的key
                        if each in data_column_list:  # 若key在all_col_list中，则收集该key，否则将删除key以及对应的数据，最终得到需要更新的列名列表
                            if each_data_dict.get(each) == "" or each_data_dict.get(each) is None:
                                set_clause = "`%s`=%s" % (each, "NULL")
                            else:
                                if isinstance(each_data_dict.get(each), str):
                                    # 这里将'替换为''是为了转义'，规避字符出含'报错
                                    set_clause = "`%s`='%s'" % (each, each_data_dict.get(each).replace("'", "''"))
                                else:
                                    set_clause = "`%s`=%s" % (each, each_data_dict.get(each))
                            set_clause_list.append(set_clause)
                        else:
                            pass
                    set_string = " , ".join(set_clause_list)  # 生成set语句完成

                    # 所有数据的key遍历完成，将开始生成更新的where语句，where条件根据主键列生成
                    where_clause_list = list()
                    for each in pk_column_list:  # 遍历所有主键列
                        if each_data_dict.get(each) == "" or each_data_dict.get(each) is None:
                            pass
                        else:
                            if isinstance(each_data_dict.get(each), str):
                                # 这里将'替换为''是为了转义'，规避字符出含'报错
                                where_clause = "`%s`='%s'" % (each, each_data_dict.get(each).replace("'", "''"))
                            else:
                                where_clause = "`%s`=%s" % (each, each_data_dict.get(each))
                            where_clause_list.append(where_clause)
                    where_string = " AND ".join(where_clause_list)  # 生成where语句完成

                    # where_string生成完成
                    update_clause = f'UPDATE `{db_name}`.`{tb_name}` SET {set_string} WHERE {where_string}'
                    update_clause_list.append(update_clause)
                query_sql = ';\n'.join(update_clause_list)
            else:
                pass
        else:
            pass
        return query_sql, query_args

    def insert(
            self,
            data_dict_list: list,
            db_name: str,
            tb_name: str,
            replace: bool = False,
            insert_ignore: bool = False
    ):
        """
        此模块的功能是插入数据
        replace参数可改为自动更新
        更新一条数据的逻辑是删除1条，再插入1条新的，所以一条更新返回的影响行数是2
        :param data_dict_list:
        :param db_name:
        :param tb_name:
        :param replace: 是否更新
        :param insert_ignore: 在insert时是否添加ignore参数忽略错误，例如主键重复的记录不会被插入
        """
        if not data_dict_list:
            return 0
        else:
            if replace:
                sql_head = 'REPLACE'
            else:
                if insert_ignore:
                    sql_head = 'INSERT IGNORE'
                else:
                    sql_head = 'INSERT'
            query_sql, query_args = self.make_query_data(
                data_dict_list=data_dict_list,
                db_name=db_name,
                tb_name=tb_name,
                sql_head=sql_head
            )
            if query_sql and query_args:
                query_res = self.query(
                    sql=query_sql,
                    args=query_args,
                    executemany=True
                )
                return query_res.get('affected_rows')
            else:
                return 0

    def update(
            self,
            data_dict_list: list,
            db_name: str,
            tb_name: str
    ):
        """
        针对MySQL的数据批量更新方法，不考虑data_dict_list为空或者无数据的情况，仅仅能批量更新，默认where条件是表格的主键，且空值不参与
        先连接目标数据库获取到目标表的结构信息
        :param db_name:需要上传到的目标数据库名称
        :param tb_name:需要上传到的目标数据表名称
        :param data_dict_list:需要上传的数据列表
        :return:
        """
        if not data_dict_list:
            if self.silence:
                pass
            else:
                showlog.warning('未传入有效数据！')
            return 0
        else:
            if self.silence:
                pass
            else:
                showlog.info(f'传入 {len(data_dict_list)} 条数据，处理中...')
            sql_head = 'UPDATE'
            query_sql, query_args = self.make_query_data(
                data_dict_list=data_dict_list,
                db_name=db_name,
                tb_name=tb_name,
                sql_head=sql_head
            )
            if self.silence:
                pass
            else:
                showlog.info(f'处理中完成，执行中...')
            if query_sql:
                sql_list = query_sql.split(';\n')
                query_res = self.query(
                    sql_list=sql_list,
                    executemany=False
                )
                affected_rows = query_res.get('affected_rows')
                if self.silence:
                    pass
                else:
                    showlog.info(f'执行完成，影响记录数：{affected_rows}')
                return affected_rows
            else:
                if self.silence:
                    pass
                else:
                    showlog.warning(f'无需要执行的记录')
                return 0

    def tb_create_sql(
            self,
            db_name: str,
            tb_name: str
    ):
        """
        获取建表语句
        :param db_name:
        :param tb_name:
        """
        sql = f'SHOW CREATE TABLE `{db_name}`.`{tb_name}`;'
        tb_create_sql_res = self.query(
            sql=sql
        )
        if tb_create_sql_res.get('data'):
            return tb_create_sql_res.get('data')[0]['Create Table']
        else:
            return


def make_con_info(
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default
):
    """
    读取当前环境的环境文件信息并生成连接信息
    """
    inner_env = envx.read(file_name=env_file_name)
    if not inner_env:
        if not silence:
            showlog.warning(f'环境文件[ {env_file_name} ]不存在！')
        exit()
    else:
        con_info = dict()

        host = inner_env.get('host')
        if host:
            con_info['host'] = host
        else:
            if not silence:
                showlog.warning('host 未填写，将设置为默认值：localhost')
            con_info['host'] = 'localhost'

        port = inner_env.get('port')
        if port:
            try:
                con_info['port'] = int(port)
            except:
                if not silence:
                    showlog.warning('port 填写错误，必须为int')
                exit()
        else:
            if not silence:
                showlog.warning('port 未填写，将设置为默认值：3306')
            con_info['port'] = 3306

        username = inner_env.get('username')
        if username:
            con_info['username'] = username
        else:
            if not silence:
                showlog.warning('username 未填写，将设置为默认值：root')
            con_info['username'] = 'root'

        password = inner_env.get('password')
        if password:
            con_info['password'] = password
        else:
            if not silence:
                showlog.warning('password 未填写，将设置为默认值：空')
            con_info['password'] = ''

        charset = inner_env.get('charset')
        if charset:
            con_info['charset'] = charset
        else:
            con_info['charset'] = default_charset

        return con_info


def con_mysql(
        host: str,
        username: str,
        password: str,
        db_name: str = None,
        port: int = 3306,
        charset: str = 'utf8',
        ssc: bool = False,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait,
        connect_timeout: int = default_connect_timeout
):
    """
    执行连接数据库
    当连接失败时，将倒计时5秒后重连，直到连接成功
    包含重试机制
    :param host:
    :param db_name:
    :param username:
    :param password:
    :param port: 默认端口为3306
    :param charset: 默认字符集为utf8
    :param ssc: 默认不使用流式游标
    :param silence: 静默模式
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :param connect_timeout: 最大查询时间
    :return:(con, cur)
    """
    while True:
        try:
            if not silence:
                showlog.info(f'User [{username}] are trying to connect to the database [{db_name}] ...')
            con = pymysql.connect(
                host=host,
                db=db_name,
                user=username,
                passwd=password,
                port=port,
                charset=charset,
                connect_timeout=connect_timeout
            )
            if ssc is False:
                cur = con.cursor()
            else:
                cur = pymysql.cursors.SSCursor(con)  # 使用流式游标
            cur.execute(query='SET NAMES utf8mb4')
            cur.execute(query='SET CHARACTER SET utf8mb4')
            cur.execute(query='SET character_set_connection=utf8mb4')
            if not silence:
                showlog.info('ok! connection success.')
            return con, cur
        except reconnect_errors:
            if auto_reconnect:
                if not silence:
                    showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                time.sleep(reconnect_wait)
            else:
                return
        except:
            if auto_reconnect:
                if not silence:
                    showlog.error(f'Oops, connection failed, Trying to reconnect in {reconnect_wait} seconds ...')
                time.sleep(reconnect_wait)
            else:
                return


def con2db(
        con_info: dict,
        db_name: str = None,
        silence: bool = silence_default,
        ssc: bool = False,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    对连接数据库的方法再次优化，此处可以定义所有数据库的连接
    包含重试机制
    :param con_info:设置连接的具体信息，必须包含：host、username、password，可选包含：port、charset
    :param db_name:设置需要连接的数据库
    :param silence:设置静默模式，为True表示静默，为False表示非静默
    :param ssc: 默认不使用流式游标
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :return:connection，由(con, cur)组成，所以返回的效果是(con, cur)
    """
    return con_mysql(
        host=con_info.get("host"),
        db_name=db_name,
        username=con_info.get("username"),
        password=con_info.get("password"),
        port=con_info.get("port", 3306),
        charset=con_info.get("charset", "utf8"),
        ssc=ssc,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )


def close_conn(conn, cursor):
    # 关闭连接
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def _query(
        sql: str,
        cur,
        con=None,
        parameter: list = None,
        operate: bool = False,  # 是否为操作
        order_dict: bool = True,
        silence: bool = silence_default
):
    """
    executemany为True时，sql中的参数以%s的形式出现
    查询结果以list(dict)形式输出
    [不包含重试机制，需要在外部执行重试]
    :param sql: 注意sql中含有%s占位符时，不要加引号
    :param cur:
    :param con:
    :param parameter: 参数化查询语句避免SQL注入list(tuple())
    :param operate: 为True的时候执行操作（执行commit），为False的时候执行查询数据（不执行commit）
    :param order_dict: 返回值是否组成有序dict
    :param silence:设置静默模式，为True表示静默，为False表示非静默
    :return:
    """
    if not parameter:
        cur.execute(query=sql)
    else:
        cur.executemany(query=sql, args=parameter)

    if operate is False:
        # 只查询
        index = cur.description
        result = list()
        for res in cur.fetchall():
            if order_dict is True:
                row = OrderedDict()
            else:
                row = dict()
            for i in range(len(index)):
                row[index[i][0]] = res[i]
            result.append(row)
        return result
    else:
        # 只操作
        effect_rows = cur.rowcount
        con.commit()
        return effect_rows


def query_table_all_data(
        db_name: str,  # 必须为内部参数，防止注入
        tb_name: str,  # 必须为内部参数，防止注入
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        order_col: str = None,  # 需要排序的列，必须为内部参数，防止注入
        order_index: str = "DESC",  # 排序规则，必须为内部参数，防止注入
        silence: bool = silence_default,
        order_dict: bool = True,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    获取表所有数据
    包含重试机制
    :param db_name: 必须为内部参数，防止注入
    :param tb_name: 必须为内部参数，防止注入
    :param con_info: 若指定，将优先使用
    :param env_file_name: 自动重连
    :param order_col: 需要排序的列，必须为内部参数，防止注入
    :param order_index: 排序规则，必须为内部参数，防止注入
    :param silence: 静默参数
    :param order_dict:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    查询某个表的所有数据
    查询结果以list(dict)形式输出
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    try:
        if order_col is None:
            sql = f"SELECT * FROM `{db_name}`.`{tb_name}`"
        else:
            sql = f"SELECT * FROM `{db_name}`.`{tb_name}` ORDER BY `{order_col}` {order_index}"

        if not silence:
            showlog.info(f"Executing sql：{sql} ...")
        while True:
            try:
                res = _query(
                    cur=cur,
                    sql=sql,
                    order_dict=order_dict,
                    silence=silence
                )
                close_conn(conn=con, cursor=cur)  # 关闭连接
                if not silence:
                    showlog.info("Executing sql success.")
                return res
            except reconnect_errors:
                if auto_reconnect:
                    if not silence:
                        showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                    time.sleep(reconnect_wait)
                    con, cur = con2db(
                        con_info=con_info,
                        db_name=db_name,
                        silence=silence,
                        auto_reconnect=auto_reconnect,
                        reconnect_wait=reconnect_wait
                    )  # 已包含重试机制
                else:
                    return
            except pymysql.err.ProgrammingError as pymysql_err:
                err_code, err_msg = pymysql_err.args
                if not silence:
                    showlog.error(err_msg)
                return
            except Exception as ex:
                if not silence:
                    showlog.warning(f"Oops! an error occurred, Exception: {ex}")
                return
    except Exception as ex:
        if not silence:
            showlog.warning(f"Oops! an error occurred, Exception: {ex}")
        return


def query_by_sql(
        sql: str,
        parameter: tuple = None,
        db_name: str = None,
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        order_dict: bool = True,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait,
        show_sql: bool = default_show_sql
):
    """
    按照sql查询
    【包含重试机制】
    :param sql: 参数用%s表示
    :param parameter: 参数化查询避免sql注入
    :param db_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param order_dict:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :param show_sql: 是否显示sql，优先级低于silence
    按照sql查询
    查询结果以list(dict)形式输出
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    try:
        if not silence:
            if show_sql:
                showlog.info(f"Executing sql：{sql} ...")
            else:
                showlog.info(f"Executing sql ...")
        while True:
            try:
                res = _query(
                    cur=cur,
                    sql=sql,
                    parameter=[parameter],
                    order_dict=order_dict,
                    silence=silence
                )
                close_conn(conn=con, cursor=cur)  # 关闭连接
                if not silence:
                    showlog.info("Executing sql success.")
                return res
            except reconnect_errors:
                if auto_reconnect:
                    if not silence:
                        showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                    time.sleep(reconnect_wait)
                    con, cur = con2db(
                        con_info=con_info,
                        db_name=db_name,
                        silence=silence,
                        auto_reconnect=auto_reconnect,
                        reconnect_wait=reconnect_wait
                    )  # 已包含重试机制
                else:
                    return
            except Exception as ex:
                if not silence:
                    showlog.warning("Oops! an error occurred, Exception: %s" % ex)
                return
    except Exception as ex:
        if not silence:
            showlog.warning("Oops! an error occurred, Exception: %s" % ex)
        return


def do_by_sql(
        sql: str,
        parameter: tuple = None,
        db_name: str = None,
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        order_dict: bool = True,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait,
        show_sql: bool = default_show_sql
):
    """
    按照sql执行
    查询结果以list(dict)形式输出
    【包含重试机制】
    :param sql: 参数用%s表示
    :param parameter: 参数化查询避免sql注入
    :param db_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param order_dict:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :param show_sql: 是否显示sql，优先级低于silence
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    if not silence:
        if show_sql:
            showlog.info(f"Executing sql：{sql} ...")
        else:
            showlog.info("Executing sql ...")
    while True:
        try:
            effect_rows = _query(
                sql=sql,
                parameter=[parameter],
                cur=cur,
                con=con,
                operate=True,
                order_dict=order_dict,
                silence=silence
            )
            close_conn(conn=con, cursor=cur)  # 关闭连接
            if not silence:
                showlog.info("Executing sql success.")
            return effect_rows
        except reconnect_errors:
            if auto_reconnect:
                if not silence:
                    showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                time.sleep(reconnect_wait)
                con, cur = con2db(
                    con_info=con_info,
                    db_name=db_name,
                    silence=silence,
                    auto_reconnect=auto_reconnect,
                    reconnect_wait=reconnect_wait
                )  # 已包含重试机制
            else:
                return


def data_bases(
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        order_dict: bool = True,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    获取MySQL的连接权限范围内的所有db列表
    【包含重试机制】
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param order_dict:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    sql = "SHOW DATABASES;"
    if not silence:
        showlog.info("Executing sql：%s ..." % sql)
    while True:
        try:
            res = _query(
                cur=cur,
                sql=sql,
                order_dict=order_dict,
                silence=silence
            )
            close_conn(conn=con, cursor=cur)  # 关闭连接
            if not silence:
                showlog.info("Executing sql success.")
            inner_db_list = list()
            for each in res:
                for k, v in each.items():
                    inner_db_list.append(v)
            return inner_db_list
        except reconnect_errors:
            if auto_reconnect:
                if not silence:
                    showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                time.sleep(reconnect_wait)
                con, cur = con2db(
                    con_info=con_info,
                    silence=silence,
                    auto_reconnect=auto_reconnect,
                    reconnect_wait=reconnect_wait
                )  # 已包含重试机制
            else:
                return
        except Exception as ex:
            if not silence:
                showlog.warning("Oops! an error occurred, Exception: %s" % ex)
            return


def tables(
        db_name: str = None,
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        order_dict: bool = True,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    获取所有表，若不指定db_name，将获取所有
    【包含重试机制】
    :param db_name: 指定数据库，若不指定，将获取所有
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param order_dict:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    sql = "SHOW TABLES;"
    if not silence:
        showlog.info("Executing sql：%s ..." % sql)
    while True:
        try:
            res = _query(
                cur=cur,
                sql=sql,
                order_dict=order_dict,
                silence=silence
            )
            close_conn(conn=con, cursor=cur)  # 关闭连接
            if not silence:
                showlog.info("Executing sql success.")
            table_list = list()
            for each in res:
                for k, v in each.items():
                    table_list.append(v)
            return table_list
        except reconnect_errors:
            if auto_reconnect:
                if not silence:
                    showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                time.sleep(reconnect_wait)
                con, cur = con2db(
                    con_info=con_info,
                    db_name=db_name,
                    silence=silence,
                    auto_reconnect=auto_reconnect,
                    reconnect_wait=reconnect_wait
                )  # 已包含重试机制
            else:
                return
        except Exception as ex:
            if not silence:
                showlog.warning("Oops! an error occurred, maybe query error. Exception: %s" % ex)
            return


def tb_info(
        db_name: str,
        tb_name: str,
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    输出表信息，其中：
    COLUMN_NAME：列名
    DATA_TYPE：数据类型
    【包含重试机制】
    :param db_name:
    :param tb_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    # ---------------- 固定设置 ----------------
    where_string = "TABLE_SCHEMA='%s' and TABLE_NAME='%s'" % (db_name, tb_name)
    sql = "SELECT * FROM `information_schema`.`COLUMNS` WHERE %s" % where_string
    res = query_by_sql(
        sql=sql,
        con_info=con_info,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait,
        silence=silence
    )
    return res


def column_list(
        db_name: str,
        tb_name: str,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        order_dict: bool = True,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    【包含重试机制】
    :param db_name:
    :param tb_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param order_dict:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    while True:
        try:
            sql1 = """
            SELECT
                `COLUMN_NAME` 
            FROM
                `information_schema`.`COLUMNS` 
            WHERE
                `TABLE_SCHEMA` = %s 
                AND `TABLE_NAME` = %s;
            """
            all_col_dict = _query(
                cur=cur,
                sql=sql1,
                parameter=[(db_name, tb_name)],
                order_dict=order_dict,
                silence=silence
            )
            all_col_list = list()
            for each in all_col_dict:
                all_col_list.append(each.get("COLUMN_NAME"))
            sql2 = """
            SELECT
                `COLUMN_NAME` 
            FROM
                `information_schema`.`KEY_COLUMN_USAGE` 
            WHERE
                `TABLE_SCHEMA` = %s 
                AND `TABLE_NAME` = %s
            """
            pk_col_dict = _query(
                cur=cur,
                sql=sql2,
                parameter=[(db_name, tb_name)],
                order_dict=order_dict,
                silence=silence
            )
            pk_col_list = list()
            for each in pk_col_dict:
                pk_col_list.append(each.get("COLUMN_NAME"))
            data_col_list = all_col_list.copy()
            for each in pk_col_list:
                try:
                    data_col_list.remove(each)
                except:
                    pass
            close_conn(conn=con, cursor=cur)  # 关闭连接
            return all_col_list, pk_col_list, data_col_list
        except reconnect_errors:
            if auto_reconnect:
                if not silence:
                    showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                time.sleep(reconnect_wait)
                con, cur = con2db(
                    con_info=con_info,
                    db_name=db_name,
                    silence=silence,
                    auto_reconnect=auto_reconnect,
                    reconnect_wait=reconnect_wait
                )  # 已包含重试机制
            else:
                return
        except Exception as ex:
            showlog.warning("Oops! an error occurred in column_list, Exception: %s" % ex)
            return


def query_to_pd(
        sql: str,
        db_name: str = None,
        parameter=None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait,
        show_sql: bool = default_show_sql
):
    """
    针对数据量较大的情况，将数据存储到pd中
    【包含重试机制】
    :param sql:
    :param db_name:
    :param parameter:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :param show_sql: 是否显示sql，优先级低于silence
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    try:
        cur.execute(query=sql, args=parameter)
        index = cur.description
        columns = list()
        for each in index:
            columns.append(each[0])
        result = list()
        p_bar = tqdm(cur.fetchall())
        for res in p_bar:
            p_bar.set_description_str("==> Downloading data")
            row = dict()
            for i in range(len(index)):
                row[index[i][0]] = res[i]
            result.append(row)
        close_conn(conn=con, cursor=cur)  # 关闭连接
        return pd.DataFrame(result)
    except:
        showlog.warning("Oops! an error occurred in query, sql: %s" % sql)
        return


def information_schema(
        db_name: str,
        table_name: str,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    输出表信息，其中：
    COLUMN_NAME：列名
    DATA_TYPE：数据类型
    【包含重试机制】
    :param db_name:
    :param table_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    # ---------------- 固定设置 ----------------
    where_string = "TABLE_SCHEMA='%s' and TABLE_NAME='%s'" % (db_name, table_name)
    sql = "SELECT * FROM `information_schema`.`COLUMNS` WHERE %s;" % where_string
    res = query_by_sql(
        sql=sql,
        con_info=con_info,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait,
        silence=silence
    )
    return res


def clean_data(
        data_dict_list: list,
        column_info_dict: dict,
        db_name: str,
        tb_name: str,
        replace_space_to_none: bool = True,  # 自动将空值null改为None
        operate: str = "REPLACE",
        ignore: bool = False
):
    """
    功能性模块
    格式化数据
    :param data_dict_list:
    :param column_info_dict:
    :param db_name:
    :param tb_name:
    :param replace_space_to_none:
    :param operate:
    :param ignore:
    """
    data_dict_list_temp = copy.deepcopy(data_dict_list)  # 深度拷贝，不更改源数据
    all_col_list = column_info_dict.get('all_col_list')  # 所有列名

    # 按照目标表的结构格式化data_dict_list，去除额外列的数据，只保留预设列的数据
    # step1: 清洗数据
    operate_param_set = set()
    for each_data_dict in data_dict_list_temp:  # 遍历数据list里的所有dict
        each_data_dict_copy = copy.deepcopy(each_data_dict)
        for each_key, each_value in each_data_dict_copy.items():  # 遍历单个dict的所有的key
            if each_key in all_col_list:  # 若key在all_col_list中，则收集该key，否则将删除key以及对应的数据，最终得到需要插入数据的列名列表
                operate_param_set.add(each_key)
            else:
                del each_data_dict[each_key]

    # step2: 生成操作语句模板
    operate_param_list = list(operate_param_set)  # 生成插入参数list
    operate_clause_tuple = "`,`".join(operate_param_list)
    insert_data_arg_list = list()
    for _ in operate_param_list:
        insert_data_arg_list.append("%s")
    data_tuple = ",".join(insert_data_arg_list)
    # 生成插入语句模板
    if operate.upper() == 'REPLACE':
        operate_clause = "REPLACE INTO `%s`.`%s`(`%s`) VALUES(%s)" % (db_name, tb_name, operate_clause_tuple, data_tuple)
    elif operate.upper() == 'INSERT':
        if ignore:
            operate_clause = "INSERT IGNORE INTO `%s`.`%s`(`%s`) VALUES(%s)" % (db_name, tb_name, operate_clause_tuple, data_tuple)
        else:
            operate_clause = "INSERT INTO `%s`.`%s`(`%s`) VALUES(%s)" % (db_name, tb_name, operate_clause_tuple, data_tuple)
    else:
        return

    # step3:
    # 生成插入数据tuple
    data_list = list()
    for each_data_dict in data_dict_list_temp:
        each_data_list = list()
        for each_data_key in operate_param_list:
            temp_data = each_data_dict.get(each_data_key)
            if temp_data == "":
                if replace_space_to_none is True:
                    each_data_list.append(None)
                else:
                    each_data_list.append("")
            else:
                if isinstance(temp_data, np.int64):
                    each_data_list.append(str(temp_data))  # 将 Int64 转换为str
                # elif np.isnan(temp_data):
                #     each_data_list.append(None)  # 将 nan 转换为 None
                elif isinstance(temp_data, decimal.Decimal):
                    each_data_list.append(str(temp_data))  # 将 decimal 转换为str
                elif isinstance(temp_data, datetime.datetime) or isinstance(temp_data, datetime.date):
                    each_data_list.append(str(temp_data))  # 将 datetime/date 转换为str
                elif isinstance(temp_data, list):
                    each_data_list.append(str(temp_data))  # 将 list 转换为str
                else:
                    each_data_list.append(temp_data)
        data_list.append(tuple(each_data_list))  # 转换为tuple确保不变
    data_list_single = list(set(data_list))  # set去重
    return operate_clause, data_list_single


def replace_into(
        data_dict_list: list,
        db_name: str,
        tb_name: str,
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        pk_col_list: list = None,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    插入和自动更新，注意，这里的更新是先对原来的数据删除，再插入，不适用于局部更新！
    【包含重试机制】
    :param data_dict_list: 数据[{},{}]
    :param db_name: 数据库名
    :param tb_name: 表名
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param pk_col_list: 主键列表
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    if not data_dict_list:
        return True
    else:
        try:
            column_info = column_list(
                db_name=db_name,
                tb_name=tb_name,
                con_info=con_info,
                auto_reconnect=auto_reconnect,
                reconnect_wait=reconnect_wait,
                silence=silence
            )  # 获取列名信息
            if column_info:  # 若未获取到列名信息，提示错误并退出
                all_col_list, pk_col_list_get, data_col_list = column_info  # 获取到列名信息
                column_info_dict = {
                    'all_col_list': all_col_list,
                    'data_col_list': data_col_list,
                }
                if pk_col_list:
                    column_info_dict['pk_col_list'] = pk_col_list  # 使用自定义主键列表
                else:
                    column_info_dict['pk_col_list'] = pk_col_list_get  # 使用数据库中定义的主键列表

                operate_clause, data_list_single = clean_data(
                    column_info_dict=column_info_dict,
                    data_dict_list=data_dict_list,
                    db_name=db_name,
                    tb_name=tb_name,
                    operate="REPLACE"
                )
                while True:
                    try:
                        if not silence:
                            showlog.info('operating %s data...' % len(data_list_single))
                        cur.executemany(query=operate_clause, args=list(data_list_single))
                        con.commit()
                        if not silence:
                            showlog.info("operate success.")
                        close_conn(conn=con, cursor=cur)  # 关闭连接
                        return True
                    except reconnect_errors:
                        if auto_reconnect:
                            if not silence:
                                showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                            time.sleep(reconnect_wait)
                            con, cur = con2db(
                                con_info=con_info,
                                db_name=db_name,
                                silence=silence,
                                auto_reconnect=auto_reconnect,
                                reconnect_wait=reconnect_wait
                            )  # 已包含重试机制
                        else:
                            return
                    except:
                        if not silence:
                            showlog.error("operate failure.operate_clause: %s" % operate_clause)
                            print(operate_clause, list(data_list_single)[0])
                        return False
            else:
                if not silence:
                    showlog.warning("Oops! can't get column_info.")
                return False
        except:
            if not silence:
                showlog.error("Oops! an error occurred!")
            return False


def insert(
        data_dict_list: list,
        db_name: str,
        tb_name: str,
        con_info: dict = None,
        env_file_name: str = env_file_name_default,
        replace_space_to_none: bool = True,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait,
        ignore: bool = False,
        str_f: str = None
):
    """
    此模块的功能是插入和自动更新
    【包含重试机制】
    :param data_dict_list:
    :param db_name:
    :param tb_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param replace_space_to_none: 自动将空值null改为None
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :param ignore: 忽略错误，例如主键重复的记录不会被插入
    :param str_f: 时间或者日期格式，例如 %Y-%m-%d %H:%M:%S
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    try:
        # 获取列名信息
        column_info = column_list(
            db_name=db_name,
            tb_name=tb_name,
            con_info=con_info,
            auto_reconnect=auto_reconnect,
            reconnect_wait=reconnect_wait,
            silence=silence
        )
        if column_info:  # 若未获取到列名信息，提示错误并退出
            all_col_list, pk_col_list, data_col_list = column_info  # 获取到列名信息
            # 按照目标表的结构格式化data_dict_list，去除额外列的数据，只保留预设列的数据
            insert_param_set = set()
            for each_data_dict in data_dict_list:  # 遍历数据list里的所有dict
                each_data_dict_in = each_data_dict.copy()  # 复制一份避免发生更改dict的错误
                for each in each_data_dict_in:  # 遍历单个dict的所有的key
                    if each in all_col_list:  # 若key在all_col_list中，则收集该key，否则将删除key以及对应的数据，最终得到需要插入数据的列名列表
                        insert_param_set.add(each)
                    else:
                        del each_data_dict[each]

            insert_param_list = list(insert_param_set)  # 生成插入参数list
            insert_clause_tuple = "`,`".join(insert_param_list)
            insert_data_arg_list = list()
            for _ in insert_param_list:
                insert_data_arg_list.append("%s")
            insert_data_tuple = ",".join(insert_data_arg_list)
            # 生成插入语句模板
            if ignore:
                insert_clause = f'INSERT IGNORE INTO `{db_name}`.`{tb_name}`(`{insert_clause_tuple}`) VALUES({insert_data_tuple})'
            else:
                insert_clause = f'INSERT INTO `{db_name}`.`{tb_name}`(`{insert_clause_tuple}`) VALUES({insert_data_tuple})'

            # 生成插入数据tuple
            insert_data_list = list()
            for each_data_dict in data_dict_list:
                each_insert_data_list = list()
                for each_data_key in insert_param_list:
                    each_data_value = each_data_dict.get(each_data_key)
                    if each_data_value == "":
                        if replace_space_to_none is True:
                            each_insert_data_list.append(None)
                        else:
                            each_insert_data_list.append("")
                    elif isinstance(each_data_value, datetime.datetime):
                        # 将datetime转化为字符串插入
                        if str_f:
                            each_insert_data_list.append(each_data_value.strftime(str_f))
                        else:
                            each_insert_data_list.append(str(each_data_value))
                    elif isinstance(each_data_value, datetime.date):
                        # 将date转化为字符串插入
                        if str_f:
                            each_insert_data_list.append(each_data_value.strftime(str_f))
                        else:
                            each_insert_data_list.append(str(each_data_value))
                    else:
                        each_insert_data_list.append(each_data_value)
                insert_data_list.append(tuple(each_insert_data_list))

            insert_data_list = set(insert_data_list)  # set去重

            while True:
                try:
                    if not silence:
                        showlog.info('Inserting %s data...' % len(insert_data_list))
                    cur.executemany(query=insert_clause, args=list(insert_data_list))
                    con.commit()
                    if not silence:
                        showlog.info("Insert success.")
                    close_conn(conn=con, cursor=cur)  # 关闭连接
                    return True
                except pymysql.err.ProgrammingError:
                    # 这里对这种错误单独处理，可能是网络不稳定导致的，当然也可能是语句本身的问题
                    this_reconnect_wait = 1
                    if auto_reconnect:
                        if not silence:
                            showlog.error(f'Oops, pymysql.err.ProgrammingError, Trying to reconnect in {this_reconnect_wait} seconds ...')
                        time.sleep(this_reconnect_wait)
                        con, cur = con2db(
                            con_info=con_info,
                            db_name=db_name,
                            silence=silence,
                            auto_reconnect=auto_reconnect,
                            reconnect_wait=this_reconnect_wait
                        )  # 已包含重试机制
                    else:
                        return
                except reconnect_errors:
                    if auto_reconnect:
                        if not silence:
                            showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                        time.sleep(reconnect_wait)
                        con, cur = con2db(
                            con_info=con_info,
                            db_name=db_name,
                            silence=silence,
                            auto_reconnect=auto_reconnect,
                            reconnect_wait=reconnect_wait
                        )  # 已包含重试机制
                    else:
                        return
                except:
                    if not silence:
                        showlog.error("Insert failure. insert_clause: %s" % insert_clause)
                        print(insert_clause, list(insert_data_list)[0])
                    return False
        else:
            if not silence:
                showlog.warning("Oops! can't get column_info.")
            return False
    except:
        if not silence:
            showlog.error("Oops! an error occurred!")
        return False


def update(
        data_dict_list: list,
        db_name: str,
        tb_name: str,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    针对MySQL的数据批量更新方法，不考虑data_dict_list为空或者无数据的情况，仅仅能批量更新，默认where条件是表格的主键，且空值不参与
    先连接目标数据库获取到目标表的结构信息
    【包含重试机制】
    :param silence:设置上传的时候是否有提示信息
    :param con_info:连接信息
    :param env_file_name:设置连接数据库的信息
    :param db_name:需要上传到的目标数据库名称
    :param tb_name:需要上传到的目标数据表名称
    :param data_dict_list:需要上传的数据列表
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    :return:
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    con, cur = con2db(
        con_info=con_info,
        db_name=db_name,
        silence=silence,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait
    )  # 已包含重试机制
    # ---------------- 固定设置 ----------------
    try:
        # 获取列名信息
        column_info = column_list(
            db_name=db_name,
            tb_name=tb_name,
            con_info=con_info,
            auto_reconnect=auto_reconnect,
            reconnect_wait=reconnect_wait,
            silence=silence
        )
        if column_info is not None:  # 若未获取到列名信息，提示错误并推出
            all_col_list, pk_col_list, data_col_list = column_info  # 获取到列名信息
            # 按照目标表的结构格式化data_dict_list，去除额外列的数据，只保留预设列的数据
            while True:
                try:
                    for each_data_dict in data_dict_list:  # 遍历数据list里的所有dict

                        set_clause_list = list()  # set语句列表
                        for each in each_data_dict:  # 遍历单个dict的所有的key
                            if each in data_col_list:  # 若key在all_col_list中，则收集该key，否则将删除key以及对应的数据，最终得到需要更新的列名列表
                                if each_data_dict.get(each) == "" or each_data_dict.get(each) is None:
                                    set_clause = "`%s`=%s" % (each, "NULL")
                                else:
                                    if isinstance(each_data_dict.get(each), str):
                                        # 这里将'替换为''是为了转义'，规避字符出含'报错
                                        set_clause = "`%s`='%s'" % (each, each_data_dict.get(each).replace("'", "''"))
                                    else:
                                        set_clause = "`%s`=%s" % (each, each_data_dict.get(each))
                                set_clause_list.append(set_clause)
                            else:
                                pass
                        set_string = " , ".join(set_clause_list)  # 生成set语句完成

                        # 所有数据的key遍历完成，将开始生成更新的where语句，where条件根据主键列生成
                        where_clause_list = list()
                        for each in pk_col_list:  # 遍历所有主键列
                            if each_data_dict.get(each) == "" or each_data_dict.get(each) is None:
                                pass
                            else:
                                if isinstance(each_data_dict.get(each), str):
                                    # 这里将'替换为''是为了转义'，规避字符出含'报错
                                    where_clause = "`%s`='%s'" % (each, each_data_dict.get(each).replace("'", "''"))
                                else:
                                    where_clause = "`%s`=%s" % (each, each_data_dict.get(each))
                                where_clause_list.append(where_clause)
                        where_string = " AND ".join(where_clause_list)  # 生成where语句完成

                        # where_string生成完成
                        update_clause = f'UPDATE `{db_name}`.`{tb_name}` SET {set_string} WHERE {where_string}'
                        # print(update_clause)
                        cur.execute(query=update_clause)
                    commit_res = con.commit()
                    close_conn(conn=con, cursor=cur)  # 关闭连接
                    return commit_res
                except reconnect_errors:
                    if auto_reconnect:
                        if not silence:
                            showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                        time.sleep(reconnect_wait)
                        con, cur = con2db(
                            con_info=con_info,
                            db_name=db_name,
                            silence=silence,
                            auto_reconnect=auto_reconnect,
                            reconnect_wait=reconnect_wait
                        )  # 已包含重试机制
                    else:
                        return
                except:
                    if not silence:
                        showlog.error("Update failure with update_clause: %s" % update_clause)
                    return
        else:
            if not silence:
                showlog.warning("Oops! can't get column_info.")
            return
    except:
        if not silence:
            showlog.error("Oops! an error occurred!")
        return


def show_create_table(
        db_name: str,
        tb_name: str,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    获取建表语句
    【包含重试机制】
    :param db_name:
    :param tb_name:
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    # ---------------- 固定设置 ----------------
    sql = 'SHOW CREATE TABLE `%s`.`%s`;' % (db_name, tb_name)
    res = query_by_sql(
        db_name=db_name,
        sql=sql,
        env_file_name=env_file_name,
        con_info=con_info,
        auto_reconnect=auto_reconnect,
        reconnect_wait=reconnect_wait,
        silence=silence
    )
    if res:
        return res[0]['Create Table']
    else:
        return


def save_as_sql(
        db_name: str,
        tb_name: str,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait
):
    """
    类似于Navicat的转储sql功能
    """
    import datetime
    import decimal
    # ---------------- 固定设置 ----------------
    if not con_info:
        con_info = make_con_info(
            env_file_name=env_file_name,
            silence=silence
        )
    # ---------------- 固定设置 ----------------
    SourceServerVersion = query_by_sql(
        sql='SELECT @@version;',
        env_file_name=env_file_name,
        silence=silence
    )[0]['@@version']  # 获取源服务器版本

    SourceHost = f"{con_info.get('host')}:{con_info.get('port')}"

    charset = query_by_sql(
        sql=f"SELECT `DEFAULT_CHARACTER_SET_NAME` FROM `information_schema`.`SCHEMATA` WHERE `schema_name` = '{db_name}';",
        env_file_name=env_file_name,
        silence=silence
    )[0]['DEFAULT_CHARACTER_SET_NAME']  # 获取数据库的charset

    tb_create_sql = show_create_table(
        db_name=db_name,
        tb_name=tb_name,
        env_file_name=env_file_name,
        silence=silence
    )

    data = query_table_all_data(
        db_name=db_name,
        tb_name=tb_name,
        env_file_name=env_file_name,
        silence=silence
    )
    if data:
        insert_sql_list = list()
        for each_data in data:
            key_list = list()
            # value_list = list()
            value_str = ''
            for data_key, data_value in each_data.items():
                key_list.append(data_key)
                if data_value:
                    if isinstance(data_value, int):
                        value_str += f"{data_value},"
                    elif isinstance(data_value, decimal.Decimal):
                        value_str += f"{data_value},"
                    elif isinstance(data_value, float):
                        value_str += f"{data_value},"
                    else:
                        value_str += f"'{str(data_value)}',"
                    # value_list.append(str(data_value))
                else:
                    value_str += f"NULL,"
                    # value_list.append(str(data_value))
            key_str = "`,`".join(key_list)
            # value_str = "','".join(value_list)
            value_str = value_str[:-1]
            each_insert_sql = f"INSERT INTO `{tb_name}` (`{key_str}`) VALUES ({value_str});"
            insert_sql_list.append(each_insert_sql)
        insert_sql_str = '\n'.join(insert_sql_list)
    else:
        insert_sql_str = ''

    content = f"""
/*
 fastmysql Data Transfer
 auther: ZeroSeeker
 email: ZeroSeeker@foxmail.com

 Source Server         : /
 Source Server Type    : MySQL
 Source Server Version : {SourceServerVersion}
 Source Host           : {SourceHost}
 Source Schema         : {db_name}

 Target Server Type    : MySQL
 Target Server Version : {SourceServerVersion}
 File Encoding         : 65001

 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
*/

SET NAMES {charset};
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for {tb_name}
-- ----------------------------
DROP TABLE IF EXISTS `{tb_name}`;
{tb_create_sql};

-- ----------------------------
-- Records of {tb_name}
-- ----------------------------
BEGIN;
{insert_sql_str}
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

    """
    return content


def db_exist(
        db_name: str,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
):
    """
    判断数据库是否存在
    """
    check_sql = f"select 1 from `information_schema`.`schemata`  where schema_name='{db_name}';"
    check_res = query_by_sql(
        sql=check_sql,
        db_name='information_schema',
        env_file_name=env_file_name,
        silence=silence
    )
    if check_res:
        return True
    else:
        return False


def tb_exist(
        tb_name: str,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
):
    """
    判断表是否存在
    """
    check_sql = f"select 1 from `information_schema`.`tables`  where table_name='{tb_name}';"
    check_res = query_by_sql(
        sql=check_sql,
        db_name='information_schema',
        env_file_name=env_file_name,
        silence=silence
    )
    if check_res:
        return True
    else:
        return False


def db_tb_exist(
        db_name: str,
        tb_name: str,
        env_file_name: str = env_file_name_default,
        silence: bool = silence_default,
):
    """
    判断数据库的表是否存在
    """
    check_sql = f"select 1 from `information_schema`.`tables`  where table_schema='{db_name}' and table_name='{tb_name}';"
    check_res = query_by_sql(
        sql=check_sql,
        db_name='information_schema',
        env_file_name=env_file_name,
        silence=silence
    )
    if check_res:
        return True
    else:
        return False


def upload(
        data: list,
        target_database: str,
        target_table: str,
        replace: bool = False,
        ignore: bool = False,
        env_file_name: str = env_file_name_default,
        pk_col_list: list = None,
        silence: bool = silence_default,
        auto_reconnect: bool = True,
        reconnect_wait: int = default_reconnect_wait,
        con_info: dict = None,
):
    """
    上传数据，合成了insert和replace两种方法
    插入和自动更新，注意，这里的更新是先对原来的数据删除，再插入，不适用于局部更新！
    【包含重试机制】
    :param data: 数据[{},{}]
    :param target_database: 数据库名
    :param target_table: 表名
    :param replace: 是否使用replace，若为False，将使用insert
    :param ignore: 只有在insert时才会生效
    :param con_info: 若指定，将优先使用
    :param env_file_name:
    :param pk_col_list: 主键列表
    :param silence:
    :param auto_reconnect: 自动重连
    :param reconnect_wait: 重连等待时间，单位为秒，默认为5秒
    """
    try:
        # ---------------- 固定设置 ----------------
        if not con_info:
            con_info = make_con_info(
                env_file_name=env_file_name,
                silence=silence
            )
        con, cur = con2db(
            con_info=con_info,
            db_name=target_database,
            silence=silence,
            auto_reconnect=auto_reconnect,
            reconnect_wait=reconnect_wait
        )  # 已包含重试机制
        # ---------------- 固定设置 ----------------
        if not data:
            return True
        else:
            column_info = column_list(
                db_name=target_database,
                tb_name=target_table,
                con_info=con_info,
                auto_reconnect=auto_reconnect,
                reconnect_wait=reconnect_wait,
                silence=silence
            )  # 获取列名信息
            if column_info:  # 若未获取到列名信息，提示错误并退出
                all_col_list, pk_col_list_get, data_col_list = column_info  # 获取到列名信息
                column_info_dict = {
                    'all_col_list': all_col_list,
                    'data_col_list': data_col_list,
                }
                if pk_col_list:
                    column_info_dict['pk_col_list'] = pk_col_list  # 使用自定义主键列表
                else:
                    column_info_dict['pk_col_list'] = pk_col_list_get  # 使用数据库中定义的主键列表
                if replace:
                    operate = "REPLACE"
                else:
                    operate = "INSERT"
                operate_clause, data_list_single = clean_data(
                    column_info_dict=column_info_dict,
                    data_dict_list=data,
                    db_name=target_database,
                    tb_name=target_table,
                    operate=operate,
                    ignore=ignore
                )
                while True:
                    try:
                        if not silence:
                            showlog.info('operating %s data...' % len(data_list_single))
                        cur.executemany(query=operate_clause, args=list(data_list_single))
                        rows = cur.rowcount
                        con.commit()
                        if not silence:
                            showlog.info("operate success.")
                        close_conn(conn=con, cursor=cur)  # 关闭连接
                        return rows
                    except reconnect_errors:
                        if auto_reconnect:
                            if not silence:
                                showlog.error(f'Oops, reconnect_errors, Trying to reconnect in {reconnect_wait} seconds ...')
                            time.sleep(reconnect_wait)
                            con, cur = con2db(
                                con_info=con_info,
                                db_name=target_database,
                                silence=silence,
                                auto_reconnect=auto_reconnect,
                                reconnect_wait=reconnect_wait
                            )  # 已包含重试机制
                        else:
                            return False
                    except:
                        if not silence:
                            showlog.error("operate failure.operate_clause: %s" % operate_clause)
                            print(operate_clause, list(data_list_single)[0])
                        return False
            else:
                if not silence:
                    showlog.warning("Oops! can't get column_info.")
                return False
    except:
        if not silence:
            showlog.error("Oops! an error occurred!")
        return False


def upload_shard(
        data: list,
        target_database: str,
        target_table: str,
        shard_mark: str,
        shard_sql: str,
        replace: bool = False,
        ignore: bool = False,

        env_file_name: str = env_file_name_default,
        shard_table_replace_str: str = '__shard_table_replace_str__',
        silence: bool = False,
        show_sql: bool = True,
        drop_before_create: bool = False
):
    """
    上传数据到shard（分表）
    自动检查创建shard表并存入数据

    :param data: 需要上传的数据，形如：[{},{}]
    :param target_database: 数据库名
    :param target_table: 表名
    :param shard_mark: 分表标记，加在target_table的后面，中间以_分隔，例如20230101，最终的表为target_table_20230101
    :param shard_sql: 分表的建表sql
    :param replace: 是否使用replace，若为False，将使用insert
    :param ignore: 只有在insert时才会生效

    :param env_file_name: 环境文件名，默认为mysql.env
    :param shard_table_replace_str: 建表语句的数据表名替换字符，默认为__shard_table_replace_str__
    :param silence:
    :param show_sql:
    :param drop_before_create: True：上传之前先删除后建表，False：不删除，直接建表
    :return:
    """
    shard_table = f"{target_table}_{shard_mark}"  # 分片表名
    if drop_before_create:
        # 先删除，再建表
        do_by_sql(
            sql=f'DROP TABLE {target_database}.{shard_table}',
            db_name=target_database,
            env_file_name=env_file_name,
            silence=silence,
            show_sql=show_sql
        )
    else:
        pass

    if not silence:
        showlog.info(f'正在创建表 [{shard_table}] ...')
    do_by_sql(
        sql=shard_sql.replace(shard_table_replace_str, shard_table),
        db_name=target_database,
        env_file_name=env_file_name,
        silence=silence,
        show_sql=show_sql
    )
    if not silence:
        showlog.info(f'正在向表[{shard_table}]存储数据...')
    return upload(
        data=data,
        target_database=target_database,
        target_table=shard_table,
        env_file_name=env_file_name,
        silence=silence,
        replace=replace,
        ignore=ignore
    )
