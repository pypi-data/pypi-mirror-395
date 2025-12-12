# text.py
from OpenGL.GL import *
from OpenGL.GLUT import (
    glutInit,
    glutBitmapCharacter,
    GLUT_BITMAP_8_BY_13,
    GLUT_BITMAP_9_BY_15,
    GLUT_BITMAP_HELVETICA_10,
    GLUT_BITMAP_HELVETICA_12,
    GLUT_BITMAP_HELVETICA_18,
    GLUT_BITMAP_TIMES_ROMAN_10,
    GLUT_BITMAP_TIMES_ROMAN_24,
)

# make sure GLUT is initialized once
_glut_initialized = False


def _ensure_glut():
    global _glut_initialized
    if not _glut_initialized:
        # no need for real argv; fonts just need GLUT initialized
        glutInit([])
        _glut_initialized = True


class Text:
    def __init__(
        self,
        x: float,
        y: float,
        text: str,
        color=(1.0, 1.0, 1.0),
        font=GLUT_BITMAP_HELVETICA_18,
    ):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font

    def draw(self):
        _ensure_glut()

        r, g, b = self.color
        glColor3f(r, g, b)

        # position is in your ortho coords: (0,0) top-left, (width,height) bottom-right
        glRasterPos2f(self.x, self.y)

        for ch in self.text:
            glutBitmapCharacter(self.font, ord(ch))
