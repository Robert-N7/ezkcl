import sys

from PyQt5.QtWidgets import QApplication

from ezkcl.gui.main_window import MainWindow

app = QApplication(sys.argv)
win = MainWindow(*sys.argv[1:])
sys.exit(app.exec_())
