from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from ezkcl.gui.kcl_calculator import KCLCalculator
from ezkcl.lib.kcl_types import KCL_TYPES


class MatWidget(QWidget):
    def __init__(self, parent, mat, colored=False):
        super().__init__(parent)
        self.controller = parent
        self.mat = mat
        self.layout = layout = QHBoxLayout()
        self.label = QLabel(mat.name, self)
        self.label.setMaximumWidth(300)
        layout.addWidget(self.label)
        type_label = list(KCL_TYPES.keys())[mat.kcl_type]
        type_label += '-' + KCL_TYPES[type_label][mat.basic_effect]
        self.button = QPushButton(type_label, self)
        self.button.clicked.connect(self.load_calculator)
        layout.addWidget(self.button)
        self.button_delete = QPushButton('X', self)
        self.button_delete.clicked.connect(self.delete)
        self.button_delete.setStyleSheet('color: red')
        self.button_delete.setFixedWidth(30)
        layout.addWidget(self.button_delete)
        self.setLayout(layout)
        if colored:
            self.setStyleSheet('background-color: rgb(250, 250, 220)')

    def delete(self):
        self.controller.remove_material(self.mat)
        self.destroy()

    def reload_mat(self):
        type_label = KCL_TYPES.keys()[self.mat.kcl_type]
        type_label += ': ' + KCL_TYPES[type_label][self.mat.basic_effect]
        self.button.setText(type_label)

    def load_calculator(self):
        self.calc_win = KCLCalculator(self.mat, self)
        self.calc_win.show()
