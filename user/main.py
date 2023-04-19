import platform
import sys
import threading
import time

from PyQt5 import QtCore, QtGui

from user.design import UiDetailsWindow

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from custom_design import CustomDialog
from design import UiAuthWindow, UiChildWindow
from user.auth import AuthSystem, MAC
from user.auth_model import ConfirmLogin, User

PLATFORM = platform.system().lower()

try:
    _LOGIN = User.get_or_none(User.mac == MAC).login
except AttributeError:
    _LOGIN = 'Аноним'

IS_AUTH = True


class BaseWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowMinimizeButtonHint
        )
        try:
            self.initUI()
            self.button_details.clicked.connect(self.handler_details)
        except AttributeError:
            pass

        self.details = DetailsWindow()
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", f"{_LOGIN} - текущий пользователь"))

        self.exit = QtWidgets.QLabel(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(28, 545, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.exit.setFont(font)
        self.exit.setStyleSheet("color: #87CEEB;")
        self.exit.setText("Выход")
        self.exit.setObjectName("exit")
        self.exit.mousePressEvent = self.handler_exit

    def check_time_left(self):
        print("Я тут!")

    def handler_details(self):
        self.details.show()

    def handler_exit(self, *args, **kwargs):
        if self.__class__.__name__ == "AuthWindow":
            return
        auth = AuthWindow()
        auth.show()
        self.destroy()

    def handler_turn_parental_control(self):
        if self.turn_parental_control.isChecked():
            self.statusBar().showMessage('Вы включили родительский контроль!')
        else:
            self.statusBar().showMessage('Вы выключили родительский контроль!')
        self.auto_clear_status_bar()

    def auto_clear_status_bar(self, timeout: int = 5):
        thread = threading.Thread(target=self._auto_clear_status_bar, args=(timeout,))
        thread.start()

    def closeEvent(self, event):
        event.ignore()

    def _auto_clear_status_bar(self, timeout: int):
        time.sleep(timeout)
        self.statusBar().showMessage('')


class DetailsWindow(QtWidgets.QMainWindow, UiDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowMinimizeButtonHint
        )


class ChildWindow(BaseWindow, UiChildWindow):
    def __init__(self, window):
        super().__init__()
        self.parent_window = window
        self.setupUi(self)

    def handler_parent(self, *args, **kwargs):
        self.parent_window.show()
        self.hide()


class AuthWindow(BaseWindow, UiAuthWindow):
    timer = QTimer()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.child = ChildWindow(self)

        self.timer.setInterval(3000)  # 3 секунды
        self.timer.timeout.connect(self.check_time_left)
        self.timer.start()

    def handler_auth_button(self):
        from user.computer import ComputerControl
        if AuthSystem.authorize_by_data(self.login.text(), self.password.text()):
            self.window = ComputerControl()
            self.window.show()
            self.destroy()
            return
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Неверные данные")
        msg.setText("Неверный логин/пароль!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def handler_child(self, *args, **kwargs):
        self.hide()
        self.child.show()

    def handler_enter_by_telegram(self, *args, **kwargs):
        from user.computer import ComputerControl
        if not AuthSystem.authorize_by_telegram():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Ошибка привязки")
            msg.setText("❌ Программа ещё не привязана к телеграмму, авторизуйтесь с помощью логина и пароля!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        dlg = CustomDialog('Выход',
                           'В ваш телеграм отправлен запрос.\nНажмите на кнопку \"✅ Это я\".\n‼️После нажатия нажмите в этом окне \"Ок\"')
        if dlg.exec():
            user = User.get_or_none(User.mac == MAC)
            conf = ConfirmLogin.get_or_none(ConfirmLogin.user == user)
            if not conf:
                pass
            if conf.status == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Отказ доступа")
                msg.setText("❌ Ваш запрос отклонили!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            elif conf.status == 1:
                self.window = ComputerControl()
                self.window.show()
                self.destroy()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
