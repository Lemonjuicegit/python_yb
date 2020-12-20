from PySide2.QtCore import *
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
import os
import exportGJ3
class TreeWieget:
    def settreeWindow(self,mainWindow,excel={"":{"":[],"":[]},"":{"":[],"":[]}}):
        mainWindow.setObjectName(u"MainWindow")
        # mainWindow.resize(690, 460)
        mainWindow.setFixedSize(680, 460)
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 661, 440))
        self.horizontalLayout = QHBoxLayout(self.gridLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        exp=exportGJ3.Ui_MainWindow()
        self.exp=exp.setupUi(self.gridLayoutWidget)

        self.tree=QTreeWidget(self.gridLayoutWidget)

        for key1 in list(excel.keys()):
            __qtreewidgetitem=self.settree(self.tree,key1)
            for key2 in list(excel[key1].keys()):
                __qtreewidgetitem_1 = self.settree(__qtreewidgetitem, key2)
                for key3 in list(excel[key1][key2]):
                    self.settree(__qtreewidgetitem_1, key3)

        self.horizontalLayout.addWidget(self.tree)
        self.table =QTableView(self.gridLayoutWidget)
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addLayout(self.exp)





        # self.tree.setHeaderItem(__qtreewidgetitem_1)


        mainWindow.setCentralWidget(self.centralwidget)

    def settree(self,tree,name):
        __qtreewidgetitem = QTreeWidgetItem(tree)
        __qtreewidgetitem.setText(0, name)
        return __qtreewidgetitem

if __name__ == '__main__':
    app = QApplication(os.sys.argv)
    mainWindow = QMainWindow()
    window = TreeWieget()
    window.settreeWindow(mainWindow)

    mainWindow.show()
    os.sys.exit(app.exec_())













