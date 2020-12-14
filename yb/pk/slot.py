import pk.ioutil
import socket
import pk.mydocx
import pk.pycmd


class Slot():
    iof = pk.ioutil.IoUtil()
    doc = pk.mydocx.DocxUtil()
    cmd = pk.pycmd.Cmd()

    def key(self):  # 加密方法
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        k = 1
        n = 0
        while n < len(ip):
            try:
                k = k * ord(name[n]) + ord(ip[n])
                n += 1
            except IndexError:
                break
        return k != 18670669457275772672

    def setgjb_path(self, txet):
        self.iof.gjb_path = txet

    def exf(self):
        self.iof.exf()

    def hzb(self):
        self.iof.hzb()

    def jzb(self):
        self.iof.jzb()

    def sms(self):
        self.doc.getsms(gjb_path=self.iof.gjb_path, save_path=self.iof.save_path, jpg_path=self.jpg_path)

    #   批量生成文件夹
    def gjb_paper_files(self):
        zddm_xm=[]
        zddm = self.iof.list_excel("宗地代码")
        xm = self.iof.list_excel("姓名")
        i=0
        while i<len(zddm):
            zddm_xm.append(zddm[i]+xm[i])
            i+=1
        self.cmd.paper_files(self.iof.save_path,zddm_xm)

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
