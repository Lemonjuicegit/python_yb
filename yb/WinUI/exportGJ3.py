import sys
from PySide2.QtCore import *
from PySide2.QtGui import QIcon, QCursor
from PySide2.QtWidgets import *
from pk.fileutil import read_json

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.collocation = read_json("yb.json")
        self.icon = self.collocation["icon"]  # 工具图标
        self.action = self.collocation["action"]
        self.actiontext = self.collocation["actiontext"]
        self.treeslotdict = {}  # 与treedict类名称对应的点击事件，键为树节点名称，值为事件函数名称
        self.slotdicts = {}  # 空间事件字典
        self.treedict = self.collocation["tree"]

        self.setupUI()

    def setupUI(self):
        width = QDesktopWidget().screenGeometry().width()
        height = QDesktopWidget().screenGeometry().height()
        self.setFixedSize(int(width * (2 / 3)), int(height * (2 / 3)))
        self.setWindowIcon(QIcon(r".\image\icon.ico"))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frame_1 = QFrame(self)
        self.frame_1.setObjectName(u"frame_1")
        sizePolicy_1 = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy_1.setHorizontalStretch(3)
        sizePolicy_1.setVerticalStretch(0)
        sizePolicy_1.setHeightForWidth(
            self.frame_1.sizePolicy().hasHeightForWidth())
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
        menujsonObjectName = 0
        actionjsonObjectName = 0
        for menubarjson in self.collocation["menubar"].keys():
            menu = menubar.addMenu(menubarjson)
            menu.setObjectName("menu_" + str(menujsonObjectName))
            for actionjson in self.collocation["menubar"][menubarjson].keys():
                if self.collocation["menubar"][menubarjson][actionjson] != {}:
                    action = QAction(
                        QIcon(self.collocation["menubar"][menubarjson][actionjson]), actionjson, self)
                    action.setObjectName("menu_%saction_%s" % (
                        actionjsonObjectName, actionjsonObjectName))
                    menu.addAction(action)

        # 工具栏
        self.toolbar(self.action, self.icon, self.actiontext)

        # tree
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabel("功能区")
        self.settrees(self.tree, self.treedict)

        # 尺寸策略
        sizePolicy_2 = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy_2.setHorizontalStretch(1)
        sizePolicy_2.setVerticalStretch(0)
        sizePolicy_2.setHeightForWidth(
            self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy_2)

        self.tree.clicked.connect(self.treeslot)  # 事件
        self.horizontalLayout_1.addWidget(self.tree)

        line_1 = QFrame(self)
        line_1.setObjectName(u"line_1")
        line_1.setFrameShape(QFrame.VLine)
        line_1.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_1.addWidget(line_1)

        self.input_1()

        #   消息提醒标签
        label_8 = QLabel(self.frame_1)
        label_8.setObjectName(u"label_8")
        label_8.setText("消息：")
        self.gridLayout_1.addWidget(label_8, 1, 0, 1, 1)

        #   编辑框
        self.plainTextEdit = QPlainTextEdit(self.frame_1)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.gridLayout_1.addWidget(self.plainTextEdit, 2, 0, 1, 1)
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

    # 导出资料
    def input_1(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        label_1 = QLabel(self.frame_1)
        label_1.setObjectName(u"label_1")
        label_1.setText("挂接表：")
        self.gridLayout_2.addWidget(label_1, 0, 0, 1, 1)

        lineEdit_1 = QLineEdit(self.frame_1)
        lineEdit_1.setObjectName(u"lineEdit_1")
        self.gridLayout_2.addWidget(lineEdit_1, 0, 1, 1, 1)

        label_2 = QLabel(self.frame_1)
        label_2.setObjectName(u"label_2")
        label_2.setText("保存到：")
        self.gridLayout_2.addWidget(label_2, 1, 0, 1, 1)

        lineEdit_2 = QLineEdit(self.frame_1)
        lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_2.addWidget(lineEdit_2, 1, 1, 1, 1)
        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    # 质量检查
    def qualitychecking(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        pushbutton_3 = QPushButton("开始exf检查")
        pushbutton_3.setObjectName("pushbutton_3")

        qcombobox_1 = QComboBox(self.frame_1)  # 质检结果保存的下拉菜单
        qcombobox_1.setObjectName("qcombobox_1")

        pushbutton_4 = QPushButton("清空记录")
        pushbutton_4.setObjectName("pushbutton_4")

        pushbutton_5 = QPushButton("一键检查")
        pushbutton_5.setObjectName("pushbutton_5")

        pushbutton_6 = QPushButton("台账检查")
        pushbutton_6.setObjectName("pushbutton_6")

        label_3 = QLabel(self.frame_1)
        label_3.setObjectName(u"label_3")
        label_3.setText("exf目录：")

        lineEdit_3 = QLineEdit(self.frame_1)
        lineEdit_3.setObjectName(u"lineEdit_3")

        label_6 = QLabel(self.frame_1)
        label_6.setObjectName(u"label_6")
        label_6.setText("台账：")

        lineEdit_11 = QLineEdit(self.frame_1)
        lineEdit_11.setObjectName(u"lineEdit_11")

        label_4 = QLabel(self.frame_1)
        label_4.setObjectName(u"label_4")
        label_4.setText("mdb数据表：")

        lineEdit_4 = QLineEdit(self.frame_1)
        lineEdit_4.setObjectName(u"lineEdit_4")

        self.tabelwidget_2 = QTableWidget(self)
        self.tabelwidget_2.setObjectName("tabelwidget_2")

        self.gridLayout_2.addWidget(pushbutton_3, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_5, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(qcombobox_1, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_4, 4, 1, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_6, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(label_3, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_3, 1, 1, 1, 7)
        self.gridLayout_2.addWidget(label_6, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_11, 3, 1, 1, 7)
        self.gridLayout_2.addWidget(label_4, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_4, 2, 1, 1, 7)
        self.gridLayout_2.addWidget(self.tabelwidget_2, 5, 0, 1, 8)

        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    # 查询宗地代码
    def input_2(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        self.tabelwidget_1 = QTableWidget(self)
        self.tabelwidget_1.setObjectName("tabelwidget_1")

        label_5 = QLabel(self.frame_1)
        label_5.setObjectName("label_5")
        label_5.setText("查询：")
        label_7 = QLabel(self.frame_1)
        label_7.setObjectName("label_7")
        label_7.setText("添加：")
        lineEdit_5 = QLineEdit(self.frame_1)
        lineEdit_5.setObjectName(u"lineEdit_5")
        lineEdit_6 = QLineEdit(self.frame_1)
        lineEdit_6.setObjectName(u"lineEdit_6")
        lineEdit_6.setPlaceholderText("乡镇名称")
        lineEdit_7 = QLineEdit(self.frame_1)
        lineEdit_7.setObjectName(u"lineEdit_7")
        lineEdit_7.setPlaceholderText("村名")
        lineEdit_8 = QLineEdit(self.frame_1)
        lineEdit_8.setObjectName(u"lineEdit_8")
        lineEdit_8.setPlaceholderText("起始编码")
        lineEdit_9 = QLineEdit(self.frame_1)
        lineEdit_9.setObjectName(u"lineEdit_9")
        lineEdit_9.setPlaceholderText("结束编码")
        lineEdit_10 = QLineEdit(self.frame_1)
        lineEdit_10.setObjectName(u"lineEdit_10")
        lineEdit_10.setPlaceholderText("编码人")
        pushbutton_1 = QPushButton(self.frame_1)
        pushbutton_1.setObjectName("pushbutton_1")
        pushbutton_1.setText("确定")
        pushbutton_2 = QPushButton(self.frame_1)
        pushbutton_2.setObjectName("pushbutton_2")
        pushbutton_2.setText("确定")

        self.gridLayout_2.addWidget(label_5, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_5, 0, 1, 1, 5)
        self.gridLayout_2.addWidget(pushbutton_1, 0, 6, 1, 1)
        self.gridLayout_2.addWidget(label_7, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_6, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_7, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_8, 1, 3, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_9, 1, 4, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_10, 1, 5, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_2, 1, 6, 1, 1)
        self.gridLayout_2.addWidget(self.tabelwidget_1, 2, 0, 1, 7)
        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabelwidget_1.setContextMenuPolicy(Qt.CustomContextMenu)

    # 分摊面积计算
    def ratio_area(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        label_9 = QLabel(self.frame_1)
        label_9.setObjectName("label_9")
        label_9.setText("共用面积列表：")
        lineEdit_12 = QLineEdit(self.frame_1)
        lineEdit_12.setPlaceholderText("共用：面积1 面积2 面积3 。。。，独用：面积1 面积2 面积3 。。。")
        lineEdit_12.setObjectName("lineEdit_12")

        pushbutton_7 = QPushButton(self.frame_1)
        pushbutton_7.setObjectName("pushbutton_7")
        pushbutton_7.setText("计算")
        self.gridLayout_2.addWidget(label_9, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_12, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_7, 0, 2, 1, 1)
        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    # 提取文件名和文件夹名
    def file_name(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        pushbutton_8 = QPushButton(self.frame_1)
        pushbutton_8.setObjectName("pushbutton_8")
        pushbutton_8.setText("提取文件名")
        pushbutton_9 = QPushButton(self.frame_1)
        pushbutton_9.setObjectName("pushbutton_9")
        pushbutton_9.setText("提取文件夹名")
        label_10 = QLabel(self.frame_1)
        label_10.setObjectName("label_10")
        label_10.setText("提取的文件夹：")
        lineEdit_14 = QLineEdit(self.frame_1)
        lineEdit_14.setObjectName(u"lineEdit_14")

        self.gridLayout_2.addWidget(pushbutton_8, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_9, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(label_10, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_14, 1, 1, 1, 10)

        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    def file_slect(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        pushbutton_10 = QPushButton(self.frame_1)
        pushbutton_10.setObjectName("pushbutton_10")
        pushbutton_10.setText("正则查找")
        pushbutton_11 = QPushButton(self.frame_1)
        pushbutton_11.setObjectName("pushbutton_11")
        pushbutton_11.setText("一般查找")
        pushbutton_12 = QPushButton(self.frame_1)
        pushbutton_12.setObjectName("pushbutton_12")
        pushbutton_12.setText("提取所有文件名")
        pushbutton_13 = QPushButton(self.frame_1)
        pushbutton_13.setObjectName("pushbutton_13")
        pushbutton_13.setText("提取文件名")
        pushbutton_14 = QPushButton(self.frame_1)
        pushbutton_14.setObjectName("pushbutton_14")
        pushbutton_14.setText("提取文件夹名")
        pushbutton_15 = QPushButton(self.frame_1)
        pushbutton_15.setObjectName("pushbutton_15")
        pushbutton_15.setText("确定")

        label_11 = QLabel(self.frame_1)
        label_11.setObjectName("label_11")
        label_11.setText("查找文件路径：")
        lineEdit_15 = QLineEdit(self.frame_1)
        lineEdit_15.setObjectName(u"lineEdit_15")
        label_12 = QLabel(self.frame_1)
        label_12.setObjectName("label_12")
        label_12.setText("拷贝到：")
        lineEdit_16 = QLineEdit(self.frame_1)
        lineEdit_16.setObjectName(u"lineEdit_16")
        pushbutton_17 = QPushButton(self.frame_1)
        pushbutton_17.setObjectName("pushbutton_17")
        pushbutton_17.setText("删除文件夹")
        pushbutton_18 = QPushButton(self.frame_1)
        pushbutton_18.setObjectName("pushbutton_18")
        pushbutton_18.setText("删除文件")

        plainTextEdit_1 = QPlainTextEdit(self.frame_1)
        plainTextEdit_1.setObjectName(u"plainTextEdit_1")
        plainTextEdit_1.setPlainText("请输入查找内容或正则表达式.....")

        self.gridLayout_2.addWidget(pushbutton_10, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_11, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_12, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_13, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_14, 0, 4, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_17, 0, 5, 1, 1)
        self.gridLayout_2.addWidget(pushbutton_18, 0, 6, 1, 1)
        self.gridLayout_2.addWidget(label_11, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_15, 1, 1, 1, 6)
        self.gridLayout_2.addWidget(label_12, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_16, 2, 1, 1, 5)
        self.gridLayout_2.addWidget(pushbutton_15, 2, 6, 1, 1)
        self.gridLayout_2.addWidget(plainTextEdit_1, 3, 0, 1, 7)

        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    def input_3(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        label_13 = QLabel(self.frame_1)
        label_13.setObjectName("label_13")
        label_13.setText("台账：")
        lineEdit_17 = QLineEdit(self.frame_1)
        lineEdit_17.setObjectName(u"lineEdit_17")
        label_14 = QLabel(self.frame_1)
        label_14.setObjectName("label_14")
        label_14.setText("矢量图片：")
        lineEdit_18 = QLineEdit(self.frame_1)
        lineEdit_18.setObjectName(u"lineEdit_18")
        label_15 = QLabel(self.frame_1)
        label_15.setObjectName("label_15")
        label_15.setText("拷贝到：")
        lineEdit_19 = QLineEdit(self.frame_1)
        lineEdit_19.setObjectName(u"lineEdit_19")
        pushbutton_16 = QPushButton(self.frame_1)
        pushbutton_16.setObjectName("pushbutton_16")
        pushbutton_16.setText("确定")

        self.gridLayout_2.addWidget(label_13, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_17, 0, 1, 1, 4)
        self.gridLayout_2.addWidget(label_14, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_18, 1, 1, 1, 4)
        self.gridLayout_2.addWidget(label_15, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_19, 2, 1, 1, 3)
        self.gridLayout_2.addWidget(pushbutton_16, 2, 4, 1, 1)

        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    #台账与矢量图框检查
    def input_4(self):
        for i in range(self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        label_16 = QLabel(self.frame_1)
        label_16.setObjectName("label_16")
        label_16 .setText("台账：")
        lineEdit_20 = QLineEdit(self.frame_1)
        lineEdit_20.setObjectName(u"lineEdit_20")
        label_17 = QLabel(self.frame_1)
        label_17.setObjectName("label_17")
        label_17.setText("shp数据表：")
        lineEdit_21 = QLineEdit(self.frame_1)
        lineEdit_21.setObjectName(u"lineEdit_21")
        label_18 = QLabel(self.frame_1)
        label_18.setObjectName("label_18")
        label_18.setText("原始台账：")
        lineEdit_22 = QLineEdit(self.frame_1)
        lineEdit_22.setObjectName(u"lineEdit_22")
        label_19 = QLabel(self.frame_1)
        label_19.setObjectName("label_19")
        label_19.setText("错误结果保存到：")
        lineEdit_23 = QLineEdit(self.frame_1)
        lineEdit_23.setObjectName(u"lineEdit_23")
        pushbutton_17 = QPushButton(self.frame_1)
        pushbutton_17.setObjectName("pushbutton_17")
        pushbutton_17.setText("开始检查")

        self.gridLayout_2.addWidget(pushbutton_17, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(label_16, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(label_17, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(label_18,3, 0, 1, 1)
        self.gridLayout_2.addWidget(label_19,4, 0, 1, 1)
        self.gridLayout_2.addWidget(lineEdit_20,1, 1, 1, 5)
        self.gridLayout_2.addWidget(lineEdit_21,2, 1, 1, 5)
        self.gridLayout_2.addWidget(lineEdit_22,3, 1, 1, 5)
        self.gridLayout_2.addWidget(lineEdit_23,4, 1, 1, 5)

        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 0, 1, 1)

    #   事件生成器
    def setevent(self, widget, widgetobjectname, signal):
        """
        @param widget: 控件类型
        @param widgetobjectname: 控件对象名字
        @param signal: 控件的事件信号
        """
        if signal == "clicked":  # pushbutton鼠标左键点击事件
            for j in widgetobjectname:
                for i in self.slotdicts[j]:
                    self.findChild(widget, j).clicked.connect(i)
        elif signal == "textChanged":  # lineEdit输入文本变化事件
            for j in widgetobjectname:
                for i in self.slotdicts[j]:
                    self.findChild(widget, j).textChanged.connect(i)
        elif signal == "triggered":  # action单击事件
            for j in widgetobjectname:
                for i in self.slotdicts[j]:
                    self.findChild(widget, j).triggered.connect(i)
        elif signal == "customContextMenuRequested":  # tabelwidget鼠标右击事件
            for j in widgetobjectname:
                for i in self.slotdicts[j]:
                    self.findChild(
                        widget, j).customContextMenuRequested.connect(i)
        elif signal == "currentIndexChanged":  # QComboBox控件选中事件
            for j in widgetobjectname:
                for i in self.slotdicts[j]:
                    self.findChild(widget, j).currentIndexChanged.connect(i)

    def foraddction(self, menueventlist: dict):
        """
        @param action_name: 名称
        @param menueventlist: 与名称对应的事件字典
        """
        menu = QMenu(self)
        actionlist = {}
        for i in menueventlist:
            action = menu.addAction(i)
            actionlist[i] = action
        item = menu.exec_(QCursor.pos())
        for m in actionlist:
            if item == actionlist[m]:
                for v in menueventlist[m]:
                    v()

    # tabelwidget控件的数据展示
    def settabelvalue(self, tabelwidget, tabeldata):
        tabelwidget.setColumnCount(len(tabeldata["header"]))
        tabelwidget.setHorizontalHeaderLabels(tabeldata["header"])
        a = 0
        if isinstance(tabeldata["data"], list):
            tabelwidget.setRowCount(len(tabeldata["data"]))
            for i in tabeldata["data"]:
                b = 0
                for n in i:
                    dataitem = QTableWidgetItem(str(n))
                    tabelwidget.setItem(a, b, dataitem)
                    b += 1
                a += 1
        else:
            m = []
            for k in tabeldata["data"].values():
                m.append(len(k))
            tabelwidget.setRowCount(max(m))
            for i in tabeldata["data"].values():
                b = 0
                for n in i:
                    dataitem = QTableWidgetItem(str(n))
                    tabelwidget.setItem(b, a, dataitem)
                    b += 1
                a += 1

    def treeslot(self):
        item = self.tree.currentItem()  # 当前选择的树节点
        try:
            for i in self.treeslotdict[item.text(0)]:
                i()
        except KeyError:
            pass
        except TypeError:
            pass

    # 工具栏生成
    def toolbar(self, action, icon, actiontext, name="tool"):
        """
        @param action:功能按钮
        @param icon:按钮图标
        @param actiontext:按钮名称
        @param name:工具条名称
        """
        tool = self.addToolBar(name)
        for i in range(len(action)):
            qaction = QAction(QIcon(icon[i]), actiontext[i], tool)
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
    window.show()
    try:
        sys.exit(app.exec_())
    finally:
        print("deedf")
