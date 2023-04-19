import datetime
import platform
import sys
import time
import threading
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from custom_design import CustomDialog
from design import UiMainWindow, UiDetailsWindow, UiAuthWindow, UiChildWindow, UiProgramWindow, UiInternetWindow, \
    UiCommunicationWindow, UiControlWindow
from user.auth import AuthSystem, MAC
from user.auth_model import ConfirmLogin, User, ControlDate

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
    user = User.get(mac=MAC)
    _limit_time_in_db = ControlDate.get_or_none(user=user)
    _amount_request_limit_time_in_db = 0

    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.program_button.clicked.connect(self.change_computer)
        self.internet_button.clicked.connect(self.change_internet)
        self.communication_button.clicked.connect(self.change_communication)
        self.content_button.clicked.connect(self.change_content)
        self.put_checkmarks_and_text()

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

    def put_checkmarks_and_text(self):
        user = User.get(mac=MAC)
        limit_time_in_db = ControlDate.get_or_none(user=user)
        if not limit_time_in_db:
            self._not_limit_time_in_db()
        day_1 = limit_time_in_db.monday.split(':')
        self.limit_day.setTime(datetime.time(int(day_1[0]), int(day_1[1]), 0))
        day_2 = limit_time_in_db.tuesday.split(':')
        self.limit_day_2.setTime(datetime.time(int(day_2[0]), int(day_2[1]), 0))
        day_3 = limit_time_in_db.wednesday.split(':')
        self.limit_day_3.setTime(datetime.time(int(day_3[0]), int(day_3[1]), 0))
        day_4 = limit_time_in_db.thursday.split(':')
        self.limit_day_4.setTime(datetime.time(int(day_4[0]), int(day_4[1]), 0))
        day_5 = limit_time_in_db.friday.split(':')
        self.limit_day_5.setTime(datetime.time(int(day_5[0]), int(day_5[1]), 0))
        day_6 = limit_time_in_db.saturday.split(':')
        self.limit_day_6.setTime(datetime.time(int(day_6[0]), int(day_6[1]), 0))
        day_7 = limit_time_in_db.sunday.split(':')
        self.limit_day_7.setTime(datetime.time(int(day_7[0]), int(day_7[1]), 0))

        self.limit_time_monday.setChecked(limit_time_in_db.monday != '23:59')
        self.limit_time_tuesday.setChecked(limit_time_in_db.tuesday != '23:59')
        self.limit_time_wednesday.setChecked(limit_time_in_db.wednesday != '23:59')
        self.limit_time_thursday.setChecked(limit_time_in_db.thursday != '23:59')
        self.limit_time_friday.setChecked(limit_time_in_db.friday != '23:59')
        self.limit_time_saturday.setChecked(limit_time_in_db.saturday != '23:59')
        self.limit_time_sunday.setChecked(limit_time_in_db.sunday != '23:59')

    def _not_limit_time_in_db(self) -> None:
        for i in range(1, 8):
            time_ = datetime.time(23, 59, 0)
            getattr(self, f'limit_day_{i}' if i != 1 else 'limit_day').setTime(time_)

    def change_time(self):
        if self._amount_request_limit_time_in_db > 5:
            self._limit_time_in_db = ControlDate.get_or_none(user=self.user)
        if not self._limit_time_in_db:
            return
        self._limit_time_in_db.monday = self.limit_day.text()
        self._limit_time_in_db.tuesday = self.limit_day_2.text()
        self._limit_time_in_db.wednesday = self.limit_day_3.text()
        self._limit_time_in_db.thursday = self.limit_day_4.text()
        self._limit_time_in_db.friday = self.limit_day_5.text()
        self._limit_time_in_db.saturday = self.limit_day_6.text()
        self._limit_time_in_db.sunday = self.limit_day_7.text()

        self._limit_time_in_db.save()
        self._amount_request_limit_time_in_db += 1

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

        enable_status = sender.isChecked()

        self._display_in_footer(enable_status, text)
        user = User.get(mac=MAC)
        limit_time_in_db = ControlDate.get_or_none(user=user)
        if not limit_time_in_db:
            limit_time_in_db = ControlDate(user=user)

        self._assign_date(limit_time_in_db, text, enable_status).save()

    def _assign_date(self, limit_time_in_db, text: str, enable_status: bool = True):
        time_ = '23:59'
        if text.count('понедельник'):
            limit_time_in_db.monday = self.limit_day.text() if enable_status else time_
        if text.count('вторник'):
            limit_time_in_db.tuesday = self.limit_day_2.text() if enable_status else time_
        if text.count('среда'):
            limit_time_in_db.wednesday = self.limit_day_3.text() if enable_status else time_
        if text.count('четверг'):
            limit_time_in_db.thursday = self.limit_day_4.text() if enable_status else time_
        if text.count('пятница'):
            limit_time_in_db.friday = self.limit_day_5.text() if enable_status else time_
        if text.count('суббота'):
            limit_time_in_db.saturday = self.limit_day_6.text() if enable_status else time_
        if text.count('воскресенье'):
            limit_time_in_db.sunday = self.limit_day_7.text() if enable_status else time_
        return limit_time_in_db

    def _display_in_footer(self, status: bool, text: str) -> None:
        if status:
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
