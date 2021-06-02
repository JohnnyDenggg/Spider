import sys
import sqlite3
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFormLayout,QDialog,QComboBox,QTextEdit,QMenu,QAction,QDialogButtonBox,QLineEdit,QMessageBox
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QIcon,QCursor
from settingDialog import dialog


'''
传入时间问题，不要每秒传一次时间
开始读取db里数据，依次检查，都有才开启timer
开始select找数据，判断，找不到数据，弹窗：请设置
'''



class mainWindow(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setFixedSize(100, 60)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 无边框
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 窗口置顶
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowIcon(QIcon("bitcoin.png"))  # 设置窗口图标
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.labeldirection = QLabel()
        self.labeldirection.setStyleSheet('''
        QLabel {
            color:white;
        }
        ''')
        self.labelprice = QLabel('右键设置')
        self.labelprice.setStyleSheet('''
                QLabel {
                    color:white;
                }
                ''')
        self.labeldirection2 = QLabel()
        self.labeldirection2.setStyleSheet('''
                QLabel {
                    color:white;
                }
                ''')
        self.labelprice2 = QLabel('右键设置')
        self.labelprice2.setStyleSheet('''
                QLabel {
                    color:white;
                }
                ''')
        self.waitTime = 1000      #等待时间
        self.remainTime = 1000  #剩余时间
        self.form.addRow(self.labeldirection, self.labelprice)
        self.form.addRow(self.labeldirection2, self.labelprice2)
        self.time = QTimer()


        # 右键菜单
        # 将ContextMenuPolicy设置为Qt.CustomContextMenu,否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        self.settingAction = self.contextMenu.addAction('设置')
        self.closeAction = self.contextMenu.addAction('关闭窗口')
        self.settingAction.triggered.connect(self.showSettingDialog)
        self.closeAction.triggered.connect(self.close)

    # 双击关闭窗口
    def mouseDoubleClickEvent(self, e):
        self.time.stop()
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
    def getDataUi(self,coin,highPrice,lowPrice,enterId,appId,secret):
        url = "https://api.hadax.com/market/history/trade?symbol={}&size=2".format(coin)

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
        if price1 > float(highPrice) and self.remainTime >= self.waitTime:
            self.remainTime -= 1
            self.sendWechatMessage(str(price1),enterId,appId,secret)
        # 低了发送消息
        if price1 < float(lowPrice) and self.remainTime >= self.waitTime:
            self.remainTime -= 1
            self.sendWechatMessage(str(price1),enterId,appId,secret)

        if self.remainTime < self.waitTime:
            self.remainTime -= 1
        if self.remainTime <= 0:
            self.remainTime = self.waitTime

    def sendWechatMessage(self,price,enterId,appId,secret):
        wx_push_access_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(enterId,secret)
        wx_push_token = requests.post(wx_push_access_url, data="").json()['access_token']
        print(wx_push_token)
        wx_push_data = {
            "agentid": appId,
            "msgtype": "text",
            "touser": "@all",
            "text": {
                "content": "您监控的币种为DOGE\n" +
                           "目前价格为" + price + "\n" +
                            "快特么操作，不然分分钟变穷逼！"
            },
            "safe": 0
        }
        requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(wx_push_token), json=wx_push_data)

    # 右键菜单槽
    def showMenu(self, pos):
        # pos 鼠标位置
        print(pos)
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def showSettingDialog(self):
        self.settingDialog = dialog()
        self.settingDialog.buttons.accepted.connect(self.acceptSetting)
        self.settingDialog.exec_()

    def acceptSetting(self):
        print('确认设置')
        self.coin = self.settingDialog.comboCoin.currentText()
        if self.settingDialog.textHigh.text().strip() == '':
            QMessageBox.information(self,'提醒','请输入监控最高价',QMessageBox.Ok)
        elif self.settingDialog.textLow.text().strip() == '':
            QMessageBox.information(self,'提醒','请输入监控最低价',QMessageBox.Ok)
        elif self.settingDialog.textLow.text().strip() >= self.settingDialog.textHigh.text().strip():
            QMessageBox.information(self,'提醒','低价必须小于输入的高价',QMessageBox.Ok)
        elif self.settingDialog.textTime.text().strip() == '':
            QMessageBox.information(self,'提醒','请输入提醒时间间隔(秒)',QMessageBox.Ok)
        elif self.settingDialog.textEnterpriseId.text().strip() == '':
            QMessageBox.information(self,'提醒','请输入企业微信"企业ID"',QMessageBox.Ok)
        elif self.settingDialog.textAppId.text().strip() == '':
            QMessageBox.information(self,'提醒','请输入企业微信应用"AgentId"',QMessageBox.Ok)
        elif self.settingDialog.textSecret.text().strip() == '':
            QMessageBox.information(self,'提醒','请输入企业微信应用"Secret"码',QMessageBox.Ok)
        else:
            self.highPrice = self.settingDialog.textHigh.text()
            self.lowPrice = self.settingDialog.textLow.text()
        #     self.waitTime = self.remainTime = self.settingDialog.textTime.text()
            self.enterpriseId = self.settingDialog.textEnterpriseId.text()
            self.agentId = self.settingDialog.textAppId.text()
            self.secret = self.settingDialog.textSecret.text()
            self.time.timeout.connect(lambda coin = self.coin,
                                             highPrice = self.highPrice,
                                             lowPrice = self.lowPrice,
                                             enterId = self.enterpriseId,
                                             appId = self.agentId,
                                             secret = self.secret :self.getDataUi(coin,highPrice,lowPrice,enterId,appId,secret))
            self.time.start(1000)
            self.settingDialog.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())