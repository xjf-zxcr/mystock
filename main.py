import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TableWidget(QMainWindow):
    h_header = ['股票代码','股票名称','买卖日期','买卖价格','盈亏率','买卖数量', '买卖金额','分红','分红税','佣金','印花税','盈利']
    filename = 'stock.txt'
    file = 'abc.txt'
    COLS = 40
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('Luge\'s Stock Stat')
        self.resize(1200,600) 
        self.table = QTableWidget(TableWidget.COLS,len(TableWidget.h_header))
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

        self.i_total = TableWidget.h_header.index('买卖金额')
        self.i_num = TableWidget.h_header.index('买卖数量')
        self.i_price = TableWidget.h_header.index('买卖价格')

        self.i_gain_rate = TableWidget.h_header.index('盈亏率')
        self.i_commission = TableWidget.h_header.index('佣金')
        self.i_tax = TableWidget.h_header.index('印花税')
        self.i_dividends = TableWidget.h_header.index('分红')
        self.i_dividends_tax = TableWidget.h_header.index('分红税')

        self.i_gain = TableWidget.h_header.index('盈利')

        newItem = QTableWidgetItem('0')
        self.table.setItem(TableWidget.COLS-1, self.i_gain, newItem)

    def clear_data(self, _item):
        
        self.table.item(_item.row(), self.i_total).setData(0, '---')
        self.table.item(_item.row(), self.i_gain_rate).setData(0, '---')
        self.table.item(_item.row(), self.i_commission).setData(0, '---')
        self.table.item(_item.row(), self.i_tax).setData(0, '---')
        if self.table.item(_item.row(), self.i_dividends).data(0) != '---' and self.table.item(_item.row(), self.i_dividends).data(0)!= '':
            pass
        else:
            self.table.item(_item.row(), self.i_dividends).setData(0, '---')

        if self.table.item(_item.row(), self.i_dividends_tax).data(0) != '---' and self.table.item(_item.row(), self.i_dividends_tax).data(0) != '':
            pass
        else:
            self.table.item(_item.row(), self.i_dividends_tax).setData(0, '---')
        self.table.item(_item.row(), self.i_gain).setData(0, '---')

    def compute_data(self, _item):

        if _item.row() != TableWidget.COLS-1:
            
            self.clear_data(_item)

            # total
            
            if '' == self.table.item(_item.row(), self.i_price).data(0):
                return

            num = 0
            if '' != self.table.item(_item.row(), self.i_num).data(0):
                num = int(self.table.item(_item.row(), self.i_num).data(0))
            
            price = float(self.table.item(_item.row(), self.i_price).data(0))
            #num = int(self.table.item(_item.row(), self.i_num).data(0))
            total = float('%.2f' %(price*num))
            #print(each_item)
            if num != 0:
                self.table.item(_item.row(), self.i_total).setData(0, str(total))

            # commission
            if abs(total*3/10000) < 5:
                commission = -5
            else:
                commission = float('%.2f' %(total*3/10000))
                commission = -1*abs(commission)
            
            if num != 0:
                self.table.item(_item.row(), self.i_commission).setData(0, str(commission))
            
            # tax
            tax = 0
            if total > 0:
                tax = float('%.2f' %(-1/1000*total))
                self.table.item(_item.row(), self.i_tax).setData(0, str(tax))

            # dividends
            dividends = 0
            dividends_tax = 0
            if self.table.item(_item.row(), self.i_dividends).data(0) != '---':
                dividends = float(self.table.item(_item.row(), self.i_dividends).data(0))
                if dividends < 0:
                    dividends *= -1
                self.table.item(_item.row(), self.i_dividends).setData(0, str(dividends))


            if self.table.item(_item.row(), self.i_dividends_tax).data(0) != '---':
                dividends_tax = float(self.table.item(_item.row(), self.i_dividends_tax).data(0))
                if dividends_tax > 0:
                    dividends_tax *= -1
                self.table.item(_item.row(), self.i_dividends_tax).setData(0, str(dividends_tax))
            
            # gain
            if num == 0:
                tax = 0
                commission = 0
            gain =  total + commission + dividends + dividends_tax + tax
            gain = float('%.2f' %gain)
            self.table.item(_item.row(), self.i_gain).setData(0, str(gain))

            
            # Profit and loss rate
            if num == 0:
                i_gain_rate = 0

        # compute total in last line
        un_compute_gain = 0
        if self.table.item(TableWidget.COLS-1, 2).data(0) != '---' and self.table.item(TableWidget.COLS-1, 2).data(0) != '':
            un_compute_gain = float('%.2f' %float(self.table.item(TableWidget.COLS-1, 2).data(0)))
            self.table.item(TableWidget.COLS-1, 2).setForeground(Qt.red)


        total_gain = un_compute_gain
        for i in range(TableWidget.COLS-1):
            if self.table.item(i, self.i_gain).data(0) != '---' and self.table.item(i, self.i_gain).data(0) != '':
                each_gain = float('%.2f' %float(self.table.item(i, self.i_gain).data(0)))
                if each_gain > 0:
                    self.table.item(i, self.i_gain).setForeground(Qt.red)
                else:
                    self.table.item(i, self.i_gain).setForeground(Qt.green)
                total_gain += each_gain
                total_gain = float('%.2f' %total_gain)
        self.table.item(TableWidget.COLS-1, self.i_gain).setData(0, str(total_gain))
        if total_gain > 0:
            self.table.item(TableWidget.COLS-1, self.i_gain).setForeground(Qt.red)
        else:
            self.table.item(TableWidget.COLS-1, self.i_gain).setForeground(Qt.green)
        
        total_tax = 0
        for i in range(TableWidget.COLS-1):
            if self.table.item(i, self.i_tax).data(0) != '---' and self.table.item(i, self.i_tax).data(0) != '':
                total_tax += float('%.2f' %float(self.table.item(i, self.i_tax).data(0)))
        self.table.item(TableWidget.COLS-1, self.i_tax).setData(0, str(total_tax))

        total_tax = 0
        for i in range(TableWidget.COLS-1):
            if self.table.item(i, self.i_tax).data(0) != '---' and self.table.item(i, self.i_tax).data(0) != '':
                total_tax += float('%.2f' %float(self.table.item(i, self.i_tax).data(0)))
        self.table.item(TableWidget.COLS-1, self.i_tax).setData(0, str(total_tax))

        total_commission = 0
        for i in range(TableWidget.COLS-1):
            if self.table.item(i, self.i_commission).data(0) != '---' and self.table.item(i, self.i_commission).data(0) != '':
                total_commission += float('%.2f' %float(self.table.item(i, self.i_commission).data(0)))
        self.table.item(TableWidget.COLS-1, self.i_commission).setData(0, str(total_commission))

        total_dividends = 0
        for i in range(TableWidget.COLS-1):
            if self.table.item(i, self.i_dividends).data(0) != '---' and self.table.item(i, self.i_dividends).data(0) != '':
                total_dividends +=  float(self.table.item(i, self.i_dividends).data(0))
                total_dividends = float('%.2f' % total_dividends)
        self.table.item(TableWidget.COLS-1, self.i_dividends).setData(0, str(total_dividends))

        total_dividends_tax = 0
        for i in range(TableWidget.COLS-1):
            if self.table.item(i, self.i_dividends_tax).data(0) != '---' and self.table.item(i, self.i_dividends_tax).data(0) != '':
                total_dividends_tax += float('%.2f' %float(self.table.item(i, self.i_dividends_tax).data(0)))
        self.table.item(TableWidget.COLS-1, self.i_dividends_tax).setData(0, str(total_dividends_tax))

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
        self.table.itemChanged.disconnect(self.item_change)
        self.compute_data(item)
        self.writeFile()
        self.table.itemChanged.connect(self.item_change)

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