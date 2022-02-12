from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ExcludedWidget(QWidget):
    def __init__(self, controller, mat):
        super().__init__(controller)
        self.controller = controller
        self.mat = mat
        self.widget = QPushButton('- ' + mat.name, self)
        self.widget.clicked.connect(self.remove_excluded)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.widget)

    def remove_excluded(self):
        self.controller.remove_excluded(self.mat)
