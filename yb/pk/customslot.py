import json
from os import walk

from pk import mydocx, pycmd, fileutil, sqlutil
from threading import Thread
from pandas import read_excel


class Slot():
    def __init__(self):
        # if CDLL(r"bin\lic.dll").getlic() == 0:
        #     exit()
        self.cmd = pycmd.Cmd()
        self.doc = mydocx.DocxUtil()
        self.results = ""
        self.execldata = fileutil.IoUtil()
        self.connenct = sqlutil.DatabaseConnect(r".\yb.json")
        self.connenct.jsonconnect()
        self.collocation = fileutil.read_json("data.json")
        self.data = []

    def getcollocation(self):
        self.collocation = fileutil.read_json("data.json")

    #   获取挂接表并检查身份证号码
    def setgjb_path(self, txet):
        self.gjb = txet
        n = [""]
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
        self.results = self.doc.getchjssms(self.execl_weigjb, self.save_path)

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
        # 获取结果
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

    def setselectvalue(self, text):
        self.selectvalue = text

    def select(self, selectvalue):
        self.data = []
        self.sqldata = self.connenct.one_sql(
            r"""SELECT id,XZMC,CM, ZDDM_QS,ZDDM_JS, BMR, DJZQDM 
                FROM ZDDM_list LEFT JOIN DJZQBM ON CM = DJZQMc 
                WHERE CM LIKE '%""" + selectvalue + r"""%' ORDER BY ZDDM_QS;""")
        for i in range(len(self.sqldata)):
            self.data.append([str(j) for j in self.sqldata[i]])
        self.results = str(len(self.data)) + "条数据"

    def insert(self, XZMC, CM, ZDDM_QS, ZDDM_JS, BMR):
        self.connenct.one_dml(
            r"""INSERT into ZDDM_list(XZMC, CM, ZDDM_QS,ZDDM_JS, BMR) 
                VALUES ('%s','%s', '%s','%s', '%s');""" % (XZMC, CM, ZDDM_QS, ZDDM_JS, BMR))
        self.results = "添加成功！"

    def delete(self, id):
        self.connenct.one_dml(r"""DELETE FROM zddm_list WHERE id = %s;""" % (id))

    def emptydata(self, data):
        with open(r"data.json", "w") as flie:
            json.dump(data, flie)

    def paper_path(self, text):
        self.paper_path = text

    def extract_file_name(self):
        file_name = walk(self.paper_path, topdown=False)
        file_path = []
        for paper__path, paper_name, file_name in file_name:
            for i in paper_name:
                file_path.append(paper_name)
        self.results = str(file_path)
        return self.results


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
        self.data_path = text
        self.results = r"(*>﹏<*)"

    def getpaper_path(self, text):
        if self.cmd.isdir(text):
            self.paper_path = text
            self.results = r"(*>﹏<*)"
        else:
            self.results = "请输入正确路径！"

    def getTZ_path(self, text):
        self.tzdata = read_excel(text)
        self.results = r"(*>﹏<*)"

    def exf(self):
        file_path = fileutil.getfilepath(self.paper_path, r".exf")
        exfdata = fileutil.read_exf(file_path)
        comparison_d = {"宗地代码": [], "权利人姓名": [], "宗地面积对比": [], "宗地代码个数": [], "地籍号一致性": []}
        data = read_excel(self.data_path)
        for i in exfdata.itertuples():
            try:
                djh = (getattr(i, "地籍号")[8:12] == getattr(i, "宗地代码")[15:])
                zdmj_comparison = round(float(data[data["ZDDM"].isin([getattr(i, "宗地代码")])]["Shape_Area"]), 2) == float(
                    getattr(i, "宗地面积"))
                if not djh or not zdmj_comparison:
                    print(float(data[data["ZDDM"].isin([getattr(i, "宗地代码")])]["Shape_Area"]))
                    print(round(float(data[data["ZDDM"].isin([getattr(i, "宗地代码")])]["Shape_Area"]), 2))
                    print(float(getattr(i, "宗地面积")))
                    comparison_d["宗地面积对比"].append(zdmj_comparison)
                    comparison_d["地籍号一致性"].append(djh)
                    comparison_d["宗地代码"].append(getattr(i, "宗地代码"))
                    comparison_d["权利人姓名"].append(getattr(i, "权利人姓名"))
                    comparison_d["宗地代码个数"].append(list(data["ZDDM"]).count(getattr(i, "宗地代码")))
            except Exception as e:
                comparison_d["宗地面积对比"].append(str(e))
                comparison_d["地籍号一致性"].append(djh)
                comparison_d["宗地代码"].append(getattr(i, "宗地代码"))
                comparison_d["权利人姓名"].append(getattr(i, "权利人姓名"))
                comparison_d["宗地代码个数"].append(list(data["ZDDM"]).count(getattr(i, "宗地代码")))
        n = 1
        f = "第1次检查"
        temp = {}
        while (f in list(fileutil.read_json(r".\data.json").keys())):
            n += 1
            f = "第%s次检查" % n
        temp[f] = comparison_d
        fileutil.write_json(r".\data.json", temp)

        self.results = comparison_d
        del comparison_d

    def TZqualitychecking(self):
        data = read_excel(r"D:\pythonProject\yb\测试数据\有效台账.xlsx")
        self.tzdata = read_excel(r"D:\pythonProject\yb\测试数据\有效台账.xlsx")
        for i in self.tzdata:
            self.tzdata[self.tzdata["宗地代码"].isin(getattr(i, "宗地代码"))["宗地代码"]]

    def tz_exf_gis(self):
        comparison_tz_exf_gis = fileutil.read_json("data.json")["comparison_tz_exf_gis"]
        file_path = fileutil.getfilepath(self.paper_path, r".exf")
        exfdata = fileutil.read_exf(file_path)
        data = read_excel(self.data_path)
        tz = read_excel(self.tz_path)


if __name__ == '__main__':
    def extract_file_name(paper_path):
        file_name = walk(paper_path, topdown=False)
        file_path=''
        for paper__path, paper_name, file_name in file_name:
            for i in  paper_name:
                file_path=file_path+str(i)+"\n"
        results = file_path
        return results
    string=extract_file_name(r"\\Pc-201904292001\渝北项目成果文件-余勇(勿删！！)\勘测站建盘数据提交文件\补点建盘数据11.12\玉峰山镇")
    print(string)

