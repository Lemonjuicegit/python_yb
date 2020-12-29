from pk import customslot
import sys
import WinUI.exportGJ2
from PySide2.QtWidgets import QMainWindow, QApplication

slo = customslot.Slot()

# if slo.key():
#     exit()

# 程序界面生成
app = QApplication(sys.argv)
mainWindow = QMainWindow()
window = WinUI.exportGJ2.Ui_MainWindow()
window.setupUi(mainWindow)
mainWindow.setWindowIcon(WinUI.exportGJ2.QIcon(r".\image\icon.ico"))

def text():
    window.plainTextEdit.setPlainText(slo.results)

# 事件slot
window.lineEdit.textChanged.connect(slo.setsavepath)
window.lineEdit.textChanged.connect(text)
window.lineEdit_2.textChanged.connect(slo.setgjb_path)
window.lineEdit_2.textChanged.connect(text)
window.lineEdit_3.textChanged.connect(slo.lineEdit_3)
window.lineEdit_3.textChanged.connect(text)

window.pushButton.clicked.connect(slo.exf)
window.pushButton.clicked.connect(text)
window.pushButton_2.clicked.connect(slo.hzb)
window.pushButton_2.clicked.connect(text)
window.pushButton_3.clicked.connect(slo.jzb)
window.pushButton_3.clicked.connect(text)
window.pushButton_4.clicked.connect(slo.sms)
window.pushButton_4.clicked.connect(text)
window.pushButton_5.clicked.connect(slo.gjb_paper_files)
window.pushButton_5.clicked.connect(text)
window.pushButton_6.clicked.connect(slo.chjssms)
window.pushButton_6.clicked.connect(text)
window.pushButton_7.clicked.connect(slo.sdckb)
window.pushButton_7.clicked.connect(text)
window.pushButton_8.clicked.connect(slo.one_click)
window.pushButton_8.clicked.connect(text)
mainWindow.show()
sys.exit(app.exec_())
