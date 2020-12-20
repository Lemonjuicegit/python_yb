import pymssql
import os

server = "192.168.0.3"     # 连接服务器地址
user = "sa"               # 连接帐号
password = "123456"           # 连接密码

conn = pymssql.connect(host=server, port=1433,user=user, password=password, database="yb",charset="utf8")  #获取连接
print(conn)
cursor = conn.cursor() # 获取光标
print(cursor)
# 查询数据
cursor.execute(r"select * from DJZQBM where DJQMC = '木耳镇';")

row = cursor.fetchall()

row=[str(i) for i in row]
a="\n".join(row)
print(a)
# while row:
#     print("ID=%s, Name=%s" % (row[0], row[1]))
#     row = cursor.fetchone()