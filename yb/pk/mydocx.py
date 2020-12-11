from docx import Document
from docx.shared import Cm
import pk.ioutil


class DocxUtil():

    def __init__(self, path=r"模板\房产面积测算说明书.docx"):
        self.docx = Document(path)

    def makevalue(self, paragraph: int, runs: int, value, string):
        para = self.docx.paragraphs
        para[paragraph].runs[runs].text = para[paragraph].runs[runs].text.replace(value, string)

    def maketablevalue(self, table: int, columu: int, row: int, paragraph: int, runs: int, value: str, string: str):
        self.docx.tables[table].cell(columu, row).paragraphs[paragraph].runs[runs].text = \
            self.docx.tables[table].cell(columu, row).paragraphs[paragraph].runs[
                runs].text.replace(value, string)

    def addtablevalue(self, table: int, columu: int, row: int, paragraph: int, value):  # 向
        self.docx.tables[table].cell(columu, row).paragraphs[paragraph].text = value

        #   房产面积测算说明书
    def getsms(self, gjb_path, jpg_path):
        execldata = pk.ioutil.IoUtil(gjb_path=gjb_path)

        for i in range(1, len(execldata.list_excel("宗地代码"))):
            self.docx = Document(r"模板\房产面积测算说明书.docx")
            value = execldata.row_excel(i)

            #   转换日期数据格式
            value[5] = value[5][:4] + "年" + value[5][5:7] + "月" + value[5][8:10] + "日"
            value[4] = value[4][:4] + "年" + value[4][5:7] + "月" + value[4][8:10] + "日"

            self.makevalue(0, 0, "F00010001", value[1])  # 不动产单元号：F00010001
            self.makevalue(11, 1, "xxx", value[2])  # 委托测绘的房屋名称：xxx
            self.makevalue(12, 1, "xxx", value[26])  # 委托测绘的房屋地址：xxx
            self.makevalue(20, 0, "2020年11月23日", value[4])
            self.makevalue(49, 3, "xx", value[2])  # 规划批准项目名称：  xx
            self.makevalue(50, 3, "xx", value[2])  # 本次申请测绘的楼盘（组团）名称：  xx
            self.makevalue(55, 1, "aa", str(value[17]))  # 总建筑面积为：aa平方米
            self.makevalue(55, 3, "bb", str(value[16]))  # 建筑占地面积为：bb平方米
            self.makevalue(57, 0, "xxx", value[33])  #
            if str(value[8]) != "nan":
                self.makevalue(65, 1, "x", value[8])  # 根据委托方提供乡村建设规划许可证及附件，x
            else:
                self.makevalue(65, 1, "x", "")
            self.makevalue(106, 2, "xxx", value[2])  # 建筑物名称:xxx
            self.makevalue(109, 2, "xxx", value[2])  # 建筑物名称: xxx
            self.makevalue(112, 2, "xxx", value[2])  # 建筑物名称: xxx
            self.makevalue(116, 2, "xxx", value[4])  # 计算者：  xxx
            self.makevalue(117, 1, "xxx", value[4])  # 制表日期：xxx
            self.makevalue(118, 0, "苏航", value[2])  # 苏航(近景)
            self.makevalue(120, 0, "苏航", value[2])  # 苏航(远景)

            self.maketablevalue(0, 0, 0, 1, 1, "2020年11月23日", value[4])  # 检查日期：   2020年11月23日
            self.maketablevalue(0, 0, 0, 3, 0, "2020年11月25日", value[5])  # 检查日期：   2020年11月25日
            self.maketablevalue(0, 1, 0, 1, 2, "2020年11月25日", value[5])  # 检查日期：   2020年11月25日

            self.maketablevalue(1, 0, 3, 0, 0, "xxx", value[0])  # 宗地号
            self.maketablevalue(1, 0, 6, 0, 0, "xx", value[2])  # 建筑物名称
            self.maketablevalue(1, 1, 3, 0, 0, "xxx", value[7])  # 地址
            self.maketablevalue(1, 4, 3, 0, 0, "xxx", value[16])  # 基底面积
            self.maketablevalue(1, 5, 3, 0, 0, "xxx", value[17])  # 总建筑面积
            self.maketablevalue(1, 5, 6, 0, 0, "xxx", value[22])  # 地面以上层数
            self.maketablevalue(1, 6, 3, 0, 0, "xxx", value[17])  # 地面以上面积
            # self.maketablevalue(1, 9, 3, 0, 0, "xxx", value[17])  # 共用建筑面积总计

            i = 18
            fcmj = []
            while str(value[i]) != "nan":
                fcmj.append(str(value[i]))
                i += 1
            for i in range(0, len(fcmj)):
                self.addtablevalue(2, 1 + i, 0, 0, "第1幢 第" + str(i + 1) + "层")  # 第一列
                self.addtablevalue(2, 1 + i, 1, 0, fcmj[i])  # 第二列
                self.addtablevalue(2, 1 + i, 2, 0, fcmj[i] + "*1")  # 第三列
            self.addtablevalue(2, 29, 1, 0, value[17])
            for i in range(0, len(fcmj)):
                self.addtablevalue(4, 1 + i, 0, 0, r"第1")  # 第一列
                self.addtablevalue(4, 1 + i, 1, 0, r"/")  # 第二列
                self.addtablevalue(4, 1 + i, 2, 0, "第" + str(i + 1))  # 第三列
                self.addtablevalue(4, 1 + i, 3, 0, "1")  # 第四列
                self.addtablevalue(4, 1 + i, 4, 0, fcmj[i])  # 第五列
                self.addtablevalue(4, 1 + i, 5, 0, "0")  # 第六列
                self.addtablevalue(4, 1 + i, 6, 0, "0")  # 第七列
                self.addtablevalue(4, 1 + i, 7, 0, fcmj[i])  # 第八列
                self.addtablevalue(4, 1 + i, 8, 0, "1")  # 第九列
            self.addtablevalue(4, 24, 4, 0, value[17])
            self.addtablevalue(4, 24, 7, 0, value[17])
            self.setjpg(jpg_path + "\\" + value[0] + value[2] + "\\" + "近景.jpg",
                        jpg_path + "\\" + value[0] + value[2] + "\\" + "远景.jpg")

            # self.docx.save(execldata.save_path+value[0]+"房产面积测算说明书.doc")
            self.docx.save(value[0] + "房产面积测算说明书.doc")

        #   不动产实地查看记录表
    def getsdckb(self,gjb_path):
        pass

        #   农村宅基地使用权及房屋所有权测绘技术说明
    def getchjssms(self,gjb_path):
        pass


    def setjpg(self, path_JJ, path_YJ):
        self.docx.paragraphs[119].add_run().add_picture(path_JJ, width=Cm(14))
        self.docx.add_picture(path_YJ, width=Cm(14))
