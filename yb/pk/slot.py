from pk import mydocx, pycmd, key, decoratorsFunc
from multiprocessing import Process, Queue


class Slot():

    def __init__(self):
        self.cmd = pycmd.Cmd()
        self.doc = mydocx.DocxUtil()
        self.results = None
        self.lic = key.licKey()
        self.save_path = ""

    def key(self):
        return self.lic.lic()

    #   获取挂接表并检查身份证号码
    def setgjb_path(self, txet):
        self.doc.execldata.gjb_path = txet

        n = self.doc.checksfz()
        if n == []:
            self.results = r"(*>﹏<*)"
        elif len(n) == 1:
            self.results = str(n)
        elif isinstance(n, str):
            self.results = n
        else:
            self.results = "\n".join(n)

    def exf(self):
        self.results = self.doc.execldata.exf(self.save_path)

    def hzb(self):
        self.results = self.doc.execldata.hzb(self.save_path)

    def jzb(self):
        self.results = self.doc.execldata.jzb(self.save_path)

    def sms(self):
        self.results = self.doc.getsmss(save_path=self.save_path)

    #   批量生成文件夹
    def gjb_paper_files(self):
        zddm_xm = []
        zddm = self.doc.execldata.list_excel("宗地代码")
        xm = self.doc.execldata.list_excel("姓名")
        i = 0
        while i < len(zddm):
            zddm_xm.append(zddm[i] + xm[i])
            i += 1
        self.cmd.paper_files(self.save_path, zddm_xm)

        self.results = "%s个文件夹创建成果" % i

    #   房产面积测算说明书
    def chjssms(self):
        self.results = self.doc.getchjssms(self.doc.execldata.save_path)

    #   不动产实地查看记录表
    def sdckb(self):
        self.results = self.doc.getsdckb(self.doc.execldata.save_path)

    # def one_click(self):
    #     pp=Pool()
    #     pp.apply_async(func=self.doc.getsmss,args=(self.doc.execldata.save_path,))
    #     pp.apply_async(func=self.doc.getsmss,args=(self.doc.execldata.save_path,))
    #     pp.apply_async(func=self.doc.getchjssms, args=(self.doc.execldata.save_path,))
    #     pp.apply_async(func=self.doc.getsdckb, args=(self.doc.execldata.save_path,))
    #     pp.apply_async(func=self.doc.execldata.exf, args=(self.doc.execldata.save_path,))
    #     pp.apply_async(func=self.doc.execldata.jzb, args=(self.doc.execldata.save_path,))
    #     pp.apply_async(func=self.doc.execldata.hzb, args=(self.doc.execldata.save_path,))
    #     pp.close()
    #     pp.join()

    def setsavepath(self, text):
        if self.cmd.isdir(text):
            self.save_path = text
            self.results = r"(*>﹏<*)"
        else:
            self.results = "请输入保存路径！"

    def lineEdit_3(self):
        self.results = "你输入了东西但是不会有什么用(*>﹏<*)"


if __name__ == '__main__':
    print("主进程开始")

