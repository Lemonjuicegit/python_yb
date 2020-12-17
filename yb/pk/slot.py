from pk import ioutil, mydocx, pycmd, key


class Slot():

    def __init__(self):
        self.iof = ioutil.IoUtil()
        self.doc = mydocx.DocxUtil()
        self.cmd = pycmd.Cmd()
        self.value = None
        self.lic = key.licKey()
        self.jpg_path = ""

    def key(self):
        return self.lic.lic()


    def setgjb_path(self, txet):
        self.iof.gjb_path = txet

    def exf(self):
        self.value = self.iof.exf()
        self.value = self.iof.results

    def hzb(self):
        self.value = self.iof.hzb()
        self.value =self.iof.results

    def jzb(self):
        self.iof.jzb()
        self.value =self.iof.results

    def setjpgpath(self, text):
        self.jpg_path = text

    def sms(self):
        self.value = self.doc.getsms(gjb_path=self.iof.gjb_path, save_path=self.iof.save_path, jpg_path=self.jpg_path)

#   批量生成文件夹
    def gjb_paper_files(self):
        zddm_xm = []
        zddm = self.iof.list_excel("宗地代码")
        xm = self.iof.list_excel("姓名")
        i = 0
        while i < len(zddm):
            zddm_xm.append(zddm[i] + xm[i])
            i += 1
        self.cmd.paper_files(self.iof.save_path, zddm_xm)

        return i

#   房产面积测算说明书
    def chjssms(self):
        self.doc.getchjssms(self.iof.gjb_path)

#   不动产实地查看记录表
    def sdckb(self):
        self.doc.getsdckb(self.iof.gjb_path)

    def setsavepath(self, text):
        self.iof.save_path = text

    def setgjbpath(self, text):
        self.iof.gjb_path = text
