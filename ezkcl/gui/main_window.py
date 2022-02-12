import os
import subprocess
import sys

from PyQt5.QtCore import Qt, QThread, QThreadPool
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QApplication, \
    QLineEdit, QFileDialog, QLabel, QMainWindow, QGridLayout

from ezkcl.files import obj, flag
from ezkcl.gui.excluded_widget import ExcludedWidget
from ezkcl.gui.mat_widget import MatWidget
from ezkcl.lib import which
from ezkcl.lib.kcl_material import KclMaterial
from ezkcl.workers.encode_worker import EncodeWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__init_ui()
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(2)
        self.fname = None
        self.cwd = os.getcwd()
        self.kclt = which.which('wkclt')
        if not self.kclt:
            raise FileNotFoundError('Unable to find Wiimms KCL Tool ' +
                                    'are you sure that its installed and on your ' +
                                    'PATH environment variable?')
        self.materials = {}
        self.current_materials = {}
        self.excluded_materials = {}

    def open_dialog(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Open file',
                                                    self.cwd, "Obj/Kcl files (*.obj;*.kcl;*.flag)")
        if fname:
            self.open(fname)
            self.file_edit.setText(fname)

    def open(self, fname):
        self.cwd, base_name = os.path.split(fname)
        base, ext = os.path.splitext(base_name)
        self.fname = os.path.join(self.cwd, base + '.obj')
        if not os.path.exists(self.fname):
            return
        flag_file_mats = self.load_mats_from_flag_file()
        # Load in current material settings
        if flag_file_mats:
            for x in flag_file_mats:
                self.materials[x] = flag_file_mats[x]

        # Add in new materials
        materials = obj.load_obj_mats(fname)
        self.current_materials = {}
        for x in materials:
            cmat = materials[x]
            if cmat.flag:
                self.materials[x] = cmat
                self.current_materials[x] = cmat
            else:
                mat = self.materials.get(x)
                if mat:     # Mat is loaded from flag file or previously exists
                    self.current_materials[cmat.name] = mat
                else:  # Not found
                    self.current_materials[cmat.name] = KclMaterial(cmat.name)
        # Take out excluded
        for x in self.excluded_materials:
            if x in self.current_materials:
                self.current_materials.pop(x)
        self.set_mats(self.current_materials, self.excluded_materials)
        self.statusBar().showMessage('Loaded ' + fname)

    def load_mats_from_flag_file(self):
        d, base = os.path.split(self.fname)
        b_name, ext = os.path.splitext(base)
        flag_file = os.path.join(d, b_name + '.flag')
        if not os.path.exists(flag_file):
            return None
        return flag.load_flag_file(flag_file)

    def set_mats(self, mats, excluded_materials):
        self.mat_widgets = {}
        self.excluded_widgets = {}
        for i in reversed(range(self.mats_layout.count())):
            self.mats_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.excluded_layout.count())):
            self.excluded_layout.itemAt(i).widget().setParent(None)
        even = False
        for mat in sorted(mats, key=lambda x: mats[x].flag):
            mat_ = mats[mat]
            widget = MatWidget(self, mat_.calc_props(), even)
            self.mats_layout.addWidget(widget)
            self.mat_widgets[mat] = widget
            even = not even
        self.mats_widget.setLayout(self.mats_layout)
        if self.mat_widgets and not self.main_mats.isVisible():
            self.main_mats.show()
            self.resize(600, 600)
        for mat in excluded_materials:
            mat_ = excluded_materials[mat]
            widget = ExcludedWidget(self, mat_)
            self.excluded_layout.addWidget(widget)
            self.excluded_widgets[mat_] = widget
        self.excluded_widget.setLayout(self.excluded_layout)
        if self.excluded_materials:
            self.main_excluded.show()

    def encode(self):
        self.start_worker(EncodeWorker(self.kclt, self.fname,
                                       self.current_materials,
                                       self.excluded_widgets
                                       ))

    def start_worker(self, worker):
        worker.connect(self.on_progress, self.on_error)
        self.thread_pool.start(worker)

    def on_progress(self, message):
        self.statusBar().showMessage(message)

    def on_error(self, err_info):
        self.statusBar().showMessage(str(err_info[0]) + str(err_info[1]))

    def decode(self):
        self.statusBar().showMessage('Decoding...')
        kcl_file = os.path.join(self.cwd,
                                os.path.splitext(os.path.basename(self.fname))[0] + '.kcl')
        subprocess.run([self.kclt, 'decode', kcl_file, '-o'])
        self.open(os.path.join(self.fname))
        self.statusBar().showMessage('Finished!')

    def remove_material(self, mat):
        self.current_materials.pop(mat.name)
        widget = self.mat_widgets.pop(mat.name)
        widget.setParent(None)
        self.excluded_materials[mat.name] = mat
        widget = ExcludedWidget(self, mat)
        self.excluded_layout.addWidget(widget)
        self.excluded_widgets[mat.name] = widget
        self.main_excluded.show()

    def remove_excluded(self, mat):
        self.excluded_materials.pop(mat.name)
        widget = self.excluded_widgets.pop(mat.name)
        widget.setParent(None)
        self.current_materials[mat.name] = mat
        self.mat_widgets[mat.name] = MatWidget(self, mat)
        self.mats_layout.addWidget(self.mat_widgets[mat.name])

    def __init_actions(self):
        # Open
        self.encode_act = encode_act = QAction('&Encode', self)
        encode_act.setShortcut('Ctrl+e')
        encode_act.setStatusTip('Encode KCL file')
        encode_act.triggered.connect(self.open_dialog)

    def __init_ui(self):
        self.__init_actions()
        self.setWindowTitle('EZ KCL')
        self.main_layout = QVBoxLayout(self)

        # File Select
        self.file_select_w = QWidget(self)
        self.main_layout.addWidget(self.file_select_w)
        self.file_layout = QHBoxLayout(self)
        self.file_edit = QLineEdit(self)
        self.file_edit.setMaximumWidth(600)
        self.file_layout.addWidget(self.file_edit)
        self.file_browse = QPushButton('Browse', self)
        self.file_browse.setMaximumWidth(150)
        self.file_browse.clicked.connect(self.open_dialog)
        self.file_layout.addWidget(self.file_browse)
        self.file_select_w.setLayout(self.file_layout)

        # Encode/Decode
        self.buttons_widget = QWidget(self)
        self.buttons_layout = QHBoxLayout(self)
        self.decode_button = QPushButton('Decode', self)
        self.decode_button.clicked.connect(self.decode)
        self.buttons_layout.addWidget(self.decode_button)
        self.encode_button = QPushButton('Encode', self)
        self.encode_button.clicked.connect(self.encode)
        self.buttons_layout.addWidget(self.encode_button)
        self.buttons_widget.setLayout(self.buttons_layout)
        self.main_layout.addWidget(self.buttons_widget)

        #   Materials
        self.main_mats = QWidget()
        layout = QVBoxLayout()
        self.mats_labels = QWidget()
        self.mats_l_layout = QHBoxLayout()
        self.mat_label_mat = QLabel('Material')
        self.mat_label_mat.setMaximumWidth(300)
        self.mat_label_type = QLabel('Collision')
        self.mat_label_delete = QLabel('Exclude')
        self.mat_label_delete.setFixedWidth(60)
        self.mats_l_layout.addWidget(self.mat_label_mat)
        self.mats_l_layout.addWidget(self.mat_label_type)
        self.mats_l_layout.addWidget(self.mat_label_delete)
        self.mats_labels.setLayout(self.mats_l_layout)
        layout.addWidget(self.mats_labels)
        self.mats_widget = QWidget()
        self.mats_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.mats_widget)
        self.mats_widget.setStyleSheet('background-color: white')
        layout.addWidget(self.scroll_area)
        self.main_mats.setLayout(layout)
        self.main_layout.addWidget(self.main_mats)

        # Excluded
        self.main_excluded = QWidget()
        layout = QVBoxLayout()
        self.excluded_label = QLabel('Excluded:')
        layout.addWidget(self.excluded_label)
        self.excluded_widget = QWidget()
        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setWidgetResizable(True)
        self.scroll_area2.setWidget(self.excluded_widget)
        self.scroll_area2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.excluded_layout = QVBoxLayout()
        self.excluded_widget.setLayout(self.excluded_layout)
        self.excluded_widget.setStyleSheet('background-color: white')
        layout.addWidget(self.scroll_area2)
        self.main_excluded.setLayout(layout)
        self.main_layout.addWidget(self.main_excluded)
        self.main_excluded.hide()
        self.main_mats.hide()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.statusBar().showMessage('Ready')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(600, 200)
    win.show()
    sys.exit(app.exec_())
