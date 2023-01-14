import OpenGL

# Error checking flag False results in ~halved OpenGL calls 
OpenGL.ERROR_CHECKING = True
# Error logging flag False provides performance boost for non-development
OpenGL.ERROR_LOGGING = True
# Full Error traces calls to OpenGL logging module for error trace
OpenGL.FULL_LOGGING = False

GL_INFO_LOG = True

import sys
from OpenGL.GL   import *
from OpenGL.GLUT import *
from OpenGL.GLU  import *

class OpenGLEnv:
    def __init__(self):
        self.window = None
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(640, 480)
        self.window = glutCreateWindow('PyOpenGL Test')
        self.setup_viewport()
        if GL_INFO_LOG:
            self.gl_info()
        glutReshapeFunc(self.reshape)
        glutIdleFunc(self.display)
        glutMouseFunc(self.mouse)
        glutKeyboardFunc(self.keyboard)
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
    
    def close(self):
        if self.window:
            print('Program closing.')
            glutDestroyWindow(self.window)

    def setup_viewport(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
        glClearColor(0.75, 0.75, 0.75, 0.0)

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        self.setup_viewport()

    def display(self, *args):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glutSwapBuffers()

    def keyboard(self, *args):
        self.close()

    def mouse(self, button, state, x, y):
        pass

    def gl_info(self):
        print('PyOpenGL Version: ', OpenGL.__version__)
        print('GL Vendor: ',        glGetString(GL_VENDOR).decode())
        print('GL Renderer: ',      glGetString(GL_RENDERER).decode())
        print('GL Version: ',       glGetString(GL_VERSION).decode())
        exts = glGetString(GL_EXTENSIONS)
        if exts is None:
            print('GL Extensions: ', exts.decode())
        else:
            print('GL Extensions:')
            for ext in exts.split():
                print('\t', ext.decode())

if __name__ == "__main__":
    print('Press any key to quit.')
    env = OpenGLEnv()
    glutMainLoop()
