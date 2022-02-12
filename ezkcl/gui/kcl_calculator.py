from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QHBoxLayout, QSpinBox

import ezkcl.lib.kcl_types


class KCLCalculator(QWidget):
    def __init__(self, kcl_material, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.material = kcl_material
        self.__init_ui()
        self.flag.setText('{:04X}'.format(kcl_material.flag))
        self.setWindowTitle('KCL Calculator')
        self.show()

    def save(self):
        self.parent_widget.reload_mat()
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
        self.basic_effect.addItems(self.items[current])
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
        main_layout = QHBoxLayout()
        self.left_widget = QWidget(self)
        main_layout.addWidget(self.left_widget)
        # LEFT
        layout = QGridLayout()
        self.type_label = QLabel('Type')
        layout.addWidget(self.type_label)
        self.type_selection = QComboBox(self)
        self.items = ezkcl.lib.kcl_types.KCL_TYPES
        self.type_selection.addItems(self.items.keys())
        self.type_selection.currentIndexChanged.connect(self.on_type_change)
        layout.addWidget(self.type_selection, 0, 1)
        self.basic_effect_label = QLabel('Basic Effect')
        layout.addWidget(self.basic_effect_label)
        self.basic_effect = QComboBox(self)
        self.basic_effect.addItems(self.items['Road'])
        self.basic_effect.currentIndexChanged.connect(self.on_basic_effect_change)
        layout.addWidget(self.basic_effect, 1, 1)
        self.flag_label = QLabel('KCL Flag')
        layout.addWidget(self.flag_label)
        self.flag = QLineEdit('{:04X}'.format(0), self)
        self.flag.textChanged.connect(self.on_flag_change)
        layout.addWidget(self.flag, 2, 1)
        self.left_widget.setLayout(layout)

        # RIGHT
        layout = QGridLayout()
        self.right_widget = QWidget(self)
        main_layout.addWidget(self.right_widget)
        self.trickable = QCheckBox('Trickable')
        self.trickable.stateChanged.connect(self.on_trick_change)
        layout.addWidget(self.trickable)
        self.drivable = QCheckBox('Not drivable')
        self.drivable.stateChanged.connect(self.on_no_drive_change)
        layout.addWidget(self.drivable)
        self.no_bounce = QCheckBox('No Bounce')
        self.no_bounce.stateChanged.connect(self.on_no_bounce_change)
        layout.addWidget(self.no_bounce)
        self.intensity_label = QLabel('Intensity')
        layout.addWidget(self.intensity_label)
        self.intensity = QSpinBox(self)
        self.intensity.setRange(0, 3)
        self.intensity.valueChanged.connect(self.on_intensity_change)
        layout.addWidget(self.intensity, 3, 1)
        self.shadow_label = QLabel('Shadow', self)
        layout.addWidget(self.shadow_label)
        self.shadow = QSpinBox(self)
        self.shadow.setRange(0, 7)
        self.shadow.valueChanged.connect(self.on_shadow_change)
        layout.addWidget(self.shadow, 4, 1)
        self.right_widget.setLayout(layout)
        self.setLayout(main_layout)
