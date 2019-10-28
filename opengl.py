import pygame
from pygame import locals as pglocals
from OpenGL import GL as gl
from OpenGL import GLU as glu
import numpy as np
import math

class Cube():
    def __init__(self, pos, scale=1):
        self.pos = np.array(pos)
        self.vertices =  scale * (np.array(((1, -1, -1), (1, 1, -1), (-1, 1, -1),
                                    (-1, -1, -1), (1, -1, 1), (1, 1, 1),
                                    (-1, -1, 1), (-1, 1, 1))) + pos)
        self.edges = np.array(((0, 1), (0, 3), (0, 4),
                    (2, 1), (2, 3), (2, 7),
                    (6, 3), (6, 4), (6, 7),
                    (5, 1), (5, 4), (5, 7)))
        
        self.surfaces = np.array((
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
            ))

    def draw(self):
        gl.glBegin(gl.GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                gl.glVertex3fv(self.vertices[vertex])
        gl.glEnd()


if __name__ == '__main__':
    vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1),
                (-1, -1, -1), (1, -1, 1), (1, 1, 1),
                (-1, -1, 1), (-1, 1, 1))
    
    edges = ((0, 1), (0, 3), (0, 4),
             (2, 1), (2, 3), (2, 7),
             (6, 3), (6, 4), (6, 7),
             (5, 1), (5, 4), (5, 7))

    pygame.init()
    w, h = 800, 600
    pygame.display.set_mode((w, h), pglocals.DOUBLEBUF | pglocals.OPENGL)
    glu.gluPerspective(45, (w/h), 0.1, 50.0)
    gl.glTranslatef(.0, .0, -5)

    # cube = Cube([0, 0, 0], .25)
    # cube2 = Cube([-2, 0, 0], .25)

    cubes_pos = [(0, 0, 0), (-2, 0, 0), (2, 0, 0), (0, -2, 0), (0, 2, 0)]
    cubes = [Cube(pos, .25) for pos in cubes_pos]
    lastPosX = 0;
    lastPosY = 0;
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos;
                dx = x - lastPosX;
                dy = y - lastPosY;
                
                mouseState = pygame.mouse.get_pressed();
                if mouseState[0]:

                    modelView = (gl.GLfloat * 16)()
                    mvm = gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX, modelView)
        
        # To combine x-axis and y-axis rotation
                    temp = (gl.GLfloat * 3)();
                    temp[0] = modelView[0]*dy + modelView[1]*dx;
                    temp[1] = modelView[4]*dy + modelView[5]*dx;
                    temp[2] = modelView[8]*dy + modelView[9]*dx;
                    norm_xy = math.sqrt(temp[0]*temp[0] + temp[1]*temp[1] + temp[2]*temp[2]);
                    gl.glRotatef(math.sqrt(dx*dx+dy*dy), temp[0]/norm_xy, temp[1]/norm_xy, temp[2]/norm_xy);

                lastPosX = x;
                lastPosY = y;

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: # wheel rolled up
                gl.glScaled(1.05, 1.05, 1.05);
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: # wheel rolled down
                gl.glScaled(0.95, 0.95, 0.95);
        # gl.glRotatef(1, 3, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        for cube in cubes:
            cube.draw()
        pygame.display.flip()
        pygame.time.wait(10)