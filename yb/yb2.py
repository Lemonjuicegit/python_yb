from pk import customslot
import sys
from WinUI import exportGJ3
from PySide2.QtWidgets import QApplication, QAction, QLineEdit

slo = customslot.Slot()
slo2 = customslot.mass_detection_slot()

if slo.key():
    exit()

# 程序界面生成
app = QApplication(sys.argv)
window = exportGJ3.Ui_MainWindow()
window.settreeslotdict({"导出资料路径": window.label_1, "exf检查": window.exfutil})


def text():
    if slo.results!="":
        window.plainTextEdit.setPlainText(slo.results)
    if slo2.results!="":
        window.plainTextEdit.setPlainText(slo2.results)

# 事件slot
window.findChild(QLineEdit, "lineEdit_1").textChanged.connect(slo.setgjb_path)
window.findChild(QLineEdit, "lineEdit_1").textChanged.connect(text)
window.findChild(QLineEdit, "lineEdit_2").textChanged.connect(slo.setsavepath)
window.findChild(QLineEdit, "lineEdit_2").textChanged.connect(text)
window.slotdicts["lineEdit_3"] = [slo2.getdata_path, text]
window.slotdicts["lineEdit_4"] = [slo2.getdata_path, text]

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
sys.exit(app.exec_())
