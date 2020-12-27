import pymysql
import pymssql
import re
import os
import decoratorsFunc


class DatabaseUtil:

    def __init__(self, serverip, user, password, port: int, database, drive, charset="utf8"):
        self.serverip = serverip  # 连接服务器地址
        self.user = user  # 用户名
        self.password = password  # 密码
        self.port = port  # 端口
        self.database = database  # 数据库名称
        self.charset = charset  # 字符编码
        if drive == "mysql":
            self.connect = pymysql.connect(host=self.serverip, port=self.port, user=self.user, password=self.password,
                                           database=self.database, charset=self.charset)  # 获取连接
        elif drive == "sqlserver":
            self.connect = pymssql.connect(host=self.serverip, port=self.port, user=self.user, password=self.password,
                                           database=self.database, charset=self.charset)  # 获取连接
        self.cursor = self.connect.cursor()  # 获取光标

    # 查询获取数据
    @decoratorsFunc.getexceptionreturn
    def select(self, table, field: list, field_like, condition="", like=0, ORDER_field="", ORDER="ASC"):

        field = ",".join(field)
        if ORDER_field != "":
            if condition == "":
                self.cursor.execute(r"SELECT %s FROM %s ORDER BY %s %s;" % (field, table, ORDER_field, ORDER))
            elif like == 0:
                self.cursor.execute(
                    r"SELECT %s FROM %s WHERE %s ORDER BY %s %s;" % (field, table, condition, ORDER_field, ORDER))
            elif like == 1:
                self.cursor.execute(r"SELECT %s FROM %s WHERE %s like %s ORDER BY %s %s;" % (
                    field, table, field_like, condition, ORDER_field, ORDER))
        else:
            if condition == "":
                self.cursor.execute(r"SELECT %s FROM %s;" % (field, table))
            elif like == 0:
                self.cursor.execute(r"SELECT %s FROM %s WHERE %s;" % (field, table, condition))
            elif like == 1:
                self.cursor.execute(r"SELECT %s FROM %s WHERE %s like %s;" % (field, table, field_like, condition))

        search_result = self.cursor.fetchall()

        return search_result

    # 表链接查询
    @decoratorsFunc.getexceptionreturn
    def select_join(self, table_, table__, field: list, link_condition, condition, ORDER_field, link="left"):
        field = ",".join(field)
        self.cursor.execute(
            r"SELECT %s FROM %s %s join %s on %s WHERE %s order by %s;" % (
            field, table_, link, table__, link_condition, condition, ORDER_field))
        search_result = self.cursor.fetchall()
        return search_result

    #  删除数据
    @decoratorsFunc.getexceptionreturn
    def delete(self, table, condition):
        search_result = self.cursor.execute(r"DELETE FROM %s WHERE %s;" % (table, condition))

        return search_result

    # 更新数据
    @decoratorsFunc.getexceptionreturn
    def updata(self, table, condition):
        search_result = self.cursor.execute(r"UPDATA SET %s WHERE %s;" % (table, condition))

        return search_result

    # 插入数据
    @decoratorsFunc.getexceptionreturn
    def insert(self, table, field, value):
        search_result = self.cursor.execute(r"INSERT INTO %s(%s) VALUES %s;" % (table, field, value))

        return search_result

    def close(self):
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    data = DatabaseUtil("192.168.0.3", "root", "123456", 3306, "test", "mysql")

    search_result = data.select_join(field=['XZMC', 'CM', 'ZDDM_QS', 'ZDDM_JS', 'BMR', 'SL', 'DJZQDM'],
                                     table_="zddm_list", table__="DJZQBM", link_condition=r"CM = DJZQMC",
                                     condition=r"CM like '%玉峰%'")
    print(['XZMC', 'CM', 'ZDDM_QS', 'ZDDM_JS', 'BMR', 'SL', 'DJZQDM'])
    search_result = [str(i) for i in search_result]
    search_result = "\n".join(search_result)

    print(search_result)
    data.close()

# while row:
#     print("ID=%s, Name=%s" % (row[0], row[1]))
#     row = cursor.fetchone()
