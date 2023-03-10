# Written by: Alice Williams

import OpenGL

# Flag Options
OpenGL.ERROR_CHECKING = True  # False gets roughly halved OpenGL calls
OpenGL.ERROR_LOGGINGi = True  # False gets performance boost for non-development
OpenGL.FULL_LOGGING   = False # Enables OpenGL logging module for error trace
GL_INFO_LOG           = False # GL vendor, version, and extension logging

# Window constants
WINDOW_TITLE = 'Dynamic Circular Coordinates'
WINDOW_DIM   = 640

# libraries
import os   # used for os.path.dirname, os.path.realpath
import sys  # used for sys.exit
import math # used for math.pi, math.sin, math.cos

# Calc constants
TAU          = 2 * math.pi
CIRCLE_PERIM = 4
PNT_MARGIN   = 0.5
PNT_LABELS   = ["A_0", "A_1", "A_2", "A_3"]
NUM_LABELS   = ["4|0", "1", "2", "3"]

# PyOpenGL library check
try:
    from OpenGL.GL   import *
    from OpenGL.GLUT import *
    from OpenGL.GLU  import *
except:
    print('PyOpenGL is not installed.')
    sys.exit(1)

# PyGLM library check
try:
    import glm
except:
    print('PyGLM is not installed.')
    sys.exit(1)

# numPy library check
try:
    import numpy
except:
    print('numPy is not installed.')
    sys.exit(1)

# opengl environment class
class OpenGLEnv:
    def __init__(self):
        self.window = None

        # stdout message
        print('Press any key to exit program.')
        
        # pass cli args
        glutInit(sys.argv)
        # What is the difference between GLUT_RGB or GLUT_RGBA does that toggle the whole alpha availability?
        glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
        
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

    def init_gl(self):
        pass

    def run(self):
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
        
        glOrtho(0.0, WINDOW_DIM, 0.0, WINDOW_DIM, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        
        glClearColor(0.75, 0.75, 0.75, 0.0) # light gray
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        
        glLoadIdentity()
        glEnable( GL_DEPTH_TEST )
        proj = glm.ortho(0, WINDOW_DIM, WINDOW_DIM, 0, -1, 1)
        
        self.a = [0.3, 0.6, 0.5, 0.8] 
        
        self.draw_circle(320, 320, 250, 1000)
        glutSwapBuffers()

    def reshape(self, width, height):
        # viewport resize
        glViewport(0, 0, width, height)
        self.setup_viewport()

    def display(self, *args):
        pass
        # moved drawing to init method to prevent redrawing while developing

    def draw_circle(self, x, y, radius, lines):

        glColor(0,0,0,0)
        glRasterPos3f(WINDOW_DIM/2 - 150, WINDOW_DIM - 25, 0)
        for char in "Dynamic Circular Coordinates":
            glutBitmapCharacter( GLUT_BITMAP_TIMES_ROMAN_24, ord(char) )

        # BLUE
        glColor(0,0,1,0)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
    
        # data point counter
        pnt = 0
        total = self.a[pnt]
        totals = [total,0,0,0]
        ratio = 360 / lines
        quads = [(0,0), (0,0), (0,0), (0,0)]
        pts = [(0,0), (0,0), (0,0), (0,0)]
        quad = 0

        # circle draw
        glBegin(GL_LINE_LOOP)
        for n in range(0, lines):
            
            theta = n * ratio

            # store quadrant coordinates
            if theta == 0 or theta == 90 or theta == 180 or theta == 270:
                quads[quad] = (x + (-radius * math.sin(-n * TAU / lines)), y + (radius * math.cos(-n * TAU / lines)))
                quad += 1

            # begin point
            if theta > 360 / (CIRCLE_PERIM / total) - PNT_MARGIN:
                glColor(1,0,0,0)

            # end point
            if theta > 360 / (CIRCLE_PERIM / total) + PNT_MARGIN:
                glColor(0,0,1,0)
                if pnt < len(self.a)-1:
                    pnt += 1
                    total += self.a[pnt]
                    totals[pnt] = total

            # store data point coordinates
            if theta == (360 / (CIRCLE_PERIM / total)):
                pts[pnt] = (x + (-radius * math.sin(-n * TAU / lines)), y + (radius * math.cos(-n * TAU / lines)))

            # circle vertex
            glVertex2f(x + (-radius * math.sin(-n * TAU / lines)), y + (radius * math.cos(-n * TAU / lines)))
        
        glEnd()

        # chord draw
        glColor(0,0,1,0)
        glBegin(GL_LINE_LOOP)
        for p in pts:
            glVertex2f(p[0], p[1])
        glEnd()

        # quadrant labels
        glColor(0,0,0,0)
        c = 0
        for q in quads:
            glRasterPos3f(quads[c][0], quads[c][1], 0)
            for char in NUM_LABELS[c]:
                glutBitmapCharacter( GLUT_BITMAP_TIMES_ROMAN_24, ord(char) )
            c += 1

        # label draw
        glColor(1,0,0,0)
        c = 0
        for p in pts:
            glRasterPos3f(pts[c][0] - 75, pts[c][1], 0)
            for char in PNT_LABELS[c] + " " + str(self.a[c]) + "(" + str(round(totals[c], 2)) + ")":
                glutBitmapCharacter( GLUT_BITMAP_TIMES_ROMAN_24, ord(char) )
            c += 1

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
    env.run()
