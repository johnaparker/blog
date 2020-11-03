cmake_minimum_required (VERSION 3.1)
cmake_policy(VERSION 3.1)

set(PROJECT_NAME circle_vis)
project(${PROJECT_NAME})

# set flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-Werror -Og")
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# find packages
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cpp/third_party/cmake")
find_package(GLM REQUIRED)
message(STATUS "GLM included at ${GLM_INCLUDE_DIR}")
find_package(GLFW3 REQUIRED)
message(STATUS "Found GLFW3 in ${GLFW3_INCLUDE_DIR}")
find_package(ASSIMP REQUIRED)
message(STATUS "Found ASSIMP in ${ASSIMP_INCLUDE_DIR}")
find_package(Freetype REQUIRED)
message(STATUS "Found ASSIMP in ${FREETYPE_INCLUDE_DIR}")

add_subdirectory(cpp/third_party/pybind11)

# set LIBS based on OS
if(WIN32)
  set(LIBS glfw3 opengl32 assimp freetype irrKlang)
elseif(UNIX AND NOT APPLE)
  find_package(OpenGL REQUIRED)
  add_definitions(${OPENGL_DEFINITIONS})
  find_package(X11 REQUIRED)
  set(LIBS ${GLFW3_LIBRARY} X11 Xrandr Xinerama Xi Xxf86vm Xcursor GL dl pthread freetype ${ASSIMP_LIBRARY})
  set (CMAKE_CXX_LINK_EXECUTABLE "${CMAKE_CXX_LINK_EXECUTABLE} -ldl")
elseif(APPLE)
  INCLUDE_DIRECTORIES(/System/Library/Frameworks)
  FIND_LIBRARY(COCOA_LIBRARY Cocoa)
  FIND_LIBRARY(OpenGL_LIBRARY OpenGL)
  FIND_LIBRARY(IOKit_LIBRARY IOKit)
  FIND_LIBRARY(CoreVideo_LIBRARY CoreVideo)
  MARK_AS_ADVANCED(COCOA_LIBRARY OpenGL_LIBRARY)
  SET(APPLE_LIBS ${COCOA_LIBRARY} ${IOKit_LIBRARY} ${OpenGL_LIBRARY} ${CoreVideo_LIBRARY})
  SET(APPLE_LIBS ${APPLE_LIBS} ${GLFW3_LIBRARY} ${ASSIMP_LIBRARY} ${FREETYPE_LIBRARIES})
  set(LIBS ${LIBS} ${APPLE_LIBS})
else()
  set(LIBS )
endif(WIN32)

# add GLAD to LIBS
add_library(GLAD "cpp/third_party/glad/glad.c")
set(LIBS ${LIBS} GLAD)

# include directories
include_directories(${CMAKE_SOURCE_DIR}/cpp/src)
include_directories(${CMAKE_SOURCE_DIR}/cpp/third_party)

# set source files
set(SOURCES ${SOURCES} 
    cpp/src/circle_vertex_instanced.cpp
    cpp/src/circle_fragment_instanced.cpp
    cpp/src/circle_vertex.cpp
    cpp/src/circle_fragment.cpp
    cpp/src/bind_pyb.cpp
    cpp/src/shader_s.cpp)

# create shared library 
add_library(${PROJECT_NAME} MODULE "${SOURCES}")
target_link_libraries(${PROJECT_NAME} PRIVATE ${LIBS} pybind11::module)
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
                                     SUFFIX "${PYTHON_MODULE_EXTENSION}")
#set(CMAKE_INSTALL_PREFIX )
install(TARGETS ${PROJECT_NAME} DESTINATION ${CMAKE_SOURCE_DIR}/scripts)
