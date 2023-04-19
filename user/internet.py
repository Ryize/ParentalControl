from user.design import UiInternetWindow
from user.main import BaseWindow


class InternetWindow(BaseWindow, UiInternetWindow):
    def initUI(self):
        self.setWindowTitle('Родительский контроль')
        self.computer_button.clicked.connect(self.change_parental)
        self.program_button.clicked.connect(self.change_computer)
        self.communication_button.clicked.connect(self.change_communication)
        self.content_button.clicked.connect(self.change_content)




    def change_content(self):
        from user.content import ContentWindow
        self.communication = ContentWindow()
        self.communication.show()
        self.destroy()

    def change_parental(self):
        from user.computer import ComputerControl
        self.parental = ComputerControl()
        self.parental.show()
        self.destroy()

    def change_computer(self):
        from user.program import ProgramWindow
        self.program = ProgramWindow()
        self.program.show()
        self.destroy()

    def change_communication(self):
        from user.communication import CommunicationWindow
        self.communication = CommunicationWindow()
        self.communication.show()
        self.destroy()
