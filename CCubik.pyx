import numpy as np
cimport numpy as np

up = ((0, 2, 7, 5), (1, 4, 6, 3), (8, 47, 14, 11), (9, 46, 15, 12), (10, 45, 16, 13))
left = ((8, 10, 25, 23), (9, 18, 24, 17), (0, 11, 32, 40), (3, 19, 35, 43), (5, 26, 37, 45))
front = ((11, 13, 28, 26), (12, 20, 27, 19), (5, 14, 34, 25), (6, 21, 33, 18), (7, 29, 32, 10))
right = ((14, 16, 31, 29), (15, 22, 30, 21), (2, 42, 34, 13), (4, 44, 36, 20), (7, 47, 39, 28))
down = ((32, 34, 39, 37), (33, 36, 38, 35), (23, 26, 29, 42), (24, 27, 30, 41), (25, 29, 31, 40))
bottom = ((40, 42, 47, 45), (41, 44, 46, 43), (0, 23, 39, 16), (1, 17, 38, 22), (8, 37, 31, 2))

rup = tuple(tuple(reversed(c)) for c in reversed(up))
rleft = tuple(tuple(reversed(c)) for c in reversed(left))
rfront = tuple(tuple(reversed(c)) for c in reversed(front))
rright = tuple(tuple(reversed(c)) for c in reversed(right))
rdown = tuple(tuple(reversed(c)) for c in reversed(down))
rbottom = tuple(tuple(reversed(c)) for c in reversed(bottom))

cpdef h_try(CCubik candidate, CCubik solution, mask):
    cdef int i = 0
    cdef int accum = 0
    for i in range(len(mask)):
        accum += candidate.v[mask[i]] != solution.v[mask[i]]
    return accum

cdef class CCubik:

    cdef public v, came_from, hash, heur, g

    move_map = {'U': up, 'L': left, 'F': front, 'R': right, 'D': down, 'B': bottom,
                "U'": rup,
                "L'": rleft,
                "F'": rfront,
                "R'": rright,
                "D'": rdown,
                "B'": rbottom,
                "U2": up + up, "L2": left + left, "F2": front + front,
                "R2": right + right, "D2": down + down, "B2": bottom + bottom}

    def __init__(self):
        self.v = np.arange(1, 49)
        self.came_from = []
        self.hash = hash(self.v.tostring())
        self.heur = 0
        self.g = 0

    def _rehash(self):
        self.hash = hash(self.v.tostring())
    
    def __repr__(self):
        return str(self.v)
    
    def repr(self, color=False):
        u = self.v[[0, 1, 2, 3, 4, 5, 6, 7]]
        u1 = ' '.join(str(_).center(2) for _ in u[:3])
        u2 = ' '.join([str(u[3]).center(2), 'U'.center(2), str(u[4]).center(2)])
        u3 = ' '.join(str(_).center(2) for _ in u[-3:])
        
        u_v = [u1, u2, u3]
        
        l = self.v[[8, 9, 10, 17, 18, 23, 24, 25]]
        l1 = ' '.join(str(_).center(2) for _ in l[:3])
        l2 = ' '.join([str(l[3]).center(2), 'L'.center(2), str(l[4]).center(2)])
        l3 = ' '.join(str(_).center(2) for _ in l[-3:])
        
        l_v = [l1, l2, l3]

        
        f = self.v[[11, 12, 13, 19, 20, 26, 27, 28]]
        f1 = ' '.join(str(_).center(2) for _ in f[:3])
        f2 = ' '.join([str(f[3]).center(2), 'F'.center(2), str(f[4]).center(2)])
        f3 = ' '.join(str(_).center(2) for _ in f[-3:])
        
        f_v = [f1, f2, f3]

        r = self.v[[14, 15, 16, 21, 22, 29, 30, 31]]
        r1 = ' '.join(str(_).center(2) for _ in r[:3])
        r2 = ' '.join([str(r[3]).center(2), 'R'.center(2), str(r[4]).center(2)])
        r3 = ' '.join(str(_).center(2) for _ in r[-3:])
        
        r_v = [r1, r2, r3]

        b = self.v[[40, 41, 42, 43, 44, 45, 46, 47]]
        b1 = ' '.join(str(_).center(2) for _ in b[:3])
        b2 = ' '.join([str(b[3]).center(2), 'B'.center(2), str(b[4]).center(2)])
        b3 = ' '.join(str(_).center(2) for _ in b[-3:])
        
        b_v = [b1, b2, b3]

        
        d = self.v[[32, 33, 34, 35, 36, 37, 38, 39]]
        d1 = ' '.join(str(_).center(2) for _ in d[:3])
        d2 = ' '.join([str(d[3]).center(2), 'D'.center(2), str(d[4]).center(2)])
        d3 = ' '.join(str(_).center(2) for _ in d[-3:])
        
        d_v = [d1, d2, d3]

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
    
    def copy(self):
        c = CCubik()
        c.v = np.copy(self.v)
        c.came_from = self.came_from[:]
        return c
    
    def permute(self, seq):
        cdef int i = 0;
        cdef int last_value = self.v[seq[-1]]
        for i in range(len(seq) - 1, 0, -1):
            self.v[seq[i]] = self.v[seq[i - 1]]
        self.v[seq[0]] = last_value
    
    def apply_permutations(self, permutations):
        for permutation in permutations:
            self.permute(permutation)

    def apply_moves(self, moves):
        for move in moves:
            self.apply_permutations(self.move_map[move])
        self._rehash()

    @staticmethod
    def valid_moves(moves):
        return all(c in "RDFLUB2' " for c in list(moves))
    
    @classmethod
    def parse_moves(cls, moves):
        """ Convert string of moves into list of (move, reverse) """
#         if not cls.valid_moves(moves):
#             raise ValueError(f"Invalid moves string:", moves)
        moves = [c for c in moves.split(" ") if c]
        expand_moves = []
        for move in moves:
            if len(move) == 1:
                if move in cls.move_map:
                    expand_moves.append(move)
            elif len(move) == 2:
                letter, modifier = move
                if letter not in cls.move_map:
                    raise ValueError("Invalid move:", move)
                if modifier == '2':
                    expand_moves.append(letter)
                    expand_moves.append(letter)
                elif modifier == "'":
                    expand_moves.append(move)
                else:
                    raise ValueError("Invalid move (modifier):", move)
            else:
                raise ValueError("Invalid move:", move)
        return expand_moves

    def is_solved(self):
        return np.all(self.v == np.arange(1, 49))

    def __eq__(self, o):
        return self.hash == o.hash
    
    def __hash__(self):
        return int(self.hash)