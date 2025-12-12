import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from pyola import input

class Window:
    def __init__(self, width, height, title="Pyola Window"):
        if not glfw.init():
            raise Exception("GLFW can't be initialized.")

        self._window = glfw.create_window(width, height, title, None, None)
        input.init_input_callbacks(self._window)

        if not self._window:
            glfw.terminate()
            raise Exception("Failed to create window.")

        glfw.make_context_current(self._window)
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.width = width
        self.height = height
        self.title = title
        self.running = True

    def update(self):
        glfw.swap_buffers(self._window)
        glfw.poll_events()
        if glfw.window_should_close(self._window):
            self.running = False

    def close(self):
        glfw.terminate()
