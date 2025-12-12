#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import decimal

from dbutils.pooled_db import PooledDB
from tqdm import tqdm
import pandas as pd
import numpy as np
import showlog
import pymysql
import time
import copy
import envx
silence_default = True  # 默认静默参数为True
env_file_name_default = 'mysql.env'  # 默认数据库连接环境文件名
reconnect_errors = (ConnectionError, ConnectionAbortedError, TimeoutError, pymysql.err.ProgrammingError)
default_charset = 'utf8'
default_show_sql = False
"""
目前存在部分特殊字符集无法正确保存问题
【待解决问题】
DBUtils下的PersistentDB/PoolDB
https://zhuanlan.zhihu.com/p/174762034
"""


class FastMySQL:
    # # -------- 单例模式 --------
    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     """
    #     单例模式
    #
    #     FastMySQL 类的 _instance 类变量用于存储唯一的实例。
    #     在 __new__ 方法中，首先检查 _instance 是否已经存在实例，
    #     如果不存在，则使用 super() 调用父类的 __new__ 方法创建一个新实例，并将其赋值给 _instance 类变量。
    #     如果已经存在实例，直接返回现有实例，确保只有一个实例存在。
    #
    #     使用单例模式可以有效地避免多次创建相同对象的开销，并确保全局只有一个对象实例，适用于需要共享状态或资源的场景。
    #     """
    #     if not cls._instance:
    #         cls._instance = super(FastMySQL, cls).__new__(cls)
    #         cls._instance.__init__(*args, **kwargs)
    #     return cls._instance
    # # -------- 单例模式 --------

    def __init__(
            self,
            env_file_name: str = env_file_name_default,
            silence: bool = silence_default,
            ssc: bool = False,
            auto_reconnect: bool = True,
            reconnect_wait: int = 5,
            max_connections: int = 1,
            max_shared: int = 0,
            max_cached: int = 5,
            min_cached: int = 2
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
        self.port = self.con_info.get("port", 3306)
        self.charset = self.con_info.get("charset", "utf8mb4")
        self.ssc = ssc
        self.auto_reconnect = auto_reconnect
        self.reconnect_wait = reconnect_wait
        self.POOL = PooledDB(
            creator=pymysql,  # 使用pymysql作为连接器
            maxconnections=max_connections,  # 连接池允许的最大连接数
            maxcached=max_cached,  # 参数用于指定连接池中允许缓存的最大空闲连接数。当连接池中存在多余的连接，并且超过了maxcached限制时，多余的空闲连接将会被关闭和释放，以避免连接池中连接数过多。
            mincached=min_cached,
            maxshared=max_shared,  # 参数用于指定在连接池中可以共享的最大连接数。当多个线程或进程同时请求数据库连接时，如果连接池中存在空闲的连接且未达到maxshared限制，那么这些请求将共享同一个连接，从而减少了连接的创建和销毁开销，提高了性能
            blocking=True,  # 如果连接池为空，getconn方法将会阻塞等待
            setsession=[],
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            charset=self.charset,  # 设置字符集
            autocommit=True,  # 自动提交事务
            cursorclass=pymysql.cursors.DictCursor,  # 返回字典形式的查询结果
            maxusage=100,  # 每个连接的最大使用次数，表示每个连接最多被使用100次。当一个连接被使用次数达到100时，连接会自动关闭，并在以后的请求中重新创建一个新的连接。这样，当连接由于长时间使用而失效时，会自动重连，保证连接的可靠性。
            connect_timeout=10  # 连接数据库的最大超时时间，单位为秒;这表示连接数据库的最大超时时间为10秒。如果在连接数据库时，超过10秒仍然未成功建立连接，连接池会自动重试连接。
        )

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
            sql: str = None,
            sql_list: list = None,
            args=None,
            executemany: bool = False,
            database_name: str = None
    ):
        """
        查询结果以list(dict)形式输出
        [不包含重试机制，需要在外部执行重试]
        :param sql: SELECT * FROM users WHERE username = %s
        :param sql_list:
        :param args: 参数化查询语句避免SQL注入
        :param executemany: 是否批量执行
        :param database_name: 指定数据库名
        :return: {"data": [], "affected_rows": 0}
        """
        retries = 0
        affected_rows = 0
        data = list()
        while True:
            connection = self.POOL.connection()  # 从连接池中获取连接对象
            try:
                with connection.cursor() as cursor:
                    if database_name:
                        cursor.execute(f"USE {database_name};")
                    else:
                        pass

                    if executemany:
                        if sql:
                            cursor.executemany(
                                query=sql,
                                args=args
                            )
                            affected_rows = cursor.rowcount
                            data = cursor.fetchall()
                        elif sql_list:
                            for sql in sql_list:
                                cursor.executemany(
                                    query=sql,
                                    args=args
                                )
                                affected_rows += cursor.rowcount
                                data.extend(cursor.fetchall())
                        else:
                            pass
                    else:
                        if sql:
                            cursor.execute(
                                query=sql,
                                args=args
                            )
                            affected_rows = cursor.rowcount
                            data = cursor.fetchall()
                        elif sql_list:
                            for sql in sql_list:
                                cursor.execute(
                                    query=sql,
                                    args=args
                                )
                                affected_rows += cursor.rowcount
                                data.extend(cursor.fetchall())
                        else:
                            pass
                    return {
                        'data': data,
                        'affected_rows': affected_rows
                    }
            except reconnect_errors:
                retries += 1
                if self.silence:
                    pass
                else:
                    showlog.warning(f'数据库连接失败，将在{self.reconnect_wait}秒后重试第{retries}次...')
                time.sleep(self.reconnect_wait)

            except Exception as e:
                connection.rollback()  # 回滚事务
                raise e
            finally:
                # 将连接对象返还给连接池
                connection.close()

    def query2df(
            self,
            sql: str,
            parameter=None
    ):
        """
        针对数据量较大的情况，将数据存储到pandas的dataframe中
        :param sql:
        :param parameter:
        """
        retries = 0
        while True:
            connection = self.POOL.connection()  # 从连接池中获取连接对象
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query=sql,
                        args=parameter
                    )
                    p_bar = tqdm(cursor.fetchall())
                    result = list()
                    for bar in p_bar:
                        p_bar.set_description_str("==> Downloading data")
                        result.extend(bar)
                    res_ = {
                        'data': pd.DataFrame(result),
                        'affected_rows': cursor.rowcount
                    }
                    return res_
            except reconnect_errors:
                retries += 1
                if self.silence:
                    pass
                else:
                    showlog.warning(f'数据库连接失败，将在{self.reconnect_wait}秒后重试第{retries}次...')
                time.sleep(self.reconnect_wait)

            except Exception as e:
                connection.rollback()  # 回滚事务
                raise e
            finally:
                # 将连接对象返还给连接池
                connection.close()

    def query_table_all_data(
            self,
            db_name: str,  # 必须为内部参数，防止注入
            tb_name: str,  # 必须为内部参数，防止注入
            order_col: str = None,  # 需要排序的列，必须为内部参数，防止注入
            order_index: str = "DESC",  # 排序规则，必须为内部参数，防止注入
    ):
        """
        获取表所有数据
        包含重试机制
        :param db_name: 必须为内部参数，防止注入
        :param tb_name: 必须为内部参数，防止注入
        :param order_col: 需要排序的列，必须为内部参数，防止注入
        :param order_index: 排序规则，必须为内部参数，防止注入
        查询某个表的所有数据
        查询结果以list(dict)形式输出
        """
        if order_col is None:
            sql = f"SELECT * FROM `{db_name}`.`{tb_name}`"
        else:
            sql = f"SELECT * FROM `{db_name}`.`{tb_name}` ORDER BY `{order_col}` {order_index}"

        if not self.silence:
            showlog.info(f"Executing sql：{sql} ...")

        return self.query(
            sql=sql
        )

    def db_names(
            self
    ):
        """
        获取MySQL的连接权限范围内的所有db列表
        """
        sql = "SHOW DATABASES;"
        if not self.silence:
            showlog.info("Executing sql：%s ..." % sql)
        db_names_res = self.query(sql=sql)
        db_names_list = list()
        if db_names_res.get('data'):
            for each in db_names_res.get('data'):
                db_names_list.extend(each.values())
        else:
            pass
        return db_names_list

    def db_table_names(
            self,
            db_name: str
    ):
        """
        获取所有表，若不指定db_name，将获取所有
        【包含重试机制】
        :param db_name: 指定数据库，若不指定，将获取所有
        """

        sql = f"SHOW TABLES FROM `{db_name}`;"
        if not self.silence:
            showlog.info(f"Executing sql：{sql} ...")
        db_table_names_res = self.query(sql=sql)
        db_table_names_list = list()
        if db_table_names_res.get('data'):
            for each in db_table_names_res.get('data'):
                db_table_names_list.extend(each.values())
        else:
            pass
        return db_table_names_list

    def tb_info(
            self,
            db_name: str,
            tb_name: str
    ):
        """
        输出表信息，其中：
        COLUMN_NAME：列名
        DATA_TYPE：数据类型
        【包含重试机制】
        :param db_name:
        :param tb_name:
        """
        where_string = f"TABLE_SCHEMA='{db_name}' and TABLE_NAME='{tb_name}'"
        sql = f"SELECT * FROM `information_schema`.`COLUMNS` WHERE {where_string}"
        tb_info_res = self.query(sql=sql).get('data')
        if tb_info_res:
            return tb_info_res[0]
        else:
            return {}

    def column_list(
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
        column_info = self.column_list(
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
