import getpass

from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.username = getpass.getuser()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 100, 321, 16))
        self.label_4.setObjectName("label_4")
        self.turn_parental_control = QtWidgets.QCheckBox(self.centralwidget)
        self.turn_parental_control.setGeometry(QtCore.QRect(600, 20, 191, 20))
        self.turn_parental_control.setStyleSheet("border: 1px solid #adb5bd;\n"
                                                 "  border-radius: 0.25em;\n"
                                                 "  margin-right: 0.5em;\n"
                                                 "  background-repeat: no-repeat;\n"
                                                 "  background-position: center center;\n"
                                                 "  background-size: 50% 50%;")
        self.turn_parental_control.setObjectName("checkBox")
        self.computer_button = QtWidgets.QPushButton(self.centralwidget)
        self.computer_button.setGeometry(QtCore.QRect(10, 50, 171, 51))
        self.computer_button.setStyleSheet("background-color: rgb(59, 130, 117);\n"
                                           "color: white;\n"
                                           "font-size: 16px;\n"
                                           "border-radius: 5px;")
        self.computer_button.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 140, 171, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 16px;\n"
                                        "border-radius: 5px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 230, 171, 51))
        self.pushButton_3.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 16px;\n"
                                        "border-radius: 5px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 320, 171, 51))
        self.pushButton_4.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 16px;\n"
                                        "border-radius: 5px;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 400, 171, 51))
        self.pushButton_5.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 15px;\n"
                                        "border-radius: 5px;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.button_details = QtWidgets.QPushButton(self.centralwidget)
        self.button_details.setGeometry(QtCore.QRect(20, 510, 111, 31))
        self.button_details.setObjectName("pushButton_6")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 480, 171, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(180, 50, 20, 511))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 271, 16))
        self.label.setObjectName("label")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 40, 781, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 70, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 400, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(210, 430, 321, 16))
        self.label_5.setObjectName("label_5")
        self.limit_time_monday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_monday.setGeometry(QtCore.QRect(220, 140, 241, 20))
        self.limit_time_monday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                             "  border-radius: 0.25em;\n"
                                             "  margin-right: 0.5em;\n"
                                             "  background-repeat: no-repeat;\n"
                                             "  background-position: center center;\n"
                                             "  background-size: 50% 50%;")
        self.limit_time_monday.setObjectName("checkBox_2")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(470, 140, 118, 24))
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setGeometry(QtCore.QRect(470, 180, 118, 24))
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.limit_time_tuesday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_tuesday.setGeometry(QtCore.QRect(220, 180, 241, 20))
        self.limit_time_tuesday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                              "  border-radius: 0.25em;\n"
                                              "  margin-right: 0.5em;\n"
                                              "  background-repeat: no-repeat;\n"
                                              "  background-position: center center;\n"
                                              "  background-size: 50% 50%;")
        self.limit_time_tuesday.setObjectName("checkBox_3")
        self.timeEdit_3 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_3.setGeometry(QtCore.QRect(470, 220, 118, 24))
        self.timeEdit_3.setObjectName("timeEdit_3")
        self.limit_time_wednesday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_wednesday.setGeometry(QtCore.QRect(220, 220, 241, 20))
        self.limit_time_wednesday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                                "  border-radius: 0.25em;\n"
                                                "  margin-right: 0.5em;\n"
                                                "  background-repeat: no-repeat;\n"
                                                "  background-position: center center;\n"
                                                "  background-size: 50% 50%;")
        self.limit_time_wednesday.setObjectName("checkBox_4")
        self.timeEdit_4 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_4.setGeometry(QtCore.QRect(470, 260, 118, 24))
        self.timeEdit_4.setObjectName("timeEdit_4")
        self.limit_time_thursday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_thursday.setGeometry(QtCore.QRect(220, 260, 241, 20))
        self.limit_time_thursday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                               "  border-radius: 0.25em;\n"
                                               "  margin-right: 0.5em;\n"
                                               "  background-repeat: no-repeat;\n"
                                               "  background-position: center center;\n"
                                               "  background-size: 50% 50%;")
        self.limit_time_thursday.setObjectName("checkBox_5")
        self.timeEdit_5 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_5.setGeometry(QtCore.QRect(470, 300, 118, 24))
        self.timeEdit_5.setObjectName("timeEdit_5")
        self.limit_time_friday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_friday.setGeometry(QtCore.QRect(220, 300, 241, 20))
        self.limit_time_friday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                             "  border-radius: 0.25em;\n"
                                             "  margin-right: 0.5em;\n"
                                             "  background-repeat: no-repeat;\n"
                                             "  background-position: center center;\n"
                                             "  background-size: 50% 50%;")
        self.limit_time_friday.setObjectName("checkBox_6")
        self.timeEdit_6 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_6.setGeometry(QtCore.QRect(470, 460, 118, 24))
        self.timeEdit_6.setObjectName("timeEdit_6")
        self.limit_time_saturday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_saturday.setGeometry(QtCore.QRect(220, 460, 241, 20))
        self.limit_time_saturday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                               "  border-radius: 0.25em;\n"
                                               "  margin-right: 0.5em;\n"
                                               "  background-repeat: no-repeat;\n"
                                               "  background-position: center center;\n"
                                               "  background-size: 50% 50%;")
        self.limit_time_saturday.setObjectName("checkBox_7")
        self.timeEdit_7 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_7.setGeometry(QtCore.QRect(470, 490, 118, 24))
        self.timeEdit_7.setObjectName("timeEdit_7")
        self.limit_time_sunday = QtWidgets.QCheckBox(self.centralwidget)
        self.limit_time_sunday.setGeometry(QtCore.QRect(220, 490, 241, 20))
        self.limit_time_sunday.setStyleSheet("border: 1px solid #adb5bd;\n"
                                             "  border-radius: 0.25em;\n"
                                             "  margin-right: 0.5em;\n"
                                             "  background-repeat: no-repeat;\n"
                                             "  background-position: center center;\n"
                                             "  background-size: 50% 50%;")
        self.limit_time_sunday.setObjectName("checkBox_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "Ограничение доступа с понедельника по пятницу"))
        self.turn_parental_control.setText(_translate("MainWindow", "Родительский контроль"))
        self.computer_button.setText(_translate("MainWindow", "Компьютер"))
        self.pushButton_2.setText(_translate("MainWindow", "Программы"))
        self.pushButton_3.setText(_translate("MainWindow", "Интернет"))
        self.pushButton_4.setText(_translate("MainWindow", "Общение"))
        self.pushButton_5.setText(_translate("MainWindow", "Контроль содержания"))
        self.button_details.setText(_translate("MainWindow", "Подробнее..."))
        self.label.setText(_translate("MainWindow", f"{self.username} - текущий пользователь"))
        self.label_2.setText(_translate("MainWindow", "Рабочие дни"))
        self.label_3.setText(_translate("MainWindow", "Выходные дни"))
        self.label_5.setText(_translate("MainWindow", "Ограничение доступа в субботу и воскресенье"))
        self.limit_time_monday.setText(_translate("MainWindow", "Ограничить время (понедельник)"))
        self.limit_time_tuesday.setText(_translate("MainWindow", "Ограничить время (вторник)"))
        self.limit_time_wednesday.setText(_translate("MainWindow", "Ограничить время (среда)"))
        self.limit_time_thursday.setText(_translate("MainWindow", "Ограничить время (четверг)"))
        self.limit_time_friday.setText(_translate("MainWindow", "Ограничить время (пятница)"))
        self.limit_time_saturday.setText(_translate("MainWindow", "Ограничить время (суббота)"))
        self.limit_time_sunday.setText(_translate("MainWindow", "Ограничить время (воскресенье)"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.action.setText(_translate("MainWindow", "Читать"))

        self.button_details.clicked.connect(self.handler_details)
        self.turn_parental_control.clicked.connect(self.handler_turn_parental_control)
        self.limit_time_day = {
            self.limit_time_monday.text(): self.limit_time_monday,
            self.limit_time_tuesday.text(): self.limit_time_tuesday,
            self.limit_time_wednesday.text(): self.limit_time_wednesday,
            self.limit_time_thursday.text(): self.limit_time_thursday,
            self.limit_time_friday.text(): self.limit_time_friday,
            self.limit_time_saturday.text(): self.limit_time_saturday,
            self.limit_time_sunday.text(): self.limit_time_sunday,
        }
        for limit_time_day in self.limit_time_day.values():
            limit_time_day.clicked.connect(self.limit_time)


class UiDetailsWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_close = QtWidgets.QPushButton(self.centralwidget)
        self.button_close.setGeometry(QtCore.QRect(40, 520, 113, 32))
        self.button_close.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 50, 711, 401))
        self.textBrowser.setObjectName("textBrowser")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(40, 490, 731, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(380, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Справка"))
        self.button_close.setText(_translate("MainWindow", "❌ Закрыть"))
        self.button_close.clicked.connect(self.handler_close)
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600;\">Возможности программы &quot;Родительский контроль&quot;</span></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:24pt; font-weight:600;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1) Создание расписаний доступа к компьютеру для ребёнка. Блок &quot;Компьютер&quot;;</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">2) Добавление запрещённых для открытия программ. Блок &quot;Программы&quot;;</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">3) Добавление запрещённых для просмотра сайтов. Блок &quot;Интернет&quot;;</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">4) Ограничение программ для общения. Блок &quot;Общение&quot;;</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">5) Ограничение доступа к сайтам, где встречаются запрещённые слова. Блок &quot;Контроль содержания&quot;;</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">6) Получить краткую информацию о программе. Кнопка &quot;Подробнее...&quot;</span></p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">* Использование данной программы для незаконных целей запрещено!</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Справка"))

    def handler_close(self):
        self.close()


class UiAuthWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 335)
        MainWindow.setStyleSheet("QPushButton {\n"
                                 "    width: 220px;\n"
                                 "    height: 50px;\n"
                                 "    border: none;\n"
                                 "    outline: none;\n"
                                 "    color: #fff;\n"
                                 "    background: #111;\n"
                                 "    cursor: pointer;\n"
                                 "    position: relative;\n"
                                 "    z-index: 0;\n"
                                 "    border-radius: 10px;\n"
                                 "}\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login = QtWidgets.QLineEdit(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(230, 90, 171, 21))
        self.login.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 10, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 70, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 130, 60, 16))
        self.label_3.setObjectName("label_3")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setEnabled(True)
        self.password.setGeometry(QtCore.QRect(230, 150, 171, 21))
        self.password.setAutoFillBackground(False)
        self.password.setText("")
        self.password.setMaxLength(32)
        self.password.setClearButtonEnabled(False)
        self.password.setObjectName("lineEdit_2")
        self.auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.auth_button.setGeometry(QtCore.QRect(240, 190, 151, 32))
        self.auth_button.setStyleSheet("QPushButton {\n"
                                       "  display: inline-block;\n"
                                       "  padding: 0.75rem 1.25rem;\n"
                                       "  border-radius: 10rem;\n"
                                       "  text-transform: uppercase;\n"
                                       "  font-size: 1rem;\n"
                                       "  letter-spacing: 0.15rem;\n"
                                       "  transition: all 0.3s;\n"
                                       "  position: relative;\n"
                                       "color: #fff;\n"
                                       "  overflow: hidden;\n"
                                       " background-color: #008fb3;\n"
                                       "  z-index: 1;\n"
                                       "border-radius: 5px;\n"
                                       "}\n"
                                       "QPushButton:after {\n"
                                       "  content: \"\";\n"
                                       "  position: absolute;\n"
                                       "  bottom: 0;\n"
                                       "  left: 0;\n"
                                       "  width: 100%;\n"
                                       "  height: 100%;\n"
                                       "  background-color: #0cf;\n"
                                       "  border-radius: 10rem;\n"
                                       "  z-index: -2;\n"
                                       "}\n"
                                       "QPushButton:before {\n"
                                       "  content: \"\";\n"
                                       "  position: absolute;\n"
                                       "  bottom: 0;\n"
                                       "  left: 0;\n"
                                       "  width: 0%;\n"
                                       "  height: 100%;\n"
                                       "  background-color: #008fb3;\n"
                                       "  transition: all 0.3s;\n"
                                       "  border-radius: 10rem;\n"
                                       "  z-index: -1;\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "  color: #fff;\n"
                                       "}\n"
                                       "QPushButton:hover:before {\n"
                                       "  width: 100%;\n"
                                       "}")
        self.auth_button.setObjectName("pushButton")
        self.child = QtWidgets.QLabel(self.centralwidget)
        self.child.setGeometry(QtCore.QRect(280, 230, 81, 16))
        self.child.setStyleSheet("color: #87CEEB")
        self.child.setObjectName("label_4")
        self.enter_by_telegram = QtWidgets.QLabel(self.centralwidget)
        self.enter_by_telegram.setGeometry(QtCore.QRect(250, 260, 141, 16))
        self.enter_by_telegram.setStyleSheet("color: #87CEEB")
        self.enter_by_telegram.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 613, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.auth_button.clicked.connect(self.handler_auth_button)
        self.child.mousePressEvent = self.handler_child
        self.enter_by_telegram.mousePressEvent = self.handler_enter_by_telegram

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Авторизация"))
        self.login.setPlaceholderText(_translate("MainWindow", "Логин..."))
        self.label.setText(_translate("MainWindow", "Авторизация"))
        self.label_2.setText(_translate("MainWindow", "Логин:"))
        self.label_3.setText(_translate("MainWindow", "Пароль:"))
        self.password.setPlaceholderText(_translate("MainWindow", "Пароль..."))
        self.auth_button.setText(_translate("MainWindow", "Авторизоваться"))
        self.child.setText(_translate("MainWindow", "Я ребёнок"))
        self.enter_by_telegram.setText(_translate("MainWindow", "Войти по телеграмм"))


class UiChildWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 614)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 10, 341, 111))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(390, 30, 371, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 120, 801, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 190, 401, 151))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border-radius: 15px;\n"
                                      "color: #fff;\n"
                                      "background-color: #008fb3;")
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 430, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(340, 430, 311, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 480, 141, 32))
        self.pushButton_2.setStyleSheet("border-radius: 15px;\n"
                                        "color: #fff;\n"
                                        "background-color: #008fb3;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.parent = QtWidgets.QLabel(self.centralwidget)
        self.parent.setGeometry(QtCore.QRect(340, 540, 81, 16))
        self.parent.setStyleSheet("color: #87CEEB")
        self.parent.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.parent.mousePressEvent = self.handler_parent

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Детский доступ"))
        self.label.setText(_translate("MainWindow", "Оставшееся время: "))
        self.label_2.setText(_translate("MainWindow", "12 часов 41 минута"))
        self.pushButton.setText(_translate("MainWindow", "Запросить время"))
        self.label_3.setText(_translate("MainWindow", "Запросить заход на сайт:"))
        self.pushButton_2.setText(_translate("MainWindow", "Запрос доступа"))
        self.parent.setText(_translate("MainWindow", "Я родитель"))


class UiProgramWindow:
    def setupUi(self, QWidget):
        QWidget.setObjectName("MainWindow")
        QWidget.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(QWidget)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(600, 20, 191, 20))
        self.checkBox.setStyleSheet("border: 1px solid #adb5bd;\n"
                                    "  border-radius: 0.25em;\n"
                                    "  margin-right: 0.5em;\n"
                                    "  background-repeat: no-repeat;\n"
                                    "  background-position: center center;\n"
                                    "  background-size: 50% 50%;")
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 50, 171, 51))
        self.pushButton.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                      "color: white;\n"
                                      "font-size: 16px;\n"
                                      "border-radius: 5px;")
        self.pushButton.setObjectName("pushButton")
        self.computer_button = QtWidgets.QPushButton(self.centralwidget)
        self.computer_button.setGeometry(QtCore.QRect(10, 140, 171, 51))
        self.computer_button.setStyleSheet("background-color: rgb(59, 130, 117);\n"
                                           "color: white;\n"
                                           "font-size: 16px;\n"
                                           "border-radius: 5px;")
        self.computer_button.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 230, 171, 51))
        self.pushButton_3.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 16px;\n"
                                        "border-radius: 5px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 320, 171, 51))
        self.pushButton_4.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 16px;\n"
                                        "border-radius: 5px;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 400, 171, 51))
        self.pushButton_5.setStyleSheet("background-color: rgb(75, 165, 148);\n"
                                        "color: white;\n"
                                        "font-size: 15px;\n"
                                        "border-radius: 5px;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 510, 111, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 480, 171, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(180, 50, 20, 511))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 271, 16))
        self.label.setObjectName("label")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 40, 781, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 60, 491, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(200, 180, 261, 41))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(490, 180, 311, 381))
        self.listWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.listWidget.setMouseTracking(False)
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listWidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 510, 271, 31))
        self.label_3.setStyleSheet("color: #87CEEB")
        self.label_3.setObjectName("label_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(470, 180, 16, 371))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        QWidget.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QWidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        QWidget.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QWidget)
        self.statusbar.setObjectName("statusbar")
        QWidget.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(QWidget)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(QWidget)
        QtCore.QMetaObject.connectSlotsByName(QWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox.setText(_translate("MainWindow", "Родительский контроль"))
        self.pushButton.setText(_translate("MainWindow", "Компьютер"))
        self.computer_button.setText(_translate("MainWindow", "Программы"))
        self.pushButton_3.setText(_translate("MainWindow", "Интернет"))
        self.pushButton_4.setText(_translate("MainWindow", "Общение"))
        self.pushButton_5.setText(_translate("MainWindow", "Контроль содержания"))
        self.pushButton_6.setText(_translate("MainWindow", "Подробнее..."))
        self.label.setText(_translate("MainWindow", "Чекашов Матвей - текущий пользователь"))
        self.label_2.setText(_translate("MainWindow", "Введите название прогаммы и выберите её в списке"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Название программы..."))
        self.label_3.setText(_translate("MainWindow", "Показать заблокированные программы"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.menu_2.setTitle(_translate("MainWindow", "Справка"))
        self.action.setText(_translate("MainWindow", "Читать"))
