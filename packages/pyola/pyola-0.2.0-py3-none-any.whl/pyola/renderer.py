from OpenGL.GL import *

def clear(color=(0.0, 0.0, 0.0)):
    r, g, b = color
    glClearColor(r, g, b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

