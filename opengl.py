import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QOpenGLContext, QOffscreenSurface
import OpenGL.GL as gl

app = QApplication(sys.argv)

surface = QOffscreenSurface()
surface.create()

ctx = QOpenGLContext()
ctx.create()
ctx.makeCurrent(surface)

print(gl.glGetString(gl.GL_RENDERER).decode())
print(gl.glGetString(gl.GL_VERSION).decode())

ctx.doneCurrent()
