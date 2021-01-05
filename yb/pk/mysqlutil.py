import pymysql
import pymssql
import decoratorsFunc
import fileutil


class DatabaseConnect:
    def __init__(self,json_path):
        jsonvalue = fileutil.jsondict(json_path)
        self.serverip = jsonvalue["databaesconnect"]["serverip"]  # 连接服务器地址
        self.user = jsonvalue["databaesconnect"]["user"]  # 用户名
        self.password = jsonvalue["databaesconnect"]["password"]  # 密码
        self.port = jsonvalue["databaesconnect"]["port"]  # 端口
        self.database = jsonvalue["databaesconnect"]["database"]  # 数据库名称
        self.charset = jsonvalue["databaesconnect"]["charset"]  # 字符编码
        self.drive=jsonvalue["databaesconnect"]["drive"]

    def jsonconnect(self):
        if self.drive== "mysql":
            self.connect = pymysql.connect(host=self.serverip, port=self.port, user=self.user, password=self.password,
                                           database=self.database, charset=self.charset)  # 获取mysql连接
        elif self.drive == "sqlserver":
            self.connect = pymssql.connect(host=self.serverip, port=self.port, user=self.user, password=self.password,
                                   database=self.database, charset=self.charset)  # 获取sqlserver连接
        self.cursor = self.connect.cursor()  # 获取光标

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
    data = DatabaseConnect(r"..\yb.json")
    data.jsonconnect()
    search_result = data.one_sql(r"SELECT XZMC,CM, ZDDM_QS,ZDDM_JS, BMR, SL, DJZQDM FROM ZDDM_list LEFT JOIN DJZQBM ON CM = DJZQMc WHERE CM LIKE '%上坝%' ORDER BY ZDDM_Qs;")
    # search_result = [str(i) for i in search_result]
    search_result=(str(i) for i in search_result)
    search_result = "\n".join(search_result)

    print(search_result)
    data.close()

# while row:
#     print("ID=%s, Name=%s" % (row[0], row[1]))
#     row = cursor.fetchone()
