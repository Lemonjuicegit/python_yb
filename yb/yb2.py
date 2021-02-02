from pk import customslot, fileutil
import sys
from WinUI import exportGJ3
from PySide2.QtWidgets import QApplication, QAction, QLineEdit, QPushButton, QComboBox


class run:
    def __init__(self):
        self.slot = customslot.Slot()
        self.slot2 = customslot.mass_detection_slot()
        self.app = QApplication(sys.argv)
        self.window = exportGJ3.Ui_MainWindow()
        self.tabeldata = {}
        self.widget = fileutil.read_json("yb.json")

    def text(self):
        if self.slot.results != "":
            self.window.plainTextEdit.setPlainText(self.slot.results)
        if self.slot2.results != "":
            self.window.plainTextEdit.setPlainText(self.slot2.results)

    def data(self, header, data):
        self.tabeldata["data"] = data
        self.tabeldata["header"] = header

    def a(self):
        temp = None
        remove = []
        for i in self.window.tabelwidget_1.selectionModel().selection().indexes():
            row = i.row()
            if row != temp:
                temp = row
                remove.append(temp)
                self.slot.delete(self.window.tabelwidget_1.item(row, 0).text())
        for r in remove:
            self.window.tabelwidget_1.removeRow(r)
        self.slot.results = "删除：%s条数据" % len(remove)

    def qcombobox_item(self):
        for i in self.slot.collocation:
            if i == "nan":
                continue
            self.window.findChild(QComboBox, "qcombobox_1").addItem(i)

    def select_event(self):
        self.window.slotdicts["pushbutton_2"] = [
            lambda: self.slot.insert(XZMC=self.window.findChild(QLineEdit, "lineEdit_6").text(),
                                     CM=self.window.findChild(QLineEdit, "lineEdit_7").text(),
                                     ZDDM_QS=self.window.findChild(QLineEdit, "lineEdit_8").text(),
                                     ZDDM_JS=self.window.findChild(QLineEdit, "lineEdit_9").text(),
                                     BMR=self.window.findChild(QLineEdit, "lineEdit_10").text()), self.text]
        header = ["id", "乡镇名称", "村名", "起始编码", "结束编码", "编码人", "地籍子区代码"]
        self.window.slotdicts["pushbutton_1"] = [
            lambda: self.slot.select(self.window.findChild(QLineEdit, "lineEdit_5").text()),
            lambda: self.data(header, self.slot.data),
            lambda: self.window.settabelvalue(self.window.tabelwidget_1, self.tabeldata), self.text]
        self.window.setevent(QPushButton, ["pushbutton_1", "pushbutton_2"], "clicked")
        self.window.tabelwidget_1.customContextMenuRequested.connect(
            lambda: self.window.foraddction(menueventlist={"删除": [self.a, self.text]}))

    def input1(self):
        self.window.setevent(QLineEdit, ["lineEdit_2", "lineEdit_1"], "textChanged")

    def exf(self):
        header = ["宗地代码", "权利人姓名", "宗地面积对比", "宗地代码个数"]
        self.window.slotdicts["lineEdit_3"] = [self.slot2.getpaper_path, self.text]
        self.window.slotdicts["lineEdit_4"] = [self.slot2.getdata_path, self.text]
        self.window.slotdicts["pushbutton_3"] = [self.slot2.exf, lambda: self.data(header, self.slot2.results),
                                                 lambda: self.window.settabelvalue(self.window.tabelwidget_2,
                                                                                   self.tabeldata), self.qcombobox_item]
        self.window.slotdicts["pushbutton_4"] = [self.slot.emptydata({}), self.qcombobox_item]

        self.window.slotdicts["qcombobox_1"] = [
            lambda: self.data(header, self.collocation[self.window.findChild(QComboBox, "qcombobox_1").currentText()]),
            lambda: self.window.settabelvalue(self.window.tabelwidget_2,
                                              self.tabeldata)]

        self.window.setevent(QComboBox, ["qcombobox_1"], "currentIndexChanged")
        self.window.setevent(QLineEdit, ["lineEdit_3", "lineEdit_4"], "textChanged")
        self.window.setevent(QPushButton, ["pushbutton_3"], "clicked")

    def event_init(self):
        self.window.treeslotdict["导出资料"] = [self.window.input_1, self.input1]
        self.window.treeslotdict["exf和台账检查"] = [self.window.exfutil, self.exf]
        self.window.treeslotdict["查询宗地代码"] = [self.window.input_2, self.select_event]

        self.window.slotdicts["lineEdit_1"] = [self.slot.setgjb_path, self.text]
        self.window.slotdicts["lineEdit_2"] = [self.slot.setsavepath, self.text]
        self.window.setevent(QLineEdit, ["lineEdit_2", "lineEdit_1"], "textChanged")

        self.window.slotdicts["action_1"] = [self.slot.exf, self.text]
        self.window.slotdicts["action_2"] = [self.slot.hzb, self.text]
        self.window.slotdicts["action_3"] = [self.slot.jzb, self.text]
        self.window.slotdicts["action_4"] = [self.slot.sms, self.text]
        self.window.slotdicts["action_5"] = [self.slot.gjb_paper_files, self.text]
        self.window.slotdicts["action_6"] = [self.slot.chjssms, self.text]
        self.window.slotdicts["action_7"] = [self.slot.sdckb, self.text]
        self.window.slotdicts["action_8"] = [self.slot.one_click, self.text]
        self.window.setevent(QAction, self.widget["action"], "triggered")

    def show(self):
        self.window.show()
        try:
            sys.exit(self.app.exec_())
        finally:
            try:
                self.slot.connenct.close()
            except AttributeError:
                pass


if __name__ == '__main__':
    window = run()
    window.event_init()
    window.show()
