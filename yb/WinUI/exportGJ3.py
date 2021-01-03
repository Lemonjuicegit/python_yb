# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '导出工具2.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys

from PySide2.QtCore import *
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        width = QDesktopWidget().screenGeometry().width()
        height = QDesktopWidget().screenGeometry().height()
        self.setFixedSize(int(width * (2 / 3)), int(height * (2 / 3)))
        self.setWindowIcon(QIcon(r".\image\icon.ico"))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")


        self.frame_1= QFrame(self.centralwidget)
        self.frame_1.setObjectName(u"verticalLayoutWidget_1")
        sizePolicy_1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy_1.setHorizontalStretch(3)
        sizePolicy_1.setVerticalStretch(0)
        sizePolicy_1.setHeightForWidth(self.frame_1.sizePolicy().hasHeightForWidth())
        self.frame_1.setSizePolicy(sizePolicy_1)
        self.horizontalLayout_1 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_1 = QGridLayout(self.frame_1)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.gridLayout_1.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2 = QGridLayout(self.frame_1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        # 菜单栏
        menubar = self.menuBar()
        menu_1 = menubar.addMenu("文件")
        menu_1.setObjectName("文件")
        menu_2 = menubar.addMenu("功能")
        menu_2.setObjectName("功能")
        menu_3 = menubar.addMenu("帮助")
        menu_3.setObjectName("帮助")

        # 工具栏
        self.icon = [r".\image\exf.png", r".\image\hzb.png", r".\image\jzb.png", r".\image\sms.png",
                     r".\image\file.png", r".\image\jssms.png", r".\image\sdckb.png", r".\image\one.png"]
        self.action = ["action_1", "action_2", "action_3", "action_4", "action_5", "action_6", "action_7", "action_8"]
        self.actiontext = ["exf导出", "汇总表导出", "界址表导出", "测绘面积说明书导出", "资料文件夹生成", "技术说明书导出", "实地查看记录表导出", "一键全导"]
        self.toolbar(self.action, self.icon, self.actiontext)

        # tree
        self.treeslotdict = {}  # 与treedict类名称对应的点击事件，键为树节点名称，值为事件函数名称
        self.slotdicts = {"lineEdit_3": [self.passs,self.passs,] ,"lineEdit_4": [self.passs,self.passs]}  # 空间事件字典
        treedict = ["导出资料路径", {"质检": ["exf检查"]}, "查询宗地代码"]
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabel("功能区")
        self.settrees(self.tree, treedict)
        # 尺寸策略
        sizePolicy_2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy_2.setHorizontalStretch(1)
        sizePolicy_2.setVerticalStretch(0)
        sizePolicy_2.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy_2)

        self.tree.clicked.connect(self.treeslot)  # 事件
        self.horizontalLayout_1.addWidget(self.tree)



        line_1 = QFrame(self.centralwidget)
        line_1.setObjectName(u"line")
        line_1.setFrameShape(QFrame.VLine)
        line_1.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_1.addWidget(line_1)

        self.label_1()

        #   消息提醒标签

        label_3 = QLabel(self.frame_1)
        label_3.setObjectName(u"label_3")
        label_3.setText("消息：")
        self.gridLayout_1.addWidget(label_3,1,0,1,1)

        #   编辑框
        self.plainTextEdit = QPlainTextEdit(self.frame_1)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.gridLayout_1.addWidget(self.plainTextEdit,2,0,1,1)
        self.horizontalLayout_1.addWidget(self.frame_1)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.setWindowTitle(
            QCoreApplication.translate("MainWindow", "hahahahah", None))

        QMetaObject.connectSlotsByName(self)

    # 批量生成树节点
    def settrees(self, treewidget, treedcit={}):
        """
        @param treewidget: 树窗体
        @param treedcit: 树的字典
        """
        if isinstance(treedcit, dict):
            treelist = list(treedcit.keys())
            for tl in treelist:
                tree = QTreeWidgetItem(treewidget)
                tree.setText(0, tl)
                self.settrees(tree, treedcit[tl])
        else:
            for i in treedcit:
                if isinstance(i, dict):
                    self.settrees(treewidget, i)
                else:
                    tree = QTreeWidgetItem(treewidget)
                    tree.setText(0, i)

    def label_1(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        label_1 = QLabel(self.frame_1)
        label_1.setObjectName(u"label_1")
        label_1.setText("挂接表：")
        self.gridLayout_2.addWidget(label_1,0,0,1,1)

        lineEdit_1 = QLineEdit(self.frame_1)
        lineEdit_1.setObjectName(u"lineEdit_1")
        self.gridLayout_2.addWidget(lineEdit_1,0,1,1,1)


        label_2 = QLabel(self.frame_1)
        label_2.setObjectName(u"label_2")
        label_2.setText("保存到：")
        self.gridLayout_2.addWidget(label_2,1,0,1,1)

        lineEdit_2 = QLineEdit(self.frame_1)
        lineEdit_2.setObjectName(u"lineEdit_2")
        self.gridLayout_2.addWidget(lineEdit_2,1,1,1,1)
        self.gridLayout_1.addLayout(self.gridLayout_2,0,0,1,1)

    def exfutil(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        label_3 = QLabel(self.frame_1)
        label_3 .setObjectName(u"label")
        label_3 .setText("exf：")
        self.gridLayout_2.addWidget(label_3 , 0, 0, 1, 1)

        lineEdit_3 = QLineEdit(self.frame_1)
        lineEdit_3.setObjectName(u"lineEdit_3")
        self.gridLayout_2.addWidget(lineEdit_3, 0, 1, 1, 1)

        label_4 = QLabel(self.frame_1)
        label_4.setObjectName(u"label_2")
        label_4.setText("mdb：")
        self.gridLayout_2.addWidget(label_4, 1, 0, 1, 1)

        lineEdit_4 = QLineEdit(self.frame_1)
        lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout_2.addWidget(lineEdit_4, 1, 1, 1, 1)
        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.findChild(QLineEdit, "lineEdit_3").textChanged.connect(self.slotdicts["lineEdit_3"][0])
        self.findChild(QLineEdit, "lineEdit_3").textChanged.connect(self.slotdicts["lineEdit_3"][1])
        self.findChild(QLineEdit, "lineEdit_3").textChanged.connect(self.slotdicts["lineEdit_4"][0])
        self.findChild(QLineEdit, "lineEdit_3").textChanged.connect(self.slotdicts["lineEdit_4"][1])
    def label_2(self):
        pass

    def settreeslotdict(self, dict):
        self.treeslotdict = dict

    def treeslot(self):
        item = self.tree.currentItem()
        try:
            self.treeslotdict[item.text(0)]()
        except KeyError:
            pass

    def toolbar(self, action, icon, actiontext,name="tool"):
        tool = self.addToolBar(name)
        for i in range(len(action)):
            qaction = QAction(QIcon(icon[i]), actiontext[i], self)
            qaction.setObjectName(action[i])
            tool.addAction(qaction)

    def passs(self):
        pass




if __name__ == '__main__':
    def a():
        print("dianjile")

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.setWindowIcon(QIcon(r"..\image\icon.ico"))
    window.findChild(QAction, "action_1").triggered.connect(a)
    window.settreeslotdict({"导出资料路径": window.label_1,"exf检查":window.exfutil})

    window.show()
    try:
        sys.exit(app.exec_())
    finally:
        print("deedf")