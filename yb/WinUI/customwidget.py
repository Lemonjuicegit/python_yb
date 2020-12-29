from PySide2.QtWidgets import *

class CustomWidgget():

    def customtree(self,QWidget:QWidget,excel:dict):
        tree = QTreeWidget(QWidget)
        def settree(tree, name):
            __qtreewidgetitem = QTreeWidgetItem(tree)
            __qtreewidgetitem.setText(0, name)
            return __qtreewidgetitem

        for key1 in list(excel.keys()):
            __qtreewidgetitem = settree(tree, key1)
            for key2 in list(excel[key1].keys()):
                __qtreewidgetitem_1 = settree(__qtreewidgetitem, key2)
                for key3 in list(excel[key1][key2]):
                    settree(__qtreewidgetitem_1, key3)