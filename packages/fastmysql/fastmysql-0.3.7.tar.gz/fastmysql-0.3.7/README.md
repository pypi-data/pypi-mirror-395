# fastmysql
![](https://img.shields.io/badge/Python-3.8.6-green.svg)

#### 介绍
简单快速的使用mysql

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip3 install fastmysql
```
2.  pip安装（使用淘宝镜像加速）
```shell script
pip3 install fastmysql -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import fastmysql
query_res = fastmysql.query_table_all_data(
    db_name='test', 
    tb_name='test'
)

# 获取建表语句
res = fastmysql.show_create_table(
    db_name='test',
    tb_name='test'
)
```

2.  防止sql注入：
写法

cursor.execute('insert into user (name,password) value (?,?)',(name,password))
　　或者

cursor.execute('insert into user (name,password) value (%s,%s)',(name,password))
　　%s与?都可以作为sql语句的占位符，它们作为占位符的功能是没有区别的，mysql.connector用 %s 作为占位符；pymysql用 ? 作为占位符。但是注意不要写成

cursor.execute('insert into user (name,password) value (?,?)'%(name,password))
　　这种写法是直接将参数拼接到sql语句中，这样数据库就容易被sql注入攻击，比如

cursor.execute('select * from user where user=%s and password=%s'%(name,password))
　　要是name和password都等于'a or 1=1'，那么这个语句会把整个user表都查询出来

3.  默认环境
- 默认使用的环境文件为：mysql.env