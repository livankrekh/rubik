import numpy as np
import sys

class Cubit:
    u_colors = {v: 'W' for v in [1, 2, 3, 4, 5, 6, 7, 8]}
    l_colors = {v: 'O' for v in [9, 10, 11, 18, 19, 24, 25, 26]}
    f_colors = {v: 'G' for v in [12, 13, 14, 20, 21, 27, 28, 29]}
    r_colors = {v: 'R' for v in [15, 16, 17, 22, 23, 30, 31, 32]}
    b_colors = {v: 'Y' for v in [33, 34, 35, 36, 37, 38, 39, 40]}
    d_colors = {v: 'B' for v in [41, 42, 43, 44, 45, 46, 47, 48]}

    cmap = {**u_colors, **l_colors, **f_colors, **r_colors, **b_colors, **d_colors}

    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return str(self.v).center(2)
    
    @property
    def col(self):
        return self.cmap.get(self.v, self.v)

class Face:
    row_map = {'T': 0, 'C': 1, 'D': 2}
    col_map = {'L': 0, 'C': 1, 'R': 2}

    def __init__(self, name, values):
        self.name = name
        self.values = values
        ve = [Cubit(v) for v in values]
        vals = ve[:4] + [name] + ve[4:]
        self.arr = np.array(vals).reshape((3, 3))

    def __repr__(self):
        return str(self.arr)

    def accessor(self, row, col):
        return self.arr[self.row_map[row], self.col_map[col]]

class Cubik:
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    l = [9, 10, 11, 18, 19, 24, 25, 26]
    f = [12, 13, 14, 20, 21, 27, 28, 29]
    r = [15, 16, 17, 22, 23, 30, 31, 32]
    b = [33, 34, 35, 36, 37, 38, 39, 40]
    d = [41, 42, 43, 44, 45, 46, 47, 48]

    def __init__(self):
        self.faces = [Face(name, values) for name, values in zip('ULFRBD', [self.u, self.l, self.f, self.r, self.b, self.d])]
        self.face_map = {name: self.faces[i] for i, name in enumerate('ULFRBD')}

    def accessor(self, seq):
        face_name, *cubit_name = seq
        face = self.face_map[face_name]
        return face.accessor(*cubit_name)
    
    def __repr__(self):
        return '\n\n'.join(str(_) for _ in self.faces)


def permute(cubik, seq):
    vals = [cubik.accessor(_) for _ in seq]
    print(vals)
    last_value = vals[-1].v
    for i in range(len(vals) - 1, 0, -1):
        cur, prev = vals[i], vals[i - 1]
        cur.v = prev.v
    vals[0].v = last_value

if __name__ == '__main__':
    cubik = Cubik()
    seq = ['FTL', 'FTR', 'FDR', 'FDL']
    vals = [cubik.accessor(_) for _ in seq]
    # print(vals)
    permute(cubik, seq)
    print(cubik)
    # print(cubik)
    # u = Face('U', [1, 2, 3, 4, 5, 6, 7, 8])
    # l = Face('L', [9, 10, 11, 18, 19, 24, 25, 26])

    # permute(u, l, ['UTL', 'UTR', 'UDR', 'UDL'])
    # print(a)
