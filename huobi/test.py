import sys
import time

import requests
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFormLayout,QDialog,QComboBox,QTextEdit,QMenu,QAction,QDialogButtonBox,QLineEdit,QMessageBox
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QIcon,QCursor
from settingDialog import dialog






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
        self.waitTime = 60      #等待时间
        self.remainTime = 60  #剩余时间
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

    def test(self):
        print('1')


    # 右键菜单槽
    def showMenu(self, pos):
        # pos 鼠标位置
        print(pos)
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def showSettingDialog(self):
        self.settingDialog = dialog()
        self.settingDialog.buttons.accepted.connect(lambda a = 1,b=2:self.acceptSetting(a,b))
        self.settingDialog.exec_()

    def acceptSetting(self,a,b):
        print(a+b)
        self.time.timeout.connect(self.test)
        self.time.start(1000)
        self.settingDialog.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())