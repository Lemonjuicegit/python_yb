import pandas as pd


class TZcheck:
    def __init__(self, TZ_path, YSTZ_path, SHP_zd_path):
        """[初始化三表]
        Args:
            TZ_path ([路径]): [台账]
            YSTZ_path ([路径]): [原始台账]
            SHP_zd_path ([路径]): [复制出来SHP_zd数据表]]
        """
        self.TZ = pd.read_excel(TZ_path)
        self.YSTZ = pd.read_excel(YSTZ_path)
        self.SHP_zd = pd.read_excel(SHP_zd_path,sheet_name="Sheet1")
        self.SHP_zrz = pd.read_excel(SHP_zd_path,sheet_name="Sheet2")
        self.results = {"不动产单元代码": [], "问题": []}

    def getFied_value(self):
        self.TZ_zddm = list(self.TZ["宗地代码"])
        self.TZ_ywbh = [str(i) for i in list(self.TZ["业务编号"])]
        self.TZ_zcs = [str(i) for i in list(self.TZ["总层数"])]
        self.TZ_zzc = [str(i) for i in list(self.TZ["所在终止层"])]
        self.TZ_qsc = [str(i) for i in list(self.TZ["所在起始层"])]
        self.TZ_myc = [str(i) for i in list(self.TZ["名义层"])]
        self.TZ_bdcdyh = list(self.TZ["不动产单元代码"])
        self.TZ_bz = list(self.TZ["备注2"])
        self.TZ_zdmj = list(self.TZ["宗地面积"])

        self.SHP_zd_zddm = list(self.SHP_zd["F_PARCEL_N"])
        self.SHP_zd_ywbh = [str(i) for i in list(self.SHP_zd["F_SERIAL_N"])]
        self.SHP_zd_zdmj = list(self.SHP_zd["F_CALCULAT"])
        self.SHP_zd_ID = list(self.SHP_zd["F_CODE_ID"])
        self.SHP_zrz_zdID = [str(i) for i in list(self.SHP_zrz["F_PARCEL_I"])]
        self.SHP_zrz_ID = [str(i) for i in list(self.SHP_zrz["F_CODE_ID"])]
        self.SHP_zrz_zcs = list(self.SHP_zrz["F_BUILDING"])
        self.SHP_zrz_zddm = list(self.SHP_zrz["F_UNDER_PA"])


    def check(self):
        self.getFied_value()

        for i in range(len(self.TZ)-1):
            temp = []
            if self.TZ_bdcdyh == "nan":
                temp.append("不动产单元号为空")
            else:
                if not (self.TZ_zddm[i] in list(self.SHP_zd["F_PARCEL_N"])):
                    temp.append("台账宗地代码在图形中找不到")
                if self.TZ_ywbh[i] == "nan":
                    temp.append("业务编号为空")
                else:
                    if not ((self.TZ_ywbh[i][:10] in self.SHP_zd_ywbh)):
                        temp.append("台账业务编号在图形中找不到：%s %s" % (self.TZ_ywbh[i][:10],self.TZ_bz[i]))
                if not (self.TZ_zcs[i] == self.TZ_zzc[i]):
                    temp.append("总层数与终止层不一致")
                if not ((self.TZ_qsc[i] + "-" + self.TZ_zzc[i]) == self.TZ_myc[i]):
                    temp.append("名义层不一致性")
                if not (self.TZ_zdmj[i] in self.SHP_zd_zdmj):
                    temp.append("台账宗地面积与图形宗地面积不一致")
                if self.TZ_zddm.count(self.TZ_zddm[i])>1:
                    temp.append("台账中宗地代码重复")

                if temp:
                    self.results["不动产单元代码"].append(self.TZ_bdcdyh[i])
                    self.results["问题"].append(str(temp))

            for i in range(len(self.TZ)-1):
                temp = []
                try:
                    zrz_index=self.SHP_zrz_zddm.index(self.SHP_zd_zddm[i])
                except ValueError:
                    temp.append("宗地代码在房屋图框中找不到")
                    continue
                try:
                    TZ_index=self.TZ_zddm.index(self.SHP_zd_zddm[i])
                except ValueError:
                    temp.append("宗地代码在台账中找不到")
                    continue

                if not (self.SHP_zrz_zdID[i] == self.SHP_zd_ID[zrz_index]):
                    temp.append("房屋中的宗地Id与宗地图层不一致")
                if not (self.SHP_zd_ywbh[i] == self.TZ_ywbh[TZ_index]):
                    temp.append("宗地图框业务编号与台账业务编号不一致")
                

        if self.results["问题"]:
            self.results = pd.DataFrame(self.results)
            self.results.to_excel(r"E:\工作文件\aaaaa\渝北区台账拆分\质检.xlsx")


if __name__ == "__main__":
    TZ = r"E:\工作文件\aaaaa\渝北区台账拆分\渝北区石船镇胆沟村存量成果台账（已上图）.xlsx"
    YSTZ = r"E:\工作文件\aaaaa\渝北区台账拆分\5个镇\石船镇台账.xlsx"
    SHP_zd = r"E:\工作文件\aaaaa\渝北区台账拆分\工作簿1.xlsx"
    check = TZcheck(TZ, YSTZ, SHP_zd)
    check.check()
    print(check.results)
