from ezkcl.lib.kcl_types import KCL_TYPES


class KclMaterial:
    def __init__(self, name,
                 flag=0,
                 kcl_type=0,
                 basic_effect=0,
                 intensity=0,
                 shadow=0,
                 trickable=0, drivable=0, no_bounce=0
                 ):
        self.no_bounce = no_bounce
        self.drivable = drivable
        self.trickable = trickable
        self.shadow = shadow
        self.intensity = intensity
        self.basic_effect = basic_effect
        self.kcl_type = kcl_type
        self.flag = flag
        self.name = name

    def calc_flag(self):
        w = self.trickable | self.drivable << 1 | self.no_bounce << 2
        x = self.intensity
        y = self.shadow
        z = self.basic_effect
        if z < 0:
            z = 0
        variant = w << 8 | x << 6 | y << 3 | z
        self.flag = self.kcl_type | variant << 5
        return self.flag

    def calc_props(self):
        self.kcl_type = self.flag & 0x1f
        variant = self.flag >> 5 & 0x7ff
        self.basic_effect = variant & 0x7
        self.shadow = variant >> 3 & 0x7
        self.intensity = variant >> 6 & 0x3
        w = variant >> 8 & 0x7
        self.trickable = w & 0x1
        self.drivable = w >> 1 & 0x1
        self.no_bounce = w >> 2 & 0x1
        return self

    def __str__(self):
        kcl_type = list(KCL_TYPES.keys())[self.kcl_type]
        return kcl_type + ' - ' + KCL_TYPES[kcl_type][self.basic_effect]
