import sys
import requests
from PyQt5.QtWidgets import QWidget,QLabel,QApplication,QFormLayout
from PyQt5.QtCore import QTimer,Qt,QPoint
from PyQt5.QtGui import QMouseEvent,QIcon

qss = '''

QLabel {
    color:white;
    
}
'''

class mainWindow(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False
    def __init__(self,parent=None):
        super(mainWindow,self).__init__(parent)
        self.setFixedSize(100,50)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 无边框
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 窗口置顶
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowIcon(QIcon("bitcoin.png"))  # 设置窗口图标
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.labeldirection = QLabel()
        self.labelprice = QLabel()
        self.labeldirection2 = QLabel()
        self.labelprice2 = QLabel()
        '''
            标签颜色设置为白色
        '''
        self.form.addRow(self.labeldirection, self.labelprice)
        self.form.addRow(self.labeldirection2, self.labelprice2)
        self.time = QTimer()
        self.time.timeout.connect(self.getDataUi)
        self.time.start(1000)

    # 双击关闭窗口
    def mouseDoubleClickEvent(self, e):
        self.close()

    # 无边框拖动窗口
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # 获取动态币价
    def getDataUi(self):
        url = "https://api.hadax.com/market/history/trade?symbol=dogeusdt&size=2"

        try:
            r = requests.get(url)
        except:
            print("数据请求失败")
        datas = r.json()  # 将字符串序列转换为json

        datas = datas["data"]  # 获取数据列表


        self.labeldirection.setText(str(datas[0]["data"][0]["direction"])[0:1] + ':')
        self.labelprice.setText(str(datas[0]["data"][0]["price"]))
        self.labeldirection2.setText(str(datas[1]["data"][0]["direction"])[0:1] + ':')
        self.labelprice2.setText(str(datas[1]["data"][0]["price"]))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())