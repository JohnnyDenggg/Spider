import sys
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFormLayout
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QIcon

qss = '''

QLabel {
    color:white;

}
'''



class mainWindow(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setFixedSize(100, 50)
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
        self.waitTime = 60      #等待时间
        self.remainTime = 15  #剩余时间
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

        price1 = datas[0]["data"][0]["price"]
        price2 = datas[1]["data"][0]["price"]
        self.labeldirection.setText(str(datas[0]["data"][0]["direction"])[0:1] + ':')
        self.labelprice.setText(str(price1))
        self.labeldirection2.setText(str(datas[1]["data"][0]["direction"])[0:1] + ':')
        self.labelprice2.setText(str(price2))
        # 高了发送消息
        if price1 > 0.35 and self.remainTime >= self.waitTime:
            self.remainTime -= 1
            self.sendWechatMessage(str(price1))
        # 低了发送消息
        if price1 < 0.28 and self.remainTime >= self.waitTime:
            self.remainTime -= 1
            self.sendWechatMessage(str(price1))

        if self.remainTime < self.waitTime:
            self.remainTime -= 1
        if self.remainTime <= 0:
            self.remainTime = self.waitTime

    def sendWechatMessage(self,price):
        wx_push_access_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wwb29d27fb30b4b334&corpsecret=mN8N_E8wQxhermZvdfpvKs83JGhvk5oDobArJEbZ0Lg'
        wx_push_token = requests.post(wx_push_access_url, data="").json()['access_token']
        print(wx_push_token)
        wx_push_data = {
            "agentid": "1000002",
            "msgtype": "text",
            "touser": "@all",
            "text": {
                "content": "您监控的币种为DOGE\n" +
                           "目前的价格为" + price + "\n" +
                            "快特么操作，不然分分钟变穷逼！"
            },
            "safe": 0
        }
        wx_push = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(wx_push_token),
            json=wx_push_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())