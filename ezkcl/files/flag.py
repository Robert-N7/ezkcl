import datetime

from ezkcl.lib.kcl_material import KclMaterial


def create_flag_file(filename, materials):
    fheader = f'#-----------------------------------------------------------------------\n' \
              f'# Flag file created with Ez KCL\n' \
              f'# {datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}' \
              f'#-----------------------------------------------------------------------\n'
    for m in materials:
        mat = materials[m]
        fheader += f'{mat.name} = {mat.flag:04X}\n'
    with open(filename, 'w') as f:
        f.write(fheader)
    return filename


def get_int(x):
    if x.startswith('0x'):
        return int(x, 16)
    return int(x)


def process_line(mats, line):
    pos = line.find('=')
    if pos > 0:
        end_pos = line.find('#', pos)
        if end_pos == -1:
            end_pos = len(line)
        name = line[:pos].strip()
        flag = line[pos + 1:end_pos].strip()
        if not flag:
            raise ValueError('Invalid flag in line ' + line)
        if flag[0] in ('f', 'a', 'i'):
            params = flag[1:].strip('()').split(',')
            if flag[0] == 'f':
                flag = get_int(params[0]) & 0x1f | get_int(params[1]) << 5
            elif flag[0] == 'a':
                flag = get_int(params[0]) & 0x1f \
                       | (get_int(params[1]) & 0x7) << 13 \
                       | (get_int(params[2]) & 0x3) << 11 \
                       | (get_int(params[3]) & 0x7) << 8 \
                       | (get_int(params[4]) & 0x7) << 5
            elif flag[0] == 'i':
                flag = get_int(params[0]) & 0x1f \
                       | (get_int(params[1]) & 0x7) << 5 \
                       | (get_int(params[2]) & 0xff) << 8
        mat = KclMaterial(name, flag)
        mats[name] = mat
        return True
    return False


def load_flag_file(filename):
    mats = {}
    with open(filename) as f:
        for x in f.readlines():
            l = x.strip()
            if l and l[0] not in ('@', '#'):
                process_line(mats, l)
    return mats
