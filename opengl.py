import pygame
from pygame.locals import *
from OpenGL import GL as gl
from OpenGL import GLU as glu
import numpy as np
import math
from copy import copy, deepcopy

class Cube():

    surfaces =  ((0,1,2,3),
                (3,2,7,6),
                (6,7,5,4),
                (4,5,1,0),
                (1,5,7,2),
                (4,0,3,6))

    vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
    
    edges = ((0, 1), (0, 3), (0, 4),
            (2, 1), (2, 3), (2, 7),
            (6, 3), (6, 4), (6, 7),
            (5, 1), (5, 4), (5, 7))

    colors = ((1, 1, 1),
              (1, 0, 0),
              (0, 0, 1),
              (255. / 255, 197. / 255, 23. / 255),
              (0, 1, 0),
              (243. / 255, 1, 23 / 255))

    def __init__(self, pos, scale=1):
        self.pos = np.array(pos)
        self.scale = scale
        self.vertices =  scale * (np.array(self.vertices) + pos)

        self.goal_state = np.array([0, 0, 0])
        self.animation_step = 1
        self.cur_state = np.array([0, 0, 0])
        self.id = None

    def draw(self):
        gl.glPushMatrix()

        gl.glRotatef(-self.cur_state[0], 1, 0, 0)
        gl.glRotatef(-self.cur_state[1], 0, 1, 0)
        gl.glRotatef(-self.cur_state[2], 0, 0, 1)

        gl.glBegin(gl.GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                gl.glVertex3fv(self.vertices[vertex])
        gl.glEnd()

        gl.glBegin(gl.GL_QUADS)
        for i, surf in enumerate(self.surfaces):
            gl.glColor3f(*self.colors[i])
            for j in surf:
                gl.glVertex3fv(self.vertices[j])
        gl.glEnd()
        gl.glPopMatrix()

    
    def update(self):
        der = self.goal_state - self.cur_state
        self.cur_state = self.cur_state + der * .1
    
    def __repr__(self):
        return f'C[CUR STATE: {self.cur_state}|GOAL: {self.goal_state}]'

    def __copy__(self):
        v = Cube(self.pos, self.scale)
        v.goal_state = np.copy(self.goal_state)
        v.animation_step = self.animation_step
        v.cur_state = np.copy(self.cur_state)
        v.id = self.id
        return v

class Rubik:
    def __init__(self):
        cubes_pos = [(1, 1, 1), (0, 1, 1), (-1, 1, 1),  # Front top row
                     (1, 0, 1), (0, 0, 1), (-1, 0, 1),  # Front center row
                     (1, -1, 1), (0, -1, 1), (-1, -1, 1), # Front down row
                     (1, 1, 0), (0, 1, 0), (-1, 1, 0),  # Center top row
                     (1, 0, 0), (0, 0, 0), (-1, 0, 0),  # Center center row
                     (1, -1, 0), (0, -1, 0), (-1, -1, 0), # Center down row
                     (1, 1, -1), (0, 1, -1), (-1, 1, -1),  # Back top row
                     (1, 0, -1), (0, 0, -1), (-1, 0, -1),  # Back center row
                     (1, -1, -1), (0, -1, -1), (-1, -1, -1), # Back down row
                ]
         #       (-1, -1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, 1),
          #      (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
           #     (1, -1, 0), (-1, 1, 0), (1, 1, 0), (-1, -1, 0)]
        
        scale = 2.25
        # cubes_pos = [(0, 0, 1), (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),
        #             (-1, -1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, 1),
        #             (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
        #             (1, -1, 0), (-1, 1, 0), (1, 1, 0), (-1, -1, 0)]
        
        cubes_pos = [[v * scale for v in _] for _ in cubes_pos]
        self.cubes = np.array([Cube(pos, .25) for pos in cubes_pos]).reshape((3, 3, 3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i, j,k].id = (i, j, k)
    
    def draw(self):
        for c in self.cubes.ravel():
            c.draw()

    def update(self):
        for c in self.cubes.ravel():
            c.update()
            # if np.isclose(c.cur_state, c.goal_state).all():
            #     print("HERE, goal:", c.goal_state)
            #     c.cur_state = c.cur_state % 360
            #     c.goal_state = c.goal_state % 360
            # c.cur_state = np.array([0, 0, 0])
    
    @property
    def front_face(self):
        return self.cubes[0, :, :].ravel()
    
    @property
    def up_face(self):
        return self.cubes[:, 0, :].ravel()

    @property
    def down_face(self):
        return self.cubes[:, 2, :].ravel()
    
    @property
    def back_face(self):
        return self.cubes[2, :, :].ravel()

    def rotate_front(self, reverse=False):
        front_map = {(0, 0): (0, 2), (0, 1): (1, 2), (0, 2): (2, 2),
                     (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                     (2, 0): (0, 0), (2, 1): (1, 0), (2, 2): (2, 0)}
        mf = {v: k for k, v in front_map.items()}
        if reverse:
            mf = front_map
        
        for c in self.front_face:
            c.goal_state[2] += -90 if reverse else 90
        front_was = np.copy(self.cubes)
        for i in range(3):
            for j in range(3):
                frm = 0, i, j
                fm = mf[(i, j)]
                to = 0, fm[0], fm[1]
                self.cubes[to] = front_was[frm]
    
    def rotate_up(self, reverse=False):
        rot_map = {(0, 0): (0, 2), (0, 1): (1, 2), (0, 2): (2, 2),
                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                (2, 0): (0, 0), (2, 1): (1, 0), (2, 2): (2, 0)}
        mf = {v: k for k, v in rot_map.items()}
        if reverse:
            mf = rot_map

        for c in self.up_face:
            c.goal_state[1] += -90 if reverse else 90
        
        up_was = [copy(c) for c in self.up_face]
        for i in range(3):
            for j in range(3):
                frm = i, 0, j
                fm = mf[(i, j)]
                to = fm[0], 0, fm[1]
                self.cubes[to] = up_was[i * 3 + j]
    
    def rotate_back(self, reverse=False):
        front_map = {(0, 0): (0, 2), (0, 1): (1, 2), (0, 2): (2, 2),
                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                (2, 0): (0, 0), (2, 1): (1, 0), (2, 2): (2, 0)}
        
        mf = {v: k for k, v in front_map.items()}
        for c in self.back_face:
            c.goal_state[2] -= -90 if reverse else 90
        for i in range(3):
            for j in range(3):
                frm = 2, i, j
                to = 2, *front_map[(i, j)]
                print(frm, self.cubes[frm], self.cubes[to])
                self.cubes[frm], self.cubes[to] = self.cubes[to], self.cubes[frm]
    
    def rotate_down(self, reverse=False):
        front_map = {(0, 0): (0, 2), (0, 1): (1, 2), (0, 2): (2, 2),
                (1, 0): (0, 1), (1, 1): (1, 1), (1, 2): (2, 1),
                (2, 0): (0, 0), (2, 1): (1, 0), (2, 2): (2, 0)}
        
        for c in self.down_face:
            c.goal_state[1] -= -90 if reverse else 90
        for i in range(3):
            for j in range(3):
                frm = i, 0, j
                fm = front_map[(i, j)]
                to = fm[0], 0, fm[1]
                print(frm, self.cubes[frm], self.cubes[to])
                self.cubes[frm], self.cubes[to] = self.cubes[to], self.cubes[frm]
        

if __name__ == '__main__':
    # vertices = ((-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), # lower left corner, clockwise
    #             (-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1))  # upper left corner, clockwise
    
    # edges = ((0, 1), (0, 3), (0, 4),
    #          (2, 1), (2, 3), (2, 7),
    #          (6, 3), (6, 4), (6, 7),
    #          (5, 1), (5, 4), (5, 7))

    # # Down, Left, Back, Right, Front, Up
    # surfaces = ((0, 1, 2, 3), # Down
    #             (0, 1, 4, 5), # Left
    #             (1, 2, 6, 5), # Back
    #             (2, 6, 7, 3), # Right
    #             (0, 4, 7, 3)) # Front
    

    pygame.init()
    w, h = 800, 600
    pygame.display.set_mode((w, h), DOUBLEBUF | OPENGL)
    glu.gluPerspective(45, (w/h), 0.1, 50.0)
    gl.glTranslatef(.0, .0, -5)
    gl.glEnable(gl.GL_DEPTH_TEST) 

    
    # scale = 2.25
    # cubes_pos = [(0, 0, 1), (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),
    #              (-1, -1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, 1),
    #              (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
    #              (1, -1, 0), (-1, 1, 0), (1, 1, 0), (-1, -1, 0)]
    
    # cubes_pos = [[v * scale for v in _] for _ in cubes_pos]
    # cubes = [Cube(pos, .25) for pos in cubes_pos]

    rubik = Rubik()
    lastPosX = 0;
    lastPosY = 0;
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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
            
            if event.type == pygame.KEYDOWN:
                rev = pygame.key.get_mods() & pygame.KMOD_SHIFT
                if event.key == pygame.K_f:
                    # print("Front")
                    # print("Reverse:", rev)
                    rubik.rotate_front(rev)

                elif event.key == pygame.K_l:
                    print("LEFT, rev:", rev)
                elif event.key == pygame.K_u:
                    rubik.rotate_up(rev)
                
                elif event.key == pygame.K_b:
                    rubik.rotate_back(rev)
                
                elif event.key == pygame.K_d:
                    rubik.rotate_down(rev)

        # gl.glRotatef(1, 3, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        
        rubik.draw()
        rubik.update()

        pygame.display.flip()
        pygame.time.wait(10)