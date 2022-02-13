import string

from PyQt5.QtCore import QObject, pyqtSignal


class WorkerSignals(QObject):
    progress_signal = pyqtSignal(object)
    error_signal = pyqtSignal(object)
    finished_signal = pyqtSignal(bool)
