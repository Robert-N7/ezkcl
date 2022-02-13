import sys
import traceback

from PyQt5.QtCore import QRunnable

from ezkcl.workers.signals import WorkerSignals


class Worker(QRunnable):
    def __init__(self, start_message='Started worker...'):
        super().__init__()
        self.start_message = start_message
        self.signal = WorkerSignals()

    def connect(self, on_progress, on_err, on_finish):
        self.signal.progress_signal.connect(on_progress)
        self.signal.error_signal.connect(on_err)
        if on_finish:
            self.signal.finished_signal.connect(on_finish)

    def exec(self):
        raise NotImplementedError()

    def run(self):
        err = False
        try:
            self.signal.progress_signal.emit(self.start_message)
            result = self.exec()
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signal.error_signal.emit((exctype, value, traceback.format_exc()))
            err = True
        else:
            if result:
                self.signal.progress_signal.emit(result)
            else:
                self.signal.progress_signal.emit('...Finished')
        finally:
            self.signal.finished_signal.emit(err)
