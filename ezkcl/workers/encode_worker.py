import os
import subprocess

from ezkcl.files import flag, obj
from ezkcl.workers.worker import Worker


class EncodeWorker(Worker):
    def __init__(self, kclt, fname, materials, excluded, destination):
        super().__init__()
        self.destination = destination
        self.kclt = kclt
        self.fname = fname
        self.current_materials = materials
        self.excluded = excluded

    def exec(self):
        d, f = os.path.split(self.fname)
        # clean out excluded materials
        obj.remove_materials(self.fname, self.excluded)
        # create flag file, and encode
        flag_fname = os.path.join(d, os.path.splitext(os.path.basename(f))[0] + '.flag')
        flag_file = flag.create_flag_file(flag_fname, self.current_materials)
        result = subprocess.run([self.kclt,
                                 'encode',
                                 self.fname,
                                 '--kcl=drop',
                                 '-o',
                                 '--flag-file', flag_fname,
                                 '-d', self.destination
                                 ])
        result.check_returncode()
        return 'Finished encoding ' + self.fname
