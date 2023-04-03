import getpass
import platform
import subprocess
import sys
import time
import threading
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget

from custom_design import CustomDialog
from design import UiMainWindow, UiDetailsWindow, UiAuthWindow, UiChildWindow, UiProgramWindow

PLATFORM = platform.system().lower()

IS_AUTH = True


class DetailsWindow(QtWidgets.QMainWindow, UiDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ChildWindow(QtWidgets.QMainWindow, UiChildWindow):
    def __init__(self, window):
        self.parent_window = window
        super().__init__()
        self.setupUi(self)

    def handler_parent(self, *args, **kwargs):
        self.parent_window.show()
        self.hide()


class AuthWindow(QtWidgets.QMainWindow, UiAuthWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.window = ParentalControl()
        self.child = ChildWindow(self)

    def handler_auth_button(self):
        if self.login.text() == 'admin' and self.password.text() == '1234':
            self.window.show()
            self.hide()
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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Отправка запроса")
        msg.setText("В ваш телеграм отправлен запрос.\nНажмите на кнопку \"Да\"!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class ParentalControl(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.details = DetailsWindow()

        self.goto("main")

    def initUI(self):
        self.setWindowTitle('Родительский контроль')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            dlg = CustomDialog('Выход', 'Вы уверены что хотите выйти?')
            if dlg.exec():
                self.close()
                # if PLATFORM == 'windows':
                #     command = "wmic product get name"
                #     result = subprocess.run(command, capture_output=True, text=True)
                #
                #     # Вывод списка всех программ на экран
                #     print(result.stdout)
                # elif PLATFORM == 'darwin':
                #     command = "ls /Applications"
                #     result = subprocess.run(command, capture_output=True, text=True, shell=True)
                #
                #     # Вывод списка всех программ на экран
                #     print(result.stdout)
                #     program_name = "название программы"
                #
                #     # Выполнение команды "killall" для закрытия программы
                #     command = f"killall Discord"
                #     subprocess.run(command, shell=True)

    def handler_details(self):
        self.details.show()

    def handler_turn_parental_control(self):
        if self.turn_parental_control.isChecked():
            self.statusBar().showMessage('Вы включили родительский контроль!')
        else:
            self.statusBar().showMessage('Вы выключили родительский контроль!')
        self.auto_clear_status_bar()

    def limit_time(self):
        sender = self.sender()
        text = sender.text()

        if sender.isChecked():
            self.statusBar().showMessage(f'Вы ограничили время {text.split(" ")[-1]}')
        else:
            self.statusBar().showMessage(f'Вы сняли ограничение {text.split(" ")[-1]}')
        self.auto_clear_status_bar(3)

    def auto_clear_status_bar(self, timeout: int = 5):
        thread = threading.Thread(target=self._auto_clear_status_bar, args=(timeout,))
        thread.start()

    def _auto_clear_status_bar(self, timeout: int):
        time.sleep(timeout)
        self.statusBar().showMessage('')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
