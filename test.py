def front(f, u, l, d, r, b):
    f.rotate()
    # tmp = u.bottom_row
    # u.bottom_row = list(reversed(l.right_col))
    # l.right_col = d.top_row
    # d.top_row = list(reversed(r.left_col))
    # r.left_col = tmp
    # 0 1 2 3 4 5 6 7
    # 2 4 7 1 6 0 3 5

def up(f, u, l, d, r, b):
    u.rotate()
    tmp = b.bottom_row
    f.bottom_row = list(reversed(top_row))


def print_faces(f, u, l, d, r, b, color=False):
    u_v = u.repr(False, color=color)
    l_v = l.repr(False, color=color)
    f_v = f.repr(False, color=color)
    r_v = r.repr(False, color=color)
    b_v = b.repr(False, color=color)
    d_v = d.repr(False, color=color)

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
    print(combined)

class Face(list):
    u_colors = {v: 'W' for v in [1, 2, 3, 4, 5, 6, 7, 8]}
    l_colors = {v: 'O' for v in [9, 10, 11, 18, 19, 24, 25, 26]}
    f_colors = {v: 'G' for v in [12, 13, 14, 20, 21, 27, 28, 29]}
    r_colors = {v: 'R' for v in [15, 16, 17, 22, 23, 30, 31, 32]}
    b_colors = {v: 'Y' for v in [33, 34, 35, 36, 37, 38, 39, 40]}
    d_colors = {v: 'B' for v in [41, 42, 43, 44, 45, 46, 47, 48]}

    cmap = {**u_colors, **l_colors, **f_colors, **r_colors, **b_colors, **d_colors}
    cmap_name = {'U': 'W', 'F': 'G', 'L': 'O', 'R': 'R', 'B': 'Y', 'D': 'B'}


    # 0 1 2 3 4 5 6 7
    # 2 4 7 1 6 0 3 5
    rot_map = {0: 2, 1: 4, 2: 7, 3: 1, 4: 6, 5: 0, 6: 3, 7: 5}
    rrot_map = {v: k for k, v in rot_map.items()}
    def __init__(self, name, values):
        self.name = name
        self.v = values

        self.center = lambda x: str(x).center(2)
    
    def repr(self, newlines=True, color=True):
        """ Some nasty code to output everything in pretty format """
        if color:
            vals = [self.cmap[_] for _ in self.v[:3]]
        else:
            vals = self.v[:3]

        r1 = ' '.join(map(self.center, vals))

        if color:
            vals = [self.cmap[self.v[3]], self.cmap_name[self.name], self.cmap[self.v[4]]]
        else:
            vals = [self.v[3], self.name, self.v[4]]

        r2 = ' '.join(map(self.center, vals))

        if color:
            vals = [self.cmap[_] for _ in self.v[-3:]]
        else:
            vals = self.v[-3:]

        r3 = ' '.join(map(self.center, vals))
        if newlines:
            return '\n'.join((r1, r2, r3))
        else:
            return r1, r2, r3
    
    def __getitem__(self, k):
        return self.v[k]
    
    def __setitem__(self, k, v):
        self.v[k] = v
    
    def rotate(self, reverse=False):
        # old = self.v[:]
        # map = self.rot_map
        # if reverse:
        #     map = self.rrot_map
        # for i in range(8):
        #     self.v[map[i]] = old[i]
        self.permute([self.tl, self.tr, self.dr, self.dl])

    @property
    def tl(self):
        return 0
    
    @tl.setter
    def tl(self, v):
        self.v[0] = v
    
    @property
    def tc(self):
        return 1
    
    @tc.setter
    def tc(self, v):
        self.v[1] = v
    
    @property
    def tr(self):
        return 2
    
    @tr.setter
    def tr(self, v):
        self.v[2] = v
    
    @property
    def cl(self):
        return 3

    @cl.setter
    def cl(self, v):
        self.v[3] = v
    
    @property
    def cr(self):
        return 4
    
    @cr.setter
    def cr(self, v):
        self.v[4] = v
    
    @property
    def dl(self):
        return 5
    
    @dl.setter
    def dl(self, v):
        self.v[5] = v
    
    @property
    def dc(self):
        return 6
    
    @dc.setter
    def dc(self, v):
        self.v[6] = v
    
    @property
    def dr(self):
        return 7
    
    @dr.setter
    def dr(self, v):
        self.v[7] = v
    
    def permute(self, seq, reverse=False):
        pass


    
    @property
    def bottom_row(self):
        """ Bottom row getter """
        return (self.v[6], self.v[5], self.v[4])
    
    @bottom_row.setter
    def bottom_row(self, v):
        self[6] = v[0]
        self[5] = v[1]
        self[4] = v[2]
    
    @property
    def right_col(self):
        return self[2:5]
    
    @right_col.setter
    def right_col(self, v):
        self[2] = v[0]
        self[3] = v[1]
        self[4] = v[2]
    
    @property
    def top_row(self):
        return self[:3]
    
    @top_row.setter
    def top_row(self, v):
        self[:3] = v
    
    @property
    def left_col(self):
        return (self[0], self[7], self[6])
    
    @left_col.setter
    def left_col(self, v):
        self[0] = v[0]
        self[7] = v[1]
        self[6] = v[2]
    


if __name__ == '__main__':
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    l = [9, 10, 11, 18, 19, 24, 25, 26]
    f = [12, 13, 14, 20, 21, 27, 28, 29]
    r = [15, 16, 17, 22, 23, 30, 31, 32]
    b = [33, 34, 35, 36, 37, 38, 39, 40]
    d = [41, 42, 43, 44, 45, 46, 47, 48]

    ff = Face('F', f)
    uu = Face('U', u)
    ll = Face('L', l)
    dd = Face('D', d)
    rr = Face('R', r)
    bb = Face('B', b)
    print_faces(ff, uu, ll, dd, rr, bb)
    print()
    print_faces(ff, uu, ll, dd, rr, bb, color=True)

    front(ff, uu, ll, dd, rr, bb)
    print()
    print_faces(ff, uu, ll, dd, rr, bb)
    print()
    print_faces(ff, uu, ll, dd, rr, bb, color=True)
    # print_faces(ff, uu, ll, dd, rr, bb)
    # front(ff, uu, ll, dd, rr, bb)
    # print()
    # print_faces(ff, uu, ll, dd, rr, bb)
    # front(ff, uu, ll, dd, rr, bb)
    # print()
    # print_faces(ff, uu, ll, dd, rr, bb)
    # front(ff, uu, ll, dd, rr, bb)
    # print()
    # print_faces(ff, uu, ll, dd, rr, bb)
