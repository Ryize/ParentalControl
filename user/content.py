from user.communication import CommunicationWindow
from user.design import UiControlWindow
from user.internet import InternetWindow
from user.main import BaseWindow
from user.program import ProgramWindow


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
        from user.computer import ComputerControl
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
