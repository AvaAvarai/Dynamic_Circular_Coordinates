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

import os   # used for os.path.dirname, os.path.realpath
import sys  # used for sys.exit
import math # used for math.pi, math.sin, math.cos

# PyOpenGL library check
try:
    from OpenGL.GL   import *
    from OpenGL.GLUT import *
    from OpenGL.GLU  import *
    from OpenGL.GL   import shaders
except:
    print('PyOpenGL is not installed.')
    sys.exit(1)

# FreeType library check
try:
    from freetype import *
except:
    print('freetype-py is not installed.')
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

text_shader_vert = """
#version 460

layout (location = 0) in vec2 in_pos;
layout (location = 1) in vec2 in_uv;

out vec2 vUV;

layout (location = 0) uniform mat4 model;
layout (location = 1) uniform mat4 projection;

void main()
{
    vUV = in_uv.xy;
    gl_Position = projection * model * vec4(in_pos.xy, 0.0, 1.0);
}
"""

text_shader_frag = """
#version 460

in vec2 vUV;

layout (binding=0) uniform sampler2D u_texture;
layout (location = 2) uniform vec3 textColor;

out vec4 fragColor;

void main()
{
    vec2 uv = vUV.xy;
    float text = texture(u_texture, uv).r;
    fragColor = vec4(textColor.rgb*text, text);
}
"""

# opengl environment class
class OpenGLEnv:
    def __init__(self):
        # setup
        self.characters = []
        self.window = None
        print('Press any key to exit program.')
        glutInit(sys.argv)
        glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
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
        # Initializ GL and Font
        self.init_gl()
        self.fontsize = 32
        self.dirname = os.path.dirname(os.path.realpath(__file__))
        self.make_font(self.dirname+'/FreeSans.ttf', self.fontsize)

    def init_gl(self):
        vertexshader = shaders.compileShader(text_shader_vert, GL_VERTEX_SHADER)
        fragmentshader = shaders.compileShader(text_shader_frag, GL_FRAGMENT_SHADER)
        self.shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

        vquad = [
          # x   y  u  v
            0, -1, 0, 0,
            0,  0, 0, 1,
            1,  0, 1, 1,
            0, -1, 0, 0,
            1,  0, 1, 1,
            1, -1, 1, 0
        ]
        vertex_attributes = numpy.array(vquad, dtype=numpy.float32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_attributes, GL_STATIC_DRAW)
        float_size = vertex_attributes.itemsize
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 4*float_size, None)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 4*float_size, c_void_p(2*float_size))
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBindVertexArray(0)

    def make_font(self, filename, fontsize):
        face = Face(filename)
        face.set_pixel_sizes(0, fontsize)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glActiveTexture(GL_TEXTURE0)

        for c in range(128):
            face.load_char(chr(c), FT_LOAD_RENDER)
            glyph = face.glyph
            bitmap = glyph.bitmap
            size = bitmap.width, bitmap.rows
            bearing = glyph.bitmap_left, glyph.bitmap_top
            advance = glyph.advance.x

            texObj = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texObj)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_R8, *size, 0, GL_RED, GL_UNSIGNED_BYTE, bitmap.buffer)
            self.characters.append((texObj, size, bearing, advance))

        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, 0)

    def run(self):
        # event loop
        glutMainLoop()

    def close(self):
        # graceful exit
        if self.window:
            print('Exiting program now.')
            glutDestroyWindow(self.window)

    def render_text(self, text, pos, scale, dir):
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.vao)
        angle_rad = math.atan2(dir[1], dir[0])
        rotateM = glm.rotate(glm.mat4(1), angle_rad, glm.vec3(0, 0, 1))
        transOriginM = glm.translate(glm.mat4(1), glm.vec3(*pos, 0))

        char_x = 0
        for c in text:
            c = ord(c)
            ch = self.characters[c]
            w, h = ch[1][0] * scale, ch[1][1] * scale
            xrel, yrel = char_x + ch[2][0] * scale, (ch[1][1] - ch[2][1]) * scale
            char_x += (ch[3] >> 6) * scale
            scaleM = glm.scale(glm.mat4(1), glm.vec3(w, h, 1))
            transRelM = glm.translate(glm.mat4(1), glm.vec3(xrel, yrel, 0))
            modelM = transOriginM * rotateM * transRelM * scaleM

            glUniformMatrix4fv(0, 1, GL_FALSE, glm.value_ptr(modelM))
            glBindTexture(GL_TEXTURE_2D, ch[0])
            glDrawArrays(GL_TRIANGLES, 0, 6)

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)

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
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glLoadIdentity()

        glEnable( GL_DEPTH_TEST )
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

        glUseProgram(self.shaderProgram)
        proj = glm.ortho(0, WINDOW_DIM, WINDOW_DIM, 0, -1, 1)
        glUniformMatrix4fv(1, 1, GL_FALSE, glm.value_ptr(proj))
        glUniform3f(2, 0.0, 0.0, 0.0)
        self.render_text("Dynamic Circular Coordinates", (5, 30), 1, (1, 0))

        glColor(1,0,0,0)
        self.draw_circle(320, 320, 250, 1000)
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
    env.run()
