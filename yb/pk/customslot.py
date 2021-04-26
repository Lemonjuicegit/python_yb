import json
import os
import re
import shutil
from time import time
from pk import mydocx, pycmd, fileutil, sqlutil, decoratorsFunc
from threading import Thread
from pandas import read_excel, DataFrame, concat
from numpy import nan


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
        for n in zddm_xm:
            self.cmd.md(self.save_path, n)

        self.results = "%s个文件夹创建成功" % i

    #   房产面积测算说明书
    def chjssms(self):
        self.results = self.doc.getchjssms(self.execl_weigjb, self.save_path)

    #   不动产实地查看记录表
    def sdckb(self):
        self.results = self.doc.getsdckb(self.execl_gjb, self.save_path)

    def one_click(self):
        exfthread = slotThreadreturn(
            self.execldata.exf, (self.execl_gjb, self.save_path,))
        hzbthread = slotThreadreturn(
            self.execldata.hzb, (self.execl_gjb, self.save_path,))
        jzbthread = slotThreadreturn(
            self.execldata.jzb, (self.gjb, self.save_path,))
        smsthread = slotThreadreturn(
            self.doc.getsmss, (self.execl_gjb, self.save_path,))
        chjssmsthread = slotThreadreturn(
            self.doc.getchjssms, (self.execl_gjb, self.save_path,))
        sdckbthread = slotThreadreturn(
            self.doc.getsdckb, (self.execl_gjb, self.save_path,))
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
        # 将结果添加到results
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
        # re.search(r"XZMC",XZMC)
        # re.search(r"XZMC", XZMC)
        # re.search(r"JC[0-9]{5}", XZMC)
        # re.search(r"JC[0-9]{5}", XZMC)
        # re.search(r"XZMC", XZMC)
        self.connenct.one_dml(
            r"""INSERT into ZDDM_list(XZMC, CM, ZDDM_QS,ZDDM_JS, BMR) 
                VALUES ('%s','%s', '%s','%s', '%s');""" % (XZMC, CM, ZDDM_QS, ZDDM_JS, BMR))
        self.results = "添加成功！"

    def delete(self, id):
        self.connenct.one_dml(
            r"""DELETE FROM zddm_list WHERE id = %s;""" % (id))

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
                os.makedirs(os.path.join(self.save_path, ZDDM + QLRXM))
                shutil.copyfile(r"%s\%s\产权证附图.jpg" % (self.rename_pictur_path, YWBH),
                                r"%s\%s%s\%s产权证附图.jpg" % (self.save_path, ZDDM, QLRXM, BDCDYH))
                shutil.copyfile(r"%s\%s\房产分户图.jpg" % (self.rename_pictur_path, YWBH),
                                r"%s\%s%s\%s登记簿附图.jpg" % (self.save_path, ZDDM, QLRXM, BDCDYH))
                shutil.copyfile(r"%s\%s\房产分户图.jpg" % (self.rename_pictur_path, YWBH),
                                r"%s\%s%s\%s登记簿附图.jpg" % (self.save_path, ZDDM, QLRXM, ZDDM))
                s += 1
        self.results = str(s) + "户"

    def set_TZ_path(self, text):
        self.TZ_path = text

    def set_picture_path(self, text):
        self.rename_pictur_path = text

    def setlineEdit_15Text(self, text):
        self.lineEdit_15Text = text
        self.results = self.lineEdit_15Text

    def setlineEdit_16Text(self, text):
        self.lineEdit_16Text = text
        self.results = self.lineEdit_16Text

    # 正则搜索与复制
    def re_search(self, REstring):
        file_names = os.walk(self.lineEdit_15Text, topdown=True)
        file_path = ''
        for paper__path, paper_name, file_name in file_names:
            for i in file_name:
                searchObj = re.search(REstring, i, re.M | re.I)
                if searchObj:
                    file_path = paper__path + ">>" + i + "\n" + file_path
        self.results = file_path

    # 一般查找
    def pushbutton_11Slot(self, string):
        self.re_search(r"(.*)\Q" + string + "\Ec(.*)")

    # 提取所有文件名
    def pushbutton_12Slot(self):
        walkobj = os.walk(self.lineEdit_15Text, topdown=True)
        catalogue_name = []
        for paper_path, dir, file_name in walkobj:
            paper_name = os.path.split(paper_path)
            catalogue_name.append(paper_name[1] + "\n")
            for f in file_name:
                catalogue_name.append(f + "\n")
        self.results = "".join(catalogue_name)

    # 提取文件名
    def pushbutton_13Slot(self):
        walkobj = os.walk(self.lineEdit_15Text, topdown=True)
        catalogue_name = []
        a = time()
        for paper_path, dir, file_name in walkobj:
            for f in file_name:
                Thread(target=catalogue_name.append, args=(f + "\n",))
                # catalogue_name.append(f + "\n")

        self.results = "".join(catalogue_name)

    # 提取文件夹名
    def pushbutton_14Slot(self):
        catalogue_name = []

        walkobj = os.walk(self.lineEdit_15Text, topdown=True)
        for r_path, dir, file_name in walkobj:
            catalogue_name.append(r_path)

        self.results = "\n".join(catalogue_name)

    def pushbutton_15Slot(self, string):
        file_path = string.split("\n")
        for folder in file_path:
            if ">>" in folder:
                folder = folder.split(">>")
                folder_name = os.path.split(folder[0])[1]
                isExists = os.path.exists(
                    self.lineEdit_16Text + "\\" + folder_name)
                if isExists:
                    shutil.copyfile(os.path.join(folder[0], folder[1]),
                                    self.lineEdit_16Text + "\\" + folder_name + "\\" + folder[1])
                else:
                    os.makedirs(self.lineEdit_16Text + "\\" + folder_name)
                    shutil.copyfile(os.path.join(folder[0], folder[1]),
                                    self.lineEdit_16Text + "\\" + folder_name + "\\" + folder[1])
            else:
                folder_name = os.path.split(folder)
                shutil.copytree(folder, os.path.join(
                    self.lineEdit_16Text, folder_name[1]))
        self.results = "复制成功"

    def pushbutton_17Slot(self, string):
        file_path = string.split("\n")
        num = 0
        for f in file_path:
            walkobj = os.walk(f, topdown=False)
            for paper_path, dir, file_name in walkobj:
                for fn in file_name:
                    os.remove(os.path.join(paper_path, fn))
                os.removedirs(paper_path)
            num = num + 1

        self.results = "删除：" + str(num) + "个文件夹"

    def pushbutton_18Slot(self, string):
        file_path = string.split("\n")
        num = 0
        for f in file_path:
            os.remove(f)
            num = num + 1

        self.results = "删除：" + str(num) + "个文件"

    def TZpath(self, text):
        self.TZ_path = text

    def ShpZdPath(self, text):
        self.SHP_zd_path = text

    def YstzPath(self, text):
        self.YSTZ_path = text

    def errorSaving(self, text):
        self.errpath = text

    # @decoratorsFunc.getexception
    def TZcheckSlot(self):
        checks = TZcheck(TZ_path=self.TZ_path, SHP_zd_path=self.SHP_zd_path,
                         YSTZ_path=self.YSTZ_path, savePath=self.errpath)
        checks.check()
        self.results = str(checks.resultsDict)
        checks.resultsDict = {}

    def setlineEdit_24Text(self, text):
        self.lineEdit_24Text = text
        self.results = self.lineEdit_24Text

    # 合并工作簿
    def mergeWorkbook(self, paths):
        pathdir = paths.split("\n")
        listpath = []
        num = 0
        for path in pathdir:
            filename = os.listdir(path)
            file_path = [os.path.join(paths, i) for i in filename]
            for i in file_path:
                if ".xlsx" in i:
                    listpath.append(read_excel(i, dtype=str))
                num += 1
        df = concat(listpath)
        df.to_excel(os.path.join(self.lineEdit_24Text,
                    "合并工作簿.xlsx"), index=False)
        self.results = "合并了%s个工作簿" % num

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
        comparison_d = {"宗地代码": [], "权利人姓名": [],
                        "宗地面积对比": [], "宗地代码个数": [], "地籍号一致性": []}
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
                    comparison_d["宗地代码个数"].append(
                        list(data["ZDDM"]).count(getattr(i, "宗地代码")))
            except Exception as e:
                comparison_d["宗地面积对比"].append(str(e))
                comparison_d["地籍号一致性"].append(djh)
                comparison_d["宗地代码"].append(getattr(i, "宗地代码"))
                comparison_d["权利人姓名"].append(getattr(i, "权利人姓名"))
                comparison_d["宗地代码个数"].append(
                    list(data["ZDDM"]).count(getattr(i, "宗地代码")))
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

    # def tz_exf_gis(self):
    #     comparison_tz_exf_gis = fileutil.read_json("data.json")["comparison_tz_exf_gis"]
    #     file_path = fileutil.getfilepath(self.paper_path, r".exf")
    #     exfdata = fileutil.read_exf(file_path)
    #     data = read_excel(self.data_path)
    #     tz = read_excel(self.tz_path)


class TZcheck:
    def __init__(self, TZ_path, YSTZ_path, SHP_zd_path, savePath):
        """[初始化三表]
        Args:
            TZ_path ([路径]): [台账]
            YSTZ_path ([路径]): [原始台账]
            SHP_zd_path ([路径]): [复制出来SHP_zd数据表]]
        """
        self.TZ = read_excel(TZ_path)
        self.TZ.replace('\s+', '', regex=True, inplace=True)
        self.YSTZ = read_excel(YSTZ_path)
        self.SHP_zd = read_excel(SHP_zd_path, sheet_name="Sheet1")
        self.SHP_zd.replace('\s+', '', regex=True, inplace=True)
        self.SHP_zrz = read_excel(SHP_zd_path, sheet_name="Sheet2")
        self.SHP_zrz.replace('\s+', '', regex=True, inplace=True)
        self.savePath = savePath
        self.resultsDict = {"业务编号": [], "宗地代码": [], "不动产单元代码": [], "问题": []}
        self.__BZLIST = ["正常", "灭失", "拆留", "复垦", "已征收",
                         "一户多宅，需拆分", "一户多宅，需拆分",
                         "一户多宅,需拆分", "迁建", "其他", "已转移"]

    def getFied_value(self):
        self.TZ_zddm = list(self.TZ["宗地代码"])
        self.TZ_ywbh = [str(i)[:10] for i in list(self.TZ["业务编号"])]
        self.TZ_zcs = [str(i)[0] for i in list(self.TZ["总层数"])]
        self.TZ_zzc = [str(i)[0] for i in list(self.TZ["所在终止层"])]
        self.TZ_qsc = [str(i)[0] for i in list(self.TZ["所在起始层"])]
        self.TZ_myc = [str(i) for i in list(self.TZ["名义层"])]
        self.TZ_bdcdyh = [str(i) for i in list(self.TZ["不动产单元代码"])]
        self.TZ_bz = list(self.TZ["备注2"])
        self.TZ_zdmj = list(self.TZ["宗地面积"])
        self.TZ_qzh = [str(i) for i in list(self.TZ["权证号"])]
        self.TZ_qlr = list(self.TZ["权利人名称"])
        self.TZ_fh = [str(i) for i in list(self.TZ["房号"])]
        self.TZ_djh = list(self.TZ["旧地籍号"])
        self.TZ_zdzt = [str(i)[0] for i in list(self.TZ["宗地状态"])]
        self.TZ_biz = list(self.TZ["标注"])
        self.TZ_jzcmj_notnull = list(self.TZ["房屋超建说明"].notnull())
        self.TZ_zdcmj_notnull = list(self.TZ["宗地超占说明"].notnull())
        self.TZ_D = list(self.TZ["东"])
        self.TZ_N = list(self.TZ["南"])
        self.TZ_X = list(self.TZ["西"])
        self.TZ_B = list(self.TZ["北"])

        self.YSTZ_ywbh = [str(i) for i in list(self.YSTZ["业务编号"])]
        self.YSTZ_qzh = [str(i) for i in list(self.YSTZ["权证号"])]

        self.SHP_zd_zddm = list(self.SHP_zd["F_PARCEL_N"])
        self.SHP_zd_ywbh = [str(i)[:10] for i in list(self.SHP_zd["F_SERIAL_N"])]
        self.SHP_zd_zdmj = list(self.SHP_zd["F_CALCULAT"])
        self.SHP_zd_ID = [str(i) for i in list(self.SHP_zd["F_CODE_ID"])]
        self.SHP_zd_qlr = list(self.SHP_zd["F_INDB_RIG"])
        self.SHP_zd_djh = list(self.SHP_zd["F_PARCEL02"])

        self.SHP_zrz_zcs = [str(i) for i in list(self.SHP_zrz["F_BUILDING"])]
        self.SHP_zrz_zdID = [str(i) for i in list(self.SHP_zrz["F_PARCEL_I"])]
        self.SHP_zrz_ID = [str(i) for i in list(self.SHP_zrz["F_CODE_ID"])]
        self.SHP_zrz_zcs = [str(i)[0] for i in list(self.SHP_zrz["F_BUILDING"])]
        self.SHP_zrz_zddm = list(self.SHP_zrz["F_UNDER_PA"])
        self.SHP_zrz_ywbh = [str(i)[:10]
                             for i in list(self.SHP_zrz["F_SERIAL_N"])]

    def check(self):
        self.getFied_value()

        for i in range(len(self.TZ) - 1):
            temp = []
            if self.TZ_zddm == "nan" and self.TZ_zddm == "" and self.TZ_zdzt[i] =="0" and self.TZ_bdcdyh[i]=="nan" and self.TZ_bdcdyh[i]=="":
                temp.append("台账宗地代码为空")
            else:
                if not (len(self.TZ_zddm[i]) == 19):
                    temp.append("台账宗地代码错误")
                elif not (len(self.TZ_bdcdyh[i]) == 28):
                    temp.append("台账不动产单元号错误")
                else:
                    if not (self.TZ_zddm[i][-4:19] == self.TZ_djh[i][8:12]):
                            temp.append("台账地籍号与宗地代码后四位不一致")
                if not (self.TZ_biz[i] in self.__BZLIST):
                    temp.append("标注错误")
                try:
                    shp_zd_index = self.SHP_zd_zddm.index(
                        self.TZ_zddm[i])
                    shp_zrz_index = self.SHP_zrz_zddm.index(
                        self.TZ_zddm[i])
                    if not (self.TZ_zdmj[i] == self.SHP_zd_zdmj[shp_zd_index]):
                        temp.append("台账宗地面积与图形宗地面积不同")
                    if not (self.SHP_zrz_zdID[shp_zrz_index] == self.SHP_zd_ID[shp_zd_index]):
                        temp.append("房屋外框的宗地Id与宗地图层不一致")
                    if not (self.SHP_zd_ywbh[shp_zd_index] == self.TZ_ywbh[i]):
                        temp.append("宗地外框业务编号与台账业务编号不一致")
                    if not (self.SHP_zrz_ywbh[shp_zrz_index] == self.TZ_ywbh[i]):
                        temp.append("房屋外框业务编号与台账业务编号不一致")
                    if not (self.SHP_zrz_zcs[shp_zrz_index] == self.TZ_zcs[i]):
                        temp.append("房屋外框总层数与台账总层数不一致")
                    if not (self.SHP_zd_qlr[shp_zd_index] == self.TZ_qlr[i]):
                        temp.append("台账的权利人姓名与宗地不一致")
                    if not (self.SHP_zd_zddm[shp_zd_index] ==19):
                        temp.append("宗地图框宗地代码错误")
                    else:
                        if not (self.SHP_zd_zddm[shp_zd_index][-4:19] == self.SHP_zd_djh[shp_zd_index][8:12]):
                            temp.append("宗地图框地籍号与宗地代码后四位不一致")  

                except ValueError:
                    temp.append("台账宗地代码在图形中找不到")

                if not (self.TZ_zddm[i] in list(self.SHP_zd["F_PARCEL_N"])):
                    temp.append("台账宗地代码在图形中找不到")
                if self.TZ_ywbh[i] == "nan":
                    temp.append("台账业务编号为空")
                else:
                    if not ((self.TZ_ywbh[i][:10] == self.SHP_zd_ywbh[shp_zd_index])):
                        temp.append("台账业务编号在图形中找不到：%s" %
                                    (self.TZ_bz[i]), )
                if not (self.TZ_zcs[i] == self.TZ_zzc[i]):
                    temp.append("总层数与终止层不一致")
                if not ((self.TZ_qsc[i][0] + "-" + self.TZ_zzc[i][0]) == self.TZ_myc[i]):
                    temp.append("名义层不一致")
                if self.TZ_zddm.count(self.TZ_zddm[i]) > 1:
                    temp.append("台账中宗地代码重复")
                if self.TZ_ywbh.count(self.TZ_ywbh[i]) > 1:
                    temp.append("台账业务编号重复")
                try:
                    ystz_index = self.YSTZ_ywbh.index(
                        self.TZ_ywbh[i][:10])
                    if not (self.TZ_qzh[i] == self.YSTZ_qzh[ystz_index]):
                        temp.append("台账权证号进行了修改")
                except ValueError:
                    temp.append("台账业务编号在原始台账中找不到")

                if not (self.TZ_fh[i][0] == self.TZ_bdcdyh[i][-1]):
                    temp.append("房号错误")

                if self.TZ_zdzt[i] in ["正常", "拆留", "改建"]:
                    if self.TZ_biz[i] != "1":
                        temp.append("宗地状态错误")
                if self.TZ_zdzt[i] in ["复垦", "已征收"]:
                    if self.TZ_biz[i] != "0":
                        temp.append("宗地状态错误")
                if self.TZ_zdcmj_notnull[i]:
                    if self.TZ_biz[i] != "超占建房":
                        temp.append("房屋标注错误")
                if self.TZ_jzcmj_notnull[i] and (not self.TZ_zdcmj_notnull[i]):
                    if self.TZ_biz[i] != "超规划建房":
                        temp.append("房屋标注错误")
                if self.TZ_D == "" or self.TZ_B == "" or self.TZ_X == "" or self.TZ_B == "" or self.TZ_D == nan or self.TZ_B == nan or self.TZ_X == nan or self.TZ_B == nan:
                        temp.append("四至为空")

            
            if not (self.TZ_biz[i] in ["转移", "已征收"]):
                temp.append("房屋标注错误")
            if not (self.TZ_zdzt[i] in ["1","0"]):
                        temp.append("宗地状态错误")

            if temp:
                self.resultsDict["业务编号"].append(self.TZ_ywbh[i][:10])
                self.resultsDict["不动产单元代码"].append(self.TZ_bdcdyh[i])
                self.resultsDict["宗地代码"].append(self.TZ_zddm[i])
                self.resultsDict["问题"].append(str(temp))

        for i in range(len(self.SHP_zd_zddm) - 1):
            temp = []
            try:
                self.SHP_zrz_zddm.index(self.SHP_zd_zddm[i])
            except ValueError:
                temp.append("宗地代码在房屋图框中找不到")
                continue
            try:
                TZ_index = self.TZ_zddm.index(self.SHP_zd_zddm[i])
            except ValueError:
                temp.append("宗地代码在台账中找不到")
                continue

            if temp:
                self.resultsDict["业务编号"].append(self.SHP_zd_ywbh[i])
                self.resultsDict["宗地代码"].append(self.SHP_zd_zddm[i])
                self.resultsDict["不动产单元代码"].append(self.TZ_bdcdyh[TZ_index])
                self.resultsDict["问题"].append(str(temp))

        if self.resultsDict["问题"]:
            self.results = DataFrame(self.resultsDict)
            self.results.to_excel(os.path.join(
                self.savePath, "质检.xlsx"), index=False)


if __name__ == '__main__':

    s = "500112139207JC00898"
    a = "YB0173020898000"
