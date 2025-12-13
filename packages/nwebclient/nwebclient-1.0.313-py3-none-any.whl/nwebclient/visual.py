
import math
from typing import Tuple
from nwebclient import util as u


class CubedOrbitalLayout:

    @staticmethod
    def get_orbit(index: int):
        return math.ceil(math.sqrt(index))

    @staticmethod
    def get_xy(index: int, r: int = 1) -> Tuple[int, int]:
        orbit = CubedOrbitalLayout.get_orbit(index)
        ug = math.pow(orbit-1, 2)+1
        # og = math.pow(orbit, 2)
        mg = ug + (orbit-1)
        pos_u = int(index - ug) + 1
        pos_o = int(index - mg)
        if index < mg:
            return orbit*r, pos_u*r
        elif index > mg:
            return pos_o*r, orbit*r
        else:
            return orbit*r, orbit*r


class Items(u.List):

    def __init__(self):
        super().__init__()

    def is_free(self, point=(100, 100)):
        for elem in self:
            if elem.intersects(point):
                return False
        return True

    def get_min_pos(self, c=0):
        res = 0
        for elem in self:
            res = min(elem.pos[c], res)
        return res

    def move_all_to_positive(self):
        x_min = self.get_min_pos(0)
        if x_min < 0:
            self.move_all((x_min, 0))
        y_min = self.get_min_pos(1)
        if y_min < 0:
            self.move_all((0, y_min))

    def move_all(self, vector):
        for elem in self:
            elem.move_by(vector)

    def layout_non_overlapping(self):
        i = 1
        for item in self:
            (x, y) = CubedOrbitalLayout.get_xy(i, 200)
            item.set_pos(x, y)
            i += 1
        pass


class Positioned:

    def __init__(self, obj=None):
        self.pos = (0, 0)
        self.obj = obj

    def __getattr__(self, item):
        if self.obj is not None:
            r = getattr(self.obj, item, None)
            if r is not None:
                return r
        return None

    def move_by(self, pos):
        self.pos[0] += self.pos[0] + pos[0]
        self.pos[1] += self.pos[1] + pos[1]

    def set_pos(self, x, y):
        self.pos = (x, y)

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]


class Box(Positioned):

    def __init__(self, obj=None):
        super().__init__(obj)
        self.size = (200, 100)

    def __contains__(self, item):
        if isinstance(item, tuple) and len(item) == 2:
            return self.intersects(item)
        else:
            return False

    def title(self):
        return u.get_title(self.obj, "Box")

    def intersects(self, point):
        x = self.get_x() < point[0] < self.get_x() + self.size[0]
        y = self.get_y() < point[1] < self.get_y() + self.size[1]
        return x and y
