from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel, QDialog


class CustomDialog(QDialog):
    def __init__(self, title: str, text: str = 'Вы уверены что хотите сделать это?'):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
