import OpenGL

# Error checking flag False gets roughly halved OpenGL calls
OpenGL.ERROR_CHECKING = True
# Error logging flag False gives performance boost for non-development
OpenGL.ERROR_LOGGING = True
# Full Logging flag enables OpenGL logging module for error trace
OpenGL.FULL_LOGGING = False
# GL vendor, version, and extension logging
GL_INFO_LOG = False

# Window constants
WINDOW_TITLE = 'Dynamic Circular Coordinates'
WINDOW_DIM   = 640

import sys  # used for sys.exit
import math # used for math.pi, math.sin, math.cos

# library check
try:
    from OpenGL.GL   import *
    from OpenGL.GLUT import *
    from OpenGL.GLU  import *
except:
    print('PyOpenGL is not installed.')
    sys.exit(1)

# opengl environment class
class OpenGLEnv:
    def __init__(self):
        # setup
        self.window = None
        print('Press any key to exit program.')
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        # 1:1 aspect ratio centered, works on single monitor,
        # bug where width is offset on dual monitor,
        # have not tested on triple monitor.
        glutInitWindowSize(WINDOW_DIM, WINDOW_DIM)
        self.screen_width  = glutGet(GLUT_SCREEN_WIDTH)
        self.screen_height = glutGet(GLUT_SCREEN_HEIGHT)
        self.window_x = int(self.screen_width/2 - WINDOW_DIM/2)
        self.window_y = int(self.screen_height/2 - WINDOW_DIM/2)
        glutInitWindowPosition(self.window_x, self.window_y)
        self.window = glutCreateWindow(WINDOW_TITLE)
        self.setup_viewport()
        # GL version logging
        if GL_INFO_LOG:
            self.gl_info()
        # callback functions
        glutReshapeFunc(self.reshape)
        glutIdleFunc(self.display)
        glutMouseFunc(self.mouse)
        glutKeyboardFunc(self.keyboard)
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        # event loop
        glutMainLoop()

    def close(self):
        # graceful exit
        if self.window:
            print('Exiting program now.')
            glutDestroyWindow(self.window)

    def setup_viewport(self):
        # perspective and camera setup
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, WINDOW_DIM, 0.0, WINDOW_DIM, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glClearColor(0.75, 0.75, 0.75, 0.0) # light gray

    def reshape(self, width, height):
        # viewport resize
        glViewport(0, 0, width, height)
        self.setup_viewport()

    def display(self, *args):
        # viewport drawing
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glColor(1,0,0,0)
        self.draw_circle(320, 320, 250, 100)
        glutSwapBuffers()

    def draw_circle(self, x, y, radius, lines):
        glBegin(GL_LINE_LOOP)
        for i in range(lines):
            glVertex2f(x + (radius * math.cos(i * (2*math.pi) / lines)), y + (radius * math.sin(i * (2*math.pi) / lines)))
        glEnd()

    def keyboard(self, *args):
        # key events
        self.close()

    def mouse(self, button, state, x, y):
        # mouse events
        pass

    def gl_info(self):
        # GL version logging
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

# main routine
if __name__ == "__main__":
    env = OpenGLEnv()