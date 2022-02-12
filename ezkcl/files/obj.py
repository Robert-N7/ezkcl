import re

from ezkcl.lib.kcl_material import KclMaterial


def extract_flag(name):
    match = re.search('F(\d{4})$', name)
    if match:
        return int(match.group(1), 16)


def load_obj_mats(filename):
    mats = {}
    g_flag = None
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('usemtl'):
                name = line[6:].strip()
                flag = extract_flag(name)
                mats[name] = KclMaterial(name, flag or g_flag)
            elif line.startswith('g'):
                name = line[1:].strip()
                g_flag = extract_flag(name)
    return mats


def remove_materials(filename, materials):
    if not materials:
        return False
    start_group = False
    i = 0
    first_group_line = 0
    mat_name = None
    all_ignored = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line and line[0] in ('g', 's', 'u'):
            if not start_group:
                if first_group_line and mat_name and mat_name in materials:
                    all_ignored.extend(range(first_group_line, i))
                start_group = True
                first_group_line = i
            if line.startswith('usemtl'):
                mat_name = line[6:].strip()
        elif line and line[0] != '#':
            start_group = False
        i += 1
    if first_group_line and mat_name and mat_name in materials:
        all_ignored.extend(range(first_group_line, i))
    all_ignored = set(all_ignored)
    n_lines = []
    for i, line in enumerate(lines):
        if i not in all_ignored:
            n_lines.append(line)

    with open(filename, 'w') as f:
        f.write(''.join(n_lines))
