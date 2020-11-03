#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 projection;
uniform mat4 transform;
uniform vec4 color;

out vec4 circleColor;
out vec2 pos;

void main() {
    gl_Position = projection * transform * vec4(aPos, 1.0);
    circleColor = color;
    pos = aPos.xy;
}
