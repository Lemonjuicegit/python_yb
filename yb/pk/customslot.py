from pk import mydocx, pycmd, key, fileutil, mysqlutil
from threading import Thread
from pandas import read_excel, DataFrame


class Slot():

    def __init__(self):
        self.cmd = pycmd.Cmd()
        self.doc = mydocx.DocxUtil()
        self.results = ""
        self.lic = key.licKey()
        self.execldata = fileutil.IoUtil()
        self.selectfield=""
        self.data=""

    def key(self):
        return self.lic.lic()

    #   获取挂接表并检查身份证号码
    def setgjb_path(self, txet):
        self.gjb = txet
        try:
            self.execl_gjb = read_excel(txet, dtype=str)
            n = self.doc.checksfz(self.execl_gjb)
        except Exception as e:
            self.results = str(e)
        if n == []:
            self.results = r"(*>﹏<*)"
        elif len(n) == 1:
            self.results = str(n)
        elif isinstance(n, str):
            self.results = n
        else:
            self.results = "\n".join(n)

    def exf(self):
        self.results = self.execldata.exf(self.execl_gjb, self.save_path)

    def hzb(self):
        self.results = self.execldata.hzb(self.execl_gjb, self.save_path)

    def jzb(self):
        self.results = self.execldata.jzb(self.gjb, self.save_path)

    def sms(self):
        self.results = self.doc.getsmss(self.execl_gjb, self.save_path)

    #   批量生成文件夹
    def gjb_paper_files(self):
        zddm_xm = []
        zddm = self.execl_gjb["宗地代码"]
        xm = self.execl_gjb["姓名"]
        i = 0
        while i < len(zddm):
            zddm_xm.append(zddm[i] + xm[i])
            i += 1
        self.cmd.paper_files(self.save_path, zddm_xm)

        self.results = "%s个文件夹创建成果" % i

    #   房产面积测算说明书
    def chjssms(self):
        self.results = self.doc.getchjssms(self.execl_gjb, self.save_path)

    #   不动产实地查看记录表
    def sdckb(self):
        self.results = self.doc.getsdckb(self.execl_gjb, self.save_path)

    def one_click(self):
        exfthread = slotThreadreturn(self.execldata.exf, (self.execl_gjb, self.save_path,))
        hzbthread = slotThreadreturn(self.execldata.hzb, (self.execl_gjb, self.save_path,))
        jzbthread = slotThreadreturn(self.execldata.jzb, (self.gjb, self.save_path,))
        smsthread = slotThreadreturn(self.doc.getsmss, (self.execl_gjb, self.save_path,))
        chjssmsthread = slotThreadreturn(self.doc.getchjssms, (self.execl_gjb, self.save_path,))
        sdckbthread = slotThreadreturn(self.doc.getsdckb, (self.execl_gjb, self.save_path,))
        exfthread.start()
        hzbthread.start()
        jzbthread.start()
        smsthread.start()
        chjssmsthread.start()
        sdckbthread.start()
        exfthread.join()
        hzbthread.join()
        jzbthread.join()
        smsthread.join()
        chjssmsthread.join()
        sdckbthread.join()
        exfthreadresult = exfthread.get_result()
        hzbthreadresult = hzbthread.get_result()
        jzbthreadresult = jzbthread.get_result()
        smsthreadresult = smsthread.get_result()
        chjssmsthreadresult = chjssmsthread.get_result()
        sdckbthreadresult = sdckbthread.get_result()
        result_list = []
        result_list.append(exfthreadresult)
        result_list.append(hzbthreadresult)
        result_list.append(jzbthreadresult)
        result_list.append(smsthreadresult)
        result_list.append(chjssmsthreadresult)
        result_list.append(sdckbthreadresult)
        result_list = [str(i) for i in result_list]

        self.results = "\n".join(result_list)

    def setsavepath(self, text):
        if self.cmd.isdir(text):
            self.save_path = text
            self.results = r"(*>﹏<*)"
        else:
            self.results = "请输入保存路径！"

    def select(self, text):
        self.selectfield = text



    def data_select(self):
        self.connenct = mysqlutil.DatabaseConnect(r".\yb.json")
        self.connenct.jsonconnect()
        self.data = self.connenct.one_sql(
            r"SELECT XZMC,CM, ZDDM_QS,ZDDM_JS, BMR, DJZQDM FROM ZDDM_list LEFT JOIN DJZQBM ON CM = DJZQMc WHERE CM LIKE '%"+self.selectfield+r"%' ORDER BY ZDDM_Qs;")

        self.results = str(len(self.data)) + "条数据"

    def insert(self):
        self.connenct = mysqlutil.DatabaseConnect(r".\yb.json")
        self.connenct.jsonconnect()
        self.data = self.connenct.one_sql(
            r"INSERT into ZDDM_list(XZMC, CM, ZDDM_QS,ZDDM_JS, BMR) VALUES ('%s','%s', '%s','%s', '%s');"%())

        self.results = str(len(self.data)) + "条数据"

#   自定义线程
class slotThreadreturn(Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return str(e)


class mass_detection_slot:
    def __init__(self):
        self.results = ""
        self.cmd = pycmd.Cmd()

    def getdata_path(self, text):
        if self.cmd.isdir(text):
            self.data_path = text
            self.results = r"(*>﹏<*)"
        else:
            self.results = "请输入正确路径！"

    def getpaper_path(self, text):
        if self.cmd.isdir(text):
            self.paper_path = text
            self.results = r"(*>﹏<*)"
        else:
            self.results = "请输入正确路径！"

    def exf(self):
        file_path = fileutil.getfilepath(self.paper_path)
        exfdata = fileutil.read_exf(file_path)
        comparison_d = {"宗地代码": [], "权利人姓名": [], "宗地面积对比": [], "宗地代码是否重复": []}
        comparison = DataFrame(columns=["宗地代码", "权利人姓名", "宗地面积对比", "宗地代码是否重复"])  # 检查结果集
        for i in exfdata.itertuples():
            data = read_excel(self.data_path)
            zdmj_comparison = float(data[data["宗地代码"] == getattr(i, "宗地代码")]["宗地面积"]) == getattr(i, "宗地面积")
            comparison_d["宗地代码"].append(getattr(i, "宗地代码"))
            comparison_d["宗地面积对比"].append(zdmj_comparison)
            comparison_d["权利人姓名"].append(getattr(i, "权利人姓名"))
            comparison_temp = DataFrame(comparison_d)
            comparison.append(comparison_temp, ignore_index=True)


if __name__ == '__main__':
    data = read_excel(r"E:\工作文件\成果数据\石船666\挂接表.xlsx")
    print(data)
    for i in data.itertuples():
        print(getattr(i, "宗地代码"))

        a = float(data[data["宗地代码"] == getattr(i, "宗地代码")]["宗地面积"])

        print(a)
