import subprocess

from ezkcl.workers.worker import Worker


class DecodeWorker(Worker):
    def __init__(self, kclt, kcl_file, destination):
        super().__init__()
        self.kclt = kclt
        self.destination = destination
        self.kcl_file = kcl_file

    def exec(self):
        result = subprocess.run([
            self.kclt, 'decode', self.kcl_file, '-o',
            '-d', self.destination
        ])
        result.check_returncode()
        return 'Finished decoding ' + self.kcl_file
