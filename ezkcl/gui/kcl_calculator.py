from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QHBoxLayout, QSpinBox, \
    QVBoxLayout, QPushButton

import ezkcl.lib.kcl_types
from ezkcl.lib import kcl_types
from ezkcl.lib.kcl_material import KclMaterial


class KCLCalculator(QWidget):
    def __init__(self, kcl_material, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.material = KclMaterial(kcl_material.name, kcl_material.flag)
        print(f'{kcl_material.name} {kcl_material.flag:04X}')
        self.material.calc_props()
        self.__init_ui()
        self.flag.setText('{:04X}'.format(kcl_material.flag))
        self.setWindowTitle('KCL Calculator')
        self.show()

    def save(self):
        self.parent_widget.save_mat(self.material)
        self.destroy()

    def calc_flag(self):
        kcl_type = self.type_selection.currentIndex()
        if kcl_type < 0:
            kcl_type = 0
        self.material.kcl_type = kcl_type
        self.material.trickable = self.trickable.isChecked()
        self.material.drivable = self.drivable.isChecked()
        self.material.no_bounce = self.no_bounce.isChecked()
        self.material.intensity = self.intensity.value()
        self.material.shadow = self.shadow.value()
        self.material.basic_effect = self.basic_effect.currentIndex()
        flag = self.material.calc_flag()
        if int(self.flag.text(), 16) != flag:
            self.flag.setText('{:04X}'.format(flag))

    def on_flag_change(self):
        try:
            flag = int(self.flag.text(), 16)
            if not 0 <= flag <= 0xffff:
                raise ValueError(self.flag.text())
            self.material.flag = flag
            self.material.calc_props()
            if self.type_selection.currentIndex() != self.material.kcl_type:
                self.type_selection.setCurrentIndex(self.material.kcl_type)
            if self.basic_effect.currentIndex() != self.material.basic_effect:
                self.basic_effect.setCurrentIndex(self.material.basic_effect)
            if self.shadow.value() != self.material.shadow:
                self.shadow.setValue(self.material.shadow)
            if self.intensity.value() != self.material.intensity:
                self.intensity.setValue(self.material.intensity)
            if self.trickable.isChecked() != self.material.trickable:
                self.trickable.setChecked(self.material.trickable)
            if self.drivable.isChecked() != self.material.drivable:
                self.drivable.setChecked(self.material.drivable)
            if self.no_bounce.isChecked() != self.material.no_bounce:
                self.no_bounce.setChecked(self.material.no_bounce)
        except ValueError:
            self.flag.setText('{:04X}'.format(0))

    def on_basic_effect_change(self):
        self.calc_flag()

    def on_type_change(self):
        self.basic_effect.clear()
        current = self.type_selection.currentText()
        self.basic_effect.addItems(kcl_types.KCL_TYPES[current])
        self.calc_flag()

    def on_trick_change(self):
        self.calc_flag()

    def on_no_drive_change(self):
        self.calc_flag()

    def on_no_bounce_change(self):
        self.calc_flag()

    def on_intensity_change(self):
        self.calc_flag()

    def on_shadow_change(self):
        self.calc_flag()

    def __init_ui(self):
        top_layout = QVBoxLayout()
        main_widget = QWidget(self)
        top_layout.addWidget(main_widget)
        main_layout = QHBoxLayout()
        self.left_widget = QWidget(self)
        main_layout.addWidget(self.left_widget)
        # LEFT
        layout = QGridLayout()
        self.type_label = QLabel('Type')
        layout.addWidget(self.type_label)
        self.type_selection = QComboBox(self)
        self.type_selection.addItems(kcl_types.KCL_KEYS)
        layout.addWidget(self.type_selection, 0, 1)
        self.type_selection.setCurrentIndex(self.material.kcl_type)
        self.basic_effect_label = QLabel('Basic Effect')
        layout.addWidget(self.basic_effect_label)
        self.basic_effect = QComboBox(self)
        type = kcl_types.KCL_KEYS[self.material.kcl_type]
        self.basic_effect.addItems(kcl_types.KCL_TYPES[type])
        self.basic_effect.setCurrentIndex(self.material.basic_effect)
        layout.addWidget(self.basic_effect, 1, 1)
        self.flag_label = QLabel('KCL Flag')
        layout.addWidget(self.flag_label)
        self.flag = QLineEdit('{:04X}'.format(0), self)
        layout.addWidget(self.flag, 2, 1)
        self.left_widget.setLayout(layout)

        # RIGHT
        layout = QGridLayout()
        self.right_widget = QWidget(self)
        main_layout.addWidget(self.right_widget)
        self.trickable = QCheckBox('Trickable')
        layout.addWidget(self.trickable)
        self.trickable.setChecked(self.material.trickable)
        self.drivable = QCheckBox('Not drivable')
        layout.addWidget(self.drivable)
        self.drivable.setChecked(self.material.drivable)
        self.no_bounce = QCheckBox('No Bounce')
        layout.addWidget(self.no_bounce)
        self.no_bounce.setChecked(self.material.no_bounce)
        self.intensity_label = QLabel('Intensity')
        layout.addWidget(self.intensity_label)
        self.intensity = QSpinBox(self)
        self.intensity.setRange(0, 3)
        layout.addWidget(self.intensity, 3, 1)
        self.intensity.setValue(self.material.intensity)
        self.shadow_label = QLabel('Shadow', self)
        layout.addWidget(self.shadow_label)
        self.shadow = QSpinBox(self)
        self.shadow.setRange(0, 7)
        layout.addWidget(self.shadow, 4, 1)
        self.shadow.setValue(self.material.shadow)
        self.right_widget.setLayout(layout)
        main_widget.setLayout(main_layout)
        self.button = QPushButton('Save', self)
        top_layout.addWidget(self.button)
        self.setLayout(top_layout)
        self.init_triggers()

    def init_triggers(self):
        self.type_selection.currentIndexChanged.connect(self.on_type_change)
        self.basic_effect.currentIndexChanged.connect(self.on_basic_effect_change)
        self.flag.textChanged.connect(self.on_flag_change)
        self.trickable.stateChanged.connect(self.on_trick_change)
        self.drivable.stateChanged.connect(self.on_no_drive_change)
        self.no_bounce.stateChanged.connect(self.on_no_bounce_change)
        self.intensity.valueChanged.connect(self.on_intensity_change)
        self.shadow.valueChanged.connect(self.on_shadow_change)
        self.button.clicked.connect(self.save)
