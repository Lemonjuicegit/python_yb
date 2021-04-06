import json, os, re
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
        for i in zddm_xm:
            self.cmd.md(self.save_path, i)

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
        file_name = os.walk(self.paper_path, topdown=False)
        file_path = ''
        for paper__path, paper_name, file_name in file_name:
            for i in paper_name:
                file_path = file_path + str(i) + "\n"
        self.results = file_path

    # 渝北项目存量图片资料改名
    def yb_rename(self):
        TZ = read_excel(self.TZ_path)
        TZ_YWBH_ZDDM = TZ[["业务编号", "权利人名称", "宗地代码", "不动产单元代码"]]
        TZ_YWBH_ZDDM = TZ_YWBH_ZDDM.dropna(subset=['宗地代码'])
        picture_path = os.walk(self.rename_pictur_path)
        paper = []
        for p, f, n in picture_path:
            paper.append(os.path.split(p)[1])
        s = 0
        for i in TZ_YWBH_ZDDM.itertuples():
            YWBH = getattr(i, "业务编号")
            ZDDM = getattr(i, "宗地代码")
            BDCDYH = getattr(i, "不动产单元代码")
            QLRXM = getattr(i, "权利人名称")
            if str(YWBH) in paper:
                self.cmd.md(self.save_path, ZDDM + QLRXM)
                self.cmd.copy(r"%s\%s\产权证附图.jpg" % (self.rename_pictur_path, YWBH),
                              r"%s\%s%s\%s产权证附图.jpg" % (self.save_path, ZDDM, QLRXM, BDCDYH))
                self.cmd.copy(r"%s\%s\房产分户图.jpg" % (self.rename_pictur_path, YWBH),
                              r"%s\%s%s\%s登记簿附图.jpg" % (self.save_path, ZDDM, QLRXM, BDCDYH))
                self.cmd.copy(r"%s\%s\房产分户图.jpg" % (self.rename_pictur_path, YWBH),
                              r"%s\%s%s\%s登记簿附图.jpg" % (self.save_path, ZDDM, QLRXM, ZDDM))
                s += 1
        self.results = str(s) + "户"

    def set_TZ_path(self, text):
        self.TZ_path = text

    def set_picture_path(self, text):
        self.rename_pictur_path = text

    def setlineEdit_15Text(self, text):
        self.lineEdit_15Text = text

    def setlineEdit_16Text(self, text):
        self.lineEdit_16Text = text

    # 正则搜索与复制
    def re_search(self,REstring):
        file_names = os.walk(self.lineEdit_15Text, topdown=False)
        file_path = ''
        for paper__path, paper_name, file_name in file_names:
            for i in file_name:
                searchObj = re.search(REstring, i, re.M | re.I)
                if searchObj:
                    file_path = paper__path + ":" +i + "\n"+file_path
        self.results = file_path

    # 一般查找
    def pushbutton_11Slot(self):
        pass

    # 提取所有文件名
    def pushbutton_12Slot(self):
        pass

    # 提取文件名
    def pushbutton_13Slot(self):
        pass

    # 提取文件夹名
    def pushbutton_14Slot(self):
        pass

    def pushbutton_15Slot(self):
        pass


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

    def re_search(REstring):
        file_names = os.walk(r"D:\pythonProject\yb", topdown=False)
        file_path = ''
        for paper__path, paper_name, file_name in file_names:
            for i in file_name:
                searchObj = re.search(REstring, i, re.I)
                if searchObj:
                    file_path = paper__path + ":" + searchObj.group(0) + "\n" + file_path
        results = file_path
        return results


    string = re_search(r"(.*)\.pyc")
    print(string)
