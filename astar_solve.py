from rubik import Cubik
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

def h_mismatch(candidate, solution):
    cnt = 0
    for f_cand, f_sol in zip(candidate.faces, solution.faces):
        # print(f_cand, f_sol)
        for v_cand, v_sol in zip(f_cand.ve, f_sol.ve):
            cnt += v_cand.v != v_sol.v
    return cnt

def h_manhattan(candidate, solution):
    accum = 0
    for f_cand, f_sol in zip(candidate.faces, solution.faces):
        for v_cand, v_sol in zip(f_cand.ve, f_sol.ve):
            accum += abs(v_cand.v - v_sol.v)
    return accum

def h_euclidean(candidate, solution):
    accum = 0
    for f_cand, f_sol in zip(candidate.faces, solution.faces):
        for v_cand, v_sol in zip(f_cand.ve, f_sol.ve):
            accum += (v_cand.v - v_sol.v) ** 2
    return accum

if __name__ == '__main__':
    cubik = Cubik()

    solution = cubik.copy()

    cubik.apply_moves(cubik.parse_moves("R D"))

    # print(cubik.repr(color=True))
    # print(h_mismatch(cubik, solution))
    # print(h_manhattan(cubik, solution))
    # print(h_euclidean(cubik, solution))

    h = h_euclidean
    cubik.heur = h(cubik, solution)
    closed = set()
    opened = PriorityQueue()
    opened.add(cubik.heur, cubik)
    cubik.g = 0

    search_path = []
    success = False

    max_time = None
    time_start = time.time()
    time_end = None if max_time is None else time_start + max_time
    iter = 0
    max_iter = float('inf')
    g_coef = 400
    verbose = True
    verbose_step = 20
    while True:
        if success:
            break
        if len(opened) == 0 or iter >= max_iter:
            fail_reason = 'max iter exceeded'
            break
        if iter % 1000 == 0 and max_time and time.time() >= time_end:
            fail_reason = 'max time exceeded'
            break
        e = opened.pop()
        closed.add(e)
        if e == solution:
            success = True
        else:
            for move in solution.move_map.keys():
                candidate = e.copy()
                hash_before = candidate.hash
                candidate.apply_moves([move])
                candidate.heur = h(candidate, solution)
                candidate.came_from = e.came_from + [move]
                candidate.g = e.g + 1

                if candidate not in opened and candidate not in closed:
                    opened.add(candidate.g * g_coef + candidate.heur, candidate)
        iter += 1
        if verbose and iter % verbose_step == 0:
            print(f"[{iter}]: n_opened = {len(opened)} | n_closed = {len(closed)} | cur_depth: {e.g} | top-5 heur: {', '.join(str(round(_, 1)) for _ in opened.k[:5])}")
    
    state_path = []
    if success:
        print(' '.join(e.came_from))