#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <shader_s.hpp>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <chrono>
#include <thread>

namespace py = pybind11;

namespace circle_vertex_instanced {

void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void processInput(GLFWwindow *window);
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods);
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
void mouse_callback(GLFWwindow* window, double xpos, double ypos);

// global variables
unsigned int SCR_WIDTH = 800;
unsigned int SCR_HEIGHT = 600;
float aspect_ratio = (float)(SCR_WIDTH) / (float)(SCR_HEIGHT);
bool paused = false;
int current_frame = 0;
int last_frame = 0;

float xshift = 0;
float yshift = 0;
float window_dx = 0;
float window_dy = 0;
float zoom = 0;
float lastX = 0;
float lastY = 0;
bool mouse_hold = false;

GLFWwindow* window;
unsigned int VBO, VAO, EBO;
unsigned int transformVBO, colorVBO;

const int Nvertices = 30;

void make_window(bool time_it) {
    // initialize
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

    // create window
    if (time_it)
        glfwWindowHint(GLFW_DOUBLEBUFFER, GL_FALSE);
    window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return;
    }

    // set callbacks
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    glfwSetKeyCallback(window, key_callback);
    glfwSetScrollCallback(window, scroll_callback);
    glfwSetCursorPosCallback(window, mouse_callback);

    // load OpenGL function pointers
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return;
    }

    // enable alpha blending
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

void bind_vetices() {
    float vertices[(Nvertices+1)*3];
    unsigned int indices[Nvertices*3];

    vertices[0] = 0;
    vertices[1] = 0;
    vertices[2] = 0;
    for (unsigned int i=0; i<Nvertices; i++) {
        float theta = 2*M_PI*(float)i/(float)(Nvertices);
        vertices[3*(i+1) + 0] = cos(theta);
        vertices[3*(i+1) + 1] = sin(theta);
        vertices[3*(i+1) + 2] = 0;

        indices[3*i + 0] = 0;
        indices[3*i + 1] = 1+i;
        indices[3*i + 2] = (1+i)%Nvertices + 1;
    }

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
}

void bind_attributes() {
    glGenBuffers(1, &transformVBO);
    glGenBuffers(1, &colorVBO);

    // position attribute
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);

    glEnableVertexAttribArray(1);
    glBindBuffer(GL_ARRAY_BUFFER, transformVBO);
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, sizeof(glm::mat4), (void*)0);
    glEnableVertexAttribArray(2);
    glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, sizeof(glm::mat4), (void*)(sizeof(glm::vec4)));
    glEnableVertexAttribArray(3);
    glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, sizeof(glm::mat4), (void*)(2 * sizeof(glm::vec4)));
    glEnableVertexAttribArray(4);
    glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, sizeof(glm::mat4), (void*)(3 * sizeof(glm::vec4)));

    glVertexAttribDivisor(1, 1);
    glVertexAttribDivisor(2, 1);
    glVertexAttribDivisor(3, 1);
    glVertexAttribDivisor(4, 1);

    glEnableVertexAttribArray(5);
    glBindBuffer(GL_ARRAY_BUFFER, colorVBO);
    glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, sizeof(glm::vec4), (void*)0);
    glVertexAttribDivisor(5, 1);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
}

void close_window() {
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
    glDeleteBuffers(1, &transformVBO);
    glDeleteBuffers(1, &colorVBO);
    glfwTerminate();
}

void update_view(py::array_t<float> dims, unsigned int shader_ID) {
    auto dims_data = dims.unchecked<2>();

    float xmin = dims_data(0,0);
    float xmax = dims_data(0,1);
    float ymin = dims_data(1,0);
    float ymax = dims_data(1,1);
    float dx = xmax - xmin;
    float dy = ymax - ymin;

    // zoom in/out
    if (zoom >= 0) {
        xmin = (xmin + xshift) + dx/2*(1 - 1/(1+pow(zoom,2)));
        xmax = (xmax + xshift) - dx/2*(1 - 1/(1+pow(zoom,2)));
        ymin = (ymin + yshift) + dy/2*(1 - 1/(1+pow(zoom,2)));
        ymax = (ymax + yshift) - dy/2*(1 - 1/(1+pow(zoom,2)));
    }
    else {
        xmin = (xmin + xshift) + dx/2*(zoom);
        xmax = (xmax + xshift) - dx/2*(zoom);
        ymin = (ymin + yshift) + dy/2*(zoom);
        ymax = (ymax + yshift) - dy/2*(zoom);
    }

    // maintain aspect ratio
    dx = xmax - xmin;
    dy = ymax - ymin; 
    if (dx/dy > aspect_ratio) {
        float buff = dx/aspect_ratio - dy;
        ymax = ymax + buff/2;
        ymin = ymin - buff/2;
    }
    else if (dx/dy < aspect_ratio) {
        float buff = dy*aspect_ratio - dx;
        xmax = xmax + buff/2;
        xmin = xmin - buff/2;
    }

    window_dx = xmax - xmin;
    window_dy = ymax - ymin;

    // set uniform projection matrix
    glm::mat4 projection = glm::ortho(xmin, xmax, ymin, ymax, -0.1f, 0.1f);
    glUniformMatrix4fv(glGetUniformLocation(shader_ID, "projection"), 1, GL_FALSE, glm::value_ptr(projection));
}

void circle_vis(py::array_t<float> pos, py::array_t<float> radii, py::array_t<float> dims, py::array_t<float> colors, py::array_t<float> background_color, const std::string vshader, const std::string fshader, bool time_it) {
    // read input arrays
    auto pos_data = pos.unchecked<3>();
    auto radii_data = radii.unchecked<1>();
    auto color_data = colors.mutable_unchecked<2>();
    auto background_color_data = background_color.unchecked<1>();

    int Ncolors = color_data.shape(0);
    int Nparticles = pos_data.shape(1);
    last_frame = pos_data.shape(0);

    // initialize OpenGL
    make_window(time_it);
    bind_vetices();
    bind_attributes();
    Shader shader = Shader(vshader, fshader);
    shader.use(); 

    // allocate instanced arrays
    glm::mat4* circleTransforms = new glm::mat4[Nparticles];;
    glm::vec4* circleColors = new glm::vec4[Nparticles];

    float t_total = 0;
    while (!glfwWindowShouldClose(window)) {
        float T0 = glfwGetTime();

        // user feedback
        processInput(window);
        update_view(dims, shader.ID);

        // set background color
        glClearColor(background_color_data(0), background_color_data(1), background_color_data(2), 1.0);
        glClear(GL_COLOR_BUFFER_BIT);

        // set instanced data for all particles
        for (int i = 0; i < Nparticles; i++) {
            glm::mat4 transform = glm::mat4(1.0f);
            transform = glm::translate(transform, glm::vec3(pos_data(current_frame,i,0), pos_data(current_frame,i,1), 0.0f));
            transform = glm::scale(transform, glm::vec3(radii_data(i), radii_data(i), 1.0f));

            circleTransforms[i] = transform;
            int idx = i % Ncolors;
            circleColors[i] = glm::vec4(color_data(idx,0), color_data(idx,1), color_data(idx,2), color_data(idx,3));
        }

        // copy instanced data to GPU
        glBindBuffer(GL_ARRAY_BUFFER, transformVBO);
        glBufferData(GL_ARRAY_BUFFER, Nparticles * sizeof(glm::mat4), &circleTransforms[0], GL_DYNAMIC_DRAW);
        glBindBuffer(GL_ARRAY_BUFFER, colorVBO);
        glBufferData(GL_ARRAY_BUFFER, Nparticles * sizeof(glm::vec4), &circleColors[0], GL_DYNAMIC_DRAW);

        // draw circles
        glBindVertexArray(VAO);
        glDrawElementsInstanced(GL_TRIANGLES, 3*Nvertices, GL_UNSIGNED_INT, 0, Nparticles);
        glfwSwapBuffers(window);
        glfwPollEvents();

        // playback
        if (!paused)
            current_frame += 1;

        float dt = glfwGetTime() - T0;
        t_total += dt;

        if (current_frame >= pos_data.shape(0)) {
            if (time_it) {
                std::cout << 1e3*t_total / current_frame << " ms" << std::endl;
                break;
            }
            current_frame = 0;
        }
    }

    close_window();
}

void processInput(GLFWwindow *window) {
    if (glfwGetKey(window, GLFW_KEY_T) == GLFW_PRESS
     || glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    if (glfwGetKey(window, GLFW_KEY_RIGHT) == GLFW_PRESS) {
        current_frame += 1;
        if (current_frame >= last_frame)
            current_frame = 0;
    }

    if (glfwGetKey(window, GLFW_KEY_LEFT) == GLFW_PRESS) {
        current_frame -= 1;
        if (current_frame < 0)
            current_frame = 0;
    }

    if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
        current_frame = 0;

    if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
        current_frame = last_frame-1;

    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        xshift -= .02*window_dx;
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        xshift += .02*window_dx;
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        yshift -= .02*window_dy;
    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        yshift += .02*window_dy;
    if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS)
        zoom -= .1;
    if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS)
        zoom += .1;
}

void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (key == GLFW_KEY_SPACE && action == GLFW_PRESS)
        paused = !paused;
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    SCR_WIDTH = width;
    SCR_HEIGHT = height;
    aspect_ratio = (float)(SCR_WIDTH) / (float)(SCR_HEIGHT);
    glViewport(0, 0, width, height);
}

void scroll_callback(GLFWwindow* window, double xoffset, double yoffset) {
    zoom -= 0.05*(float)yoffset;
}

void mouse_callback(GLFWwindow* window, double xpos, double ypos) {
    if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS) { 
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN);
        if (mouse_hold) {
            float xoffset = xpos - lastX;
            float yoffset = lastY - ypos;
            xshift -= .003*xoffset*window_dx;
            yshift -= .003*yoffset*window_dy;
        }
        mouse_hold = true;
        lastX = xpos;
        lastY = ypos;
    }
    else {
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
        mouse_hold = false;
    }
}

}
