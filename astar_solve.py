from rubik import Cubik

import bisect

class PriorityQueue(list):
    def __init__(self):
        self.v = []
        self.k = []
    
    def add(self, key, value):
        i = bisect.bisect_right(self.k, key)
        self.v.insert(i, value)
        self.k.insert(i, key)
    
    def pop(self):
        item = self.v.pop(0)
        key = self.k.pop(0)
        return item
    
    def __len__(self):
        return len(self.v)

def h_mismatch(cubik, solution):
    cnt = 0
    for f_cand, f_sol in zip(cubik.faces, solution.faces):
        # print(f_cand, f_sol)
        for v_cand, v_sol in zip(f_cand.ve, f_sol.ve):
            cnt += v_cand != v_sol
    return cnt


if __name__ == '__main__':
    cubik = Cubik()

    solution = cubik.copy()

    cubik.apply_moves(cubik.parse_moves("R2 D' B' D F2 R F2 R2 U L' F2 U' B' L2 R D B' R' B2 L2 F2 L2 R2 U2 D2"))

    print(cubik.repr(color=True))
    print(h_mismatch(cubik, solution))
