from rubik import Cubik
from astar_solve import *

if __name__ == '__main__':
    cubik = Cubik()

    solution = cubik.copy()

    cubik.apply_moves(cubik.parse_moves("R D U F2 B'"))
    success, res, path = astar_solve(cubik, solution, max_time=30, verbose=True, g_coef=20)