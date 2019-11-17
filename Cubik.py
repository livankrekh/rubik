import numpy as np
import sys
import itertools
import math


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
    
    def copy(self):
        return Cubit(self.v)

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
        self.col = self.cmap_name[name]
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
    
    def copy(self):
        f = Face(self.name, self.values)
        f.ve = [c.copy() for c in self.ve]
        vals = f.ve[:4] + [self.name] + f.ve[4:]
        f.arr = np.array(vals).reshape((3, 3))
        return f

class Cubik:
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    l = [9, 10, 11, 18, 19, 24, 25, 26]
    f = [12, 13, 14, 20, 21, 27, 28, 29]
    r = [15, 16, 17, 22, 23, 30, 31, 32]
    d = [33, 34, 35, 36, 37, 38, 39, 40]
    b = [41, 42, 43, 44, 45, 46, 47, 48]

    front_face_move = [ 4, 0, 2, 3, 5, 1, 6, 7,
                        2, 1, 0, 0, 1, 2, 0, 0,
                        4, 1, 2, 3, 8, 5, 6, 0, 7, 9, 10, 11,
                        1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0
                        ]

    left_face_move = [  3, 1, 2, 7, 0, 5, 6, 4,
                        1, 0, 0, 2, 2, 0, 0, 1,
                        0, 5, 2, 3, 1, 9, 6, 7, 8, 4, 10, 11,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ]

    back_face_move = [  0, 1, 6, 2, 4, 5, 7, 3,
                        0, 0, 2, 1, 0, 0, 1, 2,
                        0, 1, 6, 3, 4, 2, 10, 7, 8, 9, 5, 11,
                        0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0
                        ]

    right_face_move = [ 0, 5, 1, 3, 4, 6, 2, 7,
                        0, 2, 1, 0, 0, 1, 2, 0,
                        0, 1, 2, 7, 4, 5, 3, 11, 8, 9, 10, 6,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ]

    up_face_move = [1, 2, 3, 0, 4, 5, 6, 7,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    ]

    down_face_move = [  0, 1, 2, 3, 7, 4, 5, 6  ,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ]

    face_moves = [front_face_move, right_face_move, back_face_move, left_face_move, up_face_move, down_face_move]

    move_to_int = [ "F", "R", "B", "L", "U", "D",
                    "F2", "R2", "B2", "L2", "U2", "D2",
                    "F'", "R'", "B'", "L'", "U'", "D'"
                    ]


    up = [('UTL', 'UTR', 'UDR', 'UDL'), ('UTC', 'UCR', 'UDC', 'UCL'), ('LTL', 'BDR', 'RTL', 'FTL'), ('LTC', 'BDC', 'RTC', 'FTC'), ('LTR', 'BDL', 'RTR', 'FTR')]
    left = [('LTL', 'LTR', 'LDR', 'LDL'), ('LTC', 'LCR', 'LDC', 'LCL'),  ('UTL', 'FTL', 'DTL', 'BTL'), ('UCL', 'FCL', 'DCL', 'BCL'), ('UDL', 'FDL', 'DDL', 'BDL')]
    front = [('FTL', 'FTR', 'FDR', 'FDL'), ('FTC', 'FCR', 'FDC', 'FCL'), ('UDL', 'RTL', 'DTR', 'LDR'), ('UDC', 'RCL', 'DTC', 'LCR'), ('UDR', 'RDL', 'DTL', 'LTR')]
    right = [('RTL', 'RTR', 'RDR', 'RDL'), ('RTC', 'RCR', 'RDC', 'RCL'), ('UTR', 'BTR', 'DTR', 'FTR'), ('UCR', 'BCR', 'DCR', 'FCR'), ('UDR', 'BDR', 'DDR', 'FDR')]
    down = [('DTL', 'DTR', 'DDR', 'DDL'), ('DTC', 'DCR', 'DDC', 'DCL'), ('LDL', 'FDL', 'RDL', 'BDR'), ('LDC', 'FDC', 'RDC', 'BTC'), ('LDR', 'FDR', 'RDR', 'BTL')]
    bottom = [('BTL', 'BTR', 'BDR', 'BDL'), ('BTC', 'BCR', 'BDC', 'BCL'), ('UTL', 'LDL', 'DDR', 'RTR'), ('UTC', 'LCL', 'DDC', 'RCR'), ('LTL', 'DDL', 'RDR', 'UTR')]

    corners = [1,3,6,8,9,11,24,26,12,14,27,29,15,17,30,32,41,43,46,48,33,35,38,40]
    sides = [2,4,5,7,10,18,19,25,13,20,21,28,16,22,23,31,42,44,45,47,34,36,37,39]

    edge_orient_table = open("./Tables/edge_orient_table.dat", 'rb').read()
    edge_perm_corner_orient_table = open("./Tables/edge_perm_corner_orient_table.dat", 'rb').read()
    corner_edge_perm_table = open("./Tables/corner_edge_perm_table.dat", 'rb').read()
    final_table = open("./Tables/final_table.dat", 'rb').read()

    move_map = {'U': up, 'L': left, 'F': front, 'R': right, 'D': down, 'B': bottom,
                "U'": tuple(tuple(reversed(c)) for c in reversed(up)),
                "L'": tuple(tuple(reversed(c)) for c in reversed(left)),
                "F'": tuple(tuple(reversed(c)) for c in reversed(front)),
                "R'": tuple(tuple(reversed(c)) for c in reversed(right)),
                "D'": tuple(tuple(reversed(c)) for c in reversed(down)),
                "B'": tuple(tuple(reversed(c)) for c in reversed(bottom))}

    def __init__(self):
        self.faces = [Face(name, values) for name, values in zip('ULFRBD', [self.u, self.l, self.f, self.r, self.b, self.d])]
        self.face_map = {name: self.faces[i] for i, name in enumerate('ULFRBD')}
        self.came_from = []
        r = self.repr()
        self.hash = hash(r)
        self.edge_orient = 0
        self.edge_permutation = 205163983024656
        self.corner_orientation = 0
        self.corner_permutation = 16434824
        self.heuristic_functions = [self.heuristic_stage1, self.heuristic_stage2, self.heuristic_stage3, self.heuristic_stage4]

    def _rehash(self):
        self.hash = hash(self.repr())

    def is_resolved(self):
        return  self.edge_orient == 0 and self.edge_permutation == 205163983024656 and self.corner_orientation == 0 and self.corner_permutation == 16434824

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
    
    def copy(self):
        c = Cubik()
        c.faces = [face.copy() for face in self.faces]
        c.face_map = {name: c.faces[i] for i, name in enumerate('ULFRBD')}
        c.came_from = self.came_from[:]
        c.corner_permutation = self.corner_permutation
        c.corner_orientation = self.corner_orientation
        c.edge_permutation = self.edge_permutation
        c.edge_orient = self.edge_orient
        return c
    
    def calculate_orient(self, move_str):
        move = self.move_to_int.index(move_str)
        direction = int(move / 6) + 1
        face = move % 6
        move = self.face_moves[face]

        for n in range(direction):
            new_ep = 0
            new_cp = 0
            new_co = 0
            new_eo = 0
            i = 0

            for i in range(8):
                new_cp |= ((self.corner_permutation >> move[i] * 3) & 0b111) << (i * 3)
                orient = ((self.corner_orientation >> move[i] * 2) & 0b11)
                orient = (orient + move[8 + i]) % 3

                new_co |= orient << (i * 2)

            for i in range(12):
                new_ep |= ((self.edge_permutation >> (move[16 + i] * 4)) & 0b1111) << (i * 4)
                orient = (self.edge_orient >> move[16 + i]) & 0b1
                orient = (orient + move[28 + i]) % 2
                new_eo |= orient << i

            self.corner_permutation = new_cp
            self.corner_orientation = new_co
            self.edge_permutation = new_ep
            self.edge_orient = new_eo

    def permute(self, seq, reverse=False):
        vals = [self.accessor(_) for _ in seq]
        if reverse:
            vals = list(reversed(vals))
        last_value = vals[-1].v
        for i in range(len(vals) - 1, 0, -1):
            cur, prev = vals[i], vals[i - 1]
            cur.v = prev.v
        vals[0].v = last_value
    
    def apply_permutations(self, permutations, reverse=False):
        for permutation in permutations:
            self.permute(permutation, reverse=reverse)

    def apply_moves(self, moves):
        for move in moves:
            self.calculate_orient(move)

            if move[-1] == '2':
                self.apply_permutations(self.move_map[move[0]])
                self.apply_permutations(self.move_map[move[0]])
            else:
                self.apply_permutations(self.move_map[move])
        self._rehash()

    @staticmethod
    def valid_moves(moves):
        return all(c in "RDFLUB2' " for c in list(moves))
    
    @classmethod
    def parse_moves(cls, moves):
        """ Convert string of moves into list of (move, reverse) """
        if not cls.valid_moves(moves):
            raise ValueError(f"Invalid moves string:", moves)
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

    def get_as_string(self):
        line = list(itertools.chain(*[face.ve for face in self.faces]))
        line = [c.v for c in line]

        return line

    def get_new_pos(self, i):
        line = list(itertools.chain(*[face.ve for face in self.faces]))
        target_line = list(itertools.chain(*[face.ve for face in Cubik().faces]))

        line = [c.v for c in line]
        target_line = [c.v for c in target_line]

        index = line.index(i)

        return target_line[index]

    def n_choose_k(self, n, k):
        if (n < k):
            return 0

        if (n == k or k == 0):
            return 1

        return self.n_choose_k(n - 1, k - 1) + self.n_choose_k(n - 1, k)

    def permutation_to_number(self, perm, size):
        if (size <= 1):
            return 0

        next_perm = [0] * (size - 1)

        for i in range(1, size):
            next_perm[i - 1] = perm[i]

            if (next_perm[i - 1] > perm[0]):
                next_perm[i - 1] -= 1

        return math.factorial(size - 1) * perm[0] + self.permutation_to_number(next_perm, size - 1)

    def combination_to_number(self, perm, size):
        index = 0
        num_ones = 0
        i = size

        while (i > 0):
            if perm[i - 1]:
                num_ones += 1
                index += self.n_choose_k(size - i, num_ones)

            i -= 1

        return index

    def heuristic_stage1(self):
        return self.edge_orient_table[self.edge_orient]

    def heuristic_stage2(self):
        index = 0
        k = 4
        i = 1

        while (i <= 12 and k > 0):

            element = (self.edge_permutation >> (i * 4)) & 0b1111

            if (element > 3 and element < 8):
                index += self.n_choose_k(12 - i, k)
                k -= 1

            i += 1

        return self.edge_perm_corner_orient_table[495 * self.corner_orientation + index]

    def heuristic_stage3(self):
        edge_combination = [False] * 8
        corner_perm = [0] * 8
        j = 0
        i = 0

        while (i < 12):
            if i == 4:
                i = 8

            element = (self.edge_permutation >> (i * 4)) & 0b1111

            if (element == 0 or element == 2 or element == 8 or element == 10):
                edge_combination[j] = True
            else:
                edge_combination[j] = False

            j += 1
            i += 1

        for i in range(8):
            corner_perm[i] = (self.corner_permutation >> (i * 3)) & 0b111

        return self.corner_edge_perm_table[70 * self.permutation_to_number(corner_perm, 8) + self.combination_to_number(edge_combination, 8)]


    def heuristic_stage4(self):
        first_corners = [0, 2, 5, 7]
        second_corners = [1, 3, 4, 6]
        front_edges = [0, 2, 8, 10]
        right_edges = [1, 3, 9, 11]

        first_corner_perm = [0, 0, 0, 0]
        second_corner_perm = [0, 0, 0, 0] 
        front_edge_perm = [0, 0, 0, 0]
        right_edge_perm = [0, 0, 0, 0]
        middle_edge_perm = [0, 0, 0, 0]

        for i in range(4):
            first_corner_perm[i] = (self.corner_permutation >> (first_corners[i] * 3)) & 0b111
            second_corner_perm[i] = (self.corner_permutation >> (second_corners[i] * 3)) & 0b111
            front_edge_perm[i] = (self.edge_permutation >> (front_edges[i] * 4)) & 0b1111
            right_edge_perm[i] = (self.edge_permutation >> (right_edges[i] * 4)) & 0b1111
            middle_edge_perm[i] = ((self.edge_permutation >> ((i + 4) * 4)) & 0b1111) - 4

            for j in range(4):
                if (first_corner_perm[i] == first_corners[j]):
                    first_corner_perm[i] = j
                if (second_corner_perm[i] == second_corners[j]):
                    second_corner_perm[i] = j
                if (front_edge_perm[i] == front_edges[j]):
                    front_edge_perm[i] = j
                if (right_edge_perm[i] == right_edges[j]):
                    right_edge_perm[i] = j

        index = 331776 * self.permutation_to_number(second_corner_perm, 4) \
                + 13824 * self.permutation_to_number(middle_edge_perm, 4) \
                + 576 * self.permutation_to_number(first_corner_perm, 4) \
                + 24 * self.permutation_to_number(front_edge_perm, 4) \
                + self.permutation_to_number(right_edge_perm, 4)

        return self.final_table[index]

    def is_solved(self):
        return all(all(v.col == face.col for v in face.ve) for face in self.faces)

    def __eq__(self, o):
        return self.hash == o.hash
    
    def __hash__(self):
        return int(self.hash)

