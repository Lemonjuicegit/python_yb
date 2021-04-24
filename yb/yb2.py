from pk import customslot, fileutil, calculate
import sys
from WinUI import exportGJ3
from PySide2.QtWidgets import QApplication, QAction, QLineEdit, QPushButton, QComboBox, QPlainTextEdit


class run:
    def __init__(self):
        self.slot = customslot.Slot()
        self.slot2 = customslot.mass_detection_slot()
        self.app = QApplication(sys.argv)
        self.window = exportGJ3.Ui_MainWindow()
        self.tabeldata = {}
        self.widget = fileutil.read_json("yb.json")

    # 结果消息源
    def text(self):
        if self.slot.results != "":
            self.window.plainTextEdit.setPlainText(self.slot.results)
        if self.slot2.results != "":
            self.window.plainTextEdit.setPlainText(self.slot2.results)

    # 表控件数据源
    def data(self, header, data):
        self.tabeldata["data"] = data
        self.tabeldata["header"] = header

    # 删除一行表数据
    def d(self):
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

    # 生成检查记录下拉选项卡
    def qcombobox_item(self):
        for i in self.slot.collocation:
            if i == "nan":
                continue
            self.window.findChild(QComboBox, "qcombobox_1").addItem(i)

    # 查询添加宗地代码
    def select_event(self):
        self.window.slotdicts["pushbutton_2"] = [
            lambda: self.slot.insert(XZMC=self.window.findChild(QLineEdit, "lineEdit_6").text(),
                                     CM=self.window.findChild(
                                         QLineEdit, "lineEdit_7").text(),
                                     ZDDM_QS=self.window.findChild(
                                         QLineEdit, "lineEdit_8").text(),
                                     ZDDM_JS=self.window.findChild(
                                         QLineEdit, "lineEdit_9").text(),
                                     BMR=self.window.findChild(QLineEdit, "lineEdit_10").text()), self.text]
        header = ["id", "乡镇名称", "村名", "起始编码", "结束编码", "编码人", "地籍子区代码"]
        self.window.slotdicts["pushbutton_1"] = [
            lambda: self.slot.select(self.window.findChild(
                QLineEdit, "lineEdit_5").text()),
            lambda: self.data(header, self.slot.data),
            lambda: self.window.settabelvalue(self.window.tabelwidget_1, self.tabeldata), self.text]
        self.window.setevent(
            QPushButton, ["pushbutton_1", "pushbutton_2"], "clicked")
        self.window.tabelwidget_1.customContextMenuRequested.connect(
            lambda: self.window.foraddction(menueventlist={"删除": [self.d, self.text]}))

    def input1(self):
        self.window.setevent(
            QLineEdit, ["lineEdit_2", "lineEdit_1"], "textChanged")

    # 检查exf
    def exf(self):
        self.window.qualitychecking()
        self.qcombobox_item()
        header = ["宗地代码", "权利人姓名", "宗地面积对比", "宗地代码个数", ]
        self.window.slotdicts["lineEdit_3"] = [
            self.slot2.getpaper_path, self.text]
        self.window.slotdicts["lineEdit_4"] = [
            self.slot2.getdata_path, self.text]
        self.window.slotdicts["lineEdit_11"] = [
            self.slot2.getTZ_path, self.text]
        self.window.slotdicts["qcombobox_1"] = [self.slot.getcollocation,
                                                lambda: self.data(
                                                    self.slot.collocation[self.window.findChild(QComboBox,
                                                                                                "qcombobox_1").currentText()].keys(),
                                                    self.slot.collocation[self.window.findChild(QComboBox,
                                                                                                "qcombobox_1").currentText()]),
                                                lambda: self.window.settabelvalue(self.window.tabelwidget_2,
                                                                                  self.tabeldata)]
        self.window.slotdicts["pushbutton_3"] = [self.slot2.exf,
                                                 lambda: self.data(
                                                     self.slot2.results.keys(), self.slot2.results),
                                                 lambda: self.window.settabelvalue(self.window.tabelwidget_2,
                                                                                   self.tabeldata),
                                                 self.slot.getcollocation,
                                                 self.qcombobox_item]  # exf检查
        self.window.slotdicts["pushbutton_4"] = [lambda: self.slot.emptydata({}), self.slot.getcollocation,
                                                 self.qcombobox_item]  # 清空记录
        self.window.slotdicts["pushbutton_6"] = [self.slot2.TZqualitychecking]
        self.window.setevent(QComboBox, ["qcombobox_1"], "currentIndexChanged")
        self.window.setevent(
            QLineEdit, ["lineEdit_3", "lineEdit_4", "lineEdit_11"], "textChanged")
        self.window.setevent(
            QPushButton, ["pushbutton_3", "pushbutton_4", "pushbutton_6"], "clicked")

    # 计算分摊面积点击事件
    def ratio_areaslot(self):
        self.window.slotdicts["pushbutton_7"] = [self.ratio_area, self.text]
        self.window.setevent(QPushButton, ["pushbutton_7"], "clicked")

    # 计算分摊面积
    def ratio_area(self):
        text = self.window.findChild(QLineEdit, "lineEdit_12").text()
        share_area = text.split(",")[0]
        share_area = share_area.split(" ")
        share_area = [float(i) for i in share_area]
        area_list = text.split(",")[1]
        area_list = area_list.split(" ")
        area_list = [float(i) for i in area_list]
        ratio_area = calculate.share_area(share_area, area_list)
        self.slot.results = str(ratio_area)

    # 提取文件名和文件夹名事件
    def extract_file_name(self):
        self.window.slotdicts["lineEdit_14"] = [self.slot.paper_path]
        self.window.slotdicts["pushbutton_8"] = [
            self.slot.extract_file_name, self.text]
        self.window.setevent(QLineEdit, ["lineEdit_14"], "textChanged")
        self.window.setevent(QPushButton, ["pushbutton_8"], "clicked")

    # 渝北项目存量图片资料改名事件
    def yb_rename(self):
        self.window.slotdicts["lineEdit_17"] = [self.slot.set_TZ_path]
        self.window.slotdicts["lineEdit_18"] = [self.slot.set_picture_path]
        self.window.slotdicts["lineEdit_19"] = [self.slot.setsavepath]
        self.window.slotdicts["pushbutton_16"] = [
            self.slot.yb_rename, self.text]
        self.window.setevent(
            QLineEdit, ["lineEdit_17", "lineEdit_18", "lineEdit_19"], "textChanged")
        self.window.setevent(QPushButton, ["pushbutton_16"], "clicked")

    #
    def input_3Slot(self):
        self.window.slotdicts["lineEdit_15"] = [
            self.slot.setlineEdit_15Text, self.text]
        self.window.slotdicts["lineEdit_16"] = [
            self.slot.setlineEdit_16Text, self.text]
        self.window.slotdicts["pushbutton_10"] = [lambda: self.slot.re_search(self.window.findChild(QPlainTextEdit,
                                                                                                    "plainTextEdit_1").toPlainText()),
                                                  self.text]
        self.window.slotdicts["pushbutton_11"] = [lambda: self.slot.pushbutton_11Slot(self.window.findChild(QPlainTextEdit,
                                                                                                            "plainTextEdit_1").toPlainText()),
                                                  self.text]
        self.window.slotdicts["pushbutton_12"] = [
            self.slot.pushbutton_12Slot, self.text]
        self.window.slotdicts["pushbutton_13"] = [
            self.slot.pushbutton_13Slot, self.text]
        self.window.slotdicts["pushbutton_14"] = [
            self.slot.pushbutton_14Slot, self.text]
        self.window.slotdicts["pushbutton_15"] = [
            lambda: self.slot.pushbutton_15Slot(self.window.findChild(QPlainTextEdit,
                                                                      "plainTextEdit").toPlainText()), self.text]
        self.window.slotdicts["pushbutton_17"] = [
            lambda: self.slot.pushbutton_17Slot(self.window.findChild(QPlainTextEdit,
                                                                      "plainTextEdit").toPlainText()), self.text]
        self.window.slotdicts["pushbutton_18"] = [
            lambda: self.slot.pushbutton_18Slot(self.window.findChild(QPlainTextEdit,
                                                                      "plainTextEdit").toPlainText()), self.text]
        self.window.setevent(
            QLineEdit, ["lineEdit_15", "lineEdit_16"], "textChanged")
        self.window.setevent(QPushButton,
                             ["pushbutton_10", "pushbutton_11", "pushbutton_12", "pushbutton_13", "pushbutton_14",
                              "pushbutton_15", "pushbutton_17", "pushbutton_18"], "clicked")

    def tableAccountQualityInspection(self):
        self.window.slotdicts["lineEdit_20"] = [self.slot.TZpath]
        self.window.slotdicts["lineEdit_21"] = [self.slot.ShpZdPath]
        self.window.slotdicts["lineEdit_22"] = [self.slot.YstzPath]
        self.window.slotdicts["lineEdit_23"] = [self.slot.errorSaving]
        self.window.slotdicts["pushbutton_19"] = [
            self.slot.TZcheckSlot, self.text]

        self.window.setevent(QLineEdit, [
                             "lineEdit_20", "lineEdit_21", "lineEdit_22", "lineEdit_23"], "textChanged")
        self.window.setevent(QPushButton, ["pushbutton_19"], "clicked")

    def execlMergeEvent(self):
        self.window.slotdicts["lineEdit_24"] = [self.slot.setlineEdit_24Text,self.text]
        self.window.slotdicts["pushbutton_20"] = [lambda: self.slot.mergeWorkbook(
            self.window.findChild(QPlainTextEdit, "plainTextEdit_2").toPlainText()),self.text]
        self.window.slotdicts["pushbutton_21"] = []
        self.window.slotdicts["pushbutton_22"] = []
        self.window.slotdicts["pushbutton_23"] = []
        self.window.setevent(QLineEdit, ["lineEdit_24"], "textChanged")
        self.window.setevent(QPushButton, [
                             "pushbutton_20", "pushbutton_21", "pushbutton_22", "pushbutton_23"], "clicked")

    def event_init(self):
        self.window.treeslotdict["导出资料"] = [self.window.input_1, self.input1]
        self.window.treeslotdict["exf和台账检查"] = [self.exf]
        self.window.treeslotdict["查询宗地代码"] = [
            self.window.input_2, self.select_event]
        self.window.treeslotdict["分摊面积计算"] = [
            self.window.ratio_area, self.ratio_areaslot]
        self.window.treeslotdict["提取文件名和文件夹名"] = [
            self.window.file_name, self.extract_file_name]
        self.window.treeslotdict["正则搜索与复制"] = [
            self.window.file_slect, self.input_3Slot]
        self.window.treeslotdict["渝北项目存量图片资料改名"] = [
            self.window.input_3, self.yb_rename]
        self.window.treeslotdict["台账与矢量图框检查"] = [
            self.window.input_4, self.tableAccountQualityInspection]
        self.window.treeslotdict["excel表合并与拆分"] = [self.window.execlMerge,self.execlMergeEvent]

        self.window.slotdicts["lineEdit_1"] = [
            self.slot.setgjb_path, self.text]
        self.window.slotdicts["lineEdit_2"] = [
            self.slot.setsavepath, self.text]
        self.window.setevent(
            QLineEdit, ["lineEdit_2", "lineEdit_1"], "textChanged")

        self.window.slotdicts["action_1"] = [self.slot.exf, self.text]
        self.window.slotdicts["action_2"] = [self.slot.hzb, self.text]
        self.window.slotdicts["action_3"] = [self.slot.jzb, self.text]
        self.window.slotdicts["action_4"] = [self.slot.sms, self.text]
        self.window.slotdicts["action_5"] = [
            self.slot.gjb_paper_files, self.text]
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
