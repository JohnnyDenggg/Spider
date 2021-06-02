import sys
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFormLayout,QDialog,QComboBox,QTextEdit,QMenu,QAction,QDialogButtonBox,QLineEdit
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QIcon,QCursor

class dialog(QDialog):
    def __init__(self,parent=None):
        super(dialog, self).__init__(parent)
        self.setWindowTitle('币币监控参数设置')
        self.setWindowIcon(QIcon('bitcoin.png'))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 窗口置顶
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.labelCoin = QLabel('币种：')
        self.comboCoin = QComboBox()
        self.comboCoin.addItem('dogeusdt')
        self.comboCoin.addItem('filusdt')
        self.comboCoin.addItem('btcusdt')
        self.comboCoin.addItem('ethusdt')
        self.comboCoin.addItem('htusdt')
        self.comboCoin.addItem('ltcusdt')
        self.labelHigh = QLabel('提醒高价：')
        self.textHigh = QLineEdit()
        self.textHigh.setPlaceholderText('请输入在什么高价提醒(美元)')
        self.labelLow = QLabel('提醒低价：')
        self.textLow = QLineEdit()
        self.textLow.setPlaceholderText('请输入在什么低价提醒(美元)')
        self.labelTime = QLabel('提醒时间间隔：')
        self.textTime = QLineEdit()
        self.textTime.setPlaceholderText('请输入提醒间隔时间(秒)')
        self.labelEnterpriseId = QLabel('企业微信ID：')
        self.textEnterpriseId = QLineEdit()
        self.textEnterpriseId.setPlaceholderText('请输入企业微信"企业ID"')
        self.labelAppId = QLabel('AgentId:')
        self.textAppId = QLineEdit()
        self.textAppId.setPlaceholderText('请输入企业微信应用"AgentId"')
        self.labelAppSecret = QLabel('Secret:')
        self.textSecret = QLineEdit()
        self.textSecret.setPlaceholderText('请输入企业微信应用"Secret"码')
        self.form.addRow(self.labelCoin,self.comboCoin)
        self.form.addRow(self.labelHigh,self.textHigh)
        self.form.addRow(self.labelLow,self.textLow)
        self.form.addRow(self.labelTime,self.textTime)
        self.form.addRow(self.labelEnterpriseId,self.textEnterpriseId)
        self.form.addRow(self.labelAppId,self.textAppId)
        self.form.addRow(self.labelAppSecret,self.textSecret)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,Qt.Horizontal,self)
        # self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.close)
        self.form.addWidget(self.buttons)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = dialog()
    window.show()
    sys.exit(app.exec_())