from pk import customslot
import sys
from WinUI import exportGJ3
from PySide2.QtWidgets import QApplication, QAction, QLineEdit

slo = customslot.Slot()
slo2 = customslot.mass_detection_slot()

if slo.key():
    exit()


def text():
    if slo.results != "":
        window.plainTextEdit.setPlainText(slo.results)
    if slo2.results != "":
        window.plainTextEdit.setPlainText(slo2.results)


def data_select():
    window.tabeldata["data"] = slo.data


def select_event():
    window.findChild(QLineEdit, "lineEdit_5").textChanged.connect(slo.select)
    window.findChild(QLineEdit, "lineEdit_5").textChanged.connect(slo.data_select)
    window.findChild(QLineEdit, "lineEdit_5").textChanged.connect(data_select)
    window.findChild(QLineEdit, "lineEdit_5").textChanged.connect(text)


# 程序界面生成
app = QApplication(sys.argv)
window = exportGJ3.Ui_MainWindow()
window.treeslotdict["导出资料路径"] = window.input_1
window.treeslotdict["exf检查"] = window.exfutil
window.treeslotdict["查询宗地代码"] = [window.input_2, select_event]

window.tabeldata["header"] = ["乡镇名称", "村名", "起始编码", "结束编码", "编码人", "地籍子区代码"]
window.tabeldata["column"] = 6

# 事件slot
window.findChild(QLineEdit, "lineEdit_1").textChanged.connect(slo.setgjb_path)
window.findChild(QLineEdit, "lineEdit_1").textChanged.connect(text)
window.findChild(QLineEdit, "lineEdit_2").textChanged.connect(slo.setsavepath)
window.findChild(QLineEdit, "lineEdit_2").textChanged.connect(text)
window.slotdicts["lineEdit_3"] = [slo2.getdata_path, text]
window.slotdicts["lineEdit_4"] = [slo2.getdata_path, text]
window.slotdicts["pushbutton_1"] = [window.settabelvalue]

window.findChild(QAction, "action_1").triggered.connect(slo.exf)
window.findChild(QAction, "action_1").triggered.connect(text)
window.findChild(QAction, "action_2").triggered.connect(slo.hzb)
window.findChild(QAction, "action_2").triggered.connect(text)
window.findChild(QAction, "action_3").triggered.connect(slo.jzb)
window.findChild(QAction, "action_3").triggered.connect(text)
window.findChild(QAction, "action_4").triggered.connect(slo.sms)
window.findChild(QAction, "action_4").triggered.connect(text)
window.findChild(QAction, "action_5").triggered.connect(slo.gjb_paper_files)
window.findChild(QAction, "action_5").triggered.connect(text)
window.findChild(QAction, "action_6").triggered.connect(slo.chjssms)
window.findChild(QAction, "action_6").triggered.connect(text)
window.findChild(QAction, "action_7").triggered.connect(slo.sdckb)
window.findChild(QAction, "action_7").triggered.connect(text)
window.findChild(QAction, "action_8").triggered.connect(slo.one_click)
window.findChild(QAction, "action_8").triggered.connect(text)

window.show()
try:
    sys.exit(app.exec_())
finally:
    slo.connenct.close()
