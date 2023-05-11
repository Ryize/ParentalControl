import calendar
import datetime
import os
import platform
import sys
import threading
import time

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QCursor

from user.design import UiDetailsWindow

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMessageBox, QSlider

from custom_design import CustomDialog
from design import UiAuthWindow, UiChildWindow
from user.auth import AuthSystem, MAC
from user.auth_model import ConfirmLogin, User, TimeDaySession, ControlDate, Ban, RequestTime

PLATFORM = platform.system().lower()

try:
    _LOGIN = User.get_or_none(User.mac == MAC).login
except AttributeError:
    _LOGIN = 'Аноним'

IS_AUTH = True


class Status:
    time_stop: bool = False


class BaseWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.parent = self
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
        user = User.get(User.mac == MAC)
        if (self._check_time_left() or Ban.get_or_none(user=user)) and not self.check_time_request():
            return
        date_today = datetime.date.today()
        day_session = TimeDaySession.get_or_create(user=user, day=date_today)[0]
        time_ = day_session.time

        new_minute = int(time_.split(':')[1]) + 1
        new_hour = int(time_.split(':')[0])
        if new_minute >= 60:
            new_minute = 0
            new_hour += 1
        day_session.time = f'{new_hour}:{new_minute}'
        day_session.save()

    def check_time_request(self):
        user = User.get(User.mac == MAC)
        date_today = datetime.date.today()
        request_time = RequestTime.select().where(
            RequestTime.user == user,
            RequestTime.day == date_today,
        )
        if not request_time:
            return False
        request_time_amount = 0
        for i in request_time:
            if i.amount.isdigit():
                request_time_amount += int(i.amount)
        user = User.get(User.mac == MAC)
        day_session = TimeDaySession.get_or_create(user=user, day=date_today)[0]
        time_ = day_session.time
        control_date = ControlDate.get_or_create(user=user)[0]
        minutes_session = int(time_.split(':')[0]) * 60 + int(time_.split(':')[1])
        max_time_this_day = getattr(control_date,
                                    calendar.day_name[date_today.weekday()].lower())
        max_time_this_day = int(max_time_this_day.split(':')[0]) * 60 + int(max_time_this_day.split(':')[1])
        if request_time_amount + max_time_this_day - minutes_session > 0:
            return True
        return False

    def _check_time_left(self):
        user = User.get(User.mac == MAC)
        date_today = datetime.date.today()
        day_session = TimeDaySession.get_or_create(user=user, day=date_today)[0]
        time_ = day_session.time
        if day_session:
            minutes = int(time_.split(':')[0]) * 60 + int(time_.split(':')[1])
            control_date = ControlDate.get_or_create(user=user)[0]
            control_date.save()
            max_time_this_day = getattr(control_date,
                                        calendar.day_name[date_today.weekday()].lower())
            max_time_this_day = int(max_time_this_day.split(':')[0]) * 60 + int(max_time_this_day.split(':')[1])
            if minutes >= max_time_this_day:
                return True

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
    timer_time_amount = QTimer()

    def __init__(self, window):
        super().__init__()
        self.parent_window = window
        self.setupUi(self)

        self.timer_time_amount.setInterval(10000)
        self.timer_time_amount.timeout.connect(self.check_time_amount)
        self.timer_time_amount.start()

        self.check_time_amount()

    def handler_parent(self, *args, **kwargs):
        self.parent_window.show()
        self.hide()

    def check_time_amount(self):
        if Status.time_stop:
            return
        user = User.get_or_none(User.mac == MAC)
        if not user:
            return
        limit = ControlDate.get_or_none(ControlDate.user == user)
        if not limit:
            return
        today = datetime.date.today()
        day = calendar.day_name[today.weekday()].lower()
        limit = getattr(limit, day)
        session = TimeDaySession.get_or_none(TimeDaySession.user == user, TimeDaySession.day == today)
        if not session:
            hour, minute = self.get_humanize_time(limit)
            self.label_2.setText(f'{hour} {minute}')
            return

        date_today = datetime.date.today()
        request_time = RequestTime.select().where(
            RequestTime.user == user,
            RequestTime.day == date_today,
        )
        status = True
        if not request_time:
            status = False

        hour_limit = int(limit.split(':')[0])
        minute_limit = int(limit.split(':')[1])

        hour_session = int(session.time.split(':')[0])
        minute_session = int(session.time.split(':')[1])

        hour = '0 часов'
        minute = '0 минут'

        request_time_amount = 0
        for i in request_time:
            if i.amount.isdigit():
                request_time_amount += int(i.amount)
        if hour_limit + int(request_time_amount) // 60 - hour_session > 0:
            if status:
                hour, _ = self.get_humanize_time(f'{(hour_limit - hour_session + int(request_time_amount) // 60)}:1')
            else:
                hour, _ = self.get_humanize_time(f'{hour_limit - hour_session}:1')
        if minute_limit - minute_session > 0:
            if status:
                _, minute = self.get_humanize_time(
                    f'1:{(minute_limit - minute_session + int(request_time_amount)) % 60}')
            else:
                _, minute = self.get_humanize_time(f'1:{minute_limit - minute_session}')
        self.label_2.setText(f'{hour} {minute}')

    def get_humanize_time(self, time_):
        _hour = int(time_.split(":")[0])
        hour = f'{_hour} {self._correct_word(_hour, ("часов", "час", "часа",))}'
        _minute = int(time_.split(":")[1])
        minute = f'{_minute} {self._correct_word(_minute, ("минут", "минута", "минуты",))}'
        return hour, minute

    def handler_request_time(self):
        user = User.get(User.mac == MAC)
        request_time = RequestTime(user=user)
        request_time.save()

    def _correct_word(self, number, lst):
        assert len(lst) == 3
        units = number % 10
        tens = (number // 10) % 10
        if tens == 1:
            return lst[0]
        if units in [0, 5, 6, 7, 8, 9]:
            return lst[0]
        if units == 1:
            return lst[1]
        if units in [2, 3, 4]:
            return lst[2]


class AuthWindow(BaseWindow, UiAuthWindow):
    timer_add_time = QTimer()
    timer_stop_cursor = QTimer()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.child = ChildWindow(self)

        self.timer_add_time.setInterval(60000)
        self.timer_add_time.timeout.connect(self.check_time_left)
        self.timer_add_time.start()

        self.timer_stop_cursor.setInterval(1000)
        self.timer_stop_cursor.timeout.connect(self.stop_cursor)
        self.timer_stop_cursor.start()

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.handler_auth_button()

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

    def stop_cursor(self):
        user = User.get(User.mac == MAC)
        if (self._check_time_left() and not self.check_time_request()) or Ban.get_or_none(user=user):
            self.child.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.child.show()
            self.child.showMaximized()
            p = QCursor()
            p.setPos(self.child.request_time.x() + 100, self.child.request_time.y() + 100)
            width = self.child.size().width() // 2
            self.child.label.move(width - self.child.label.width(), self.child.label.y())
            self.child.label_2.move(width - self.child.label_2.width() + 375, self.child.label_2.y())
            self.child.line.move(width - self.child.line.width() + 375, self.child.line.y())
            self.child.request_time.move(width - self.child.request_time.width() + 175, self.child.request_time.y())
            self.child.parent.move(width - self.child.parent.width() + 27999, self.child.parent.y())

            self.child.label_2.setText('Время вышло!')
            Status.time_stop = True
            return
        if not self.child.isHidden():
            self.child.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.child.show()
            self.child.showNormal()
            self.child.label.move(40, 10)
            self.child.label_2.move(390, 30)
            self.child.line.move(0, 120)
            self.child.request_time.move(200, 190)
            self.child.parent.move(340, 365)
            Status.time_stop = False

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
