import numpy as np
import sys
import itertools
import pandas as pd


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

    up = [('UTL', 'UTR', 'UDR', 'UDL'), ('UTC', 'UCR', 'UDC', 'UCL'), ('LTL', 'BDR', 'RTL', 'FTL'), ('LTC', 'BDC', 'RTC', 'FTC'), ('LTR', 'BDL', 'RTR', 'FTR')]
    left = [('LTL', 'LTR', 'LDR', 'LDL'), ('LTC', 'LCR', 'LDC', 'LCL'),  ('UTL', 'FTL', 'DTL', 'BTL'), ('UCL', 'FCL', 'DCL', 'BCL'), ('UDL', 'FDL', 'DDL', 'BDL')]
    front = [('FTL', 'FTR', 'FDR', 'FDL'), ('FTC', 'FCR', 'FDC', 'FCL'), ('UDL', 'RTL', 'DTR', 'LDR'), ('UDC', 'RCL', 'DTC', 'LCR'), ('UDR', 'RDL', 'DTL', 'LTR')]
    right = [('RTL', 'RTR', 'RDR', 'RDL'), ('RTC', 'RCR', 'RDC', 'RCL'), ('UTR', 'BTR', 'DTR', 'FTR'), ('UCR', 'BCR', 'DCR', 'FCR'), ('UDR', 'BDR', 'DDR', 'FDR')]
    down = [('DTL', 'DTR', 'DDR', 'DDL'), ('DTC', 'DCR', 'DDC', 'DCL'), ('LDL', 'FDL', 'RDL', 'BDR'), ('LDC', 'FDC', 'RDC', 'BTC'), ('LDR', 'FDR', 'RDR', 'BTL')]
    bottom = [('BTL', 'BTR', 'BDR', 'BDL'), ('BTC', 'BCR', 'BDC', 'BCL'), ('UTL', 'LDL', 'DDR', 'RTR'), ('UTC', 'LCL', 'DDC', 'RCR'), ('LTL', 'DDL', 'RDR', 'UTR')]

    corners = [1,3,6,8,9,11,24,26,12,14,27,29,15,17,30,32,41,43,46,48,33,35,38,40]
    sides = [2,4,5,7,10,18,19,25,13,20,21,28,16,22,23,31,42,44,45,47,34,36,37,39]

    corner_db = pd.read_csv("./corner_db.csv")
    side_db = pd.read_csv("./side_db.csv")
    corner_moves_db = pd.read_csv("./corner_moves_db.csv")
    side_moves_db = pd.read_csv("./side_moves_db.csv")
    corner_db.columns = ['index', 'side', 'position', 'grade']
    side_db.columns = ['index', 'side', 'position', 'grade']
    all_db = pd.concat([corner_db, side_db], ignore_index=True)

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

    def _rehash(self):
        self.hash = hash(self.repr())

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
        return c
    
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

    def get_new_pos(self, i):
        line = list(itertools.chain(*[face.ve for face in self.faces]))
        target_line = list(itertools.chain(*[face.ve for face in Cubik().faces]))

        line = [c.v for c in line]
        target_line = [c.v for c in target_line]

        index = line.index(i)

        return target_line[index]

    def manh_distance_corner(self, actions=[]):
        curr_cubik = self.copy()
        curr_cubik.apply_moves(actions)
        res = 0

        for corner in curr_cubik.corners:
            new_corner_pos = curr_cubik.get_new_pos(corner)

            if (new_corner_pos == corner):
                continue

            curr_dist = curr_cubik.corner_db[(curr_cubik.corner_db["side"] == corner) &
                                       (curr_cubik.corner_db["position"] == new_corner_pos)]['grade'].min()

            res += curr_dist

        return res

    def manh_distance_side(self, actions=[]):
        curr_cubik = self.copy()
        curr_cubik.apply_moves(actions)
        res = 0

        for side in curr_cubik.sides:
            new_side_pos = curr_cubik.get_new_pos(side)

            if (new_side_pos == side):
                continue

            curr_dist = curr_cubik.side_db[(curr_cubik.side_db["side"] == side) &
                                       (curr_cubik.side_db["position"] == new_side_pos)]['grade'].min()

            res += curr_dist

        return res

    def manh_distance(self, cubits, actions=[]):
        curr_cubik = self.copy()
        curr_cubik.apply_moves(actions)
        res = 0

        for side in cubits:
            new_side_pos = curr_cubik.get_new_pos(side)

            if (new_side_pos == side):
                continue

            curr_dist = curr_cubik.all_db[(curr_cubik.all_db["side"] == side) &
                                       (curr_cubik.all_db["position"] == new_side_pos)]['grade'].min()

            res += curr_dist

        return res

    def other_corner_distance(self, actions, prohibited_moves=[]):
        curr_cubik = self.copy()
        curr_cubik.apply_moves(actions)
        res = 0

        for corner in curr_cubik.corners:
            new_corner_pos = curr_cubik.get_new_pos(corner)

            if (new_corner_pos == corner):
                continue

            valid = False
            tmp_db = self.corner_moves_db[(self.corner_moves_db['corner'] == corner) &
                                          (self.corner_moves_db['position'] == new_corner_pos)]

            for i, row in tmp_db.iterrows():
                l_tmp = pd.unique(row[['first_move', 'second_move', 'third_move']].values.ravel('K'))
                matches = [x for x in list(l_tmp) if x in prohibited_moves]

                if len(matches) < 1:
                    valid = True
                    break

            if not valid:
                res += 1

        return res

    def other_side_distance(self, actions, prohibited_moves=[]):
        curr_cubik = self.copy()
        curr_cubik.apply_moves(actions)
        res = 0

        for side in curr_cubik.sides:
            new_side_pos = curr_cubik.get_new_pos(side)

            if (new_side_pos == side):
                continue

            valid = False
            tmp_db = self.side_moves_db[(self.side_moves_db['side'] == side) &
                                        (self.side_moves_db['position'] == new_side_pos)]

            for i, row in tmp_db.iterrows():
                l_tmp = pd.unique(row[['first_move', 'second_move', 'third_move']].values.ravel('K'))
                matches = [x for x in list(l_tmp) if x in prohibited_moves]

                if len(matches) < 1:
                    valid = True
                    break

            if not valid:
                res += 1

        return res


    def is_solved(self):
        return all(all(v.col == face.col for v in face.ve) for face in self.faces)

    def __eq__(self, o):
        return self.hash == o.hash
    
    def __hash__(self):
        return int(self.hash)

all_actions = ["U", "R", "F", "D", "L", "B",
               "U'", "R'", "F'", "D'", "L'", "B'"
               "U2", "R2", "F2", "D2", "L2", "B2"
               ]

def recurs_a_star(cubik, action, prev_dist, i):
    if i > 7:
        return None

    new_cubik = cubik.copy()
    new_cubik.apply_moves([action])
    curr_dist = new_cubik.other_side_distance([], ["L", "R", "L'", "R'"])

    if (curr_dist < 1):
        return [action]

    print("Prev dist =", prev_dist)
    print("Curr dist =", curr_dist)

    # if prev_dist <= curr_dist:
    #     return None

    current_actions = all_actions[:]

    for act in current_actions:
        if (act[-1] == "'" and action[-1] != "'" and act[0] == action[0]):
            continue
        if (act[-1] != "'" and action[-1] == "'" and act[0] == action[0]):
            continue

        res = recurs_a_star(new_cubik, act, curr_dist, i+1)

        if (res == None):
            pass
        else:
            return [action] + res

    return None


if __name__ == '__main__':
    cubik = Cubik()

    print(cubik.faces)
    # cubik.apply_moves(["U2", "B2", "B", "R2", "U'", "B'", "L", "F'"])
    # cubik.apply_moves(["U", "B", "R"])
    cubik.apply_moves(cubik.parse_moves("R2 D' B' D F2 R F2 R2 U L' F2 U' B' L2 R D B' R' B2 L2 F2 L2 R2 U2 D2"))

    print(cubik.faces)

    # curr_corn_dist = cubik.other_corner_distance([], ["U", "D", "U'", "D'"])
    actions = []

    new_cubik = cubik.copy()
    curr_manh = new_cubik.other_side_distance([], ["L", "R", "L'", "R'"])

    print("G0 distance =", curr_manh)

    for action in all_actions:
        res = recurs_a_star(cubik, action, curr_manh, 0)

        print(res)

        if res != None:
            actions += res
            break

    # while curr_manh > 0:
    #     for action in all_actions:
    #         best_manh = curr_manh
    #         best_action = None

    #         tmp_manh = new_cubik.other_corner_distance([action], ["L", "R", "L'", "R'"])

    #         if tmp_manh < best_manh:
    #             best_manh = tmp_manh
    #             best_action = action

    #     if (best_action != None):
    #         curr_manh = best_manh
    #         new_cubik.apply_moves([action])
    #         actions += [action]

    #         print("Current distance =", curr_manh)
    #     else:
    #         print("No resolve for G0")
    #         break


    # for action in all_actions:
    #     res = recurs_a_star(cubik, action, curr_corn_dist, 0)

    #     print(res)

    #     if res != None:
    #         actions = res
    #         break

    # new_cubik = cubik.copy()
    # new_cubik.apply_moves(actions)
    # curr_corn_dist = new_cubik.manh_distance([4,5,18,19,20,21,36,37])

    # current_actions = all_actions[:]
    # del current_actions[current_actions.index("U")]
    # del current_actions[current_actions.index("D")]
    # del current_actions[current_actions.index("U'")]
    # del current_actions[current_actions.index("D'")]

    # curr_manh = new_cubik.other_corner_distance([], ["U", "D", "U'", "D'"])

    # while curr_manh > 0:
    #     for action in all_actions:
    #         best_manh = curr_manh
    #         best_action = None

    #         tmp_manh = new_cubik.other_corner_distance([action], ["U", "D", "U'", "D'"])

    #         if tmp_manh < best_manh:
    #             best_manh = tmp_manh
    #             best_action = action

    #     if (best_action != None):
    #         curr_manh = best_manh
    #         new_cubik.apply_moves([action])
    #         actions += [action]

    #         print("Current distance =", curr_manh)
    #     else:
    #         break

    cubik.apply_moves(actions)

    print(cubik.faces)

    print("Resolve =", actions)
    print("Solved -", cubik.is_solved())

    # print(cubik.manh_distance_corner(["B"]))
    # print(cubik.manh_distance_corner(["B"]))
    # print(cubik.manh_distance_corner(["R"]))
    # print(cubik.manh_distance_corner(["U'"]))
    # print(cubik.manh_distance_corner(["B'"]))
    # print(cubik.manh_distance_corner(["L"]))
    # print(cubik.manh_distance_corner(["L"]))

    # cubik.apply_moves(['R', 'B'])
    # print(cubik.is_solved(), cubik.hash)
    # cubik.apply_moves(["B'","R'"])
    # print(cubik.is_solved(), cubik.hash)
    # cubik.apply_moves(cubik.parse_moves("R2 D' B' D F2 R F2 R2 U L' F2 U' B' L2 R D B' R' B2 L2 F2 L2 R2 U2 D2"))
    # print(cubik.is_solved(), cubik.hash)
