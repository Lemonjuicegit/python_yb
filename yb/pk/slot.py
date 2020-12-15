from pk import ioutil, mydocx, pycmd, key


class Slot():

    def __init__(self):
        self.iof = ioutil.IoUtil()
        self.doc = mydocx.DocxUtil()
        self.cmd = pycmd.Cmd()
        self.value = None

    def key(self):  # 加密方法
        return key.getkey() != 18670669457275772673

    def setgjb_path(self, txet):
        self.iof.gjb_path = txet

    def exf(self):
        self.value = self.iof.exf()

    def hzb(self):
        self.value = self.iof.hzb()

    def jzb(self):
        self.value = self.iof.jzb()

    def sms(self):
        self.doc.getsms(gjb_path=self.iof.gjb_path, save_path=self.iof.save_path, jpg_path=self.jpg_path)

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

    def chjssms(self):
        self.doc.getchjssms(self.iof.gjb_path)

    def sdckb(self):
        self.doc.getsdckb(self.iof.gjb_path)

    def setsavepath(self, text):
        self.iof.save_path = text

    def setgjbpath(self, text):
        self.iof.gjb_path = text

    def setjpgpath(self, text):
        self.jpg_path = text
