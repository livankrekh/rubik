def front(f, u, l, d, r, b):
    f.rotate()
    tmp = u.bottom_row
    u.bottom_row = list(reversed(l.right_col))
    l.right_col = d.top_row
    d.top_row = list(reversed(r.left_col))
    r.left_col = tmp

def up(f, u, l, d, r, b):
    u.rotate()
    tmp = b.bottom_row
    f.bottom_row = list(reversed(top_row))


def print_faces(f, u, l, d, r, b):
    u_v = u.repr(False)
    l_v = l.repr(False)
    f_v = f.repr(False)
    r_v = r.repr(False)
    b_v = b.repr(False)
    d_v = d.repr(False)

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
    def __init__(self, name, values):
        self.name = name
        self.v = values
    
    def repr(self, newlines=True):
        r1 = ' '.join(str(_).center(2) for _ in self.v[:3])
        r2 = f'{str(self.v[7]).center(2)} {str(self.name).center(2)} {str(self.v[3]).center(2)}'
        r3 = f'{str(self.v[6]).center(2)} {str(self.v[5]).center(2)} {str(self.v[4]).center(2)}'
        if newlines:
            return '\n'.join((r1, r2, r3))
        else:
            return r1, r2, r3
    
    def __getitem__(self, k):
        return self.v[k]
    
    def __setitem__(self, k, v):
        self.v[k] = v
    
    def rotate(self, reverse=False):
        if reverse:
            self.v = self.v[2:] + self.v[:2]
        else:
            self.v = self.v[-2:] + self.v[:-2]
    
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
    f = [1, 2, 3, 4, 5, 6, 7, 8]
    u = [9, 10, 11, 12, 13, 14, 15, 16]
    l = [17, 18, 19, 20, 21, 22, 23, 24]
    d = [25, 26, 27, 28, 29, 30, 31, 32]
    r = [33, 34, 35, 36, 37, 38, 39, 40]
    b = [41, 42, 43, 44, 45, 46, 47, 48]

    ff = Face('F', f)
    uu = Face('U', u)
    ll = Face('L', l)
    dd = Face('D', d)
    rr = Face('R', r)
    bb = Face('B', b)
    print_faces(ff, uu, ll, dd, rr, bb)
    front(ff, uu, ll, dd, rr, bb)
    print_faces(ff, uu, ll, dd, rr, bb)
    front(ff, uu, ll, dd, rr, bb)
    print_faces(ff, uu, ll, dd, rr, bb)
    front(ff, uu, ll, dd, rr, bb)
    print_faces(ff, uu, ll, dd, rr, bb)
    front(ff, uu, ll, dd, rr, bb)
    print_faces(ff, uu, ll, dd, rr, bb)
