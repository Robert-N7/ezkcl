import os


def which(program):
    def is_exe(exe_file):
        return os.path.isfile(exe_file) and os.access(exe_file, os.X_OK)

    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if is_exe(exe_file):
            return exe_file
        exe_file += '.exe'
        if is_exe(exe_file):
            return exe_file
