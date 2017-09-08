import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class TableWidget(QMainWindow):
    h_header = ['股票代码','股票名称','买卖日期','买卖价格','盈亏率','买卖数量', '买卖金额','分红','分红税','佣金','印花税','盈利']
    filename = 'stock.txt'
    file = 'abc.txt'
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('TableWidget')
        self.table = QTableWidget(40,len(TableWidget.h_header))
        self.setCentralWidget(self.table)
        self.table.setHorizontalHeaderLabels(TableWidget.h_header)
        '''     
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                cnt = '(%d,%d)'% (i,j)
                newItem = QTableWidgetItem(cnt)
                self.table.setItem(i,j,newItem)
'''
        #self.table.verticalHeader().setVisible(False)
        #self.table.setShowGrid(False)
        #self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        #self.table.setSelectionBehavior(QTableWidget.SelectRows)
        #self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        self._list = []

        self.readFile(TableWidget.file)
        

    def readFile(self, filename='abc.txt'):
        i = 0
        j = 0
        try:
            with open(filename, 'r', encoding='UTF-8') as f:
                for each_line in f:
                    templ = each_line.strip().split(';',len(TableWidget.h_header)-1)
                    j = 0
                    for each_item in templ:
                        newItem = QTableWidgetItem(each_item)
                        self.table.setItem(i,j,newItem)
                        j += 1
                    i += 1
            
        except IOError as err:
            print(str(err))

        self.table.itemChanged.connect(self.item_change)

    def item_change(self, item):
        self.writeFile()

    def writeFile(self, filename='abc.txt'):
        try:
            with open(filename, 'w', encoding='UTF-8') as f:
                for i in range(self.table.rowCount()):
                    for j in range(self.table.columnCount()):
                        if self.table.item(i, j) != None:
                            print(self.table.item(i, j).text(), file=f, end='')
                        if j != (self.table.columnCount()-1):
                            print(';', file=f, end='')
                    print(file=f)
        except IOError as err:
            print(str(err))

        





app = QApplication(sys.argv)
tb = TableWidget()
tb.show()
app.exec_()