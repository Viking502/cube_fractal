from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import numpy as np


class Cube:
    def __init__(self, size, position, state):
        self.visible = state
        self.pos = position
        self.vertices = []
        for z in range(2):
            for y in range(2):
                for x in range(2):
                    self.vertices.append(np.add(self.pos, [x * size, y * size, z * size]))

        self.edges = []
        for i in (0, 2, 4, 6):
            self.edges.append([i, i + 1])
        for i in (0, 1, 4, 5):
            self.edges.append([i, i + 2])
        for i in range(4):
            self.edges.append([i, i + 4])

        self.sides = []
        for z in (0, 4):
            self.sides.append([0 + z, 1 + z, 3 + z, 2 + z])
        for x in (0, 1):
            self.sides.append([x, x + 2, x + 6, x + 4])
        for y in (0, 2):
            self.sides.append([y, y + 1, y + 5, y + 4])

    def draw(self):
        # sides
        if not self.visible:
            return

        glBegin(GL_QUADS)
        for side in self.sides:
            for v in side:
                glColor3f(1, 0.4, 0)
                glVertex3fv(self.vertices[v])
        glEnd()
        # lines
        glLineWidth(3)
        glBegin(GL_LINES)
        for edge in self.edges:
            for v in edge:
                glColor3f(1, 1, 1)
                glVertex3fv(self.vertices[v])
        glEnd()
        """
        # points
        glPointSize(8)
        glBegin(GL_POINTS)
        for vertex in self.vertices:
            glColor3f(0, 0, 1)
            glVertex3fv(vertex)
        glEnd()
        """


class Fractal:

    def __init__(self, state, lvl, position):
        self.pos = position
        self.state = state
        self.subFractal = []
        self.level = lvl
        if lvl == 0:
            self.subFractal.append(Cube(3, self.pos, state))
        else:
            for z in range(3):
                for y in range(3):
                    for x in range(3):
                        if (z == 1 and (x % 2 != 0 or y % 2 != 0)) or ((z == 0 or z == 2) and (x == 1 and y == 1)):
                            self.subFractal.append(Fractal(0, lvl - 1, np.add(self.pos, np.multiply([x, y, z], 3**lvl))))
                        else:
                            self.subFractal.append(Fractal(state, lvl - 1, np.add(self.pos, np.multiply([x, y, z], 3**lvl))))

    def draw(self):
        for f in self.subFractal:
            f.draw()


def move_camera_mouse():

    mouse = pygame.mouse
    mouse.get_rel()

    while mouse.get_pressed()[0]:
        pygame.event.wait()
        vec = mouse.get_rel()
        glRotatef(15, vec[1], vec[0], 0)
        update_window()


def update_window():
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    fractal.draw()

    pygame.display.flip()


def main():

    pygame.init()

    win_size = (1280, 720)
    pygame.display.set_mode(win_size,  pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    run_flag = True

    gluPerspective(45, win_size[0]/win_size[1], 0.4, 500)
    glTranslate(0, 0, -50 * f_size)
    glEnable(GL_DEPTH_TEST)

    while run_flag:

        mouse = pygame.mouse

        for eve in pygame.event.get():
            if eve.type == pygame.QUIT or eve.type == pygame.K_ESCAPE:
                run_flag = False
            if mouse.get_pressed()[0]:
                move_camera_mouse()

        keys = pygame.key.get_pressed()

        angle = 15

        if keys[pygame.K_LEFT]:
            glRotatef(angle, 0, -1, 0)
        if keys[pygame.K_RIGHT]:
            glRotatef(angle, 0, 1, 0)
        if keys[pygame.K_UP]:
            glRotatef(angle, -1, 0, 0)
        if keys[pygame.K_LEFT]:
            glRotatef(angle, 1, 0, 0)

        update_window()


f_size = 2

fractal = Fractal(1, f_size, np.multiply([1, 1, 1], -(3**f_size)*3/2))

main()
