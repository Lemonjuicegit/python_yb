import pk.slot
import sys
import WinUI.exportGJ2
from PySide2.QtWidgets import QMainWindow, QApplication


slo = pk.slot.Slot()

if slo.key():
    exit()

#程序界面生成
app = QApplication(sys.argv)
mainWindow = QMainWindow()
window = WinUI.exportGJ2.Ui_MainWindow()
window.setupUi(mainWindow)
mainWindow.setWindowIcon(WinUI.exportGJ2.QIcon("图标.ico"))

#事件slot
window.lineEdit.textChanged.connect(slo.setsavepath)
window.lineEdit_2.textChanged.connect(slo.setgjbpath)
window.lineEdit_3.textChanged.connect(slo.setjpgpath)

window.pushButton.clicked.connect(slo.exf)
window.pushButton_2.clicked.connect(slo.hzb)
window.pushButton_3.clicked.connect(slo.jzb)
window.pushButton_4.clicked.connect(slo.sms)
window.pushButton_5.clicked.connect(slo.gjb_paper_files)
window.pushButton_6.clicked.connect(slo.chjssms())
window.pushButton_7.clicked.connect(slo.sdckb())

mainWindow.show()
sys.exit(app.exec_())
