import platform
import sys
import time
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from custom_design import CustomDialog
from design import UiMainWindow, UiDetailsWindow, UiAuthWindow, UiChildWindow, UiProgramWindow, UiInternetWindow, \
    UiCommunicationWindow, UiControlWindow
from user.auth import AuthSystem, MAC
from user.auth_model import ConfirmLogin, User

PLATFORM = platform.system().lower()

_LOGIN = User.get_or_none(User.mac == MAC).login or 'Аноним'

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

    def handler_details(self):
        self.details.show()

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
        self.parent_window = window
        super().__init__()
        self.setupUi(self)

    def handler_parent(self, *args, **kwargs):
        self.parent_window.show()
        self.hide()


class AuthWindow(BaseWindow, UiAuthWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.child = ChildWindow(self)

    def handler_auth_button(self):
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


class ComputerControl(BaseWindow, UiMainWindow):
    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.program_button.clicked.connect(self.change_computer)
        self.internet_button.clicked.connect(self.change_internet)
        self.communication_button.clicked.connect(self.change_communication)
        self.content_button.clicked.connect(self.change_content)

    def change_content(self):
        self.communication = ContentWindow()
        self.communication.show()
        self.destroy()

    def change_computer(self):
        self.computer = ProgramWindow()
        self.computer.show()
        self.destroy()

    def change_internet(self):
        self.internet = InternetWindow()
        self.internet.show()
        self.destroy()

    def change_communication(self):
        self.communication = CommunicationWindow()
        self.communication.show()
        self.destroy()

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

    def limit_time(self):
        sender = self.sender()
        text = sender.text()

        if sender.isChecked():
            self.statusBar().showMessage(f'Вы ограничили время {text.split(" ")[-1]}')
        else:
            self.statusBar().showMessage(f'Вы сняли ограничение {text.split(" ")[-1]}')
        self.auto_clear_status_bar(3)


class ProgramWindow(BaseWindow, UiProgramWindow):
    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.computer_button.clicked.connect(self.change_parental)
        self.internet_button.clicked.connect(self.change_internet)
        self.communication_button.clicked.connect(self.change_communication)
        self.content_button.clicked.connect(self.change_content)

    def change_content(self):
        self.communication = ContentWindow()
        self.communication.show()
        self.destroy()

    def change_parental(self):
        self.parental = ComputerControl()
        self.parental.show()
        self.destroy()

    def change_internet(self):
        self.internet = InternetWindow()
        self.internet.show()
        self.destroy()

    def change_communication(self):
        self.communication = CommunicationWindow()
        self.communication.show()
        self.destroy()


class InternetWindow(BaseWindow, UiInternetWindow):
    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.computer_button.clicked.connect(self.change_parental)
        self.program_button.clicked.connect(self.change_computer)
        self.communication_button.clicked.connect(self.change_communication)
        self.content_button.clicked.connect(self.change_content)

    def change_content(self):
        self.communication = ContentWindow()
        self.communication.show()
        self.destroy()

    def change_parental(self):
        self.parental = ComputerControl()
        self.parental.show()
        self.destroy()

    def change_computer(self):
        self.program = ProgramWindow()
        self.program.show()
        self.destroy()

    def change_communication(self):
        self.communication = CommunicationWindow()
        self.communication.show()
        self.destroy()


class CommunicationWindow(BaseWindow, UiCommunicationWindow):
    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.computer_button.clicked.connect(self.change_parental)
        self.program_button.clicked.connect(self.change_computer)
        self.internet_button.clicked.connect(self.change_internet)
        self.content_button.clicked.connect(self.change_content)

    def change_content(self):
        self.communication = ContentWindow()
        self.communication.show()
        self.destroy()

    def change_parental(self):
        self.parental = ComputerControl()
        self.parental.show()
        self.destroy()

    def change_computer(self):
        self.program = ProgramWindow()
        self.program.show()
        self.destroy()

    def change_internet(self):
        self.program = InternetWindow()
        self.program.show()
        self.destroy()


class ContentWindow(BaseWindow, UiControlWindow):
    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.computer_button.clicked.connect(self.change_parental)
        self.program_button.clicked.connect(self.change_computer)
        self.internet_button.clicked.connect(self.change_internet)
        self.communication_button.clicked.connect(self.change_communication)

    def change_communication(self):
        self.communication = CommunicationWindow()
        self.communication.show()
        self.destroy()

    def change_parental(self):
        self.parental = ComputerControl()
        self.parental.show()
        self.destroy()

    def change_computer(self):
        self.program = ProgramWindow()
        self.program.show()
        self.destroy()

    def change_internet(self):
        self.program = InternetWindow()
        self.program.show()
        self.destroy()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
