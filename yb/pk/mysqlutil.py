import pymysql
import pymssql
import decoratorsFunc
import fileutil


class DatabaseConnect:
    def jsonconnect(self, json_path):
        jsonvalue = fileutil.jsondict(json_path)
        serverip = jsonvalue["databaesconnect"]["serverip"]  # 连接服务器地址
        user = jsonvalue["databaesconnect"]["user"]  # 用户名
        password = jsonvalue["databaesconnect"]["password"]  # 密码
        port = jsonvalue["databaesconnect"]["port"]  # 端口
        database = jsonvalue["databaesconnect"]["database"]  # 数据库名称
        charset = jsonvalue["databaesconnect"]["charset"]  # 字符编码
        if jsonvalue["databaesconnect"]["drive"] == "mysql":
            self.connect = pymysql.connect(host=serverip, port=port, user=user, password=password,
                                           database=database, charset=charset)  # 获取mysql连接
        elif jsonvalue["databaesconnect"]["drive"] == "sqlserver":
            self.connect = pymssql.connect(host=serverip, port=port, user=user, password=password,
                                   database=database, charset=charset)  # 获取sqlserver连接
        self.cursor = self.connect.cursor()  # 获取光标


    def connect(self, serverip, user, password, port: int, database, drive, charset="utf8"):
        """
        @param serverip:服务器ip地址
        @param user:用户名
        @param password:用户密码
        @param port:端口号
        @param database:数据库名称
        @param drive:要连接那种数据库（mysql sqlserver）
        @param charset:字符编码
        """
        serverip = serverip  # 连接服务器地址
        user = user  # 用户名
        password = password  # 密码
        port = port  # 端口
        database = database  # 数据库名称
        charset = charset  # 字符编码
        if drive == "mysql":
            self.connect = pymysql.connect(host=serverip, port=port, user=user, password=password,
                                           database=database, charset=charset)  # 获取mysql连接
        elif drive == "sqlserver":
            self.connect = pymssql.connect(host=serverip, port=port, user=user, password=password,
                                           database=database, charset=charset)  # 获取sqlserver连接
        self.cursor = self.connect.cursor()  # 获取光标

    # 基本查询数据
    @decoratorsFunc.getexceptionreturn
    def select(self, table, field: list, field_like="", condition="", like=0, ORDER_field="", ORDER="ASC"):
        """
        @param table: 查询表名
        @param field: 查询字段
        @param [field_like:]模糊查询匹配的字段
        @param [condition:]查询条件
        @param [like:] 是否模糊查询
        @param [ORDER_field:] 排序字段
        @param [ORDER:] 排序方式
        @return: 返回查询结果
        """
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

    # 执行一条SQL语句
    @decoratorsFunc.getexceptionreturn
    def one_sql(self, sql: str):
        self.cursor.execute(sql)
        search_result = self.cursor.fetchall()

        return search_result

    def close(self):
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    data = DatabaseConnect()
    data.jsonconnect(r"..\yb.json")
    search_result = data.one_sql("select * from djzqbm where djqmc = '玉峰山镇'")
    print(['XZMC', 'CM', 'ZDDM_QS', 'ZDDM_JS', 'BMR', 'SL', 'DJZQDM'])
    # search_result = [str(i) for i in search_result]
    search_result=(str(i) for i in search_result)
    search_result = "\n".join(search_result)

    print(search_result)
    data.close()

# while row:
#     print("ID=%s, Name=%s" % (row[0], row[1]))
#     row = cursor.fetchone()
