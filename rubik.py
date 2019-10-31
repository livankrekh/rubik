import numpy as np
import sys

class Cubit:
    u_colors = {v: 'W' for v in [1, 2, 3, 4, 5, 6, 7, 8]}
    l_colors = {v: 'O' for v in [9, 10, 11, 18, 19, 24, 25, 26]}
    f_colors = {v: 'G' for v in [12, 13, 14, 20, 21, 27, 28, 29]}
    r_colors = {v: 'R' for v in [15, 16, 17, 22, 23, 30, 31, 32]}
    b_colors = {v: 'Y' for v in [41, 42, 43, 44, 45, 46, 47, 48]}
    d_colors = {v: 'B' for v in [33, 34, 35, 36, 37, 38, 39, 40]}

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
    cmap_name = {'U': 'W', 'F': 'G', 'L': 'O', 'R': 'R', 'B': 'Y', 'D': 'B'}

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.ve = [Cubit(v) for v in values]
        vals = self.ve[:4] + [name] + self.ve[4:]
        self.arr = np.array(vals).reshape((3, 3))
        
        self.center = lambda x: str(x).center(2)

    def __repr__(self):
        return str(self.arr)

    def accessor(self, row, col):
        return self.arr[self.row_map[row], self.col_map[col]]

    def repr(self, newlines=True, color=True):
        """ Some nasty code to output everything in pretty format """
        if color:
            vals = [_.col for _ in self.ve[:3]]
        else:
            vals = self.ve[:3]

        r1 = ' '.join(map(self.center, vals))

        if color:
            vals = [self.ve[3].col, self.cmap_name[self.name], self.ve[4].col]
        else:
            vals = [self.ve[3], self.name, self.ve[4]]

        r2 = ' '.join(map(self.center, vals))

        if color:
            vals = [_.col for _ in self.ve[-3:]]
        else:
            vals = self.ve[-3:]

        r3 = ' '.join(map(self.center, vals))
        if newlines:
            return '\n'.join((r1, r2, r3))
        else:
            return r1, r2, r3

class Cubik:
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    l = [9, 10, 11, 18, 19, 24, 25, 26]
    f = [12, 13, 14, 20, 21, 27, 28, 29]
    r = [15, 16, 17, 22, 23, 30, 31, 32]
    d = [33, 34, 35, 36, 37, 38, 39, 40]
    b = [41, 42, 43, 44, 45, 46, 47, 48]

    def __init__(self):
        self.faces = [Face(name, values) for name, values in zip('ULFRBD', [self.u, self.l, self.f, self.r, self.b, self.d])]
        self.face_map = {name: self.faces[i] for i, name in enumerate('ULFRBD')}

    def accessor(self, seq):
        face_name, *cubit_name = seq
        face = self.face_map[face_name]
        return face.accessor(*cubit_name)
    
    def __repr__(self):
        return '\n\n'.join(str(_) for _ in self.faces)
    
    def repr(self, color=False):
        u_v = self.face_map['U'].repr(False, color=color)
        l_v = self.face_map['L'].repr(False, color=color)
        f_v = self.face_map['F'].repr(False, color=color)
        r_v = self.face_map['R'].repr(False, color=color)
        b_v = self.face_map['B'].repr(False, color=color)
        d_v = self.face_map['D'].repr(False, color=color)

        left_pad = f'{(len(l_v[0])) * " "}|'
        right_pad = f'|{(len(r_v[0]) + len(r_v[0])) * " "}'
        
        r1 = left_pad + u_v[0] + right_pad
        r2 = left_pad + u_v[1] + right_pad
        r3 = left_pad + u_v[2] + right_pad
        
        r4 = '|'.join([l_v[0], f_v[0], r_v[0], b_v[0]])
        r5 = '|'.join([l_v[1], f_v[1], r_v[1], b_v[1]])
        r6 = '|'.join([l_v[2], f_v[2], r_v[2], b_v[2]])
        
        r7 = left_pad + d_v[0] + right_pad
        r8 = left_pad + d_v[1] + right_pad
        r9 = left_pad + d_v[2] + right_pad
        
        combined = '\n'.join((r1, r2, r3, r4, r5, r6, r7, r8, r9))
        return combined


def permute(cubik, seq, reverse=False):
    vals = [cubik.accessor(_) for _ in seq]
    if reverse:
        vals = list(reversed(vals))
    last_value = vals[-1].v
    for i in range(len(vals) - 1, 0, -1):
        cur, prev = vals[i], vals[i - 1]
        cur.v = prev.v
    vals[0].v = last_value

def apply_permutations(cubik, permutations, reverse=False):
    for permutation in permutations:
        permute(cubik, permutation, reverse=reverse)

def apply_moves(cubik, moves, reverse=False):
    for move in moves:
        apply_permutations(cubik, move, reverse=reverse)

if __name__ == '__main__':
    cubik = Cubik()
    seq = ['FTL', 'FTR', 'FDR', 'FDL']
    up = [('UTL', 'UTR', 'UDR', 'UDL'), ('UTC', 'UCR', 'UDC', 'UCL'), ('LTL', 'BDR', 'RTL', 'FTL'), ('LTC', 'BDC', 'RTC', 'FTC'), ('LTR', 'BDL', 'RTR', 'FTR')]
    left = [('LTL', 'LTR', 'LDR', 'LDL'), ('LTC', 'LCR', 'LDC', 'LCL'),  ('UTL', 'FTL', 'DTL', 'BTL'), ('UCL', 'FCL', 'DCL', 'BCL'), ('UDL', 'FDL', 'DDL', 'BDL')]
    front = [('FTL', 'FTR', 'FDR', 'FDL'), ('FTC', 'FCR', 'FDC', 'FCL'), ('UDL', 'RTL', 'DTR', 'LDR'), ('UDC', 'RCL', 'DTC', 'LCR'), ('UDR', 'RDL', 'DTL', 'LTR')]
    right = [('RTL', 'RTR', 'RDR', 'RDL'), ('RTC', 'RCR', 'RDC', 'RCL'), ('UTR', 'BTR', 'DTR', 'FTR'), ('UCR', 'BCR', 'DCR', 'FCR'), ('UDR', 'BDR', 'DDR', 'FDR')]
    down = [('DTL', 'DTR', 'DDR', 'DDL'), ('DTC', 'DCR', 'DDC', 'DCL'), ('LDL', 'FDL', 'RDL', 'BDR'), ('LDC', 'FDC', 'RDC', 'BTC'), ('LDR', 'FDR', 'RDR', 'BTL')]
    bottom = [('BTL', 'BTR', 'BDR', 'BDL'), ('BTC', 'BCR', 'BDC', 'BCL'), ('UTL', 'LDL', 'DDR', 'RTR'), ('UTC', 'LCL', 'DDC', 'RCR'), ('LTL', 'DDL', 'RDR', 'UTR')]

    apply_moves(cubik, (up, left, front, right, down, bottom))
    print(cubik.repr(color=True))
    apply_moves(cubik, (bottom, down, right, front, left, up), reverse=True)



    # apply_permutations(cubik, front_permutations, reverse=True)
    # apply_permutations(cubik, up_permutations, reverse=True)
    # apply_permutations(cubik, up_permutations, reverse=True)
    # apply_permutations(cubik, up_permutations)

    # print(vals)
    # permute(cubik, seq)
    print(cubik.repr(color=True))
    # print(cubik)
    # u = Face('U', [1, 2, 3, 4, 5, 6, 7, 8])
    # l = Face('L', [9, 10, 11, 18, 19, 24, 25, 26])

    # permute(u, l, ['UTL', 'UTR', 'UDR', 'UDL'])
    # print(a)
