import pyximport
pyximport.install(language_level=3)
from CCubik import *
# from rubik import Cubik
import time
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

def h_mismatch(candidate, solution, mask=None):
    cnt = 0
    for f_cand, f_sol in zip(candidate.faces, solution.faces):
        for v_cand, v_sol in zip(f_cand.ve, f_sol.ve):
            if mask is None or (v_sol.v in mask):
                cnt += v_cand.v != v_sol.v
    return cnt

def h_manhattan(candidate, solution, mask=None):
    accum = 0
    for f_cand, f_sol in zip(candidate.v, solution.v):
        if mask is None or (f_sol in mask):
            accum += abs(f_cand - f_sol)
    return accum

def h_euclidean(candidate, solution, mask=None):
    accum = 0
    for f_cand, f_sol in zip(candidate.faces, solution.faces):
        for v_cand, v_sol in zip(f_cand.ve, f_sol.ve):
            if mask is None or (v_sol.v in mask):
                accum += (v_cand.v - v_sol.v) ** 2
    return accum

def h_null(candidate, solution, mask=None):
    return 1

def astar_solve(cubik, target, mask=None, max_iter=float('inf'), max_time=None, g_coef=4, heuristic=h_manhattan, verbose=False, verbose_step=20, debug=False):
    # cubik = cubik.copy()  # Don't work properly if uncommented
    cubik.heur = heuristic(cubik, target, mask)

    closed = set()
    opened = PriorityQueue()
    opened.add(cubik.heur, cubik)
    cubik.g = 0

    search_path = []
    success = False

    time_start = time.time()

    time_end = None if max_time is None else time_start + max_time
    iter = 0
    while True:
        if success:
            break
        if len(opened) == 0 or iter >= max_iter:
            fail_reason = 'max iter exceeded'
            break
        if iter % 100 == 0 and max_time and time.time() >= time_end:
            fail_reason = 'max time exceeded'
            break
        e = opened.pop()
        if debug:
            print("E.heur:", e.heur)
            print(e.repr())
        closed.add(e)
        if e == target or e.heur == 0:
            success = True
        else:
            for move in target.move_map.keys():
                if len(e.came_from) and move == e.came_from[-1]:
                    continue
                candidate = e.copy()
                hash_before = candidate.hash
                candidate.apply_moves([move])
                candidate.heur = heuristic(candidate, target, mask)
                if debug:
                    print("CANDIDATE HEUR:", candidate.heur)
                    print(candidate.repr())
                candidate.came_from = e.came_from + [move]
                candidate.g = e.g + 1

                if candidate not in opened and candidate not in closed:
                    opened.add(candidate.g * g_coef + candidate.heur, candidate)
        iter += 1
        if verbose and iter % verbose_step == 0:
            print(f"[{iter}]: n_opened = {len(opened)} | n_closed = {len(closed)} | cur_depth: {e.g} | top-5 heur: {', '.join(str(round(_.heur, 1)) for _ in opened.v[:5])}")
    
    return success, e, e.came_from[:]

if __name__ == '__main__':
    cubik = CCubik()
    print("TARGET:")
    print(cubik.repr())
    solution = cubik.copy()

    cubik.apply_moves(cubik.parse_moves("R2 D' B' D F2 R F2 R2 U L' F2 U' B' L2 R D B' R' B2 L2 F2 L2 R2 U2 D2"))
    print("")
    print(cubik.repr())
    print("PHASE 1:")
    #[2, 4, 5, 7]
    success, result_state, path = astar_solve(cubik, solution, mask=(1, 3, 4, 6), verbose=True, g_coef=440, heuristic=h_try)
    print('SUCCESS:', success)
    print(result_state.repr())
    print("Path:", path)
    print("PHASE 2:")
    # success, result_state2, path2 = astar_solve(result_state, solution, mask=[1, 2, 3, 4, 5, 6, 7, 8] + [9, 10, 11, 12, 13, 14, 15, 16, 17, 41, 42, 43], verbose=True, g_coef=0, heuristic=h_try)
    # print('SUCCESS:', success)
    # print(result_state2.repr())
    # print("Path:", path2)

    # success, result_state3, path3 = astar_solve(result_state2, solution, mask=[1, 2, 3, 4, 5, 6, 7, 8] + [9, 10, 11, 12, 13, 14, 15, 16, 17, 41, 42, 43] + [18, 19, 20, 21, 22, 23, 44, 45], verbose=True, g_coef=20, heuristic=h_manhattan)
    # print('SUCCESS:', success)
    # print(result_state3.repr())
    # print("Path:", path3)

    # print("COMBINED PATH:", path3)