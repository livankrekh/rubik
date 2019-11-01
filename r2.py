import numpy as np

class Cubit:
    def __init__(self, pos):
        self.pos = pos  # 3d index
    
    def __repr__(self):
        return f'{self.pos}'

if __name__ == '__main__':
    cubes = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                cubes.append(Cubit(np.array([k, j, i])))
    
    cube = np.array(cubes).reshape((3, 3, 3))
    print(cube[0, 0, :])