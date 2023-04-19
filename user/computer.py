import datetime

from PyQt5.QtCore import Qt

from custom_design import CustomDialog
from user.auth import MAC
from user.auth_model import User, ControlDate
from user.design import UiMainWindow
from user.main import BaseWindow
from user.content import ContentWindow
from user.communication import CommunicationWindow
from user.internet import InternetWindow
from user.program import ProgramWindow


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
