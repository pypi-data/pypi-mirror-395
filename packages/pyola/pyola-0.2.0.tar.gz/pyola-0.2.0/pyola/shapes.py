from OpenGL.GL import *
import math

class Rectangle:
    def __init__(self, x, y, width, height, color=(1, 1, 1)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        r, g, b = self.color
        glColor3f(r, g, b)

        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

class Line:
    def __init__(self, pos1, pos2, color=(1, 1, 1)):
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color

    def draw(self):
        r, g, b = self.color
        glColor3f(r, g, b)

        glBegin(GL_LINES)
        glVertex2f(self.pos1[0], self.pos1[1])
        glVertex2f(self.pos2[0], self.pos2[1])
        glEnd()

class Circle:
    def __init__(self, x, y, radius, color=(1, 1, 1), segments=32):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.segments = segments

    def draw(self):
        r, g, b = self.color
        glColor3f(r, g, b)

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.x, self.y)
        for i in range(self.segments + 1):
            angle = 2 * math.pi * i / self.segments
            dx = self.radius * math.cos(angle)
            dy = self.radius * math.sin(angle)
            glVertex2f(self.x + dx, self.y + dy)
        glEnd()