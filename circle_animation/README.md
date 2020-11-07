# Realtime visualization of a large number of circles using OpenGL

## Instructions

Run the `download_data.sh` shell script to download the 3 files required to run the scripts.

To compile the C++ and OpenGL code, run the following:
```bash
mkdir build && cd build
cmake ..
make
make install
```
This should install a `.so` library to the `scripts` folder.
Make sure that `pybind11` is available at `cpp/third_party/pybind11`; if not, run `git submodule init` and `git submodule update`.

In the scripts folder, run the Python scripts:
* `mpl_simple.py` uses Matplotlib to animate the circles
* `mpl_collection.py` uses Matplotlib with collection objects to animate the circles
* `opengl_vertex.py` uses OpenGL using a vertex approach to animate the circles
* `opengl_fragment.py` uses OpenGL using a fragment approach to animate the circles
* `opengl_vertex_instanced.py` uses the OpenGL vertex approach with instanced drawing
* `opengl_fragment_instanced.py` uses the OpenGL fragment approach with instanced drawing

## Folders
* `cpp/` contains the C++ and OpenGL source code, as well as third party dependencies
* `shaders/` contains the OpenGL vertex and fragment shaders to draw circles (vertex, fragment approach, plus instanced drawing)
* `scripts/` contains the Python scripts to run the animations
* `img/` contains code to make images in the blog post

## Link to post
https://www.jparker.me/blog/circle-graphics
