# Dynamic Circular Coordinates

[WIP] OpenGL data visualization of 4-D points encoded in dynamic circular coordinates.  
Coordinate system consisting of a circle with a circumrference of 4 units.  

Example 4-D point a = (0.3, 0.6, 0.5, 0.8)  

# Packages

Required packages: numPy, PyOpenGL and PyOpenGL_accelerate, PyGLM, freetype-py  
Optional packages: wheel for build improvements  

## virtualenv setup

Using python3 virtualenv, for per project pip package installs preserving system default Python.  

First time setup:  

mkdir <dir_name>  
cd    <dir_name>  
python3 -m venv ./  
source bin/activate  
pip install <optional_packages> # space delimited  
pip install <required_packages> # space delimited  
... # do stuff  
deactivate  

Returning setup:  

source bin/activate  
... # do stuff  
deactivate  

## references

-[Python OpenGL introduction](https://noobtuts.com/python/opengl-introduction)  
-[glutGet state integer constants](https://www.opengl.org/resources/libraries/glut/spec3/node70.html)  
-[openGL wikibook](https://en.wikibooks.org/wiki/OpenGL_Programming)  
-[openGL primitive](https://www.khronos.org/opengl/wiki/Primitive)  
-[Text-Rendering](https://learnopengl.com/In-Practice/Text-Rendering)  
-[Text-Rendering Demo](https://github.com/Rabbid76/graphics-snippets/blob/master/example/python/text_freetype/freetype_text.md)  
-[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)  

