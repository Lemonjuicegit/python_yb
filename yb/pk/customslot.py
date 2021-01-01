from pk import mydocx, pycmd, key, fileutil
from threading import Thread
from pandas import read_excel


class Slot():

    def __init__(self):
        self.cmd = pycmd.Cmd()
        self.doc = mydocx.DocxUtil()
        self.results = None
        self.lic = key.licKey()
        self.save_path = ""
        self.execldata = fileutil.IoUtil()

    def key(self):
        return self.lic.lic()

    #   获取挂接表并检查身份证号码
    def setgjb_path(self, txet):
        self.gjb = txet
        self.execl_gjb = read_excel(txet, dtype=str)

        n = self.doc.checksfz(self.execl_gjb)
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
        hzbthread = slotThreadreturn(self.execldata.hzb, (self.gjb, self.save_path,))
        jzbthread = slotThreadreturn(self.execldata.jzb, (self.execl_gjb, self.save_path,))
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

    def lineEdit_3(self):
        self.results = "你输入了东西但是不会有什么用(*>﹏<*)"


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


if __name__ == '__main__':
    print("主进程开始")
