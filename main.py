# import sys
#
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Пример окна на PyQt5")
#
#         self.label = QLabel(self)
#         self.label.setText("Введите длину (в см, м или км):" )
#         self.label.move(20, 20)
#
#         self.input = QLineEdit(self)
#         self.input.move(20, 50)
#         self.input.resize(200, 30)
#
#         self.button = QPushButton(self)
#         self.button.setText("Проверить")
#         self.button.move(20, 100)
#         self.button.clicked.connect(self.validate)
#
#     def validate(self):
#         # разделение строки на число и единицы измерения
#         parts = self..split('_')
#         if len(parts) != 2:
#             return False
#
#         # разделение единиц измерения на отдельные элементы
#         units = parts[1].split()
#         if len(units) > 2:
#             return False
#
#         # проверка, что каждый элемент единиц измерения является допустимым
#         for unit in units:
#             if unit not in ['см', 'м', 'км']:
#                 return False
#
#         # проверка, что число является целым
#         try:
#             number = int(parts[0])
#         except ValueError:
#             return False
#
#         # проверка, что число положительное
#         if number < 0:
#             return False
#
#         return True
#
# if __name__ == "__main__":
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec_()


import getpass
import platform
import subprocess
import sys
import time
import threading
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from custom_design import CustomDialog
from design import UiMainWindow, UiDetailsWindow

PLATFORM = platform.system().lower()


class DetailsWindow(QtWidgets.QMainWindow, UiDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ParentalControl(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.details = DetailsWindow()

    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.show()

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
    window = ParentalControl()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

'Hello my name is John'

r'm.*J'
